from django.shortcuts import render
from django.contrib import messages

import os.path


def index(request):
    homedir = os.path.expanduser("~")
    dirs=homedir +'/Downloads'
    
    if request.method == "POST":
        url=request.POST.get('link')

    return render(request, 'core/index.html')
