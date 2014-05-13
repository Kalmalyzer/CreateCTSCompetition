
import codecs
import json

with open('class_config.json', 'r') as file:
	class_config = json.load(file)

def load_registrations(filename):
	with open(filename, 'r') as file:
		return json.load(file)


def generate_registration_entry(registration):

	class_meos_id = class_config[registration['class_id']]['meos_id']
	team_name = registration['team_name']
	legs = "4"
	runner_1_name = registration['name_1']
	runner_1_si_number = str(registration['si_1'])
	runner_1_rented = "Yes" if registration['si_1'] == 0 else ""
	runner_2_name = registration['name_2']
	runner_2_si_number = str(registration['si_2'])
	runner_2_rented = "Yes" if registration['si_2'] == 0 else ""

	columns = [
		"",	# Stno		stno
		"",	# Descr		desc
		"",	# Block
		"",	# nc
		"",	# Start		start
		"",	# Time		time
		"",	# Classifier	status
		"",	# Club no.	clubno
		"",	# Cl.name
		team_name,	# City		club
		"",	# Nat		nat
		class_meos_id,	# Cl. no.	classno
		"",	# Short		class
		"",	# Long
		legs,	# Legs		legs
		"",	# Num1
		"",	# Num2
		"",	# Num3
		"",	# Text1
		"",	# Text2
		"",	# Text3
		"",	# Start fee	fee
		"",	# Paid		paid

		"",	# Surname
		runner_1_name,	# First name
		"",	# YB
		"",	# S
		"",	# Start
		"",	# Finish
		"",	# Time
		"",	# Classifier
		runner_1_si_number,	# Chip
		runner_1_rented,	# Rented
		"",	# Database Id

		"",	# Surname
		runner_2_name,	# First name
		"",	# YB
		"",	# S
		"",	# Start
		"",	# Finish
		"",	# Time
		"",	# Classifier
		runner_2_si_number,	# Chip
		runner_2_rented,	# Rented
		"",	# Database Id
		]
	return columns

def create_registrations_csv(registrations):

	registrations_csv = 'Stno;Descr;Block;nc;Start;Time;Classifier;Club no.;Cl.name;City;Nat;Cl. no.;Short;Long;Legs;Num1;Num2;Num3;Text1;Text2;Text3;Start fee;Paid;Surname;First name;YB;S;Start;Finish;Time;Classifier;Chip;Rented;Database Id;Surname;First name;YB;S;Start;Finish;Time;Classifier;Chip;Rented;Database Id;Surname;First name;YB;S;Start;Finish;Time;Classifier;Chip;Rented;Database Id\n'
	for registration in registrations:
		registrations_csv += ';'.join(generate_registration_entry(registration)) + '\n'

	return registrations_csv

def save_registrations_csv(registrations_csv):
	with codecs.open('registrations.csv', 'w', encoding='latin_1') as file:
		file.write(registrations_csv)

def create_runner_import_list_OE_CSV():

	registrations = load_registrations('../ExtractDataFromDB/registrations.json')
	registrations_csv = create_registrations_csv(registrations)
	save_registrations_csv(registrations_csv)

if __name__ == '__main__':
	create_runner_import_list_OE_CSV()
