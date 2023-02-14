#Automated Teacher Evaluations
#Brendan Cordy, 2015

import csv
import os
import stats
from decimal import *

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
		with open(direc + '/' + csvfile, 'rb') as rawdata:
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

		#Write the tex file.
		with open(direc + '/' + csvfile[:-4] + '.tex', 'w') as eval_report:
			eval_report.write(r'\documentclass[letterpaper,11pt]{exam}' + '\n')
			eval_report.write(r'\usepackage{amsmath}' + '\n')
			eval_report.write(r'\usepackage{amssymb}' + '\n')
			eval_report.write(r'\usepackage{multirow}' + '\n')
			eval_report.write(r'\textheight=9.4in' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\makeatletter' + '\n')
			eval_report.write(r'\let\@oddfoot\@empty' + '\n')
			eval_report.write(r'\let\@evenfoot\@empty' + '\n')
			eval_report.write(r'\makeatletter' + '\n')
			eval_report.write(r'\addtolength{\topmargin}{0.15in}' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\pagestyle{headandfoot}' + '\n')
			eval_report.write(r'\firstpageheadrule' + '\n')
			eval_report.write(r'\firstpageheader{\LARGE{Evaluations - ' + term + ' ' + year + ' - ' + course + ' Sec.\,' + section + '}}{}{\LARGE{' + teacher_name[0] + '. ' + teacher_name[1:] + '}}' + '\n')
			eval_report.write(r'\runningheader{}{}{}' + '\n')
			eval_report.write(r'\firstpagefooter{}{}{}' + '\n')
			eval_report.write(r'\runningfooter{}{}{}' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\setlength{\rightpointsmargin}{1.3cm}' + '\n')
			eval_report.write(r'\pointsinrightmargin' + '\n')
			eval_report.write(r'\marginpointname{\ P.}' + '\n')
			eval_report.write(r'\boxedpoints' + '\n')
			eval_report.write(r'\addpoints' + '\n')
			eval_report.write(r'\totalformat{\fbox{Total: \totalpoints}}' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\begin{document}' + '\n')
			eval_report.write('\n')
			eval_report.write(r'Students are given the following five options for responses to each survey question.' + '\n')
			eval_report.write(r'\begin{center}' + '\n')
			eval_report.write(r'\begin{tabular}{l}' + '\n')
			eval_report.write(r'1 - Rarely/Low/Unsatisfactory/Light \\' + '\n')
			eval_report.write(r'2 - Sometimes/Mediocre/Needed Improvement \\' + '\n')
			eval_report.write(r'3 - Normally/Medium/Satisfactory \\' + '\n')
			eval_report.write(r'4 - Often/Very Good/Heavy \\' + '\n')
			eval_report.write(r'5 - Frequently/Very Heavy/Excellent/Always' + '\n')
			eval_report.write(r'\end{tabular}' + '\n')
			eval_report.write(r'\end{center}' + '\n')
			eval_report.write(r'\vspace{0.0in}' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\begin{center}' + '\n')
			eval_report.write(r'\begin{tabular}{lcc}' + '\n')
			eval_report.write(r'\qquad\qquad\qquad \ \ Question & \ \ \ Summary \ \ \ & \ \ Frequencies (1 $\rightarrow$ 5) \ \  \\' + '\n')
			eval_report.write(r'\hline' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\multirow{2}{*}{}The teacher arrives punctually and teaches & $\overline{x} =' + averages[0]+ r'$ & \multirow{2}{*}{' + freqs[0][0] + r' - ' + freqs[0][1] + r' - ' + freqs[0][2] + r' - ' + freqs[0][3] + r' - ' + freqs[0][4] + r'} \\' + '\n')
			eval_report.write(r'until the official end of the period. & $s =' + stdevs[0] + r'$  &  \\' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r"\multirow{2}{*}{The teacher's self-confidence is...} & $\overline{x} =" + averages[1]+ r'$ & \multirow{2}{*}{' + freqs[1][0] + r' - ' + freqs[1][1] + r' - ' + freqs[1][2] + r' - ' + freqs[1][3] + r' - ' + freqs[1][4] + r'} \\' + '\n')
			eval_report.write(r'& $s =' + stdevs[1] + r'$  &  \\' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\multirow{2}{*}{Are the lectures well-organized?} & $\overline{x} =' + averages[2]+ r'$ & \multirow{2}{*}{' + freqs[2][0] + r' - ' + freqs[2][1] + r' - ' + freqs[2][2] + r' - ' + freqs[2][3] + r' - ' + freqs[2][4] + r'} \\' + '\n')
			eval_report.write(r' & $s =' + stdevs[2] + r'$  &  \\' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\multirow{2}{*}{}The teacher clarifies material that needs & $\overline{x} =' + averages[3]+ r'$ & \multirow{2}{*}{' + freqs[3][0] + r' - ' + freqs[3][1] + r' - ' + freqs[3][2] + r' - ' + freqs[3][3] + r' - ' + freqs[3][4] + r'} \\' + '\n')
			eval_report.write(r'explanation. & $s =' + stdevs[3] + r'$  &  \\' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\multirow{2}{*}{}The pace of teaching allows you to take & $\overline{x} =' + averages[4]+ r'$ & \multirow{2}{*}{' + freqs[4][0] + r' - ' + freqs[4][1] + r' - ' + freqs[4][2] + r' - ' + freqs[4][3] + r' - ' + freqs[4][4] + r'} \\' + '\n')
			eval_report.write(r'useful notes. & $s =' + stdevs[4] + r'$  &  \\' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\multirow{2}{*}{}The teacher maintains an atmosphere & $\overline{x} =' + averages[5]+ r'$ & \multirow{2}{*}{' + freqs[5][0] + r' - ' + freqs[5][1] + r' - ' + freqs[5][2] + r' - ' + freqs[5][3] + r' - ' + freqs[5][4] + r'} \\' + '\n')
			eval_report.write(r'conducive to learning. & $s =' + stdevs[5] + r'$  &  \\' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\multirow{2}{*}{The teacher treats students with respect.} & $\overline{x} =' + averages[6]+ r'$ & \multirow{2}{*}{' + freqs[6][0] + r' - ' + freqs[6][1] + r' - ' + freqs[6][2] + r' - ' + freqs[6][3] + r' - ' + freqs[6][4] + r'} \\' + '\n')
			eval_report.write(r'& $s =' + stdevs[6] + r'$  &  \\' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\multirow{2}{*}{}The teacher encourages student & $\overline{x} =' + averages[7]+ r'$ & \multirow{2}{*}{' + freqs[7][0] + r' - ' + freqs[7][1] + r' - ' + freqs[7][2] + r' - ' + freqs[7][3] + r' - ' + freqs[7][4] + r'} \\' + '\n')
			eval_report.write(r'participation in class. & $s =' + stdevs[7] + r'$  &  \\' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r"\multirow{2}{*}{}Rate the teacher's answers to questions in & $\overline{x} =" + averages[8]+ r'$ & \multirow{2}{*}{' + freqs[8][0] + r' - ' + freqs[8][1] + r' - ' + freqs[8][2] + r' - ' + freqs[8][3] + r' - ' + freqs[8][4] + r'} \\' + '\n')
			eval_report.write(r'class. & $s =' + stdevs[8] + r'$  &  \\' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\multirow{2}{*}{}The teacher makes links with other & $\overline{x} =' + averages[9]+ r'$ & \multirow{2}{*}{' + freqs[9][0] + r' - ' + freqs[9][1] + r' - ' + freqs[9][2] + r' - ' + freqs[9][3] + r' - ' + freqs[9][4] + r'} \\' + '\n')
			eval_report.write(r'disciplines in the program. & $s =' + stdevs[9] + r'$  &  \\' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\multirow{2}{*}{}The teacher follows the schedule and time  & $\overline{x} =' + averages[10]+ r'$ & \multirow{2}{*}{' + freqs[10][0] + r' - ' + freqs[10][1] + r' - ' + freqs[10][2] + r' - ' + freqs[10][3] + r' - ' + freqs[10][4] + r'} \\' + '\n')
			eval_report.write(r'lines presented in the course outline. & $s =' + stdevs[10] + r'$  &  \\' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\multirow{2}{*}{Was the grading scheme explained clearly?} & $\overline{x} =' + averages[11]+ r'$ & \multirow{2}{*}{' + freqs[11][0] + r' - ' + freqs[11][1] + r' - ' + freqs[11][2] + r' - ' + freqs[11][3] + r' - ' + freqs[11][4] + r'} \\' + '\n')
			eval_report.write(r'& $s =' + stdevs[11] + r'$  &  \\' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\multirow{2}{*}{}The teacher grades the assignments and tests & $\overline{x} =' + averages[12]+ r'$ & \multirow{2}{*}{' + freqs[12][0] + r' - ' + freqs[12][1] + r' - ' + freqs[12][2] + r' - ' + freqs[12][3] + r' - ' + freqs[12][4] + r'} \\' + '\n')
			eval_report.write(r'impartially. & $s =' + stdevs[12] + r'$  &  \\' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\end{tabular}' + '\n')
			eval_report.write(r'\end{center}' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\begin{center}' + '\n')
			eval_report.write(r'\begin{tabular}{lcc}' + '\n')
			eval_report.write(r'\qquad\qquad\qquad \ \ Question & \ \ \ Summary \ \ \ & \ \ Frequencies (1 $\rightarrow$ 5) \ \  \\' + '\n')
			eval_report.write(r'\hline' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\multirow{2}{*}{}Rate the availability of the teacher outside of  & $\overline{x} =' + averages[13]+ r'$ & \multirow{2}{*}{' + freqs[13][0] + r' - ' + freqs[13][1] + r' - ' + freqs[13][2] + r' - ' + freqs[13][3] + r' - ' + freqs[13][4] + r'} \\' + '\n')
			eval_report.write(r'class hours. & $s =' + stdevs[13] + r'$  &  \\' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\multirow{2}{*}{Rate the overall performance of the teacher} & $\overline{x} =' + averages[14]+ r'$ & \multirow{2}{*}{' + freqs[14][0] + r' - ' + freqs[14][1] + r' - ' + freqs[14][2] + r' - ' + freqs[14][3] + r' - ' + freqs[14][4] + r'} \\' + '\n')
			eval_report.write(r'& $s =' + stdevs[14] + r'$  &  \\' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\multirow{2}{*}{}The workload in this course compared to other & $\overline{x} =' + averages[15]+ r'$ & \multirow{2}{*}{' + freqs[15][0] + r' - ' + freqs[15][1] + r' - ' + freqs[15][2] + r' - ' + freqs[15][3] + r' - ' + freqs[15][4] + r'} \\' + '\n')
			eval_report.write(r'courses is... & $s =' + stdevs[15] + r'$  &  \\' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\multirow{2}{*}{}Were you mathematically well-prepared for & $\overline{x} =' + averages[16]+ r'$ & \multirow{2}{*}{' + freqs[16][0] + r' - ' + freqs[16][1] + r' - ' + freqs[16][2] + r' - ' + freqs[16][3] + r' - ' + freqs[16][4] + r'} \\' + '\n')
			eval_report.write(r'this course. & $s =' + stdevs[16] + r'$  &  \\' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\multirow{2}{*}{Rate the usefulness/quality of the textbook.} & $\overline{x} =' + averages[17]+ r'$ & \multirow{2}{*}{' + freqs[17][0] + r' - ' + freqs[17][1] + r' - ' + freqs[17][2] + r' - ' + freqs[17][3] + r' - ' + freqs[17][4] + r'} \\' + '\n')
			eval_report.write(r'& $s =' + stdevs[17] + r'$  &  \\' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\multirow{2}{*}{Your overall impression of the course.} & $\overline{x} =' + averages[18]+ r'$ & \multirow{2}{*}{' + freqs[18][0] + r' - ' + freqs[18][1] + r' - ' + freqs[18][2] + r' - ' + freqs[18][3] + r' - ' + freqs[18][4] + r'} \\' + '\n')
			eval_report.write(r'& $s =' + stdevs[18] + r'$  &  \\' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\multirow{2}{*}{How often do you read the textbook?} & $\overline{x} =' + averages[19]+ r'$ & \multirow{2}{*}{' + freqs[19][0] + r' - ' + freqs[19][1] + r' - ' + freqs[19][2] + r' - ' + freqs[19][3] + r' - ' + freqs[19][4] + r'} \\' + '\n')
			eval_report.write(r'& $s =' + stdevs[19] + r'$  &  \\' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\multirow{2}{*}{}How often have you consulted your teacher & $\overline{x} =' + averages[20]+ r'$ & \multirow{2}{*}{' + freqs[20][0] + r' - ' + freqs[20][1] + r' - ' + freqs[20][2] + r' - ' + freqs[20][3] + r' - ' + freqs[20][4] + r'} \\' + '\n')
			eval_report.write(r'outside class hours? & $s =' + stdevs[20] + r'$  &  \\' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\noalign{\smallskip}' + '\n')
			eval_report.write(r'\multirow{2}{*}{How regularly have you attended lectures?} & $\overline{x} =' + averages[21]+ r'$ & \multirow{2}{*}{' + freqs[21][0] + r' - ' + freqs[21][1] + r' - ' + freqs[21][2] + r' - ' + freqs[21][3] + r' - ' + freqs[21][4] + r'} \\' + '\n')
			eval_report.write(r'& $s =' + stdevs[21] + r'$  &  \\' + '\n')
			eval_report.write('\n')
			eval_report.write(r'\end{tabular}' + '\n')
			eval_report.write(r'\end{center}' + '\n')
			eval_report.write(r'\end{document}' + '\n')
