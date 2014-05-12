
import datetime
import xml.dom.minidom
import xml.etree.ElementTree as ElementTree

import config

timestamp = datetime.datetime.now()

config = config.create()

def prettify(xmltree):
	"""Return a pretty-printed XML string for the Element.
	"""
	rough_string = ElementTree.tostring(xmltree)
	reparsed = xml.dom.minidom.parseString(rough_string)
	pretty_xml = reparsed.toprettyxml(indent='  ', encoding='latin_1')
	pretty_xml_lines = pretty_xml.splitlines()
	pretty_xml_lines2 = filter(str.strip, pretty_xml_lines)
	pretty_xml2 = "\n".join(pretty_xml_lines2)
	return pretty_xml2

def generate_new_name_id():
	return 'meos_' + timestamp.strftime('%Y%m%d_%H%M%S_%f')
	
def convert_time_to_seconds(time):
	segments = time.split(":")
	return int(segments[0]) * 60 * 60 + int(segments[1]) * 60 + int(segments[2])

def get_current_updated_timestamp():
	return timestamp.strftime('%Y%m%d%H%M%S')

def create_meosdata_oData():
	oData = ElementTree.parse('templates/meosdata-oData.xml')
	oData.find('CardFee').text = config['rental price for SI-pin']
	oData.find('EliteFee').text = "0"
	oData.find('EntryFee').text = "0"
	oData.find('YouthFee').text = "0"
	oData.find('YouthAge').text = "0"
	oData.find('LateEntryFactor').text = config['price increase for late registration, in percent'] + " %"
	return oData.getroot()

def create_control(control_description):
	control_tree = ElementTree.parse('templates/Control.xml')
	control_tree.find('Id').text = control_description['id']
	control_tree.find('Updated').text = get_current_updated_timestamp()
	control_tree.find('Numbers').text = control_description['numbers']
	return control_tree.getroot()
	
def create_controls():
	control_list = ElementTree.Element("ControlList")
	for control_description in config['controls']:
		control_list.append(create_control(control_description))
		
	return control_list

def create_course(course_description):
	course_tree = ElementTree.parse('templates/course.xml')
	course_tree.find('Id').text = course_description['id']
	course_tree.find('Name').text = course_description['name']
	course_tree.find('Updated').text = get_current_updated_timestamp()
	course_tree.find('Length').text = course_description['length']
	controls = ""
	for control_reference in course_description['controls']:
		controls += control_reference + ';'
	course_tree.find('Controls').text = controls
	return course_tree.getroot()
	
def create_courses():
	course_list = ElementTree.Element("CourseList")
	for course_description in config['courses']:
		course_list.append(create_course(course_description))
	return course_list


def create_class_oData(class_description):
	oData = ElementTree.parse('templates/Class-oData.xml')
	oData.find('ClassFee').text = "TODO: compute"
	oData.find('HighClassFee').text = "TODO: compute"
	oData.find('ClassFeeRed').text = "TODO: compute"
	oData.find('HighClassFeeRed').text = "TODO: compute"
	oData.find('SortIndex').text = class_description['sort_index']
	return oData.getroot()

def create_class(class_description):
	_class = ElementTree.parse('templates/Class.xml')
	_class.find('Id').text = class_description['id']
	_class.find('Name').text = class_description['name']
	_class.find('Updated').text = get_current_updated_timestamp()
	if 'course' in class_description:
		course = ElementTree.Element('Course')
		course.text = class_description['course']
		_class.getroot().append(course)
	elif 'forked_multileg_courses' in class_description:
		multicourse = ElementTree.Element('MultiCourse')
		multicourse_string = ""
		for fork in class_description['forked_multileg_courses']:
			forks = " ".join(fork)
			multicourse_string += forks + ";"
		multicourse.text = multicourse_string
		_class.getroot().append(multicourse)

		legmethod = ElementTree.Element('LegMethod')
		starting_time_delta = str(convert_time_to_seconds(class_description['start']) - convert_time_to_seconds(config['start']))
		legmethod.text = '(ST:NO:%s:-1:-1:-1)*(CH:NO:0:-1:-1:-1)*(CH:NO:0:-1:-1:0)*(CH:NO:0:-1:-1:1)' % starting_time_delta
		_class.getroot().append(legmethod)
	else:
		raise Exception("Course specification missing in config")

	_class.getroot().append(create_class_oData(class_description))
	return _class.getroot()

def create_classes():
	class_list = ElementTree.Element("ClassList")
	for class_description in config['classes']:
		class_list.append(create_class(class_description))
	return class_list

def create_competition():

	meosdata = ElementTree.parse('templates/meosdata.xml')
	meosdata.find('Name').text = "Autogenerated on " + get_current_updated_timestamp()
	meosdata.find('NameId').text = generate_new_name_id()
	meosdata.find('ZeroTime').text = str(convert_time_to_seconds(config['start']))
	meosdata.find('Updated').text = get_current_updated_timestamp()

	meosdata.getroot().append(create_meosdata_oData())

	meosdata.getroot().append(create_controls())
	meosdata.getroot().append(create_courses())
	meosdata.getroot().append(create_classes())
	
	print prettify(meosdata.getroot())
	

if __name__ == '__main__':
	create_competition()