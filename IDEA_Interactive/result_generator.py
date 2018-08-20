# Common
import re
import os
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from konlpy.tag import Mecab
from sklearn.feature_extraction.text import CountVectorizer

# Word Cloud
from collections import Counter, OrderedDict
import json # To make json file for echarts

# Semantic Network Analysis
import networkx as nx
import community
from fa2 import ForceAtlas2
import xml.etree.ElementTree as ET # To modify gexf file for echarts

def make_corpus(raw_data):
    nlp = Mecab("/usr/local/lib/mecab/dic/mecab-ko-dic")  # Make Mecab object
    
    if type(raw_data) == str:
        contents_list = raw_data.split("\n")  # Split string data by line
    else:
        contents_list = raw_data  # Case : Data input by auto crawler (list type)

    contents_nouns = []
    for content in contents_list:
        content = re.sub(r"\W", " ", content)
        contents_nouns.append(re.sub(r"\W"," ", str(nlp.nouns(content))))

    contents_data = pd.DataFrame(contents_nouns)
    contents_data.columns = ["content"]

    corpus = np.array(contents_data["content"])
    return corpus

def make_sna_gexf(contents_raw, edge_remove_threshold=0, node_num=50, sw = ""):

    corpus = make_corpus(contents_raw)

    ##- Stop Words Process -##
    if sw != "":
        sw = sw.replace(" ", "")
        sw_list = sw.split(",")

    else:
        sw_list = None

    ##- Make cooccur_matrix -## 
    term_vectorizer = CountVectorizer(min_df = 1, token_pattern = r"\w{2,}", stop_words = sw_list) # Count if(Frequency >=1, Length >=2)
    token_dict = term_vectorizer.fit(corpus)
    term_names = token_dict.get_feature_names()
    td_matrix = term_vectorizer.fit_transform(corpus)

    tf_cooccur = (td_matrix.T).dot(td_matrix)
    tf_cooccur.setdiag(0) # Set diagonal line 0 (They don't have means)

    cooccur_matrix = pd.DataFrame(data = tf_cooccur.todense(), index = term_names, columns = term_names)

    ##-- Make Raw Graph --##
    G = nx.from_pandas_adjacency(cooccur_matrix)

    ##-- Edge_remove_threshold & Make Isolated Nodes List--##
    edge_low=list()
    isolated_nodes_candidates=list()
    for u,v in G.edges:
        if G[u][v]["weight"] <= edge_remove_threshold: 
            edge_low.append((u,v))
            if u not in isolated_nodes_candidates:
                isolated_nodes_candidates.append(u)
            if v not in isolated_nodes_candidates:
                isolated_nodes_candidates.append(v)
    G.remove_edges_from(edge_low) # Remove Edge If(edge weight <= edge_remove_threshold)

    isolated_nodes=list()
    for node in isolated_nodes_candidates:
        edge_weight_sum=0
        for to in G[node]:
            edge_weight_sum += G[node][to]['weight']
        if edge_weight_sum < 1:
            isolated_nodes.append(node)
        else: continue

    ##- make tf_sum_dict (Total of Term Frequency Dictionary) -##
    tf_sum = td_matrix.toarray().sum(axis=0)
    tf_sum_dict = {}

    for i in range(len(term_names)):
        tf_sum_dict[term_names[i]] = tf_sum[i]

    # Remove Isolated Nodes (Set Node Weight 0)
    for node in isolated_nodes:
        tf_sum_dict[node] = 0

    ##- Get Top Frequency Nodes to make sub_G -##
    tf_sum_dict_sorted = sorted(tf_sum_dict.items(), key=lambda x: x[1], reverse=True)
    sub_nodes = []

    for node in tf_sum_dict_sorted[:node_num]:  # Set the Number of Nodes
        sub_nodes.append(node[0])

    sub_G = G.subgraph(sub_nodes)  # sub_graph

    # Add Node Weight
    scaled_weight_list = []
    for s in tf_sum_dict_sorted[:node_num]:
        scaled_weight = (s[1] * 2500 / tf_sum_dict_sorted[0][1])**(1/2)
        scaled_weight_list.append((s[0],scaled_weight))

    scaled_weight_dict = dict()
    for sw in scaled_weight_list:
        scaled_weight_dict[sw[0]] = sw[1]

    for node in scaled_weight_dict:
        sub_G.nodes[node]['viz'] = {'size':scaled_weight_dict[node]}


    # Node Position Add
    forceatlas2 = ForceAtlas2()
    pos = forceatlas2.forceatlas2_networkx_layout(sub_G, iterations=90)

    for node in pos:
        raw_x, raw_y = pos[node]
        ##-- Scaling Pos --##
        adj_x, adj_y = [math.log(abs(coord) ** 2.5, 300) for coord in pos[node]]
        if raw_x < 0: adj_x *= -1
        if raw_y < 0: adj_y *= -1
        ##-----------------##
        sub_G.nodes[node]['viz']['position'] = {'x' : adj_x, 'y' : adj_y}

    # Add Node Modularity Class
    partition = community.best_partition(sub_G)
    nx.set_node_attributes(sub_G, partition, "Modularity_Class")


    # Write Original gexf File
    nx.write_gexf(sub_G,os.path.join(os.getcwd(),"IDEA_Interactive/static/IDEA_Interactive/result_data/origin_sna_gexf.gexf"), encoding='utf-8', prettyprint=True)


    ##- Modify original gexf File -##

    # To remove ns0
    ET.register_namespace("", "http://www.gexf.net/1.2draft")

    # Parse gexf file
    doc = ET.parse(os.path.join(os.getcwd(),"IDEA_Interactive/static/IDEA_Interactive/result_data/origin_sna_gexf.gexf"))

    # get root node
    root = doc.getroot()

    # Modify some attrib for echarts
    for tag in root.iter("{http://www.gexf.net/1.2draft}attribute"):
        tag.attrib["id"] = "modularity_class"
        tag.attrib["type"] = "integer"

    for tag in root.iter("{http://www.gexf.net/1.2draft}attvalue"):
        tag.attrib["for"] = "modularity_class"

    # Modify original gexf file
    ET.dump(doc)
    doc.write(os.path.join(os.getcwd(),"IDEA_Interactive/static/IDEA_Interactive/result_data/sna_gexf.gexf"), encoding="utf-8", xml_declaration=True)

def make_wc_json(data, sw = ""):
    data = re.sub(r"\W"," ",data)  # Use regular expression for data scailing
    
    nlp = Mecab("/usr/local/lib/mecab/dic/mecab-ko-dic") # Make Mecab object
    
    data_nouns = nlp.nouns(data)  # Extract nouns from data and input it to data_nouns
    data_nouns_cnt = Counter(data_nouns)  # Count nouns from data_nouns and make it dict type data

    if sw != "":
        sw = sw.replace(" ", "")
        sw_list = sw.split(",")
        for word in sw_list:
            del data_nouns_cnt[word]
            
    json_output = list()
    for val in data_nouns_cnt:
        json_dict = OrderedDict()
        json_dict["name"] = val
        json_dict["value"] = data_nouns_cnt[val]
        json_dict["textStyle"] = {"normal": {}, "emphasis": {}}
        json_output.append(json_dict)
    
    with open(os.path.join(os.getcwd(),"IDEA_Interactive/static/IDEA_Interactive/result_data/wc_json.json"),"w", encoding="utf-8") as f:
        json.dump(json_output, f, ensure_ascii=False, indent="\t")