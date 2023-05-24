#Automated Teacher Evaluations
#Brendan Cordy, 2015
# Malcolm Harper 2023

import csv
import os
import json
from pathlib import Path
import re
# not used in the current incarnation
from decimal import *

from jinja2 import Environment, FileSystemLoader, StrictUndefined

import stats
from filter_lib import j2_latex_filter

def main():

    # Define the data formats

    # Get the opscan question texts
    questions_opscan_mc, questions_opscan_la = configure_opscan_data('templates/opscan1.json')
    
    # Define the output format
    template = configure_tex('report.tex.jinja')

    # Find data that needs processing

    #Find csvs in subdirectories without corresponding texs.
    for direc, subdirects, files in os.walk('.'):
        # This is not as elegant as Brendan's technique, but it allows us to track both .csv and .asc
        unevaluated = []
        for f in files:
            # opscan files
            if f[-4:] == '.asc':
                course = course_opscan(f)
                output_file = Path(direc)/Path(tex_filename(course)+'.tex')
                if not output_file.is_file():
                    unevaluated.append({'data_file':Path(direc)/Path(f), 'type':'opscan', 'course':course, 'tex_file':output_file})

            # Survey Monkey files (csv)
            if f[-4:] == '.csv':
                course = course_sm(f)
                if course :
                    output_file = Path(direc)/Path(tex_filename(course)+'.tex')
                    if not output_file.is_file():
                        with open(Path(direc)/Path(f), 'r') as data_file:
                        unevaluated.append({'data_file':Path(direc)/Path(f), 'type':'sm_summary', 'course':course, 'tex_file':output_file})

        for report in unevaluated:
            print(f"Processing {report['data_file']}.")
            if report['type'] == 'opscan':
                questions_mc = questions_opscan_mc
                questions_la = questions_opscan_la

                #Read csv data from good old scan-o-matic 2000.
                with open(report['data_file'], 'r', encoding='utf-8') as rawdata:
                    reader = csv.reader(rawdata)
                    str_eval_scores = list(reader)

                #Create a list of lists of integer scores for each question. Throw away the blanks.
                eval_scores = clean_opscan_data(str_eval_scores)

                # Sanity check
                if len(eval_scores) != len(questions_mc):
                    raise SystemExit(f"Wrong number of questions in {report['data_file']}.  Stopping.")

                #Find frequences for each question.
#                freqs = []
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
#                    freqs.append(counts_list)
                    questions_mc[i]['freqs'] = counts_list
                    questions_mc[i]['responses'] = stats.n_f(counts_list)

            elif report['type'] == 'sm_summary':
                with open(report['data_file'], 'r') as data_file:
                    sm_summary_data = data_file.read()
                questions_mc, questions_la = parse_sm_summary(sm_summary_data)
                if questions_la:
                    for question in questions_la:
                        sm_comment_file = report['data_file'].parent/('Q'+question['number']+'_Text.csv')
                        question['comments'] = sm_summary_comments(sm_comment_file)

            max_responses_mc = max([question['responses'] for question in questions_mc])
            for i in range(len(questions_mc)):
                _ , questions_mc[i]['mean'], questions_mc[i]['stdev'] = stats.stats_f(questions_mc[i]['freqs'])
                questions_mc[i]['sparks'] = [questions_mc[i]['freqs'][j]/max_responses_mc for j in range(5)]

            tex_document = template.render(
                {'course':report['course'],
                'questions_mc':questions_mc,
                'questions_la':questions_la,
                },
                undefined=StrictUndefined)

            #Write the tex file.
            with open(report['tex_file'], 'w', encoding='utf-8') as eval_report:
                print(f"Writing file {report['tex_file']}.")
                eval_report.write(tex_document)

def configure_opscan_data(question_texts):
    """Read and return the question texts (list of dicts) for opscan questionnaires."""
    with open(question_texts, 'r', encoding='utf-8') as question_file:
        return json.load(question_file), False

def configure_tex(template_file):
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
    latex_jinja_env.filters['escape_latex'] = j2_latex_filter

    return latex_jinja_env.get_template(template_file)

def course_opscan(filename):
    """Extract teacher, section, and term information."""
    name_sep = filename.index('-')
    teacher_name = [filename[:name_sep][0], filename[:name_sep][1:]]
    leftover = filename[name_sep+1:]

    course_sep = leftover.index('s')
    course_number = leftover[:course_sep]
    leftover = leftover[course_sep+1:]

    section_sep = leftover.index('-')
    section_number = leftover[:section_sep]
    leftover = leftover[section_sep+1:]

    if(leftover[0] == 'F'):
        term = 'Fall'
    elif(leftover[0] == 'W'):
        term = 'Winter'
    else:
        term = 'Summer'

    year = leftover[1:5]

    return {'course':course_number,'section':section_number, 'year':year, 'term':term, 'teacher':teacher_name}

