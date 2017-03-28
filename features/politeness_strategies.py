import codecs
import os
import re
from itertools import chain
from collections import defaultdict

# Get the Local Directory to access support files.
local_dir = os.path.split(__file__)[0]

#### HEDGES ####################################################################
####     Words that are typically used to lessen the impact of an utterance. For
####     example, once could could 'lessen the impact' of an utterance during a
####     debate by saying "that seems incorrect" instead of "that's wrong".
hedges = ["almost", "apparent", "apparently", "appear", "appeared", "appears",
          "approximately", "argue", "argued", "argues", "around", "assume",
          "assumed", "broadly", "certain amount", "certain extent",
          "certain level", "claim", "claimed", "claims", "doubt", "doubtful",
          "essentially", "estimate", "estimated", "fairly", "feel", "feels",
          "felt", "frequently", "from my perspective", "from our perspective",
          "from this perspective", "generally", "guess", "in general",
          "in most cases", "in most instances", "in my opinion", "in my view",
          "in our opinion", "in our view", "in this view", "indicate",
          "indicated", "indicates", "largely", "likely", "mainly", "may",
          "maybe", "might", "mostly", "often", "on the whole", "ought",
          "perhaps", "plausible", "plausibly", "possible", "possibly",
          "postulate", "postulated", "postulates", "presumable", "presumably",
          "probable", "probably", "quite", "rather", "relatively", "roughly",
          "seems", "should", "sometimes", "somewhat", "suggest", "suggested",
          "suggests", "suppose", "supposed", "supposes", "suspect", "suspects",
          "tend to", "tended to", "tends to", "think", "thinking", "thought",
          "to my knowledge", "typical", "typically", "uncertain", "uncertainly",
          "unclear", "unclearly", "unlikely", "usually"]

#### POSITIVE & NEGATIVE WORD LISTS ############################################
####    Minqing Hu and Bing Liu. "Mining and summarizing customer reviews."
####        Proceedings of the ACM SIGKDD International Conference on Knowledge
####        Discovery & Data Mining (KDD-2004, full paper), Seattle, Washington,
####        USA, Aug 22-25, 2004.
####    http://www.cs.uic.edu/~liub/publications/kdd04-revSummary.pdf
pos_filename = os.path.join(local_dir, "liu-positive-words.txt")
positive_words = set(map(lambda x: x.strip(), codecs.open(pos_filename, encoding='utf-8').read().splitlines()))

neg_filename = os.path.join(local_dir, "liu-negative-words.txt")
negative_words = set(map(lambda x: x.strip(), codecs.open(neg_filename, encoding='utf-8').read().splitlines()))

#### PARSE ELEMENT ANCESTORS ###################################################
####    Given a dependency parse string, such as "nsubj(dont-5, I-4)", tranform
####    or return specific constituents.
parse_element_split_re = re.compile(r"([-\w!?]+)-(\d+)")
getleft = lambda p: parse_element_split_re.findall(p)[0][0].lower()
getleftpos = lambda p: int(parse_element_split_re.findall(p)[0][1])
getright = lambda p: parse_element_split_re.findall(p)[1][0].lower()
getrightpos = lambda p: int(parse_element_split_re.findall(p)[1][1])
remove_numbers = lambda p: re.sub(r"\-(\d+)" , "", p)
getdeptag = lambda p: p.split("(")[0]

#### STRATEGY FUNCTIONS ########################################################
####    Each strategy function is defined as a named lambda function that
####    returns a boolean: True if the strategy is detected; False otherwise.
####    Some functions operate on dependency-parse elements, others on string
####    text inputs, and other on token lists.

#### POLITENESS STRATEGIES #####################################################
####    Based on dependency-parses.
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

#### REQUEST IDENTIFICATION HEURISTICS #########################################
####    Based on dependency-parses.
polar_set = set(["am", "are", "can", "could", "dare", "did", "do", "does",
                 "had", "has", "have", "how", "if", "is", "may", "might",
                 "must", "need", "ought", "shall", "should", "was", "were",
                 "when", "which", "who", "whom", "will", "would"])

initial_polar = lambda p: (getleftpos(p)==1 and getleft(p) in polar_set) or (getrightpos(p)==1 and getright(p) in polar_set)
initial_polar.__name__ = "Initial Polar"

aux_polar = lambda p: getdeptag(p) == "aux" and getright(p) in polar_set
aux_polar.__name__ = "Aux Polar"

####    Based on strings.
####    Verb moods.
subjunctive = lambda s: "could you" in s or "would you" in s
subjunctive.__name__ = "SUBJUNCTIVE"

indicative = lambda s: "can you" in s or "will you" in s
indicative.__name__ = "INDICATIVE"

####    Based on token lists.
has_hedge = lambda l: len(set(l).intersection(hedges)) > 0
has_hedge.__name__ = "HASHEDGE"

has_positive = lambda l: len(positive_words.intersection(l)) > 0
has_positive.__name__ = "HASPOSITIVE"

has_negative = lambda l: len(negative_words.intersection(l)) > 0
has_negative.__name__ = "HASNEGATIVE"

#### EVALUATE STRATEGY FUNCTIONS ###############################################
VERBOSE_ERRORS = False

def check_elems_for_strategy(elems, strategy_fnc):
    """
    Given a strategy and a list of elements, return True if the strategy is
    present in at least one of the elements. Return False if the strategy is
    not present in any of the elements.
    """
    for elem in elems:
        try:
            testres = strategy_fnc(elem)
            if testres:
                return True
        except Exception as e:
            if VERBOSE_ERRORS:
                print(strategy_fnc.__name__)
                print(e, elem)
    return False


#### FEATURE EXTRACTION ########################################################
####    Define the dependency-based strategies to include:
DEPENDENCY_STRATEGIES = [please, pleasestart, btw, hashedges, really, deference,
                         gratitude, apologize, groupidentity, firstperson,
                         firstperson_start, secondperson, secondperson_start,
                         hello, why, conj]

####    Define the text-based strategies to include:
TEXT_STRATEGIES = [subjunctive, indicative]

####    Define the term-based strategies to include:
TERM_STRATEGIES = [has_hedge, has_positive, has_negative]

####    Generate a list of all feature names based on the strategies. The lambda
####    function converts the strategy names into feature names.
fnc2feature_name = lambda f: "feature_politeness_==%s==" % f.__name__.replace(" ","_")
POLITENESS_FEATURES = map(fnc2feature_name, chain(DEPENDENCY_STRATEGIES, TEXT_STRATEGIES, TERM_STRATEGIES))

def get_politeness_strategy_features(document):
    """
    Given a pre-processed request document of the form:
        {
            "sentences": ["sent1", "sent2", ...],
            "parses": [
                          ["nsubj(dont-5, I-4)", ...],
                          ["nsubj(dont-5, I-4)", ...],
                          ...
                      ],
            "unigrams": ["a", "b", "c", ...]
        }

    Return a binary feature dict of the following form, where the value for each
    feature is a binary value (1 or 0):
        { "feature_1": 1, "feature_2": 0, "feature_3": 1, ... }

    This currently only returns binary features; a value of 1 indicates the the
    strategy is present in the document (0 indicates not present). You could
    modify this code to count the number occurrences of each strategy (if you
    are inclined to do so) by changing Line
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

    # Text-based features:
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

