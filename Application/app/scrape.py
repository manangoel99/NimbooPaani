import requests
import PyPDF2
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

try:
    from .models import ForecastPlace
except:
    try:
        from models import ForecastPlace
    except:
        try:
            from app.models import ForecastPlace
        except:
            print("Python chutiya")

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

        documents = {'documents' : [
            {
                'id' : '1',
                'language' : 'en',
                'text' : data,
            }
        ]}

        headers = {'Ocp-Apim-Subscription-Key': subscription_key}
        response = requests.post(key_phrase_api_url, headers=headers, json=documents)
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
        url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + ph + "&key=AIzaSyBoWI6Ak-GWL6mOdGZ-vrkUIc7WSmNF6VE"

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
            place = models.ForecastPlace()
            place.name = o["Name"]
            place.lat = o["Lat"]
            place.lon = o["Lon"]
            place.save()

getPhrases()

