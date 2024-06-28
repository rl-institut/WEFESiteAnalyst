import sys
import json
from copy import copy

from preprocessing.formparser import FormParser
from preprocessing.utils import get_survey



def pick_last_form_number(mydict, formtype):
	n=0
	for key in mydict.keys():
		if formtype in key and int(key.split(sep="_")[-1]) > n:
			n = int(key.split(sep="_")[-1])

	return n

def process_survey(DUMP=False, surv_id="atiMZ5E4jaZHv37TUekb6N", token="ea290627972a055fd067e1efc02c803869b1747c"):
	forms = get_survey(survey_id=surv_id, api_t=token)
	parser = FormParser()

	output_dict = {}
	form_name = None
	h_count, b_count, s_count, a_count = 0,0,0,0

	for form in forms:
		parser.init_parser(form)
		if parser.formtype == "household":
			h_count += 1
			form_name = f"{parser.formtype}_{h_count}"
		elif parser.formtype == "business":
			b_count += 1
			form_name = f"{parser.formtype}_{b_count}"
		elif parser.formtype == "service":
			s_count += 1
			form_name = f"{parser.formtype}_{s_count}"
		elif parser.formtype == "agroprocessing":
			a_count += 1
			form_name = f"{parser.formtype}_{a_count}"

		parser.create_dictionary()

		if DUMP:
			with open(f"preprocessing/test/{form_name}.json", "w") as file:
				json.dump(parser.output_dict, file)
			file.close()

		output_dict[form_name] = copy(parser.output_dict)

	if DUMP:
		with open(f"preprocessing/test/test.json", "w") as file:
	        	json.dump(output_dict, file)
		file.close()
	return output_dict

if __name__ == "__main__":

	o = process_survey()
	print(o.keys())