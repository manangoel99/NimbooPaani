"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from django.template import RequestContext
from datetime import datetime
from python_webapp_django.settings import BASE_DIR
from app.models import *
import pandas as pd
from django.core import serializers

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    # Camps.objects.create(
    #     name = "CM's Relief Fund",
    #     capacity = 20,
    #     contact = 9125891910,
    #     lat = 10.027458,
    #     lon = 76.338064 
          
    # )


    data = pd.read_csv(BASE_DIR+'/app/static/app/data/keralaTweetDump3.csv',delimiter=';')
    locations = data['Location'].tolist()
    descriptions = data['Status'].tolist()
    people = data['People'].tolist()
    locations = zip(locations,descriptions,people)
    locations = list(set(locations))

    print(locations)

    return render(
        request,
        'app/map.html',
        {
            # 'title':'Home Page',
            # 'year':datetime.now().year,
            'locations' : locations[:10]
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


def returnClosestCamps(request):
    camps = Camps.objects.filter(capacity__gt = 0)

    camps_json = serializers.serialize('json', camps)
    return HttpResponse(camps_json, content_type='application/json')
