import pandas as pd
import json
import rauth
import webbrowser
import time

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


def oauth_headers(oauth):
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


def refresh_access_token(credentials, redirect_uri):
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
    

def token_valid_check(start_time):
    """ 
    Checks to see if the token is still valid
    """
    #calculate the time elapsed since token was last refreshed
    elapsed_time = time.time() - start_time
    #take action if token is expired
    if elapsed_time > 3540:
        return False
    return True


def create_access_token(oauth):
	"""
    Creates an access token from the supplied oauth2.0 object
    """
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

	#NEED TO ADD IN 'REFRESH TOKEN' FUNCTION HERE SOMEWHERE
	#
	
	#create parameters
	data = {'code': code,
			'redirect_uri': redirect_uri,
			'grant_type': 'authorization_code'}
	#build the headers
	headers = oauth_headers(oauth)
	#create the raw access token
	raw_access = oauth.get_raw_access_token(data=data, headers=headers)
	#parse the raw access token and add to credentials variable
	credentials.update(access_parse(raw_access))

	#parse access token from credentials
	access_token = credentials['access_token']
	#return access token
	return access_token
	
	
# =============================================================================
# Project code
# =============================================================================
def query_setup():
	project_path = 'C:/Users/Joe/Projects/fantasy_football/'

	#read in the api keys
	with open(project_path+'yahoo_api_key.json') as api:
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

	access_token = create_access_token(oauth)
	s = oauth.get_session(token=access_token)
	#return session
	return s, oauth.base_url


def available_players_query():
	"""
	API query to return all available players, ssorted by number of fantasy points\n
	Returns three lists: players' full names, their associated Yahoo API player key, and their main position
	"""
	#start the calculation timer
	calc_start = time.time()

	#initialize everything
	last_first_names = []
	full_names = []
	player_key = []
	player_pos = []
	start = 1
	done = False

	#this is where the data is actually created
	#loop thru to get all of the players available
	while(not done):
		query_url = base_query_url + 'league/' + leagueID + '/players;status=A;sort=PTS;start=%s;count=25' %start
		
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
			#get player position
			output_pos = list(output1[9].values())[0]
            #add items to lists
			last_first_names.append(last_first)
			full_names.append(full)
			player_key.append(output_key)
			player_pos.append(output_pos)
		
		#stopping rule: if the number of players on the page is less than 25, then stop
		start += 25
		if count < 25:
			done = True

	#stop the timer
	calc_end = time.time()
	#print the calculation time
	print('Process complete')
	print('Calculation time for all available players: {0:0.2f} seconds'.format((calc_end-calc_start)))
	#return the players name and player key lists
	return full_names, player_key, player_pos


def team_players_query():
    """
    Finds the players of a given team\n
    Returns three lists: one with the players' full name, the Yahoo API player key value, and the player's primary position
    """
    #start the calculation timer
    calc_start = time.time()

    #initialize everything
    last_first_names = []
    full_names = []
    player_key = []
    player_pos = []
    
    #build the query URL
    query_url = base_query_url + 'team/' + leagueID + teamID + '/roster'

    #get the json data
    r = s.get(query_url, params={'format': 'json'})
    output = r.json()
    output = output['fantasy_content']['team'][1]['roster']['0']['players']
    player_num = list(output.keys())
    player_num = player_num[0:len(player_num)-1]
    #loop thru all of the players and extract the necessary info
    for i in player_num:
        result = output[i]
        result = result['player'][0]
        #store the player key
        player_k = result[0]['player_key']
        #store the player position
        pos = result[9]['display_position']
        #store player names
        output_name = result[2]['name']
        f_name = output_name['first']
        l_name = output_name['last']
        full = output_name['full']
        #build formatted name
        last_first = l_name + ', ' + f_name
        #add to lists
        full_names.append(full)
        last_first_names.append(last_first)
        player_key.append(player_k)
        player_pos.append(pos)
        
    #stop the timer
    calc_end = time.time()
    #print the calculation time
    print('Process complete')
    print('Calculation time for rostered players: {0:0.2f} seconds'.format((calc_end-calc_start)))
    #return full names and player keys
    return full_names, player_key, player_pos


# =============================================================================
# Run project
# =============================================================================
#if __name__ == '__main__':
#create the authenticated session
s, base_url = query_setup()

#create the basic components of the query
base_query_url = base_url + 'fantasy/v2/'
leagueID = 'nfl.l.778518'
teamID = '.t.2'

#collect all available players
avail_full_names, avail_player_key, avail_player_pos = available_players_query()
#collect players on roster
team_full_names, team_player_key, team_player_pos = team_players_query()

#make data frames out of the collected lists
df_avail = pd.DataFrame({'name': avail_full_names, 'key': avail_player_key, 'pos1': avail_player_pos})
df_roster = pd.DataFrame({'name': team_full_names, 'key': team_player_key, 'pos1': team_player_pos})

# =============================================================================
# Testing
# =============================================================================
#build url
def player_stats_query(week, player_list, session=s):
    """
    Returns the player stats for the given week\n
    Takes the player list as an argument so the function can be used for available players and rostered players\n
    Only works for offensive players (QB, WR, RB, TE) right now
    """    
    #initialize lists
    pos_list = []
    team_list = []
    
    #cycle thru each player that is currently available
    for player in avail_player_key:
        #build the API url for the unique player key
        url_player = base_query_url+'league/'+leagueID+'/players;player_keys='+player+'/stats;type=week;week='+str(week)
        #convert API call to json
        raw = s.get(url_player, params={'format': 'json'}).json()
        #parse out the players details info (e.g. position, owned, etc.)
        player_details = raw['fantasy_content']['league'][1]['players']['0']['player'][0]
        #parse out position from player details
        pos = player_details[9]['display_position'].upper()
        
        ## FILTER OUT NON-OFFENSE POSITIONS
        if pos not in ['QB', 'WR', 'RB', 'TE']:
            continue
        else:
        
            #parse out team from player_details
            team = player_details[6]['editorial_team_abbr'].upper()
            #append data to lists
            pos_list.append(pos)
            team_list.append(team)
            
            #initialize a stats list
            stats_list = []
            #parse out the player stats
            player_stats = raw['fantasy_content']['league'][1]['players']['0']['player'][1]['player_stats']['stats']
            #loop thru all of the various stats
            for stat in player_stats:
                stat_dict = stat['stat']
                stats_list.append(stat_dict)
                
        return stats_list