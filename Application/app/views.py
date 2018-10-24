"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from python_webapp_django.settings import BASE_DIR
import pandas as pd

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)


    data = pd.read_csv(BASE_DIR+'/app/static/app/data/keralaTweetDump3.csv',delimiter=';')
    locations = data['Location'].tolist()
    descriptions = data['Status'].tolist()
    locations = zip(locations,descriptions)
    locations = list(set(locations))

    print(locations)

    return render(
        request,
        'app/map.html',
        {
            # 'title':'Home Page',
            # 'year':datetime.now().year,
            'locations' : locations[:5]
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
