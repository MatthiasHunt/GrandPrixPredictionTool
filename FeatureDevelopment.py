#This adds the feature "Days since set release" by using data from a separate Wikipedia Page

from bs4 import BeautifulSoup
import requests
import datetime
import pandas as pd
import numpy as np

#GrandPrix class will be used to process CSV data

#Global Variable that is a collection of datetime.date objects
_release_dates = None

class GrandPrix:
    
    def __init__(self,season,location,gp_format,gp_date,winner,attendance):
        self.season = season
        self.location = location
        self.gp_format = gp_format
        self.gp_date = gp_date.to_pydatetime().date()
        self.winner = winner
        self.attendance = attendance
        
    def days_since_release(self):
        # If Release Dates have not been scraped yet, scrapes them to a global variable
        global _release_dates
        if _release_dates is None:
            # Last checked page for compatibility on 05.24.2018
            Set_Release_URL = 'https://en.wikipedia.org/wiki/List_of_Magic:_The_Gathering_sets'
            r = requests.get(Set_Release_URL)
            soup = BeautifulSoup(r.content, 'lxml')

            _release_dates = []
            tables = soup.find_all('table',{'class':'wikitable'})

            #Core Set Table
            rows = tables[0].find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                try:
                    set_release = cells[4].text
                    #Eliminate Footnotes
                    if set_release[-1:] == "]":
                        set_release = set_release[:set_release.index("[")]
                    #Dates in this table take on two possible formats. Day set to 1 when no day available
                    if len(set_release.split()) == 2:
                        set_date = datetime.datetime.strptime(set_release,"%B %Y")
                        print(set_date)
                    else:
                        set_date = datetime.datetime.strptime(set_release,"%B %d, %Y")
                        print(set_date)
                    _release_dates.append(set_date.date())
                except (IndexError, ValueError):
                    continue
                
            #Table of Expansion Sets
            rows = tables[1].find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                try:
                    set_release = cells[5].text
                    #Eliminate Footnotes
                    if set_release[-1:] == "]":
                        set_release = set_release[:set_release.index("[")]
                    #Dates in this table take on two possible formats. Day set to 1 when no day available
                    if len(set_release.split()) == 2:
                        set_date = datetime.datetime.strptime(set_release,"%B %Y")
                        print(set_date)
                    else:
                        set_date = datetime.datetime.strptime(set_release,"%B %d, %Y")
                        print(set_date)
                    _release_dates.append(set_date.date())
                except (IndexError, ValueError):
                    continue
        
        #Code for actual member function goes here
        days_passed = min([(self.gp_date - set_release).days for set_release in _release_dates if (self.gp_date - set_release).days >= 0])
        return days_passed
    
    def getRegion(self):
        #List of cities manually coded by region
        cities_by_region = {'Western US/CA': ['Anaheim','Las Vegas','Los Angeles','Oakland','Portland','Sacramento','San Diego','San Francisco','San Jose','Santa Clara','Seattle','Vancouver'],
                            'Northeast US/CA': ['Atlantic City','Baltimore','Boston','Boston-Worcester','Hartford','Massachusetts','Montreal','New Jersey','New York City','Ottawa','Philadelphia','Providence','Quebec City','Richmond','Washington, D.C.'],
                            'Midwest US/CA':['Charleston','Charlotte','Chicago','Cincinnati','Cleveland','Columbus','Detroit','Indianapolis','Louisville','Pittsburgh','Toronto'],
                            'General US/CA':['Albuquerque','Atlanta','Austin','Birmingham','Calgary','Dallas','Daytona Beach','Denver','Houston','Kansas City','Lincoln','Madison','Memphis','Miami','Milwaukee','Minneapolis','Nashville','New Orleans','Oklahoma City','Omaha','Orlando','Phoenix','Salt Lake City','San Antonio','St. Louis','Tampa'],
                            'Western Continental Europe':['Amsterdam','Antwerp','Barcelona','Biarritz','Bilbao','Bochum','Bologna','Brussels','Cannes','Cologne','Como','Copenhagen','Dortmund','Eindhoven','Florence','Frankfurt','Genoa','Ghent','Gothenburg','Hamburg','Hanover','Hasselt','Heidelberg','Leipzig','Lille','Lisbon','Lyon','Madrid','Metz','Milan','Munich','Naples','Paris','Porto','Reims','Rimini','Rotterdam','Sevilla','Seville','Strasbourg','Stuttgart','Toulouse','Tours','Turin','Utrecht','Valencia','Verona','Vienna','Zürich'],
                            'Other Europe':['Athens','Brighton','Cardiff','Helsinki','Krakow','Kraków','Liverpool','London','Malmö','Manchester','Moscow','Nottingham','Oslo','Prague','Stockholm','Warsaw'],
                            'Latin America':['Buenos Aires','Curitiba','Guadalajara','Mexico City','Porto Alegre','Rio de Janeiro','Santiago','São Paulo'],
                            'Japan':['Chiba','Fukuoka','Hamamatsu','Hiroshima','Kitakyushu','Kobe','Kyoto','Kyushu','Matsuyama','Nagoya','Niigata','Okayama','Osaka','Sapporo','Sendai','Shizuoka','Tohoku','Tokyo','Utsunomiya','Yamagata','Yokohama'],
                            'Other Asia':['Bangkok','Beijing','Guangzhou','Hong Kong','Kaohsiung','Kuala Lumpur','Manila','Shanghai','Singapore','Taipei'],
                            'Other':['Auckland','Brisbane','Cape Town','Melbourne','Sydney']}
        for region in cities_by_region:
            if self.location in cities_by_region[region]:
                return region
        return "Other"
    
    
#Read each GP From the CSV file and create GrandPrix object
gp_data = pd.read_csv("gp_data.csv")
gp_data['Date'] = pd.to_datetime(gp_data.Date)
for i in range(gp_data.shape[0]):
    event = GrandPrix(gp_data.iloc[i,0],gp_data.iloc[i,1],gp_data.iloc[i,2],gp_data.iloc[i,3],gp_data.iloc[i,4],gp_data.iloc[i,5])
#    print(event.days_since_release())
#    print(event.getRegion())

