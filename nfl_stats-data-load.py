import os
import mysql.connector as mysql
import sshtunnel as ssh

def csv_to_mysql(load_sql):
    """
    Load data from CSV files into the nfl_stats database
    """
    try:
        #ssh payload
        ssh_config = {'ssh_address_or_host': '63.162.123.67',
                      'ssh_username': 'jchristo',
                      'ssh_password': 'Lordofthemanor1',
                      'ssh_port': '22',
                      'remote_bind_address': ('127.0.0.1', 3306)}
        
        with ssh.SSHTunnelForwarder(**ssh_config) as tunnel:
			#mysql payload
			mysql_config = {'user': 'root',
							'password': 'Lordofthemanor1',
							'database': 'nfl_stats',
							'host': '127.0.0.1',
							'port': tunnel.local_bind_port}
			
			#create connection object
			cxn = mysql.connect(**mysql_config)
			print('Connected to: jchristo_mysql')
			
			#load the data
			cursor = cxn.cursor()
			cursor.execute(load_sql)
			#make sure to commit the data to the database
			cxn.commit()
			#print to console
			print('Successfully loaded the table from csv')
			
			#close connections
			cursor.close()
			cxn.close()
        
    except Exception as e:
        print('Error: {}'.format(str(e)))


# =============================================================================
# Run the code
# =============================================================================
#find all of the files that need to be sent to the SQL table
data_files = os.listdir('C:/Users/Joe/Downloads/armchair_analysis')

#load all of the data into the database
for f in data_files[0]:
    #find just the table name
    stop = f.find('.')
    tbl = f[2:stop]
	#set the table to up loaded
    load_sql = "LOAD DATA LOCAL INFILE 'C:/Users/Joe/Downloads/armchair_analysis/" + tbl + ".csv'\
				INTO TABLE nfl_stats." + tbl + "\
				FIELDS TERMINATED BY ','\
				LINES TERMINATED BY '\n'\
				IGNORE 1 LINES;"
    
    #upload to database
    csv_to_mysql(load_sql)