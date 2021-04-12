# Authenticate user credentials
from google.colab import auth
auth.authenticate_user()

# API key and enpoints
key = API_KEY
NewListID = LIST_ENDPOINT_ID
VendorListID = VENDOR_ENDPOINT_ID

# Import modules
import requests
import json
import hashlib
import gspread
from oauth2client.client import GoogleCredentials
from mc_api_functions import subscribe, unsubscribe

# Import data from Google sheets
gc = gspread.authorize(GoogleCredentials.get_application_default())

keyword_worksheet = gc.open('Emails/domains').worksheet('Keywords')
keyword_rows = keword_worksheet.get_all_values()
keywords = [i.pop().lower() for i in keyword_rows]

vendor_worksheet = gc.open('Emails/domains').worksheet('Vendors')
vendor_rows = worksheet.get_all_values()
vendor_keywords = [i.pop().lower() for i in vendor_rows]

# API links
api_link = 'https://us6.api.mailchimp.com/'
export_endpoint = 'export/1.0/list'
NewList_endpoint = f'3.0/lists/{NewListID}/members/'
VendorList_endpoint = f'3.0/lists/{VendorListID}/members/'
export_link = api_link + export_endpoint

# Retrieve API data from API
retrieve_params = {'apikey':key, 'id':NewListID}
mc_data = requests.get(export_link, params=retrieve_params)

# Create subscriber list from API data
api_string = mc_data.text.lower()
api_split_string = api_string.split('"')
subscribers = [i for i in api_split_string if '@' in i]

# Create unsubscribe list by iterating keywords over subscriber list
unsubscribe_list = []
for keyword in keywords:
    unsubscribe_list += [email for email in subscribers if keyword in email]
print(f'{len(unsubscribe)} emails to be removed.')

# Create vendor subscribe list
vendor_list = []
for keyword in vendor_keywords:
    vendor_list += [email for email in subscribers if keyword in email]
print(f'{len(vendor_list)} vendor emails found.')

# Unsubscribe report
unsub_audit = unsubscribe()
unsub_set = set()
try:
    for i in unsub_audit:
        unsub_set.add(i[1:3])
except:
    unsub_set.add((200, 'OK'))    

# Subscribe report
sub_audit = subscribe()
sub_set = set()
try:
    for i in sub_audit:
        sub_set.add(i[1:3])
except:
    sub_set.add((200, 'OK')
print(sub_set)
for i in sub_audit:
    if i[1] == 400:
        print(i)
