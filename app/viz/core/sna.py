import networkx as nx
import community
import math
from fa2 import ForceAtlas2
from .sna_sub import *

__all__ = [
    'make_sna_gexf',
    'make_sna_png',
]


def make_sna_gexf(data, node_num=30, edge_remove_threshold=0, sw=None, remove_isolated_node=True,
                  layout='fr', iterations=50, fr_k=None, fa2_option=(2, 100)):
    """Make sna_gexf for SNA Interactive

    :param str,list data: String Data (One post per line) | List Data (One post per element)
    :param int node_num: Number of nodes
    :param int edge_remove_threshold:
    :param str sw: Stopwords separated ','
    :param bool remove_isolated_node:
    :param str layout:
    :param int iterations:
    :param int fr_k:
    :param tuple fa2_option:
    :return: none

    """

    corpus = get_corpus(data=data)
    matrix = get_matrix(corpus=corpus, sw=sw)
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

    # Add Node Weight
    scaled_weight_list = []
    for s in tf_sum_dict_sorted[:node_num]:
        if s[1] == -1: continue  # If Node Weight == -1 (It means that this node is a isolated node), then do nothing
        else:
            scaled_weight = (s[1] * (40**2) / tf_sum_dict_sorted[0][1])**(1/2)
            scaled_weight_list.append((s[0], scaled_weight))

    scaled_weight_dict = dict(scaled_weight_list)

    for node in scaled_weight_dict:
        sub_G.nodes[node]['viz'] = {'size': scaled_weight_dict[node]}

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
            adj_x, adj_y = [math.log(abs(coord) ** fa2_option[0], fa2_option[1]) for coord in pos[node]]
            if raw_x < 0: adj_x *= -1
            if raw_y < 0: adj_y *= -1
            # ----------------- #
            sub_G.nodes[node]['viz']['position'] = {'x': adj_x, 'y': adj_y}
    # -------------------------- #
    write_gexf(graph=sub_G)


def make_sna_png(data, node_num=30, edge_remove_threshold=0, sw=None, remove_isolated_node=True,
                layout='fr', iterations=50, fr_k=None, fa2_option=(2, 100)):
    """Make SNA image for SNA Simple Image

    :param str,list data: String Data (One post per line) | List Data (One post per element)
    :param int node_num: Number of nodes
    :param int edge_remove_threshold:
    :param str sw: Stopwords separated ','
    :param bool remove_isolated_node:
    :param str layout:
    :param int iterations:
    :param int fr_k:
    :param tuple fa2_option:
    :return: none

    """
    
    corpus = get_corpus(data=data)
    matrix = get_matrix(corpus=corpus, sw=sw)
    cooccur_matrix = matrix.get('cooccur_matrix')
    
    # -- Make Raw Graph -- #
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
    tf_sum_dict = sub_data.get('tf_sum_dict')

    edge_weight_max = max([sub_G[u][v]['weight'] for u, v in sub_G.edges])

    # -- Set Options -- #
    partition = community.best_partition(sub_G)
    color_map = {0: '#63c2e5', 1: '#F6DD58', 2: '#F78181', 3: '#F781F3', 4: '#81F79F', 5: '#87dde1',
                 6: '#57a0d5', 7: '#f9dc71', 8: '#ea7a94', 9: '#8178e3', 10: '#da94ce', 11: '#9ebefa',
                 12: '#aee4bb', 13: '#d16aab',}

    # tf_sum_dict_sorted[0][1] == Maximum Frequency
    node_weights = [(tf_sum_dict[node] * 1e+9 / tf_sum_dict_sorted[0][1])**(1/2) for node in sub_G]
    node_colors = [color_map[partition[node]] for node in sub_G]
    edge_weights = [sub_G[u][v]["weight"] * 20 / edge_weight_max for u, v in sub_G.edges]
    edge_colors = [color_map[partition[v]] for u, v in sub_G.edges]

    # ------ Set Layout ------ #
    # Fruchterman Reingold
    if layout == 'fr':
        pos = nx.spring_layout(sub_G, k=fr_k, iterations=iterations)
        
    # ForceAtals2
    elif layout == 'fa2':
        forceatlas2 = ForceAtlas2()
        pos = forceatlas2.forceatlas2_networkx_layout(sub_G, iterations=iterations)

        for node in pos:
            raw_x, raw_y = pos[node]
            # -- Scaling Pos -- #
            adj_x, adj_y = [math.log(abs(coord) ** fa2_option[0], fa2_option[1]) for coord in pos[node]]
            if raw_x < 0: adj_x *= -1
            if raw_y < 0: adj_y *= -1
            # ----------------- #
            pos[node][0] = adj_x
            pos[node][1] = adj_y
    # -------------------------- #
    
    # -- Make Option Dict -- #
    options = {
        "pos": pos,
        "node_size": node_weights,
        "node_color": node_colors,
        "width": edge_weights,
        "edge_color": edge_colors,
        "with_labels": False,
        "font_weight": "regular",
    }

    # -- Draw the Result -- #
    write_png(graph=sub_G, options=options)
