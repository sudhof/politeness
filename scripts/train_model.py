
import random
import cPickle
import numpy as np

from sklearn import svm
from scipy.sparse import csr_matrix
from sklearn.metrics import classification_report

from politeness.features.vectorizer import PolitenessFeatureVectorizer

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
    :param documents- politeness-annotated training data
    :type documents- list of dicts
        each document must be preprocessed and
        'sentences' and 'parses' and 'score' fields.

    :param ntesting- number of docs to reserve for testing
    :type ntesting- int

    returns fitted SVC, which can be serialized using cPickle
    """
    # Generate and persist list of unigrams, bigrams  
    PolitenessFeatureVectorizer.generate_bow_features(documents)

    # For good luck
    random.shuffle(documents)
    testing = documents[-ntesting:]
    documents = documents[:-ntesting]

    # SAVE FOR NOW
    cPickle.dump(testing, open("testing-data.p", 'w'))

    X, y = documents2feature_vectors(documents)
    Xtest, ytest = documents2feature_vectors(testing)

    print "Fitting"
    clf = svm.SVC(C=0.02, kernel='linear', probability=True)
    clf.fit(X, y)

    # Test
    y_pred = clf.predict(Xtest)
    print(classification_report(ytest, y_pred))

    return clf


def documents2feature_vectors(documents):
    vectorizer = PolitenessFeatureVectorizer()
    fks = False
    X, y = [], []
    for d in documents:
        fs = vectorizer.features(d)
        if not fks:
            fks = sorted(fs.keys())
        fv = [fs[f] for f in fks]
        # If politeness score > 0.0, 
        # the doc is polite, class=1
        l = 1 if d['score'] > 0.0 else 0
        X.append(fv)
        y.append(l)
    X = csr_matrix(np.asarray(X))
    y = np.asarray(y)
    return X, y



if __name__ == "__main__":


    """
    Train a dummy model off our 4 sample request docs
    """

    from test_documents import TEST_DOCUMENTS

    train_svm(TEST_DOCUMENTS, ntesting=1)

