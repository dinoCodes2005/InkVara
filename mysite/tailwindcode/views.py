from functools import reduce
from os import remove

from django.http import HttpResponse
from django.shortcuts import render, redirect


def tailwind(request):
    return render(request,'base.html')



