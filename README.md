# README.md

This repository contains python scripts for processing the raw data obtained
from teaching evaluation questionnaires.  The scripts produce `.tex` files which
when compiled yield reports on the questionnaire responses.

## evaluator3.py

`evaluator3.py` is a rewrite of `evaluator.py`.  It updates it to python 3 and adds
the ability to process Survey Monkey summary data.

### Requirements

To run `evaluator3.py` a python 3 environment with the jinja2 module available is needed.

### Installation

You will need the files `evaluator3.py`, `stats.py`, `filter_lib.py`, as well as the contents of the `templates` directory.

* If you have [poetry](https://python-poetry.org/) installed, you should just be able to
    download `poetry.lock`, and `pyproject.toml` and run `poetry install`.
* or you can install `jinja2` into your python environment or into a virtual environment.

### To generate report code

`evaluator3.py`, ala `evaluator.py`, will search subdirectories for files with extensions `.asc` (OpScan data)
and `.csv` (Survey Monkey data).  When such a file is found, it will parse the filename
to see if the file is the main data file for evaluation survey data.  If it is,
it will determine if there is a already a report (`.tex` file) generated for that data in the same directory.
If not, it will process the data and generate a `.tex` file.  For the Survey Monkey files,
it will look in the same directory as the main file for additional `.csv` files containing the
responses to the survey's long answer questions.

1. All data files should be in subdirectories of the directory containing `evaluator3.py` and friends.
1. Any long answer response files (with names like `Q23_Text.csv`) must be in the same directory as the
    associated main data file (with names like `Department of Mathematics Course Evaluation Survey
    Fall 2023 201-N11-LA section 00001 Malcolm Harper.csv`).
1. Run `evaluator3.py` using poetry or a virtual environment as appropriate for your installation
    * for me, on Windows, either `poetry run py evaluator3.py` or `venv & py evaluator3.py` works

### Generate the reports

Run LaTeX on the `.tex` files.  How you do this depends on your installation.

I use something like `latexmk -cd ./*/*/*.tex` & `latexmk -cd -c ./*/*/*.tex`
with the number of *s required depending on the level of subdirectory nesting.

## evaluator.py

`evaluator.py` is a python 2 program that processes data files produced by scanning
completed OpScan questionnaires.  It outputs `.tex` files which can be compiled to
produce reports for teachers and the evaluation committee.

### To Scan Forms in the Second Floor Computer Lab:

1. Login to OpScan Computer: User/Pass -> opscan/opscan
1. In RemarkOEM: Open Template, NCS/Math/CordyCSV <- (something like that).
2. Scan Forms for one section. Ignore blanks/multiples/etc.
3. Save as ASCII (commas), rename saved file in this format: BCordy-NYAs123-W2016.asc.
4. Move these csvs to a computer with python 2.7.

### To Generate Reports:

1. Create new subdirectories, one for each teacher, of a directory containing evalutor.py.
2. Copy .ascs into the appropriate teacher directory.
3. Use python 2.7 to run evaluator.py.
4. Compile the texs it produces.
