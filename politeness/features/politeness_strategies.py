
import os
import re
from itertools import chain
from collections import defaultdict

#####
# Word lists

hedges = [
    "think", "thought", "thinking", "almost",
    "apparent", "apparently", "appear", "appeared", "appears", "approximately", "around",
    "assume", "assumed", "certain amount", "certain extent", "certain level", "claim",
    "claimed", "doubt", "doubtful", "essentially", "estimate",
    "estimated", "feel", "felt", "frequently", "from our perspective", "generally", "guess",
    "in general", "in most cases", "in most instances", "in our view", "indicate", "indicated",
    "largely", "likely", "mainly", "may", "maybe", "might", "mostly", "often", "on the whole",
    "ought", "perhaps", "plausible", "plausibly", "possible", "possibly", "postulate",
    "postulated", "presumable", "probable", "probably", "relatively", "roughly", "seems",
    "should", "sometimes", "somewhat", "suggest", "suggested", "suppose", "suspect", "tend to",
    "tends to", "typical", "typically", "uncertain", "uncertainly", "unclear", "unclearly",
    "unlikely", "usually", "broadly", "tended to", "presumably", "suggests",
    "from this perspective", "from my perspective", "in my view", "in this view", "in our opinion",
    "in my opinion", "to my knowledge", "fairly", "quite", "rather", "argue", "argues", "argued",
    "claims", "feels", "indicates", "supposed", "supposes", "suspects", "postulates"
]

# Positive and negative words from Liu
local_dir = os.path.split(__file__)[0]
pos_filename = os.path.join(local_dir, "liu-positive-words.txt")
neg_filename = os.path.join(local_dir, "liu-negative-words.txt")

positive_words = set(map(lambda x: x.strip(), open(pos_filename).read().splitlines()))
negative_words = set(map(lambda x: x.strip(), open(neg_filename).read().splitlines()))


####
# Parse element accessors.
# Given parse element string like "nsubj(dont-5, I-4)" 
# transform or return specific constituents

parse_element_split_re = re.compile(r"([-\w!?]+)-(\d+)")
getleft = lambda p: parse_element_split_re.findall(p)[0][0].lower()
getleftpos = lambda p: int(parse_element_split_re.findall(p)[0][1])
getright = lambda p: parse_element_split_re.findall(p)[1][0].lower()
getrightpos = lambda p: int(parse_element_split_re.findall(p)[1][1])
remove_numbers = lambda p: re.sub(r"\-(\d+)" , "", p)
getdeptag = lambda p: p.split("(")[0]

####
## Strategy Functions
## Defined as named lambda functions that return booleans
## Each function checks for a single strategy,
## returns True if strategy detected, False otherwise.
## Some functions operate on dependency-parse elements,
## some on string text inputs, some on token lists
####

####
# Dependency-based politeness strategies

please = lambda p: len(set([getleft(p), getright(p)]).intersection(["please"])) > 0 and 1 not in [getleftpos(p), getrightpos(p)]
please.__name__ = "Please"

pleasestart = lambda p: (getleftpos(p) == 1 and getleft(p) == "please") or (getrightpos(p) == 1 and getright(p) == "please")
pleasestart.__name__ = "Please start"

hashedges = lambda p:   getdeptag(p) == "nsubj" and  getleft(p) in hedges
hashedges.__name__ = "Hedges"

deference = lambda p: (getleftpos(p) == 1 and getleft(p) in ["great","good","nice","good","interesting","cool","excellent","awesome"]) or (getrightpos(p) == 1 and getright(p) in ["great","good","nice","good","interesting","cool","excellent","awesome"]) 
deference.__name__ = "Deference"

gratitude = lambda p: getleft(p).startswith("thank") or getright(p).startswith("thank") or "(appreciate, i)" in remove_numbers(p).lower()
gratitude.__name__ = "Gratitude"

apologize = lambda p: getleft(p) in ("sorry","woops","oops") or getright(p) in ("sorry","woops","oops") or remove_numbers(p).lower() in ("dobj(excuse, me)", "nsubj(apologize, i)", "dobj(forgive, me)")
apologize.__name__ = "Apologizing"

groupidentity = lambda p: len(set([getleft(p), getright(p)]).intersection(["we", "our", "us", "ourselves"])) > 0
groupidentity.__name__ = "1st person pl."

firstperson = lambda p: 1 not in [getleftpos(p), getrightpos(p)] and len(set([getleft(p), getright(p)]).intersection(["i", "my", "mine", "myself"])) > 0
firstperson.__name__ = "1st person"

secondperson_start = lambda p: (getleftpos(p) == 1 and getleft(p) in ("you","your","yours","yourself")) or (getrightpos(p) == 1 and getright(p) in ("you","your","yours","yourself")) 
secondperson_start.__name__ = "2nd person start"

firstperson_start = lambda p: (getleftpos(p) == 1 and getleft(p) in ("i","my","mine","myself")) or (getrightpos(p) == 1 and getright(p) in ("i","my","mine","myself")) 
firstperson_start.__name__ = "1st person start"

hello = lambda p: (getleftpos(p) == 1 and getleft(p) in ("hi","hello","hey")) or (getrightpos(p) == 1 and getright(p) in ("hi","hello","hey")) 
hello.__name__ = "Indirect (greeting)"

really = lambda p: (getright(p) == "fact" and getdeptag(p) == "prep_in") or remove_numbers(p) in ("det(point, the)","det(reality, the)","det(truth, the)") or len(set([getleft(p), getright(p)]).intersection(["really", "actually", "honestly", "surely"])) > 0  
really.__name__ = "Factuality"

