from functools import reduce
from os import remove

from django.http import HttpResponse
from django.shortcuts import render, redirect


def index(request):
    params = {'name':'dino','place':'Earth'}
    return render(request,'index.html',params)


def login(request):
    return redirect('login')

def signUp(request):
    return render(request,'signUp.html')


# def analyze(request):
#     text = request.POST.get('text','default')
#     removepunc = request.POST.get('removepunc','off')
#     capitalize = request.POST.get('capitalize','off')
#     analyzed = text
#
#     def removepuncFunction(text):
#         punctuations = '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''
#         temp = ''
#         for char in text:
#             if(char not in punctuations):
#                 temp += char
#         return temp
#
#     def capitalizeFunction(text):
#         return text.upper()
#
#     if(removepunc == 'on'):
#         analyzed = removepuncFunction(analyzed)
#     if(capitalize == 'on'):
#         analyzed = capitalizeFunction(analyzed)
#     params = {'purpose':'Removed Punctuations','analyzed_text':analyzed}
#     return render(request,'analyze.html',params)
