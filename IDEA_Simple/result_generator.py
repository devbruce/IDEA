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
from wordcloud import WordCloud
from PIL import Image

# Semantic Network Analysis
import networkx as nx
import community
from fa2 import ForceAtlas2

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


def make_sna(contents_raw, edge_remove_threshold=0, node_num=30, sw = "", remove_isolated_node="on",
                layout="FR", fr_k=1, fr_iter=50, fa2_1=2, fa2_2=100, fa2_iter=50):
    
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

    # Edge_remove_threshold
    edge_low=list()
    for u,v in G.edges:
        if G[u][v]["weight"] <= edge_remove_threshold:
            edge_low.append((u,v))
    G.remove_edges_from(edge_low) # Remove Edge If(edge weight <= edge_remove_threshold)
    
    # Make tf_sum_dict (Total of Term Frequency Dictionary)
    tf_sum = td_matrix.toarray().sum(axis=0)
    tf_sum_dict = {}
    for i in range(len(term_names)):
        tf_sum_dict[term_names[i]] = tf_sum[i]

    # Get Top Frequency Nodes to make sub_G
    tf_sum_dict_sorted = sorted(tf_sum_dict.items(), key=lambda x: x[1], reverse=True)

    ##-- Process : Remove Isolated Node --##
    if remove_isolated_node == "on":
        # Make Remove Isolated Nodes List
        isolated_nodes=list()
        main_network_nodes = [i[0] for i in tf_sum_dict_sorted[:node_num]]
        for node in G.nodes:
            edge_weight_sum=0
            for to in G[node]:
                if to in main_network_nodes: # If edge is realted to main_nodes, add this edge_weight edge_weight_sum
                    edge_weight_sum += G[node][to]['weight']
            if edge_weight_sum==0:
                isolated_nodes.append(node)

        # Make temp_dict for setting isolated node weight -1
        temp_dict = OrderedDict()
        for val in tf_sum_dict_sorted:
            temp_dict[val[0]] = val[1]

        # Set Isolated nodes' weight -1
        for node in isolated_nodes:
            temp_dict[node] = -1
        tf_sum_dict_sorted = list(temp_dict.items())
    else: pass
    ##-------------------------------------##

    # Make Sub Graph
    sub_nodes = []
    for node_data in tf_sum_dict_sorted[:node_num]:  # Set the Number of Nodes
        if node_data[1] == -1: # If Node Weight == -1 (It means that this node is a isolated node)
            continue
        else: sub_nodes.append(node_data[0])

    sub_G = G.subgraph(sub_nodes)

    edge_weight_max = max([sub_G[u][v]['weight'] for u,v in sub_G.edges])

    ##-- Set Options --##

    partition = community.best_partition(sub_G)
    
    color_map = { 0:'#63c2e5', 1:'#F4FA58', 2:'#F78181', 3:'#F781F3', 4:'#81F79F', 5:'#87dde1',  
                  6:'#57a0d5', 7:'#f9dc71', 8:'#ea7a94', 9:'#8178e3', 10:'#da94ce', 11:'#9ebefa', 
                  12:'#aee4bb', 13:'#d16aab', }

    node_weights = [(tf_sum_dict[node] * 1e+10 / tf_sum_dict_sorted[0][1])**(1/2) for node in sub_G]  # tf_sum_dict_sorted[0][1] == Maximum Frequency
    node_colors = [color_map[partition[node]] for node in sub_G]
    edge_weights = [sub_G[u][v]["weight"] * 20 / edge_weight_max for u,v in sub_G.edges]
    edge_colors = [color_map[partition[v]] for u,v in sub_G.edges]

    ##------- Set Layout -------##
    
    # Fruchterman Reingold
    if layout == "FR":
        pos = nx.spring_layout(sub_G, k=fr_k, iterations=fr_iter)
        
    # ForceAtals2
    elif layout == "FA2":
        forceatlas2 = ForceAtlas2()
        pos = forceatlas2.forceatlas2_networkx_layout(sub_G, iterations=fa2_iter)

        for node in pos:
            raw_x, raw_y = pos[node]
            ##-- Scaling Pos --##
            adj_x, adj_y = [math.log(abs(coord) ** fa2_1, fa2_2) for coord in pos[node]]
            if raw_x < 0: adj_x *= -1
            if raw_y < 0: adj_y *= -1
            ##-----------------##
            pos[node][0] = adj_x
            pos[node][1] = adj_y
    ##----------------------------------##
    
    ##-- Make Option Dict --##
    options = {
        "pos" : pos,
        "node_size" : node_weights,
        "node_color": node_colors,
        "width": edge_weights,
        "edge_color": edge_colors,
        "with_labels": False,
        "font_weight": "regular",
    }

    ##-- Draw the Result --##
    plt.figure(figsize=(85,55), dpi=64)
    nx.draw_networkx(sub_G, **options)
    nx.draw_networkx_labels(sub_G, pos, font_family="NanumBarunGothic", font_size=60)
    # ax = plt.gca()
    # ax.collections[0].set_edgecolor("#EAECEE")
    plt.axis("off")
    plt.savefig(os.path.join(os.getcwd(),"IDEA_Simple/result_data/sna.png"), bbox_inches="tight")
    plt.clf()


def make_wc(data, max_word_size=100, bg_color="white", shape="default", sw =""):
    data = re.sub(r"\W"," ",data)  # Use regular expression for data scailing
    
    nlp = Mecab("/usr/local/lib/mecab/dic/mecab-ko-dic") # Make Mecab object
    
    data_nouns = nlp.nouns(data) # Extract nouns from data and input it to data_nouns
    data_nouns_cnt = Counter(data_nouns) # Count nouns from data_nouns and make it dict type data

    if sw != "":
        sw = sw.replace(" ", "")
        sw_list = sw.split(",")
        for word in sw_list:
            del data_nouns_cnt[word]
    
    wc_font = os.path.join(os.getcwd(),"additional/fonts/NanumBarunGothic.ttf") # Set Font
    wc_mask = np.array(Image.open(os.path.join(os.getcwd(),"IDEA_Simple/wc_mask/{}.png".format(shape)))) # Set Image Mask

    wc = WordCloud(max_font_size = max_word_size,
                      font_path = wc_font,
                      background_color = bg_color,
                      mask = wc_mask).generate_from_frequencies(data_nouns_cnt)

    plt.figure(figsize=(35, 35))  # Set Image Size
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig(os.path.join(os.getcwd(),"IDEA_Simple/result_data/wc.png"), bbox_inches="tight")
    plt.clf()