#Activate Skicaster environment
import requests as rq 
from bs4 import BeautifulSoup as soup 
import psycopg2 as postgres
import re 



def main():
        #Establish connection to database
        day = datetime.date
        try:
            conn = postgres.connect('dbname = skicasterDB user = postgres password = password')
            curr = conn.cursor()

            #Get daily conditions
            conditions = daily_conditions()
            push_to_database(conditions, curr, day)

            #Close connection
            curr.close()
            conn.close()

        except Exception as error:
            print('The following error occured: %s', error)    


def daily_conditions():
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
        result_param = []
        rating_arr = []
        rating_desc_arr = []
        rating_regex = re.compile('\d')
        rating_desc_regex = re.compile('\w+$')

        #Run through the loop once for each level (Alpine/Treeline/Below Treeline)
        #Returns an array eg: [3 ,2, 1, "considerable", "moderate", "low"]
        for i in range(0,len(data_param)):
            result = r1_soup.select(str(data_param[i]))
            result_param.append(result[0].text) 
            rating_arr.append(int(rating_regex.search(result_param[i]).group()))
            rating_desc_arr.append(rating_desc_regex.search(result_param[i]).group())

        
        return ['Daily'] + rating_arr + rating_desc_arr



def push_to_database(data, curr, date):
    
    #Determine the datasource
    if data[0] in ['Daily']:

        try:
        pg_insert =  ''' INSERT INTO Location_R1 (BT_Rating, BT_Desc, TL_Rating, TL_Desc, AP_Rating, AP_Desc) VALUES (%s,%s,%s)'''

        print('Daily')
        except:



main()
