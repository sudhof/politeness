
import os
import cPickle
import string
import nltk
from itertools import chain
from collections import defaultdict

# local import
from politeness_strategies import get_politeness_strategy_features

# Will need access to local dir
# for support files
LOCAL_DIR = os.path.split(__file__)[0]


def get_unigrams_and_bigrams(document):
    """
    Grabs unigrams and bigrams from document 
    sentences. NLTK does the work.
    """
    # Get unigram list per sentence:
    unigram_lists = map(lambda x: nltk.word_tokenize(x), document['sentences'])
    # Generate bigrams from all sentences:
    bigrams = chain(*map(lambda x: nltk.bigrams(x), unigram_lists))
    # Chain unigram lists
    unigrams = chain(*unigram_lists)
    return unigrams, bigrams



class PolitenessFeatureVectorizer:

    """
    Returns document features based on-
        - unigrams and bigrams
        - politeness strategies 
            (inspired by B&L, modeled using dependency parses)
    """

    UNIGRAMS_FILENAME = os.path.join(LOCAL_DIR, "featunigrams.p")
    BIGRAMS_FILENAME = os.path.join(LOCAL_DIR, "featbigrams.p")

    def __init__(self):
        """
        Load pickled lists of unigram and bigram features
        These lists can be generated using the training set
        and PolitenessFeatureVectorizer.generate_bow_features
        """
        self.unigrams = cPickle.load(open(self.UNIGRAMS_FILENAME))
        self.bigrams = cPickle.load(open(self.BIGRAMS_FILENAME))


    def features(self, document):
        """
        document must be a dict of the following format-- 
            {
                'sentences': ["sentence str"],
                'parses': [[dependency parse list]]
            }
        """
        feature_dict = {}
        # Add unigram, bigram features:
        feature_dict.update(self._get_term_features(document))
        # Add politeness strategy features:
        feature_dict.update(get_politeness_strategy_features(document))
        return feature_dict

    def _get_term_features(self, document):
        # One binary feature per ngram in
        # in self.unigrams and self.bigrams
        unigrams, bigrams = get_unigrams_and_bigrams(document)
        # Add unigrams to document for later use
        document['unigrams'] = unigrams
        unigrams, bigrams = set(unigrams), set(bigrams)
        f = {}
        f.update(dict(map(lambda x: ("UNIGRAM_" + str(x), 1 if x in unigrams else 0), self.unigrams)))
        f.update(dict(map(lambda x: ("BIGRAM_" + str(x), 1 if x in bigrams else 0), self.bigrams)))
        return f


    @staticmethod
    def generate_bow_features(documents, min_unigram_count=20, min_bigram_count=20):
        """
        Given a list of documents, compute and store list of unigrams and bigrams
        with a frequency > min_unigram_count and min_bigram_count, respectively.
        This method must be called prior to the first vectorizer instantiation.
        
        documents - 

            each document must be a dict
            {
                'sentences': ["sentence one string", "sentence two string"],
                'parses': [ ["dep(a,b)"], ["dep(b,c)"] ]
            }
        """
        punctuation = string.punctuation
        punctuation = punctuation.replace("?","").replace("!","")
        unigram_counts, bigram_counts = defaultdict(int), defaultdict(int)
        # Count unigrams and bigrams:
        for d in documents:
            unigrams, bigrams = get_unigrams_and_bigrams(d)
            # Count
            for w in unigrams:
                unigram_counts[w] += 1
            for w in bigrams:
                bigram_counts[w] += 1
        # Keep only ngrams that pass frequency threshold:
        unigram_features = filter(lambda x: unigram_counts[x] > min_unigram_count, unigram_counts.iterkeys())
        bigram_features = filter(lambda x: bigram_counts[x] > min_bigram_count, bigram_counts.iterkeys())
        # Save results:
        cPickle.dump(unigram_features, open(PolitenessFeatureVectorizer.UNIGRAMS_FILENAME, 'w'))
        cPickle.dump(bigram_features, open(PolitenessFeatureVectorizer.BIGRAMS_FILENAME, 'w'))





if __name__ == "__main__":

    """
    Extract features from test documents
    """

    from test_documents import TEST_DOCUMENTS

    vectorizer = PolitenessFeatureVectorizer()

    for doc in TEST_DOCUMENTS:
        f = vectorizer.features(doc)

        # Print summary of features that are present
        print "\n===================="
        print "Text: ", doc['text']
        print "\tUnigrams, Bigrams: %d" % len(filter(lambda x: f[x] > 0 and ("UNIGRAM_" in x or "BIGRAM_" in x), f.iterkeys()))
        print "\tPoliteness Strategies: \n\t\t%s" % "\n\t\t".join(filter(lambda x: f[x] > 0 and "feature_politeness_" in x, f.iterkeys()))
        print "\n"


