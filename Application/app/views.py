"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from django.template import RequestContext
from datetime import datetime
from python_webapp_django.settings import BASE_DIR
from django.core.exceptions import ObjectDoesNotExist
from app.models import *
from app.forms import *
import pandas as pd
from django.core import serializers
import json

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    # Camps.objects.create(
    #     name = "India4Kerala Camp",
    #     currentPeople = 0,
    #     capacity = 80,
    #     contact = 9122591910,
    #     lat = 8.859175, 
    #     lon = 76.782781 
    # )

    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            # 'locations' : locations[:10]
        }
    )

def maps(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    rescue = RescueSpot.objects.all()

    print(rescue)

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
            'locations' : locations[:10],
            'newlocations' : rescue
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

def addToDB(form):
    form = form.cleaned_data
    print(form)

    camp = Camps.objects.get(name = form["camp"])
    camp.capacity -= form["noOfPeople"]
    if(camp.capacity < 0): 
        camp.capacity = 0
    camp.save()


    specialneeds = form["specialNeeds"]
    l = [[i for i in j.strip().split(' ')] for j in specialneeds.split(';')]

    for i in l:
        try:
            created2 = ResourcesAvail.objects.get(cid = camp, resource=i[0])
        except ObjectDoesNotExist:
            if(i[0]!=''):
                ResourcesAvail.objects.create(
                    cid = camp,
                    resource = i[0],
                    qty = 0,
                    unit = ''
                )      
        try:        
            created = ResourcesNeed.objects.get(cid = camp, resource=i[0])
            # print(created.qty)
            created.qty = int(created.qty) + int(i[1])
            created.save()

        except ObjectDoesNotExist:
            if(i[0]!=''):
                ResourcesNeed.objects.create(
                    cid = camp,
                    resource = i[0],
                    qty = i[1],
                    unit = i[2]
                )
           

        


def AddNewRefugee(request):
    if request.method == 'POST':
        form = NewRefugee(request.POST)
        if form.is_valid():
            addToDB(form)
            return render(request, 'app/newref.html', {'form':form, 'recv':"Added Successfully"})
    else:
        form = NewRefugee()

    return render(request, 'app/newref.html', {'form':form})

def viewResources(request):
    if request.method == 'POST':
        form = ChooseCamp(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            camp = Camps.objects.get(name = form["camp"])
            rescA = ResourcesAvail.objects.filter(cid = camp)
            rescN = ResourcesNeed.objects.filter(cid = camp)        

            print(rescN)
            
            form = ChooseCamp()
            
            return render(request, 'app/allresources.html', {'form':form, 'rescA':rescA, 'rescN':rescN})


    else:
        form = ChooseCamp()

    return render(request, 'app/allresources.html', {'form':form})




def returnClosestCamps(request):
    camps = Camps.objects.filter(currentPeople__gt = 0)

    camps_json = serializers.serialize('json', camps)
    return HttpResponse(camps_json, content_type='application/json')

def AddRescueSpot(request):
    #print(request.body.decode('ascii'))
    obj = json.loads(request.body.decode('ascii'))
    print(obj)
    spot = RescueSpot()
    spot.lat = obj["lat"]
    spot.lon = obj["lon"]
    try:
        spot.description = obj["ppl"]
    except:
        pass

    spot.save()
    return HttpResponse("Saved Successfully")
