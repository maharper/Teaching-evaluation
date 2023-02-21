# filter_lib.py
"""Jinja2 filters"""

import re

def j2_latex_filter(string):
    """
    Given a string it returns a string sanitized for use in a LaTeX document.

    :param str string: string to execute replacements on
    :rtype: str
    """
    replacements = {'#':r'\#',
        '$':r'\$',
        '%':r'\%',
        '&':r'\&',           # r'\textampersand{}' someday?
        r'~':r'\textasciitilde{}',
        '_':r'\_',
        '^':r'\textasciicircum{}',
        '\\':r'\textbackslash{}',
        '{':r'\{',
        '}':r'\}',
        }

    replacements =  dict((re.escape(k), v) for k, v in replacements.items())

    pattern = re.compile("|".join(replacements.keys()))

    return pattern.sub(lambda match: replacements[re.escape(match.group(0))], string)
    