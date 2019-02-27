import networkx as nx
import math
from fa2 import ForceAtlas2
from .sna_sub import *

__all__ = [
    'make_sna_gexf',
]


def make_sna_gexf(
        data,
        node_num=30,
        edge_remove_threshold=0,
        word_len_min=2,
        stopwords=None,
        remove_isolated_node=True,
        layout='fr',
        iterations=50,
        fr_k=None,
        fa2_square=2, fa2_log_base=100
):
    """Make sna_gexf for SNA Interactive

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
    G = nx.from_pandas_adjacency(cooccur_matrix)

    # Get Sub Data
    sub_data = get_sub_data(
        graph=G, node_num=node_num,
        edge_remove_threshold=edge_remove_threshold,
        remove_isolated_node=remove_isolated_node,
        matrix=matrix
    )
    sub_G = sub_data.get('sub_graph')
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
        sub_G.nodes[node]['viz'] = {'size': scaled_weight_dict[node]}

    # Add edge weight
    edge_weight_max = max([sub_G[u][v]['weight'] for u, v in sub_G.edges])
    for u, v in sub_G.edges:
        sub_G[u][v]['viz'] = {'thickness': sub_G[u][v]['weight'] * 35 / edge_weight_max}

    # ------ Set Layout ------ #
    # Fruchterman Reingold
    if layout == "fr":
        pos = nx.spring_layout(sub_G, k=fr_k, iterations=iterations)
        for node in pos:
            sub_G.nodes[node]['viz']['position'] = {'x': pos[node][0], 'y': pos[node][1]}
        
    # ForceAtlas2
    elif layout == "fa2":
        forceatlas2 = ForceAtlas2()
        pos = forceatlas2.forceatlas2_networkx_layout(sub_G, iterations=iterations)

        for node in pos:
            raw_x, raw_y = pos[node]
            # -- Scaling Pos -- #
            adj_x, adj_y = [math.log(abs(coord) ** fa2_square, fa2_log_base) for coord in pos[node]]
            if raw_x < 0: adj_x *= -1
            if raw_y < 0: adj_y *= -1
            # ----------------- #
            sub_G.nodes[node]['viz']['position'] = {'x': adj_x, 'y': adj_y}
    # -------------------------- #
    write_gexf(graph=sub_G)
