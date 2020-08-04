from django.shortcuts import render
import random

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse

from django import forms
from .models import Entry
from markdown2 import Markdown




class NameForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    content = forms.CharField(widget=forms.Textarea,label='Content')

def index(request):
    """The Home Page for topic names"""
    entries=util.list_entries()
    context={'entries':entries}
    return render(request,'encyclopedia/index.html',context)


def entry(request,entry_name):
    markdowner = Markdown()
    try:
        entry=util.get_entry(entry_name)
        html_entry=markdowner.convert(entry)
    except TypeError:
        return render(request,"encyclopedia/404.html")
    context={'entry':html_entry,'entry_title':entry_name}
    return render(request,'encyclopedia/entry.html',context)

def newpage(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            obj = NameForm()
            obj.title = form.cleaned_data['title']
            obj.content = form.cleaned_data['content']
            filename = f"entries/{obj.title}.md"
            if default_storage.exists(filename):
                return HttpResponseRedirect(reverse("encyclopedia:exist"))
            util.save_entry(obj.title,obj.content)
                

            return HttpResponseRedirect(reverse("encyclopedia:index"))

    else:
        return render(request, "encyclopedia/newpage.html", {
            "form": NameForm()

        })

def randomfunction(request):
    markdowner = Markdown()
    #getting a random item from the list
    entries=util.list_entries()
    entry=random.choice(entries)
    #by using that random item, retrieving that item in md format
    entry_name=util.get_entry(entry)
    #converting it back to html and passing as a context
    html_random_entry=markdowner.convert(entry_name)
    context={'entry':html_random_entry}
    return render(request,"encyclopedia/random.html",context)


def edit(request,entry_title):
    form=NameForm()
    if request.method !='POST':
            #Initial request; pre-filled form with the current entry
            form=NameForm({'title':entry_title,'content':util.get_entry(entry_title)})
    else:
        form = NameForm(request.POST)
        if form.is_valid():
            obj = NameForm()
            obj.title = form.cleaned_data['title']
            obj.content = form.cleaned_data['content']
            util.edit_entry(obj.title,obj.content)
            return HttpResponseRedirect(reverse("encyclopedia:index"))

    context={'form':form,'entry_title':entry_title}
    return render(request,"encyclopedia/edit.html",context)



def search(request):        
    if request.method == 'GET': # this will be GET now     
        title =  request.GET.get('q') # do some research what it does
        try:
            content=util.get_entry(title) 
            html=converterFactory(content)  
        except TypeError:
            return render(request,"encyclopedia/404.html")
        return render(request,"encyclopedia/search.html",{"content":html})
    else:
        return render(request,"encyclopedia/404.html")


def converterFactory(mdContent):
    markdown=Markdown()
    HtmlContent=markdown.convert(mdContent)
    return HtmlContent


def exist(request):
    return render(request,"encyclopedia/exist.html")


