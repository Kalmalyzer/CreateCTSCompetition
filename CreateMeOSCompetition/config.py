import codecs
import json

config_defaults = {
	'start' : '18:00:00',
	'rental price for SI-pin' : '20',
	'price increase for late registration, in percent' : '50',
	}

def create_courses_from_ocad_output_file(filename):	
	with codecs.open(filename, encoding='latin_1') as file:
		courses = []
		id = 1
		for line in file:
			words = line.split('\t')
			name = words[0]
			length = str(int(float(words[1].replace(',', '.')) * 1000 + 0.5))
			controls = words[2].split('-')[1:-1]
			course = {}
			course['id'] = str(id)
			course['name'] = name
			course['length'] = length
			course['controls'] = controls
			id += 1
			courses.append(course)
		return courses

def create_controls_from_courses(courses):
	controls = []
	created_controls = { }
	for course in courses:
		for control_reference in course['controls']:
			if not control_reference in created_controls:
				created_controls[control_reference] = True
				control = {}
				control['id'] = control_reference
				control['numbers'] = control_reference
				controls.append(control)
	return controls

def course_name_to_id(courses, course_name):
	for course in courses:
		if course['name'] == course_name:
			return course['id']

	raise Exception("Course name %s does not exist" % course_name)

def generate_forks(legs):
	courses = [
		[ legs[0], legs[3], legs[0], legs[3], ],
		[ legs[1], legs[2], legs[2], legs[1], ],
		[ legs[2], legs[1], legs[1], legs[2], ],
		[ legs[3], legs[0], legs[0], legs[3], ],
		]
	return courses
	
def create_classes_from_json(filename, courses):
	with codecs.open(filename, encoding='latin_1') as file:
		classes_json = json.load(file)
		classes = []
		id = 1
		for class_description in classes_json:
			_class = {}
			_class['id'] = str(id)
			_class['sort_index'] = str(id * 10)
			_class['name'] = class_description['name']
			if 'course' in class_description:
				_class['course'] = course_name_to_id(courses, class_description['course'])
			elif 'forked_multileg_courses' in class_description:
				if len(class_description['forked_multileg_courses']) != 4:
					raise Exception("forked_multileg_courses should always have 4 courses specified")
				legs = [course_name_to_id(courses, leg_name) for leg_name in class_description['forked_multileg_courses']]
				_class['forked_multileg_courses'] = generate_forks(legs)
				_class['start'] = class_description['start']
			else:
				raise Exception("Course specification missing in class")
			id += 1
			classes.append(_class)

		return classes

def create():

	config = config_defaults

	courses = create_courses_from_ocad_output_file('CTS2013Config/Courses.txt')
	controls = create_controls_from_courses(courses)
	classes = create_classes_from_json('CTS2013Config/Classes.txt', courses)
	
	config['controls'] = controls
	config['courses'] = courses
	config['classes'] = classes
	return config
