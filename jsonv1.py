import csv

filename = "input.csv"


def getFieldName(name):
	name = name.lower().split()

	if  '.' in name[len(name) - 1]:
		name[len(name) - 1] = name[len(name) - 1][:-1]

	name = "_".join(name)
	return name

def getModelName(name):
	name = name.lower().split()
	name = [x.capitalize() for x in name]
	name = "".join(name)
	return name




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

jsons = {}
all_lists = []

for head in heads:
	body = data[head]
	dept = "land_administration"
	head = getModelName(head)
	f = open("json_output.txt", "a")
	json_list = []
	for line in body:
		field_name, field_type = line
		field_label = field_name

		if "section" in field_name or  "Section" in field_name:
			field_type = "section"

		field_name = getFieldName(field_name)
		# field_type = getFieldType(field_type)
		field = field_name + " = " + field_type

		if field_name != 'main_form':
			# f.write("\t" + field + "\n")
			if field_type == 'list' or field_type == 'boolean':
				all_lists.append(field_name.upper())
				json_field = {
                    "field_name": field_name,
                    "field_type": "select",
                    "field_label": field_label,
                    "field_value": "",
                    "input_format": "select",
                    "field_options": [
                        {
                            "id": "YES",
                            "name": "YES"
                        },
                        {
                            "id": "NO",
                            "name": "NO"
                        }
                    ]
                }
			else:
				json_field = {
						"field_name": field_name,
						"field_type": "text",
						"field_label": field_label,
						"field_value": "",
						"input_format": "text"
					}

			json_list.append(json_field)
			# f.write("\t" + str(json_field) + "\n")
	single_json = {head:json_list}
	jsons.update(single_json)
	f.write("\t" + str(jsons) + "\n")
	jsons = {}






	f.write("\n\n\n\n\n\n")
	

f = open("json_output.txt", "a")
for ilist in all_lists:
	f.write(ilist + "\n")
f.close()



