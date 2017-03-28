
import random
import _pickle
import numpy as np
import os
import sys
import json

from sklearn import svm
from scipy.sparse import csr_matrix
from sklearn.metrics import classification_report

#### PACKAGE IMPORTS ###########################################################
from features.vectorizer import PolitenessFeatureVectorizer
from corpora import PARSED_STACK_EXCHANGE, PARSED_WIKIPEDIA

"""
Sample script to train a politeness SVM

Buckets documents by politeness score
   'polite' if score > 0.0
   'impolite' otherwise
Could also elect to not bucket
and treat this as a regression problem
"""


def train_svm(documents, ntesting=500):
    """
    Given a list annotated documents (training data) of the following form, and
    an integer specifying the number of documents to withhold for testing,
    return a fitted SVC, serialized via pickle.
        {
            "sentences": ["sent1 text", "sent2 text", ...],
            "parses": [
                          [list of sent1 dependency-parses],
                          [list of sent2 dependency-parses],
                          ...
                      ]
        }
    """
    # Generate and persist list of unigrams, bigrams
    print("Gathering N-Grams...")
    PolitenessFeatureVectorizer.generate_bow_features(documents)

    # For good luck
    print("Splitting Testing and Training Docs...")
    random.shuffle(documents)
    testing = documents[-ntesting:]
    documents = documents[:-ntesting]

    # SAVE FOR NOW
    print("Saving Testing Docs for Later...")
    _pickle.dump(testing, open("testing-data.p", 'wb'))

    X, y = documents2feature_vectors(documents)
    Xtest, ytest = documents2feature_vectors(testing)

    print("Fitting...")
    clf = svm.SVC(C=0.02, kernel='linear', probability=True)
    clf.fit(X, y)

    # Test
    y_pred = clf.predict(Xtest)
    print(classification_report(ytest, y_pred))

    return clf


def documents2feature_vectors(documents):
    """ Generate feature vectors for the given list of documents. """
    print("Calculating Feature Vectors...")
    vectorizer = PolitenessFeatureVectorizer()
    fks = False
    X, y = [], []
    cnt = 0
    for d in documents:
        fs = vectorizer.features(d)
        if not fks:
            fks = sorted(fs.keys())
        fv = [fs[f] for f in fks]
        # If politeness score > 0.0, 
        # the doc is polite, class=1
        try:
            l = 1 if float(d['score']) > 0.0 else 0
        except ValueError:
            l = 0
        X.append(fv)
        y.append(l)
        print(cnt)
        cnt+=1
    X = csr_matrix(np.asarray(X))
    y = np.asarray(y)
    return X, y

def train_classifier(dataset, ntesting=500):
    """
    Wrapper function for train_svm(). Given a dataset identifier ('all',
    'wikipedia', or 'stackexchange') and an integer specifying how many
    documents to withhold for testing, grab the annotated documents from
    the preprocessed annotated dataset(s).

    If errors occur in this function, it is likely that the preprocessed
    annotated datasets need to be downloaded and extracted. See
    /corpora/download.py for functions to automatically download them for you.
    """
    all_docs = []
    if dataset == 'all':
        print("Gathering All Available Docs...")
        all_docs = json.loads(open(PARSED_STACK_EXCHANGE, 'r').read()) + json.loads(open(PARSED_WIKIPEDIA, 'r').read())
    elif dataset == 'wikipedia':
        print("Gathering All Wikipedia Docs...")
        all_docs = json.loads(open(PARSED_WIKIPEDIA, 'r').read())
    elif dataset == 'stackexchange':
        print("Gathering All Stack Exchange Docs...")
        all_docs = json.loads(open(PARSED_STACK_EXCHANGE, 'r').read())
    else:
        print("Defaulting to All Available Docs...")
        all_docs = json.loads(open(PARSED_STACK_EXCHANGE, 'r').read()) + json.loads(open(PARSED_WIKIPEDIA, 'r').read())

    print("Starting to Train Model...")
    FITTED_SVC = train_svm(all_docs, ntesting=ntesting)
    print("Dumping Model to File...")
    _pickle.dump(FITTED_SVC, open("politeness-svm.p", 'wb'))
    print("Finishing up...")

if __name__ == "__main__":
    # Train a dummy model off our 4 sample request docs

    from test_documents import TEST_DOCUMENTS

    train_svm(TEST_DOCUMENTS, ntesting=1)

