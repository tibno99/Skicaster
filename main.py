#Activate Skicaster environment
import requests as rq 
from bs4 import BeautifulSoup as soup 
import psycopg2 as postgres
import re 
import datetime



def main():
    #Establish connection to database
    try:
        conn = postgres.connect('dbname = skicasterDB user = postgres password = password')
        curr = conn.cursor()

    except Exception as error:
        print('The following error occured: %s', error)    

    #Get the daily conditions and push them to database
    daily_conditions()

    #Close connection
    curr.close()
    conn.close()

#Creates a dictionary with none values based off provided keys
def empty_dictionary(keys):
    dictionary = {}
    return dictionary.fromkeys(keys, None)
        

def daily_conditions():

    #Initialize dictionary with which we will use to pull data
    keys = ['AP Rating', 'AP Desc', 'TL Rating', 'TL Desc', 'BT Rating', 'BT Desc']
    data_dict = empty_dictionary(keys)

    #Download and save today's Avalance Canada data
    r1 = rq.get('https://avalanche.pc.gc.ca/bulletin-eng.aspx?r=1&d=TODAY')
    r1.raise_for_status()
    open('avalanche_data_today.html', 'wb').write(r1.content)
    open('avalanche_data_today.txt', 'wb').write(r1.content)
    with open('avalanche_data_today.html', 'r') as file:
        r1_data = file.read()

    #Parse the html file & use regex to separate the rating from the description
    r1_soup = soup(r1_data, 'html.parser')
    data_param = ['#pageContent_lblFirstdayAlpineRateHeader','#pageContent_lblFirstdayTreelineRateHeader', '#pageContent_lblFirstdayBelowtreelineRateHeader' ]
    rating_arr = []
    rating_regex = re.compile('\d')
    rating_desc_regex = re.compile('\w+$')

    #Run through the loop once for each level (Alpine/Treeline/Below Treeline)
    #Returns an array eg: [3 ,"considerable", 2, "moderate", 1, "low"]
    #Puts these values in a dictionary for ease of transfer to db
    for i in range(0,len(data_param)):
        result = r1_soup.select(str(data_param[i]))
        rating_arr.append(int(rating_regex.search(result[0].text).group()))
        rating_arr.append(rating_desc_regex.search(result[0].text).group())

    i = 0
    for key in data_dict:
        data_dict[key] = rating_arr[i]
        i += 1

    data_dict['Date'] = str(datetime.date.today())
    print(data_dict)

    #push results to the database
    push_to_db(data_dict)

    return

def push_to_db(dictionary):
    return

main()