def course_sm(filename):
    """Extract teacher, section, and term information from a csv filename and return as dict.  Return False if it is not possible."""
    regex = r'''^Department\ of\ Mathematics\ Course\ Evaluation\ Survey\s+ # Detect Survey Monkey file
(?P<term>\b\w+\b)\s+ # term
(?P<year>\d{4})\s+ # four digit year
(?P<course>[\w-]+)\s+ # Course nummber composed of alphanumerics and hyphen
section\s+0*(?P<section>\d{2})\s+ # Section number truncated to two digits
(?P<first>\b\w+\b)\s+ # First name
(?P<rest>.+) # The rest of the name
\.csv'''
    sm_match = re.search(regex, filename, re.VERBOSE)
    if sm_match:
        teacher_name = [sm_match.group('first'), sm_match.group('rest')]
        return dict(zip(('course','section', 'year','term'),sm_match.group('course','section','year','term'))) | {'teacher':teacher_name}
    return False

def tex_filename(course):
    '''produce a standardized output filename
        based on the course and teacher parameters
    '''
    return course['teacher'][0][0]+course['teacher'][1]+'-'+course['course']+'s'+course['section']+'-'+course['term'][0]+course['year']

def clean_opscan_data(raw_data):
    """Return a list of lists of integer scores.  Dirty data is removed."""
    clean_data = []
    for i in range(len(raw_data[0])):
        cleaned_column = []
        for j in range(len(raw_data)):
            if (raw_data[j])[i] == 'BLANK':
                pass
            elif (raw_data[j])[i] == 'MULT':
                pass
            elif (raw_data[j])[i] == '*':
                pass
            else:
                cleaned_column.append(int(float((raw_data[j])[i])))
        clean_data.append(cleaned_column)
    return clean_data

def parse_sm_summary(sm_summary_data):
    """Parses the Survey Monkey summary file (as a string) and returns a list of dicts of
    multiple choice question texts, total responses, and category frequencies and
    a list of dicts of long answer questions texts and individual responses.
    """
    rx_questions_mc = re.compile(r"""
        ^
        Q(?P<q_number>\d{1,2})\.\s*
        (?P<q_text>.+)$\n
        Answer\s+Choices\s*,\s*Response\s+Percent\s*,\s*Responses\s*
        (?P<q_freqs>[\s\S]*?)\n
        \s*,\s*Answered\s*,(?P<q_responses>\d+)
        [\s\S]*?
        (?=^Q|\Z)
    """, re.MULTILINE | re.VERBOSE)

    rx_freqs = re.compile(r'^\s*.+,\s*.+\s*,\s*(\d+)$', re.MULTILINE | re.VERBOSE)

    # replace sticky spaces with spaces, else LaTeX complains
    # sm_summary_data.replace("\xc2\xa0",' ')
    # Could do this in jinja instead
    questions_mc = [{'number':question.group('q_number'),
                        'text':question.group('q_text'),
                        'responses':int(question.group('q_responses')),
                        'freqs':[int(count) for count in rx_freqs.findall(question.group('q_freqs'))],
                        } for question in rx_questions_mc.finditer(sm_summary_data.replace("\xc2\xa0",' '))]
    
    rx_questions_la = re.compile(r"""
        ^
        Q(?P<q_number>\d{1,2})\.\s*
        (?P<q_text>.+)$\n
        \s*Answered\s*,(?P<q_responses>\d+)
        [\s\S]*?
        (?=^Q|\Z)
    """, re.MULTILINE | re.VERBOSE)

    questions_la = [{'number':question.group('q_number'),
                        'text':question.group('q_text'),
                        'responses':int(question.group('q_responses')),
                        } for question in rx_questions_la.finditer(sm_summary_data.replace("\xc2\xa0",' '))]

    return questions_mc, questions_la

def sm_summary_comments(comment_file_path):
    """Parse the comments from a Survey Monkey file.  Return a list of comments."""
    if comment_file_path.is_file():
        with open(comment_file_path, 'r', encoding='utf-8') as comments:
            question_text = comments.readline()
            reader = csv.DictReader(comments)
            next(comments)
            cols = reader.fieldnames
            if 'Responses' not in cols:
                print(f"    A column labelled 'Reponses' was not found in {comment_file_path}")
                return [f"Responses column not found in {comment_file_path}"]
            return [line['Responses'] for line in reader]
    else:
        print(f"    The comment file {comment_file_path} was not found")
        return [f"The comment file {comment_file_path} was not found"]

# Not used in the current incarnation
# The rounding and truncating is done by jinja
def format(x):
    str(Decimal(x).quantize(Decimal('.01')))

if __name__ == '__main__':
    main()
