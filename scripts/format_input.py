import json
import os
import re
import requests
import sys
import traceback

from json import JSONDecodeError
from requests.exceptions import RequestException
from nltk.tokenize import sent_tokenize

HEADERS = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}
PARAMS = {'properties': "{'annotators': 'tokenize,ssplit,pos,parse,depparse'}"}
URL = ''

def clean_depparse(dep):
    """
    Given a dependency dictionary, return a formatted string representation.
    """
    return str(dep['dep'] + "(" + dep['governorGloss'].lower() + "-" +
               str(dep['governor']) + ", " + dep['dependentGloss'] + "-" +
               str(dep['dependent']) + ")")

def clean_treeparse(tree):
    cleaned_tree = re.sub(r' {2,}', ' ', tree)
    cleaned_tree = re.sub(r'\n', '', cleaned_tree)
    cleaned_tree = re.sub(r'\([^\s]*\s', '', cleaned_tree)
    cleaned_tree = re.sub(r'\)', '', cleaned_tree)
    cleaned_tree = re.sub(r'-LRB-', '(', cleaned_tree)
    cleaned_tree = re.sub(r'-RRB-', ')', cleaned_tree)

    return cleaned_tree

def get_sentences(doc_text):
    temp = doc_text.strip().split('\n')
    sents = []
    for s in temp:
        sents += sent_tokenize(s.strip())

    return sents

def get_parses(sent):
    global HEADERS, PARAMS, URL
    parse = {'deps': [], 'sent': ""}
    try:
        response = requests.post(
                URL, params=PARAMS, headers=HEADERS,
                data=sent.encode('UTF-8')
            )
        response.raise_for_status()
        for sentence in response.json()['sentences']:
            parse['deps'] = sentence['enhancedPlusPlusDependencies']
            parse['sent'] = sent
    except Exception as e:
        sys.stderr.write('Exception\n')
        sys.stderr.write('  Sentence: {}\n'.format(sent[:50]))
        extype, exvalue, extrace = sys.exc_info()
        traceback.print_exception(extype, exvalue, extrace)
        raw_parses.append({'deps': 'X', 'sent': 'X'})

    return parse

def format_doc(doc_text):
    sents = get_sentences(doc_text)
    raw_parses = []
    for sent in sents:
        raw_parses.append(get_parses(sent))
    results = []
    for raw in raw_parses:
        result = {'parses': [], 'sentences': []}
        for dep in raw['deps']:
            result['parses'].append(clean_depparse(dep))
        result['sentences'].append(clean_treeparse(raw['sent']))

        results.append(result)

    return results
