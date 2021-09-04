import os
import re
from django.core.files.storage import default_storage
from django.forms import widgets
from django.http.response import HttpResponse
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from . import util

import random

class WikiSearch(forms.Form):
    q = forms.CharField(label= "", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}), max_length = 100)
    
#class EditContent(forms.Form):
#    edit = forms.CharField(label="", widget=forms.Textarea)

def index(request):
    if request.method == "POST":
        form = WikiSearch(request.POST)
        if form.is_valid():
            query = form.cleaned_data["q"]
            return HttpResponseRedirect(f'{query}')
        else:
            return render(request, "encyclopedia/index.html", {
                "form" : form,
                })
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": WikiSearch()
    })

def wiki_title(request, title):
    if(title in util.list_entries()):
        return render(request, "encyclopedia/main.html", {
            "title": title,
            "content": util.get_entry(title),
            "form": WikiSearch(request.POST or None)
    })
    # substring or not condition
    elif(title not in util.list_entries()):
        search_result_list = []
        for entry in util.list_entries():
            if(entry.find(title) != -1):
                search_result_list.append(entry)
        
        if(len(search_result_list) != 0):
            return render(request, "encyclopedia/searchResults.html", {
                "title": title,
                "entries": search_result_list,
                "form": WikiSearch(request.POST or None),
                })
        else:
            return render(request, "encyclopedia/error.html", {
                "title":title,
                "form": WikiSearch(request.POST or None),
                }) 
    

def new_page(request):
    input_from_form = request.GET
    markdown_title_entry = input_from_form.get('markdown_title', False)
    markdown_content_entry = input_from_form.get('markdown_content', False)
    if((markdown_title_entry in util.list_entries()) and (markdown_title_entry != False)):
        return render(request, "encyclopedia/error.html", {
            "title_new_page": markdown_title_entry
        })
    if((markdown_title_entry != False) and (markdown_content_entry != False)):
        save_path = "E:\VENISH_FOLDER\wiki\wiki\entries"
        file_name = f"{markdown_title_entry}.md"

        completeName = os.path.join(save_path, file_name)

        with open(completeName, "w") as file:
            file.write(markdown_content_entry)
    if ((request.POST != None) and (markdown_content_entry != False)):
        return HttpResponseRedirect(f'{markdown_title_entry}')

    return render(request, "encyclopedia/CreateNewPage.html")


def random_page(request):
    title = random.choice(util.list_entries())
    return render(request, "encyclopedia/RandomPage.html", {
        "title": title,
        "content": util.get_entry(title),
        "form": WikiSearch(request.POST or None)
    })
    
