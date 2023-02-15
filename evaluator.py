#Automated Teacher Evaluations
#Brendan Cordy, 2015

import csv
import os
import stats
from decimal import *
import json

from jinja2 import Environment, FileSystemLoader, StrictUndefined

# Get the question texts

question_texts = 'templates/opscan1.json'
with open(question_texts, 'r') as question_file:
	questions = json.load(question_file)

# Define the output format

template_file = 'report.tex.jinja'
file_loader = FileSystemLoader('templates')
latex_jinja_env = Environment(
	block_start_string =    '\BLOCK{',
	block_end_string =      '}',
	variable_start_string = '\VAR{',
	variable_end_string =   '}',
	comment_start_string =  '\#{',
	comment_end_string =    '}',
	line_statement_prefix = '%-',
	line_comment_prefix =   '%#',
	trim_blocks = True,
	lstrip_blocks=True,
	autoescape = False,
	loader=file_loader,
	)
template = latex_jinja_env.get_template(template_file)

#Find csvs in subdirectories without corresponding texs.
for direc, subdirects, files in os.walk('.'):
	tex_filenames = [f[:-4] for f in files if f[-4:] == '.tex']
	csv_filenames = [f[:-4] for f in files if f[-4:] == '.asc']
	unevaluated = list(set(csv_filenames)-set(tex_filenames))
	unevaluated_csvs = [f + '.asc' for f in unevaluated]

	for csvfile in unevaluated_csvs:
		#Extract teacher, section, and term information.
		name_sep = csvfile.index('-')
		teacher_name = csvfile[:name_sep]
		leftover = csvfile[name_sep+1:]

		course_sep = leftover.index('s')
		course = leftover[:course_sep]
		leftover = leftover[course_sep+1:]

		section_sep = leftover.index('-')
		section = leftover[:section_sep]
		leftover = leftover[section_sep+1:]

		if(leftover[0] == 'F'):
			term = 'Fall'
		elif(leftover[0] == 'W'):
			term = 'Winter'
		else:
			term = 'Summer'

		year = leftover[1:-4]

		#Read csv data from good old scan-o-matic 2000.
		with open(direc + '/' + csvfile, 'r') as rawdata:
			reader = csv.reader(rawdata)
			str_eval_scores = list(reader)

		#Create a list of lists of integer scores for each question. Throw away the blanks.
		eval_scores = []
		for i in range(len(str_eval_scores[0])):
			cleaned_column = []
			for j in range(len(str_eval_scores)):
				if (str_eval_scores[j])[i] == 'BLANK':
					pass
				elif (str_eval_scores[j])[i] == 'MULT':
					pass
				elif (str_eval_scores[j])[i] == '*':
					pass
				else:
					cleaned_column.append(int(float((str_eval_scores[j])[i])))
			eval_scores.append(cleaned_column)

		#Find average for each question.
		averages = []
		for i in range(len(eval_scores)):
			averages.append(str(Decimal(stats.mean(eval_scores[i])).quantize(Decimal('.01'))))

		#Find sample std dev for each question.
		stdevs = []
		for i in range(len(eval_scores)):
			stdevs.append(str(Decimal(stats.stdev(eval_scores[i])).quantize(Decimal('.01'))))

		#Find frequences for each question.
		int_freqs = []
		for i in range(len(eval_scores)):
			counts_list = [0,0,0,0,0]
			for j in range(len(eval_scores[i])):
				if((eval_scores[i])[j] == 1):
					counts_list[0]+=1
				elif((eval_scores[i])[j] == 2):
					counts_list[1]+=1
				elif((eval_scores[i])[j] == 3):
					counts_list[2]+=1
				elif((eval_scores[i])[j] == 4):
					counts_list[3]+=1
				elif((eval_scores[i])[j] == 5):
					counts_list[4]+=1
			int_freqs.append(counts_list)

		#Cast the frequencies to strings.
		freqs = []
		for i in range(len(int_freqs)):
			str_counts_list = []
			for j in range(len(int_freqs[i])):
				str_counts_list.append(str((int_freqs[i])[j]))
			freqs.append(str_counts_list)

		tex_document = template.render(
			{'teacher':teacher_name,
			'course':{'year':year, 'term':term, 'course':course, 'section':section},
			'questions':questions,
			'averages':averages,
			'stdevs':stdevs,
			'freqs':freqs
			},
			undefined=StrictUndefined)

		#Write the tex file.
		with open(direc + '/' + csvfile[:-4] + '.tex', 'w') as eval_report:
			eval_report.write(tex_document)