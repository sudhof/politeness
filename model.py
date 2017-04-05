import sys
import os
import _pickle

# This file provides an interface to a pre-trained politeness SVM.

#### CHECK DEPENDENCIES ########################################################
try:
    import numpy as np
except:
    sys.stderr.write("Package not found: Politeness model requires python pack",
                     "age numpy\n")
    sys.exit(2)

try:
    import scipy
    from scipy.sparse import csr_matrix
except:
    sys.stderr.write("Package not found: Politeness model requires python pack",
                     "age scipy\n")
    sys.exit(2)

try:
    import sklearn
except:
    sys.stderr.write("Package not found: Politeness model requires python pack",
                     "age scikit-learn\n")
    sys.exit(2)

try:
    import nltk
except:
    sys.stderr.write("Package not found: Politeness model requires python pack",
                     "age nltk\n")
    sys.exit(2)

#### CHECK DEPENDENCY VERSIONS #################################################

packages2versions = [("scikit-learn", sklearn, "0.18.1"),
                     ("numpy", np, "1.12.0"),
                     ("nltk", nltk, "3.2.1"),
                     ("scipy", scipy, "0.18.1")]

for name, package, expected_v in packages2versions:
    if package.__version__ < expected_v:
        sys.stderr.write("Warning: package '%s', expected version >= %s, detec",
                         "ted %s. Code functionality not guaranteed.\n"
                         % (name, expected_v, package.__version__))

#### PACKAGE IMPORTS ###########################################################
from features.vectorizer import PolitenessFeatureVectorizer

# Serialized model filename
MODEL_FILENAME = os.path.join(os.path.split(__file__)[0], 'politeness-svm.p')

# Load model, initialize vectorizer
clf = _pickle.load(open(MODEL_FILENAME, 'rb'), encoding='latin1', fix_imports=True)
vectorizer = PolitenessFeatureVectorizer()

def score(request):
    """
    :param request - The request document to score
    :type request - dict with 'sentences' and 'parses' field
        sample (taken from test_documents.py)--
        {
            'sentences': [
                "Have you found the answer for your question?",
                "If yes would you please share it?"
            ],
            'parses': [
                ["csubj(found-3, Have-1)", "dobj(Have-1, you-2)",
                 "root(ROOT-0, found-3)", "det(answer-5, the-4)",
                 "dobj(found-3, answer-5)", "poss(question-8, your-7)",
                 "prep_for(found-3, question-8)"],
                ["prep_if(would-3, yes-2)", "root(ROOT-0, would-3)",
                 "nsubj(would-3, you-4)", "ccomp(would-3, please-5)",
                 "nsubj(it-7, share-6)", "xcomp(please-5, it-7)"]
            ]
        }

    returns class probabilities as a dict
        { 'polite': float, 'impolite': float }
    """
    # Vectorizer returns {feature-name: value} dict
    features = vectorizer.features(request)
    fv = [features[f] for f in sorted(features.keys())]
    # Single-row sparse matrix
    X = csr_matrix(np.asarray([fv]))
    probs = clf.predict_proba(X)
    # Massage return format
    probs = {"polite": probs[0][1], "impolite": probs[0][0]}
    return probs


if __name__ == "__main__":
    # Sample classification of requests
    args = sys.argv[1:]
    if len(args) != 1:
        sys.exit(1)
    else:
        from scripts.format_input import format_doc
        doc_text = ""
        with open(args[0], "r") as doc:
            doc_text = doc.read()
        parsed_docs = format_doc(doc_text)
        polite = []
        impolite = []
        for i, doc in enumerate(parsed_docs):
            probs = score(doc)
            polite.append(probs['polite'])
            impolite.append(probs['impolite'])
            print("\n====\nSentence " + str(i) + ":\n" + str(doc['sentences'][0]))
            print("\tP(polite) = %.3f" % probs['polite'])
            print("\tP(impolite) = %.3f" % probs['impolite'])

        print("\n====\nDocument:")
        print("\tP(polite) = %.3f" % np.mean(polite))
        print("\tP(impolite) = %.3f" % np.mean(impolite))

#    from test_documents import TEST_DOCUMENTS

#    for doc in TEST_DOCUMENTS:

#        probs = score(doc)

#        print("====================")
#        print("Text: ", doc['text'])
#        print("\tP(polite) = %.3f" % probs['polite'])
#        print("\tP(impolite) = %.3f" % probs['impolite'])
#        print("\n")


