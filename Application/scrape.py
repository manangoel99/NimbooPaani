import requests
import PyPDF2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()

driver.get("http://www.imd.gov.in/pages/allindiawxwarningbulletin.php")
elem = driver.find_element_by_tag_name("iframe")
response = requests.get(elem.get_attribute("src"))
#print(response.content)
with open("./x.pdf", 'wb') as f:
    f.write(response.content)

PDF = open("x.pdf", 'rb')

reader = PyPDF2.PdfFileReader(PDF)

for page in range(reader.numPages):
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
    print(key_phrases)
