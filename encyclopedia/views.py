from django.shortcuts import render
import random

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
    entry=util.get_entry(entry_name)
    html_entry=markdowner.convert(entry)
    context={'entry':html_entry,'entry_title':entry_name}
    return render(request,'encyclopedia/entry.html',context)

def newpage(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            obj = NameForm()
            obj.title = form.cleaned_data['title']
            obj.content = form.cleaned_data['content']
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
            util.save_entry(obj.title,obj.content)
            return HttpResponseRedirect(reverse("encyclopedia:index"))

    context={'form':form,'entry_title':entry_title}
    return render(request,"encyclopedia/edit.html",context)
