"""
Definition of views.
"""

import json
from datetime import datetime

import pandas as pd
import requests
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template import RequestContext

from app.forms import *
from app.models import *
from python_webapp_django.settings import BASE_DIR


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

    #getPhrases()

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


def getPhrases():
    driver = webdriver.Firefox()

    driver.get("http://www.imd.gov.in/pages/allindiawxwarningbulletin.php")
    elem = driver.find_element_by_tag_name("iframe")
    response = requests.get(elem.get_attribute("src"))
    #print(response.content)
    with open("./x.pdf", 'wb') as f:
        f.write(response.content)

    PDF = open("x.pdf", 'rb')

    reader = PyPDF2.PdfFileReader(PDF)

    phrase_list = []

    for page in range(1):
        pageObj = reader.getPage(page)
        #print(pageObj.extractText())
        data = pageObj.extractText()
        subscription_key = '600731bee309440d84da055472e37a23'
        assert subscription_key

        text_analytics_base_url = "https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/"

        key_phrase_api_url = text_analytics_base_url + "keyPhrases"

        documents = {'documents': [
            {
                'id': '1',
                'language': 'en',
                'text': data,
            }
        ]}

        headers = {'Ocp-Apim-Subscription-Key': subscription_key}
        response = requests.post(
            key_phrase_api_url, headers=headers, json=documents)
        key_phrases = response.json()
        #return key_phrases
        #print(key_phrases['documents'][0]['keyPhrases'])

        for phrase in key_phrases['documents'][0]['keyPhrases']:
            if phrase != "Service" or phrase != 'Nation' or phrase != "contact" or "india" not in phrase or "India" not in phrase:
                phrase_list.append(phrase)
    #print(phrase_list)

    obj_list = []

    for phrase in phrase_list:
        phrase = phrase.split(" ")
        ph = ''
        for p in phrase:
            ph += p + '+'
        ph = ph[:-1]
        url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + \
            ph + "&key=AIzaSyBoWI6Ak-GWL6mOdGZ-vrkUIc7WSmNF6VE"

        #print(url)
        response = requests.get(url)
        obj = json.loads(response.content.decode('ascii'))

        if obj["status"] == 'OK':
            z = obj["results"][0]["geometry"]["location"]
            if z["lat"] >= 8.4 and z["lat"] <= 35.3:
                if z["lng"] >= 68.7 and z["lng"] <= 97.25:
                    if "India" not in ph:
                        x = {}
                        x["Name"] = ph.replace("+", " ")
                        x["Lon"] = z["lng"]
                        x["Lat"] = z["lat"]
                        obj_list.append(x)

        for o in obj_list:
            place = ForecastPlace()
            place.name = o["Name"]
            place.lat = o["Lat"]
            place.lon = o["Lon"]
            place.save()

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
