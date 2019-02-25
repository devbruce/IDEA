from django.conf import settings
from konlpy.tag import Mecab
from sklearn.feature_extraction.text import CountVectorizer
from collections import OrderedDict
import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import community
import xml.etree.ElementTree as ET

__all__ = [
    'get_corpus',
    'get_matrix',
    'get_sub_data',
    'write_gexf',
    'write_png',
]


def get_corpus(data):
    """Make corpus with string or list data

    :param str,list data: String Data (One post per line) | List Data (One post per element)
    :return: corpus (numpy.ndarray)

    """
    nlp = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')  # Make Mecab (NLP) Instance
    
    if type(data) == list:
        post_list = data  # Case: DataType is list and Each element is string
    else:
        post_list = data.split('\n')  # Split string data by line (\n)

    cleaned_post_list = []
    for post in post_list:
        # Cleansing Process (Only get nouns)
        post = re.sub(r'\W', ' ', post)  # Change Special Characters and blanks (Not words) to ' '(one blank)
        post = ' '.join(nlp.nouns(post))  # nlp.nouns returns nouns list. so, unpacking list (to str)
        if post:  # if post is null, Not add
            cleaned_post_list.append(post)  # Append cleaned post(only nouns) to cleaned_post_list

    corpus = np.array(cleaned_post_list)
    return corpus


def get_matrix(corpus, stopwords):
    """Make data related to matrix

    :param numpy.ndarray corpus: corpus data made by ``core.sna_sub.get_corpus``
    :param str stopwords: Stopwords separated ','
    :return: dict

    **Keys of returned dict**

    - term_names (list)
    - td_matrix (scipy.sparse.csr.csr_matrix)
    - cooccur_matrix (pandas.core.frame.DataFrame)

    """
    # -- Make Stop Word List -- #
    if stopwords:
        stopwords = stopwords.replace(' ', '')
        stopwords_list = stopwords.split(',')
    else:
        stopwords_list = None

    # -- Make Cooccur Matrix -- #
    term_vectorizer = CountVectorizer(
        min_df=1,  # Frequency >= 1
        token_pattern=r'\w{1,}',  # Length >= 1
        stop_words=stopwords_list,
    )
    term_names = term_vectorizer.fit(corpus).get_feature_names()
    td_matrix = term_vectorizer.fit_transform(corpus)  # Get Term-Document Matrix

    tf_cooccur = (td_matrix.T).dot(td_matrix)
    tf_cooccur.setdiag(0)  # Set diagonal line 0 (They don't have means)

    cooccur_matrix = pd.DataFrame(
        data=tf_cooccur.todense(),  # Assign matrix data (todense) of tf_cooccur
        index=term_names,  # Set names of rows on matrix
        columns=term_names,  # Set names of columns on matrix
    )

    result = {
        'term_names': term_names,
        'td_matrix': td_matrix,
        'cooccur_matrix': cooccur_matrix,
    }
    return result


