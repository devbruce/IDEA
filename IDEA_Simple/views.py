from django.shortcuts import render
from django.http import HttpResponse
from .models import ModelAutoSNA, ModelAutoWC, ModelSNA, ModelWC
from .forms import FormAutoSNA, FormAutoWC, FormSNA, FormWC
from .result_generator import *
from .auto_crawler import *

def home(request):
    return render(request, 'IDEA_Simple/home.html')


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
            }

            response = HttpResponse(content_type="image/png")
            make_sna(get_data, **options)
            img = Image.open(os.path.join(os.getcwd(),"IDEA_Simple/result_data/sna.png"))
            img.save(response, 'png')
            return response
    else:
        form = FormAutoSNA
    return render(request, 'IDEA_Simple/sna_auto.html', {'form':form})


def wc_auto(request):
    if request.method == "POST":
        form = FormAutoWC(request.POST)
        if form.is_valid():
            
            # Get data by auto_crawler
            get_data = wc_auto_crawler(request.POST['keyword'], page_range=int(request.POST['page_range']))

            # Set Options
            options = {
                'max_word_size' : int(request.POST['max_word_size']),
                'bg_color' : request.POST['bg_color'],
                'shape' :request.POST['shape'],
                'sw' : request.POST['stop_words'],
            }

            response = HttpResponse(content_type="image/png")
            make_wc(get_data, **options)
            img = Image.open(os.path.join(os.getcwd(),"IDEA_Simple/result_data/wc.png"))
            img.save(response, 'png')
            return response
    else:
        form = FormAutoWC
    return render(request, 'IDEA_Simple/wc_auto.html', {'form':form})


def sna(request):
    if request.method == "POST":
        form = FormSNA(request.POST)
        if form.is_valid():
            options = {
                'edge_remove_threshold' : int(request.POST['edge_remove_threshold']),
                'node_num' : int(request.POST['node_num']),
                'sw' : request.POST['stop_words'],
            }
            response = HttpResponse(content_type="image/png")
            make_sna(request.POST['text_input'], **options)
            img = Image.open(os.path.join(os.getcwd(),"IDEA_Simple/result_data/sna.png"))
            img.save(response, 'png')
            return response
    else:
        form = FormSNA
    return render(request, 'IDEA_Simple/sna.html', {'form':form})


def wc(request):
    if request.method == "POST":
        form = FormWC(request.POST)
        if form.is_valid():
            response = HttpResponse(content_type="image/png")
            options = {
                'max_word_size' : int(request.POST['max_word_size']),
                'bg_color' : request.POST['bg_color'],
                'shape' :request.POST['shape'],
                'sw' : request.POST['stop_words'],
            }
            make_wc(request.POST['text_input'], **options)
            img = Image.open(os.path.join(os.getcwd(),'IDEA_Simple/result_data/wc.png'))
            img.save(response, 'png')
            return response
    else:
        form = FormWC
    return render(request, 'IDEA_Simple/wc.html', {'form':form})