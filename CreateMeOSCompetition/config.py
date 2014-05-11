
control_1 = { 'id' : '1' }
control_2 = { 'id' : '2' }
control_3 = { 'id' : '3' }
control_4 = { 'id' : '4' }
control_5 = { 'id' : '5' }

course_bana_1 = {
	'id' : '1',
	'name' : 'Bana 1',
	'length' : '1234',
	'controls' : [control_1, control_2, control_3, control_4, control_5],
	}

courses = [
	course_bana_1,
	]

class_om2 = {
	'id' : '1',
	'name' : 'OM2',
	'has_multicourse' : False,
	'course' : course_bana_1,
	}
	
classes = {
	'OM2' : class_om2,
	}

config = {
	'rental price for SI-pin' : '20',
	'price increase for late registration, in percent' : '50',
	'courses' : courses,
	'classes' : classes,
	}