def get_sub_data(graph, node_num, edge_remove_threshold, remove_isolated_node, matrix):
    """Make Sub Graph and Term Frequency Dictionary

    :param networkx.classes.graph.Graph graph:
    :param int node_num: Number of nodes
    :param int edge_remove_threshold:
    :param bool remove_isolated_node:
    :param dict matrix:
    :return: dict

    **Keys of returned dict**

    - sub_graph (networkx.classes.graph.Graph)
    - tf_sum_dict (dict)
    - tf_sum_dict_sorted (list)

    """
    # Edge Remove Threshold
    if edge_remove_threshold > 0:
        edge_low = list()
        for u, v in graph.edges:
            if graph[u][v]['weight'] <= edge_remove_threshold:
                edge_low.append((u, v))
        graph.remove_edges_from(edge_low)  # Remove Edge If(edge weight <= edge_remove_threshold)

    # Make tf_sum_dict (Total of Term Frequency Dictionary)
    td_matrix = matrix.get('td_matrix')
    tf_sum = td_matrix.toarray().sum(axis=0)
    term_names = matrix.get('term_names')
    tf_sum_dict = {}
    for i in range(len(term_names)):
        tf_sum_dict[term_names[i]] = tf_sum[i]

    # Get Top Frequency Nodes to make sub_G
    tf_sum_dict_sorted = sorted(tf_sum_dict.items(), key=lambda x: x[1], reverse=True)

    # -- Process : Remove Isolated Node -- #
    if remove_isolated_node:
        # Make Remove Isolated Nodes List
        isolated_nodes = list()
        main_network_nodes = [i[0] for i in tf_sum_dict_sorted[:node_num]]
        for node in graph.nodes:
            edge_weight_sum=0
            for to in graph[node]:
                if to in main_network_nodes:  # If edge is realted to main_nodes, add this edge_weight edge_weight_sum
                    edge_weight_sum += graph[node][to]['weight']
            if edge_weight_sum == 0:
                isolated_nodes.append(node)

        # Make temp_dict for setting isolated node weight -1
        temp_dict = OrderedDict(tf_sum_dict_sorted)

        # Set Isolated nodes' weight -1
        for node in isolated_nodes:
            temp_dict[node] = -1
        tf_sum_dict_sorted = list(temp_dict.items())
    # ------------------------------------- #

    # Make Sub Graph
    sub_nodes = []
    for node_data in tf_sum_dict_sorted[:node_num]:  # Set the Number of Nodes
        if node_data[1] == -1:  # If Node Weight == -1 (It means that this node is a isolated node)
            continue
        else:
            sub_nodes.append(node_data[0])

    sub_graph = graph.subgraph(sub_nodes)
    result = {
        'sub_graph': sub_graph,
        'tf_sum_dict': tf_sum_dict,
        'tf_sum_dict_sorted': tf_sum_dict_sorted,
    }
    return result


def write_gexf(graph):
    """Save SNA gexf file (``/.viz_raw/sna_gexf.gexf``)

    :param networkx.classes.graph.Graph graph:
    :return: none

    """
    # Add Node Modularity Class
    partition = community.best_partition(graph)
    nx.set_node_attributes(graph, partition, 'Modularity_Class')

    # Write Original gexf File
    nx.write_gexf(graph, os.path.join(settings.ROOT_DIR, '.viz_raw/sna_gexf.gexf'), encoding='utf-8', prettyprint=True)

    # -- Modify original gexf File -- #

    # To remove ns0
    ET.register_namespace('', 'http://www.gexf.net/1.2draft')

    # Parse gexf file
    doc = ET.parse(os.path.join(settings.ROOT_DIR, '.viz_raw/sna_gexf.gexf'))

    # get root node
    root = doc.getroot()

    # Modify some attrib for echarts
    for tag in root.iter('{http://www.gexf.net/1.2draft}attribute'):
        tag.attrib['id'] = 'modularity_class'
        tag.attrib['type'] = 'integer'

    for tag in root.iter('{http://www.gexf.net/1.2draft}attvalue'):
        tag.attrib['for'] = 'modularity_class'

    # Modify original gexf file
    ET.dump(doc)
    doc.write(os.path.join(settings.ROOT_DIR, '.viz_raw/sna_gexf.gexf'), encoding='utf-8', xml_declaration=True)


def write_png(graph, options):
    """Save SNA image file (``/.viz_raw/sna.png``)

    :param networkx.classes.graph.Graph graph:
    :param dict options:
    :return: none

    """
    plt.figure(figsize=(90, 45), dpi=36)
    nx.draw_networkx(graph, **options)
    nx.draw_networkx_labels(graph, options.get('pos'), font_family='DOSGothic', font_size=40)
    plt.axis('off')
    plt.savefig(os.path.join(settings.ROOT_DIR, '.viz_raw/sna.png'), bbox_inches='tight')
    plt.close()
