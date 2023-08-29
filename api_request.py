#AZAD_HOSSEN
from pprint import pprint
import httplib2
import csv
#from apiclient.discovery import build
from googleapiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
import urllib.parse

def send_request(service, property_uri, request):
    return service.searchanalytics().query(
        siteUrl=property_uri, body=request).execute()

# Copy your credentials from the console
CLIENT_ID = 'YOUR_CLIENT_ID' #your CLIENT_ID
CLIENT_SECRET = 'YOUR_CLIENT_SECRET' #your CLIENT_SECRET
OAUTH_SCOPE = 'https://www.googleapis.com/auth/webmasters.readonly'
REDIRECT_URI = 'https://www.domain.com' #put your redirect url
flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
authorize_url = flow.step1_get_authorize_url()
print('Click the link and authorize: ' + authorize_url)
code = input('Enter the full link: ').strip()
code = urllib.parse.unquote(code).split('&')[0].split('code=')[1]
credentials = flow.step2_exchange(code)
http = httplib2.Http()
http = credentials.authorize(http)
search_console_ser = build('searchconsole', 'v1', http=http)
site_list = search_console_ser.sites().list().execute()
request = {
    'startDate': '2021-07-01', #put start date
    'endDate': '2023-08-27', #put end date
    'dimensions': ['query'], #other dimenssions: page, query, country, device, searchAppearance
    'rowLimit': 25000, #set limit between 0 to 25000
    'startRow': 100000 #initially set 0
}

# site_list = webmasters_service.sites().list().execute()
# print(site_list)
#for root domain put sc-domain:
get_response = send_request(search_console_ser, 'YOUR-DOMAIN', request) #put the domain here

#writingg to csv
csv_file = open('query_haha.csv','a+',encoding='utf-8-sig',errors='ignore', newline='')
writer = csv.writer(csv_file)
writer.writerow(['query','impressions','clicks']) #comment after running for the 1st time
x = get_response['rows']
for i in x:
    query = i['keys'][0]
    impressions = i['impressions']
    clicks = i['clicks']
    writer.writerow([query,impressions,clicks])
csv_file.close()
#END
