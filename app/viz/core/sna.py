import networkx as nx
import math
import community
from fa2 import ForceAtlas2
from .sna_sub import *

__all__ = [
    'gen_gexf_and_pass_partition_data',
]


def gen_gexf_and_pass_partition_data(
        data,
        node_num=30,
        edge_remove_threshold=0,
        word_len_min=2,
        stopwords=None,
        remove_isolated_node=True,
        layout='fr',
        iterations=50,
        fr_k=None,
        fa2_square=2,
        fa2_log_base=100,
):
    """Generate gexf file for SNA Interactive and Pass partition data

    :param str,list data: String Data (One post per line) | List Data (One post per element)
    :param int node_num: Number of nodes
    :param int edge_remove_threshold:
    :param int word_len_min:
    :param str stopwords: Stopwords separated ','
    :param bool remove_isolated_node:
    :param str layout:
    :param int iterations:
    :param int fr_k:
    :param int fa2_square:
    :param int fa2_log_base:
    :return: none

    """

    corpus = get_corpus(data=data)
    matrix = get_matrix(corpus=corpus, word_len_min=word_len_min, stopwords=stopwords)
    cooccur_matrix = matrix.get('cooccur_matrix')

    # Get Graph
    graph = nx.from_pandas_adjacency(cooccur_matrix)

    # Get Sub Data
    sub_data = get_sub_data(
        graph=graph,
        node_num=node_num,
        edge_remove_threshold=edge_remove_threshold,
        remove_isolated_node=remove_isolated_node,
        matrix=matrix
    )
    sub_graph = sub_data.get('sub_graph')
    tf_sum_dict_sorted = sub_data.get('tf_sum_dict_sorted')

    # ------ Set Attributes for gexf file ------ #
    # Add Node Weight
    scaled_weight_list = []
    for s in tf_sum_dict_sorted[:node_num]:
        if s[1] == -1: continue  # If Node Weight == -1 (It means that this node is a isolated node), then do nothing
        else:
            scaled_weight = (s[1] * (70 ** 2) / tf_sum_dict_sorted[0][1])**(1/2)
            scaled_weight_list.append((s[0], scaled_weight))

    scaled_weight_dict = dict(scaled_weight_list)

    for node in scaled_weight_dict:
        sub_graph.nodes[node]['viz'] = {'size': scaled_weight_dict[node]}

    # Add edge weight
    edge_weight_max = max([sub_graph[u][v]['weight'] for u, v in sub_graph.edges])
    for u, v in sub_graph.edges:
        sub_graph[u][v]['viz'] = {'thickness': sub_graph[u][v]['weight'] * 35 / edge_weight_max}

    # ------ Set Layout ------ #
    # Fruchterman Reingold
    if layout == "fr":
        pos = nx.spring_layout(sub_graph, k=fr_k, iterations=iterations)
        for node in pos:
            sub_graph.nodes[node]['viz']['position'] = {'x': pos[node][0], 'y': pos[node][1]}
        
    # ForceAtlas2
    elif layout == "fa2":
        forceatlas2 = ForceAtlas2()
        pos = forceatlas2.forceatlas2_networkx_layout(sub_graph, iterations=iterations)

        for node in pos:
            raw_x, raw_y = pos[node]
            # -- Scaling Pos -- #
            adj_x, adj_y = [math.log(abs(coord) ** fa2_square, fa2_log_base) for coord in pos[node]]
            if raw_x < 0: adj_x *= -1
            if raw_y < 0: adj_y *= -1
            # ----------------- #
            sub_graph.nodes[node]['viz']['position'] = {'x': adj_x, 'y': adj_y}
    # -------------------------- #

    # Generate gexf file
    write_gexf(graph=sub_graph)

    # ------ Pass partition data to template ------ #
    partition = community.best_partition(sub_graph)
    partition_len = max(partition.values()) + 1
    node_freq_per_klass = {n: list() for n in range(partition_len)}
    for node, klass in partition.items():
        node_freq_per_klass[klass].append((node, scaled_weight_dict[node]))

    top_node_per_klass = [None] * partition_len
    for klass, node_freq in node_freq_per_klass.items():
        top_node_per_klass[klass] = max(node_freq, key=lambda x : x[1])[0]

    partition_pass_to_template = {
        'partition_len': partition_len,
        'top_node_per_klass': top_node_per_klass,
    }
    return partition_pass_to_template
