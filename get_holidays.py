import json
import requests
import pandas as pd 
import datetime as datetime

def	get_holidays():

	URL = 'https://calendarific.com/api/v2/holidays?'

#list of countries 

	country_list = ['UK','PL','RO','MX']
	name = []
	date = []
	country_name = []

#get holidays data for each country

	for country in country_list:
	    parameters = {
	        # Required
	        'country': country,
	        'year':    2021,
	        'api_key' : 'your_api_key'
	    }
	    
	    response = requests.get(URL, params=parameters);
	    data     = json.loads(response.text)

	    for item in data['response']['holidays']:
	        name.append(item['name'])
	        date.append(item['date']['iso'])
	        country_name.append(item['country']['name'])

#create DataFrame object	    
	dic = {'name' :name, 'date': date, 'country' : country_name }


	df = pd.DataFrame(dic)

#clean dates and get first 5 holidays

	df['date'] = df['date'].str[:10]
	df['date'] = pd.to_datetime(df.date, format = '%Y-%m-%d') 
	df.sort_values(by='date')
	df = df.loc[df.date >=  datetime.datetime.today()]
	df['date'] = df['date'].dt.strftime('%Y-%m-%d')	


	df.head(5).to_json('holidays.json', orient = 'split' ,index = False )

if __name__ == "__main__":
	
	get_holidays()
