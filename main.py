#Activate Skicaster environment
import requests as rq 
from bs4 import BeautifulSoup as Soup 

#Download and save today's Avalance Canada data
r1 = rq.get('https://avalanche.pc.gc.ca/bulletin-eng.aspx?r=1&d=TODAY')
r1.raise_for_status()
open('avalanche_data_today.html', 'wb').write(r1.content)
open('avalanche_data_today.txt', 'wb').write(r1.content)
with open('avalanche_data_today.html', 'r') as file:
    r1_data = file.read()

#Parse the html file
r1_data = Soup(r1_data, 'html.parser')
r1_AP_element = r1_data.select('#pageContent_lblFirstdayAlpineRateHeader')
r1_TL_element = r1_data.select('#pageContent_lblFirstdayTreelineRateHeader')
r1_BT_element = r1_data.select('#pageContent_lblFirstdayBelowtreelineRateHeader')


#open('log.txt', 'w').write(str(txt))



#test
print(r1_AP_element[0].text)
print(r1_TL_element[0].text)
print(r1_BT_element[0].text)



