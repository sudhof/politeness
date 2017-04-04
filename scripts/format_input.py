import os
import requests
import sys
import traceback

from politeness.model import score

from json import JSONDecodeError
from requests.exceptions import RequestException
from nltk.tokenize import sent_tokenize

HEADERS = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}
PARAMS = {'properties': "{'annotators': 'tokenize,ssplit,pos,parse,depparse'}"}
URL = ""

def clean_depparse(dep):
    """
    Given a dependency dictionary, return a formatted string representation.
    """
    return str(dep['dep'] + "(" + dep['governorGloss'].lower() + "-" +
               str(dep['governor']) + ", " + dep['dependentGloss'] + "-" +
               str(dep['dependent']) + ")")

def get_sentences(doc_text):
    temp = doc_text.strip().split('\n')
    sents = []
    for s in temp:
        sents += sent_tokenize(s.strip())
        
    return sents
    
def get_parses(sents):
    global HEADERS, PARAMS, URL
    raw_parses = []
    for sent in sents:
        parse = {'deps': "", 'sent': ""}
        try:
            response = requests.post(
                    URL, params=PARAMS, headers=HEADERS,
                    data=sent.encode('UTF-8')
                )
            response.raise_for_status()
            for sentence in response.json()['sentences']:
                parse['deps'] = sentence['ehancedPlusPlusDependencies']
                parse['sent'] = sentence
                raw_parses.append(parse)
                
        except Exception as e:
            sys.stderr.write('Exception\n')
            sys.stderr.write('  Text: {}\n'.format(self.text[:50]))
            extype, exvalue, extrace = sys.exc_info()
            traceback.print_exception(extype, exvalue, extrace)
            raw_parses.append({'deps': 'X', 'sent': 'X'})
        
    return raw_parses
            
def format_doc(doc_text):
    sents = get_sentences(doc_text)
    raw_parses = get_parses(sents)
    results = []
    result = {'parses': [], 'sentences': []}
    for raw in raw_parses:
        for dep in raw['deps']:
            result['parses'].append(clean_depparse(dep))
        result['sentences'] = raw['sent']
        
        print(result)
        results.append(result)
        
    return results

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        sys.exit(1)
    else:
        doc_text = ""
        with open(args[0], "r") as doc:
            doc_text = doc.read()
            
       parsed_doc = format_doc(doc_text)
       print(parsed_doc)
       print(score(parsed_doc))
       
