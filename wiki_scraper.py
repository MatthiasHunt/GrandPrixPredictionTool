# This Scraper takes Grand Prix data from Wikipedia and converts it to a csv file for later use
# TODO have it produce a SQL friendly format

from bs4 import BeautifulSoup
import requests
import unicodecsv

# Last checked page for compatibility on 05.23.2018

Grand_Prix_URL = 'https://en.wikipedia.org/wiki/List_of_Magic:_The_Gathering_Grand_Prix_events'
r = requests.get(Grand_Prix_URL)
soup = BeautifulSoup(r.content, 'lxml')
table_data = []

# Helper functions I'm going to use while cleaning the data
def EditOut(string,a,b):
    while string.find(a) != -1 and string.find(b) != -1:
        before_snip = string[0:string.find(a)]
        after_snip = string[string.find(b)+1:]
        string = before_snip + after_snip
    return string

# Initialize our CSV with empty values
wikitable = soup.find('table', {'class':'wikitable sortable'})
rows = wikitable.find_all('tr')
nrows = len(rows)
ncolumns = 6
    
#  Table Headers
table_data.append(["Season","Location","Format","Date","Winner","Attendance"])
    
# Add Wikitable data to our table
for i in range(1,nrows):
    row = rows[i]
    # Cells are, in order, {Season, Location, Format, Date, Winner, Players}
    cells = row.find_all(['td','th'])
    # No reformatting needed for Season
    cells[0] = cells[0].text
    # Location needs to be removed from hyperlink
    cells[1] = cells[1].text
    # Remove any astrisks and parenthesis from Format
    cells[2] = cells[2].text.replace('*','')
    cells[2] = EditOut(cells[2],'(',')').rstrip()
    # Date range changed to just the end date of the event
    if cells[3].find('span'):
        date_text = cells[3].find('span')
        cells[3] = str(date_text)[44:54]
    else:
        date_text = cells[3].text
        date_text = date_text.replace(u'\u2013','-')
        cells[3] = date_text[date_text.index('-')+1:]
    # Winner reduced to just names
    winners = cells[4].find_all('span',{'class':'sorttext'})
    if winners:
        winners_names = [winner.text for winner in winners]
        cells[4] = ", ".join(winners_names)
    else:
        cells[4] = ''
    # Team Counts Edited Out
    cells[5] = EditOut(cells[5].text,'(',')').rstrip()
    
    table_data.append(cells)

# Write To Our CSV file
with open('gp_data.csv','wb') as csv_file:
    csv_writer = unicodecsv.writer(csv_file)
    for i in range(nrows):
        print(table_data[i])
        csv_writer.writerow(table_data[i])
    
csv_file.close()

