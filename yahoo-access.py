import pandas as pd
import json
import rauth
import webbrowser
import time
import xmljson
from xml.etree import ElementTree as ET

# =============================================================================
# Helper functions
# =============================================================================
def access_parse(raw_access):
    """
    Parse oauth2 access
    """
    parsed_access = json.loads(raw_access.content.decode('utf-8'))
    access_token = parsed_access['access_token']
    token_type = parsed_access['token_type']
    refresh_token = parsed_access['refresh_token']
    guid = parsed_access['xoauth_yahoo_guid']
    #build a dictionary to hold everything
    credentials = {
            'access_token': access_token,
            'token_type': token_type,
            'refresh_token': refresh_token,
            'guid': guid
            }
    return credentials


def oauth_headers():
    """
    Generate header for oauth2
    """
    import base64
    encoded_credentials = base64.b64encode(('{0}:{1}'.format(oauth.client_id, oauth.client_secret)).encode('utf-8'))
    headers = {
            'Authorization': 'Basic {0}'.format(encoded_credentials.decode('utf-8')),
            'Content-Type': 'application/x-www-form-urlencoded'
            }
    return headers


def refresh_access_token():
    """
    Refresh access token
    """
    headers = oauth_headers()
    data = {
            'refresh_token': credentials['refresh_token'],
            'redirect_uri': redirect_uri,
            'grant_type': 'refresh_token'
            }
    raw_access = oauth.get_raw_access_token(data=data, headers=headers)
    parsed = access_parse(raw_access)
    credentials.update(parsed)
    return credentials
    

def token_valid_check():
    """ 
    Checks to see if the token is still valid
    """
    #calculate the time elapsed since token was last refreshed
    elapsed_time = time.time() - start_time
    #take action if token is expired
    if elapsed_time > 3540:
        return False
    return True


# =============================================================================
# Project code
# =============================================================================
project_path = 'C:/Users/Joe/Desktop/fantasy-football-analysis/'

#read in the api keys
with open(project_path+'yahoo-api-key-secret.json') as api:
    file = json.load(api)
    key = file['consumer_key']
    secret = file['consumer_secret']

#create OAuth2 object
oauth = rauth.OAuth2Service(client_id=key,
                            client_secret=secret,
                            name='yahoo',
                            access_token_url='https://api.login.yahoo.com/oauth2/get_token',
                            authorize_url='https://api.login.yahoo.com/oauth2/request_auth',
                            base_url='https://fantasysports.yahooapis.com/')

#create parameters for API authorization
redirect_uri = 'oob'
params = {'client_secret': oauth.client_secret,
          'redirect_uri': redirect_uri,
          'response_type': 'code'}
#store the access code
url = oauth.get_authorize_url(**params)

#open a web browser to get access token and then store it via manual input
webbrowser.open(url)
code = input('Enter code: ')
#create credentials item
start_time = time.time()
#create dictionary to hold credentials and store beginning time
credentials = {'token_time': start_time}

#create parameters
data = {'code': code,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'}
#build the headers
headers = oauth_headers()
#create the raw access token
raw_access = oauth.get_raw_access_token(data=data, headers=headers)
#parse the raw access token and add to credentials variable
credentials.update(access_parse(raw_access))

#start a session
access_token = credentials['access_token']
s = oauth.get_session(token=access_token)


# =============================================================================
# Build available players query
# =============================================================================
base_query_url = oauth.base_url + 'fantasy/v2/league/'
leagueID = 'nfl.l.778518'
teamID = '.t.2'

#initialize everything
last_first_names = []
full_names = []
player_key = []
start = 1
done = False

#loop thru to get all of the players available
#while(not done):
query_url = base_query_url + leagueID + '/players;status=A;sort=PTS;start=%s,count=25' %start

r = s.get(query_url, params={'format': 'json'})
output = r.json()
output = output['fantasy_content']
output = output['league']
output = output[1]
output = output['players']
count = output['count']
player_num = list(output.keys())
player_num = player_num[0:len(player_num)-1]
#grab the names for each of the players in this batch of players
for i in player_num:
    #get to player details
    output1 = output[i]
    output1 = output1['player']
    output1 = output1[0]
    #get player name
    output_name = output1[2]
    output_name = output_name['name']
    first = output_name['first']
    last = output_name['last']
    full = output_name['full']
    last_first = last + ', ' + first
    #get player key
    output_key = list(output1[0].values())[0]
    #add items to lists
    last_first_names.append(last_first)
    full_names.append(full)
    player_key.append(output_key)

    
    
    #stopping rule
#    start += 25
#    if count < 25:
#        done = True

