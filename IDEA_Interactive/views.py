from django.shortcuts import render
from .models import ModelAutoSNA, ModelAutoWC, ModelSNA, ModelWC
from .forms import FormAutoSNA, FormAutoWC, FormSNA, FormWC
from .result_generator import *
from .auto_crawler import *
import time

def home(request):
    return render(request, 'IDEA_Interactive/home.html')


def sna_auto(request):
    if request.method == "POST":
        form = FormAutoSNA(request.POST)
        if form.is_valid():

            # Get data by auto_crawler
            get_data = sna_auto_crawler(request.POST['keyword'], page_range=int(request.POST['page_range']))
            
            # Set Options
            options = {
                'edge_remove_threshold' : int(request.POST['edge_remove_threshold']),
                'node_num' : int(request.POST['node_num']),
                'sw' : request.POST['stop_words'],
                'remove_isolated_node' : request.POST['remove_isolated_node'], 
                'layout' : request.POST['layout'], 
                'fr_k' : int(request.POST['fr_k']),
                'fr_iter' : int(request.POST['fr_iter']),
                'fa2_1' : int(request.POST['fa2_1']),
                'fa2_2' : int(request.POST['fa2_2']),
                'fa2_iter' : int(request.POST['fa2_iter']),
            }
            make_sna_gexf(get_data, **options)
            time.sleep(2)
            return render(request, 'IDEA_Interactive/echarts_result/les-miserables_auto.html')
    else:
        form = FormAutoSNA
    return render(request, 'IDEA_Interactive/sna_auto.html', {'form':form})


def wc_auto(request):
    if request.method == "POST":
        form = FormAutoWC(request.POST)
        if form.is_valid():

            # Get data by auto_crawler
            get_data = wc_auto_crawler(request.POST['keyword'], page_range=int(request.POST['page_range']))

            make_wc_json(get_data, request.POST['stop_words'])
            time.sleep(2)
            return render(request, 'IDEA_Interactive/echarts_result/echarts_wc.html')
    else:
        form = FormAutoWC
    return render(request, 'IDEA_Interactive/wc_auto.html', {'form':form})


def sna(request):
    if request.method == "POST":
        form = FormSNA(request.POST)
        if form.is_valid():

            # Set Options
            options = {
                'edge_remove_threshold' : int(request.POST['edge_remove_threshold']),
                'node_num' : int(request.POST['node_num']),
                'sw' : request.POST['stop_words'],
                'remove_isolated_node' : request.POST['remove_isolated_node'], 
                'layout' : request.POST['layout'], 
                'fr_k' : int(request.POST['fr_k']),
                'fr_iter' : int(request.POST['fr_iter']),
                'fa2_1' : int(request.POST['fa2_1']),
                'fa2_2' : int(request.POST['fa2_2']),
                'fa2_iter' : int(request.POST['fa2_iter']),
            }
            make_sna_gexf(request.POST['text_input'], **options)
            time.sleep(2)
            return render(request, 'IDEA_Interactive/echarts_result/les-miserables.html')
    else:
        form = FormAutoSNA
    return render(request, 'IDEA_Interactive/sna.html', {'form':form})


def wc(request):
    if request.method == "POST":
        form = FormWC(request.POST)
        if form.is_valid():
            make_wc_json(request.POST['text_input'], request.POST['stop_words'])
            time.sleep(2)
            return render(request, 'IDEA_Interactive/echarts_result/echarts_wc.html') 
    else:
        form = FormWC
    return render(request, 'IDEA_Interactive/wc.html', {'form':form})