why = lambda p: (getleftpos(p) in (1,2) and getleft(p) in ("what","why","who","how")) or (getrightpos(p) in (1,2) and getright(p) in ("what","why","who","how"))
why.__name__ = "Direct question"

conj = lambda p: (getleftpos(p) == 1 and getleft(p) in ("so","then","and","but","or")) or (getrightpos(p) == 1 and getright(p) in ("so","then","and","but","or"))
conj.__name__ = "Direct start"

btw = lambda p: getdeptag(p) == "prep_by" and getright(p) == "way" and getrightpos(p) == 3
btw.__name__ = "Indirect (btw)"

secondperson = lambda p: 1 not in (getleftpos(p), getrightpos(p)) and len(set([getleft(p), getright(p)]).intersection(["you","your","yours","yourself"])) > 0
secondperson.__name__ = "2nd person"

####
# Dependency-based request identification heuristics

polar_set = set([
    "is", "are", "was", "were", "am", "have", 
    "has", "had", "can", "could", "shall", 
    "should", "will", "would", "may", "might", 
    "must", "do", "does", "did", "ought", "need", 
    "dare", "if", "when", "which", "who", "whom", "how"
])
initial_polar = lambda p: (getleftpos(p)==1 and getleft(p) in polar_set) or (getrightpos(p)==1 and getright(p) in polar_set)
initial_polar.__name__ = "Initial Polar"

aux_polar = lambda p: getdeptag(p) == "aux" and getright(p) in polar_set
aux_polar.__name__ = "Aux Polar"

####
# String-based politeness strategies
# (i.e., input is a sentence)

# Verb moods
subjunctive = lambda s: "could you" in s or "would you" in s
subjunctive.__name__ = "SUBJUNCTIVE"

indicative = lambda s: "can you" in s or "will you" in s
indicative.__name__ = "INDICATIVE"

####
# Token list politeness strategies

has_hedge = lambda l: len(set(l).intersection(hedges)) > 0
has_hedge.__name__ = "HASHEDGE"

has_positive = lambda l: len(positive_words.intersection(l)) > 0
has_positive.__name__ = "HASPOSITIVE"

has_negative = lambda l: len(negative_words.intersection(l)) > 0
has_negative.__name__ = "HASNEGATIVE"


####
# strategy_fnc application helper

# For debugging, prints exceptions
VERBOSE_ERRORS = False

def check_elems_for_strategy(elems, strategy_fnc):
    # given a strategy lambda function, 
    # see if strategy present in at least one elem
    for elem in elems:
        try:
            testres = strategy_fnc(elem)
            if testres:
                return True
        except Exception, e:
            if VERBOSE_ERRORS:
                print strategy_fnc.__name__
                print e, elem
    return False


####
## Feature extraction
## Detect politeness strategies in documents
## by applying strategy fncs.
## Return feature dict
####

# Define the dependency-based strategies to include:
DEPENDENCY_STRATEGIES = [
    please, pleasestart, btw, 
    hashedges, really, deference, 
    gratitude, apologize, groupidentity, 
    firstperson, firstperson_start, 
    secondperson, secondperson_start,
    hello, why, conj
]
# And raw text-based strategies:
TEXT_STRATEGIES = [subjunctive, indicative]
# And term list strategies:
TERM_STRATEGIES = [has_hedge, has_positive, has_negative]

# Use strategies to generate list of all feature names
# lambda function turns strategy function names into feature names
fnc2feature_name = lambda f: "feature_politeness_==%s==" % f.__name__.replace(" ","_")
POLITENESS_FEATURES = map(fnc2feature_name, chain(DEPENDENCY_STRATEGIES, TEXT_STRATEGIES, TERM_STRATEGIES))
#print POLITENESS_FEATURES


def get_politeness_strategy_features(document):
    """
    :param document- pre-processed request document
    :type document- dict with 'sentences', 'parses',
                        and 'unigrams' fields

        {
          "sentences": ["sentence 1", "sentence 2"],
          "parses": [
            ["nsubj(dont-5, I-4)", ...],
            ["nsubj(dont-5, I-4)", ...],
          ],
          "unigrams": ['a', 'b', 'c']
        }


    Returns- binary feature dict
        {
            feature_name: 1 or 0
        }

    Currently return binary features- just checking for 
    presence of a strategy. One could alternatively decide 
    to count occurrences of the strategies. 
    """
    if not document.get('sentences', False) or not document.get('parses', False):
        # Nothing here. Return all 0s
        return {f: 0 for f in POLITENESS_FEATURES}
    
    features = {}

    # Parse-based features:
    parses = document['parses']
    for fnc in DEPENDENCY_STRATEGIES:
        f = fnc2feature_name(fnc)
        features[f] = int(check_elems_for_strategy(parses, lambda p: check_elems_for_strategy(p, fnc)))

    # Text-based
    sentences = map(lambda s: s.lower(), document['sentences'])
    for fnc in TEXT_STRATEGIES:
        f = fnc2feature_name(fnc)
        features[f] = int(check_elems_for_strategy(sentences, fnc))

    # Term-based features:
    terms = map(lambda x: x.lower(), document['unigrams'])
    for fnc in TERM_STRATEGIES:
        f = fnc2feature_name(fnc)
        ## HACK: weird feature names right now
        #f = f.replace("==", "=")
        features[f] = int(check_elems_for_strategy([terms], fnc))

    return features

