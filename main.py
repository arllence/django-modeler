import csv

filename = "input.csv"

def getFieldType(field_type):
	varchar = 'models.CharField(max_length=100)'
	text = 'models.TextField()'
	number = 'models.IntegerField()'
	date = 'models.DateField()'
	section = 'JSONField()'

	field_type = field_type.lower()

	if field_type == 'varchar':
		return varchar
	elif field_type == 'number':
		return number
	elif field_type == 'date':
		return date
	elif field_type == 'section':
		return section
	elif field_type == 'text':
		return text
	else:
		return varchar


def getFieldName(name):
	name = name.lower().split()

	if  '.' in name[len(name) - 1]:
		name[len(name) - 1] = name[len(name) - 1][:-1]

	name = "_".join(name)
	return name

def getModelName(name):
	suffix = "(models.Model)"
	name = name.lower().split()
	name = [x.capitalize() for x in name]
	name = "".join(name) + suffix
	return name

def getDefaults(name,dept):

	name = getFieldName(name)
	schema = None
	braces = "{"+"}"

	if dept == 'land_registration':
		schema = 'LAND_REGISTRATION_DEPT_SCHEMA'
	elif dept == 'land_administration':
		schema = 'LAND_ADMINISTRATION_SCHEMA'
	elif dept == 'land_valuation':
		schema = 'LAND_VALUATION_DEPT_SCHEMA'
	elif dept == 'land_vrb':
		schema = 'LAND_VRB_DEPT_SCHEMA'
	elif dept == 'data_cleaning':
		schema = 'LAND_DATA_CLEANING_DEPT_SCHEMA'



	department = """department = models.ForeignKey(
		Department,
		related_name="{}_{}_department",
		on_delete=models.CASCADE,
	)""".format(dept,name)

	document = """document = models.ForeignKey(
		DocumentUpload,
		related_name="{}_{}_document",
		on_delete=models.CASCADE,
	)""".format(dept,name)

	def_str= """def __str__(self):
		return self.id"""

	meta = """class Meta:
		db_table = u'"{}"."{}"'.format(
			settings.{}
		)
		""".format(braces,name,schema)

	return department, document, def_str, meta


# reading csv file
with open(filename, 'r') as csvfile:
	# creating a csv reader object
	csvreader = csv.reader(csvfile)
		
	# extracting each data row one by one
	data = {}
	heads = []
	fields = []


	for row in csvreader:
		if row and row[0] and row[0] != 'DONE':
			fields.append(row)	


		if row and row[0] and row[0] == 'DONE':
			head = fields[0][0]
			heads.append(head)
			fields.pop(0)
			sub_data = {head: fields}
			data.update(sub_data)
			fields = []


	print(data,"\n")
	print(heads,"\n")

for head in heads:
	body = data[head]
	dept = "land_vrb"
	department, document, def_str, meta = getDefaults(head,dept)
	head = getModelName(head)
	head = "class " + head + ":"
	id = "id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)"
	f = open("output.txt", "a")
	f.write(head + "\n")
	f.write("\t"+id + "\n")
	for line in body:
		field_name, field_type = line

		if "section" in field_name or  "Section" in field_name:
			field_type = "section"

		field_name = getFieldName(field_name)
		field_type = getFieldType(field_type)
		field = field_name + " = " + field_type
		if field_name != 'main_form':
			f.write("\t" + field + "\n")


	f.write("\n\t"+department+"\n\n\t"+document+"\n\n\t"+def_str+"\n\n\t"+meta)
	f.write("\n\n")
	f.close()

