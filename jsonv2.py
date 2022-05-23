import csv
import json
import sys

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

form = {
	"forms": [
		{
            "fields": [
                {
                    "field_name": "file_number",
                    "field_type": "text",
                    "field_label": "File Number",
                    "field_value": "",
                    "input_format": "text"
                },
                {
                    "field_name": "folio_number",
                    "field_type": "text",
                    "field_label": "Folio Number",
                    "field_value": "",
                    "input_format": "text"
                }
            ],
            "formname": "main_form",
            "formtype": "single",
            "field_collapsed": 'true'
        },
	],
	"formgroup": "whitecardform"
	}

field = {
		"field_name": 'field_name',
		"field_type": "text",
		"field_label": 'field_label',
		"field_value": "",
		"input_format": "text"
	}

def getSectionOutline():
	section_otline = {
			"fields": [
			
			],
			"formname": "transferee_section",
			"formtype": "array",
			"field_collapsed": 'true'
		}
	return section_otline

def getId():
	id_field = {
                    "field_name": "identifiaction_type",
                    "field_type": "select",
                    "field_label": "Identification Type",
                    "field_value": "",
                    "input_format": "select",
                    "field_options": [
                        {
                            "id": "NATIONAL_ID",
                            "name": "NATIONAL ID"
                        },
                        {
                            "id": "PASSPORT_NUMBER",
                            "name": "PASSPORT NUMBER"
                        }
                    ]
                }
	return id_field

def getSignature():
	signature = {
					"field_name": "land_registrar_signature",
					"field_type": "select",
					"field_label": "Land Registrar's Signature",
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
	return signature

def getAreaUnits():
	units = {
                "field_name": "unit_area",
                "field_type": "select",
                "field_label": "Unit Area",
                "field_value": "",
                "input_format": "select",
                "field_options": [
                   {
                      "id": "HECTARES",
                      "name": "HECTARES"
                   },
                   {
                      "id": "SQUARE_METRES",
                      "name": "SQUARE_METRES"
                   },
                   {
                      "id": "SQUARE_FEET",
                      "name": "SQUARE_FEET"
                   },
                   {
                      "id": "ACRES",
                      "name": "ACRES"
                   }
                ]
             }
	return units

def getNumberingType():
	num_type = {
                    "field_name": "title_numbering_type",
                    "field_type": "select",
                    "field_label": "Title Numbering Type",
                    "field_value": "",
                    "input_format": "select",
                    "field_options": [
                        {
                            "id": "IR",
                            "name": "IR"
                        },
                        {
                            "id": "BLOCK",
                            "name": "BLOCK"
                        },
                        {
                            "id": "GLA",
                            "name": "GLA"
                        },
                        {
                            "id": "IRN",
                            "name": "IRN"
                        }
                    ]
                }
	return num_type


# reading csv file
with open(filename, 'r') as csvfile:
	# creating a csv reader object
	csvreader = csv.reader(csvfile)
		
	# extracting each data row one by one
	heads = []
	section = []
	get_section_outline = None
	current_section = 'None'
	is_section = False
	counter = 0
	for row in csvreader:
		if row and row[0] and row[0] != 'DONE':
			if not row[1] and counter == 0:
				heads.append(row[0])

			if 'section' in row[0].lower():

				is_section = True
				current_section = row[0].lower()
				if get_section_outline:
					form['forms'].append(get_section_outline)

				get_section_outline = getSectionOutline() #dict(section_otline)
				get_section_outline['formname'] = current_section.strip()
				continue
			
			if is_section:
				common_type = ['varchar','integer','date']
				if row[1] in common_type:
					if 'area units' in row[0].lower():
						get_section_outline['fields'].append(getAreaUnits())
					else:
						field = dict(field)
						field['field_name'] = getFieldName(row[0])
						field['field_label'] = getFieldName(row[0])
						get_section_outline['fields'].append(field)
				elif row[1] == 'list':
					if 'identification type' in row[0].lower():
						get_section_outline['fields'].append(getId())
					if 'signature' in row[0].lower():
						get_section_outline['fields'].append(getSignature())
					if 'area units' in row[0].lower():
						get_section_outline['fields'].append(getAreaUnits())
					if 'numbering type' in row[0].lower():
						get_section_outline['fields'].append(getNumberingType())
				else:	
					get_section_outline['fields'].append(row)

		counter += 1



	form['forms'].append(get_section_outline)
	form['formgroup'] = getModelName(heads[0])
	# print(heads,"\n")
	print(form,"\n")
	f = open("json_output.json", "w")
	f.write(json.dumps(form))
	f.close()


sys.exit(0)

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





