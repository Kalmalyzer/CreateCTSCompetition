
import json
import logging
import MySQLdb
import sys

import translation

logger = logging.getLogger('main')

def retrieve_clubs(cursor):
	cursor.execute('SELECT * from ok_clubs')
	results = cursor.fetchall()
	return results

def reformat_clubs(clubs_sql_data):
	clubs = {}
	for row in clubs_sql_data:
		clubs[str(row[0])] = row[1]
	
	return clubs

def retrieve_registrations(cursor, event_id):
	cursor.execute('SELECT * from ok_teamsprint WHERE event_id in (' + event_id +')')
	results = cursor.fetchall()
	return results

def reformat_registrations(registration_sql_data, clubs):
	registrations = []
	for row in registration_sql_data:
	
		club_1 = None
		if row[6] != 0:
			club_1 = clubs[str(row[6])]

		club_2 = None
		if row[7] != 0:
			club_2 = clubs[str(row[7])]

		registration = {
			'event_id' : translation.ok_teamsprint_event_ids_to_common_event_ids[str(row[0])],
			'class_id' : translation.ok_teamsprint_class_ids_to_common_class_ids[str(row[1])],
			'name_1' : row[2],
			'name_2' : row[3],
			'year_1' : row[4],
			'year_2' : row[5],
			'club_1' : club_1,
			'club_2' : club_2,
			'si_1' : row[8],
			'si_2' : row[9],
			'email_1' : row[10],
			'email_2' : row[11],
			'team_name' : row[12],
			'late' : row[13] }

		registrations.append(registration)
	
	return registrations

def get_registrations(username, password, event_id):

	try:
		connection = MySQLdb.connect('localhost', username, password, '154327-centrum');
		cursor = connection.cursor()

		logger.info('Retrieving clubs information from MySQL server')
		clubs_sql_data = retrieve_clubs(cursor)
		logger.info('Retrieving registration information from MySQL server')
		registrations_sql_data = retrieve_registrations(cursor, event_id)
		
		logger.info('Parsing clubs information')
		clubs = reformat_clubs(clubs_sql_data)
		logger.info('Parsing registration information and combining with clubs information')
		registrations = reformat_registrations(registrations_sql_data, clubs)
		logger.info('Registration & club retrieval complete')
		return registrations
		
	except MySQLdb.Error, e:

		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

	finally:

		if connection:
			connection.close()

def save_registrations(registrations, output_file_name):
	logger.info('Saving registrations to ' + output_file_name)
	with open(output_file_name, 'w') as file:
		json.dump(registrations, file)

if __name__ == '__main__':

	logging.basicConfig(level=logging.INFO)
	registrations = get_registrations(username=sys.argv[1], password=sys.argv[2], event_id='6')
	save_registrations(registrations=registrations, output_file_name='registrations.json')
	logger.info('Done.')
