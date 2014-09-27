politeness
==========

Sample implementation of a politeness model to classify the politeness of requests using python and scikit-learn.

Based on the model described in "A computational approach to politeness with application to social factors". 

A computational approach to politeness with application to social factors. Cristian Danescu-Niculescu-Mizil, Moritz Sudhof, Dan Jurafsky, Jure Leskovec, Christopher Potts. Proceedings of ACL, 2013.

We release this code in the hope that others will access and improve on our work.

Further resources--
    Info about our work: http://www.mpi-sws.org/~cristian/Politeness.html
    A web interface to the politeness model: http://politeness.mpi-sws.org/
    The Stanford Politeness Corpus: http://www.mpi-sws.org/~cristian/Politeness_files/Stanford_politeness_corpus.zip


Code--

- Classify documents using politeness.model.score

- Train models using politeness.scripts.train_model

- Modify politeness features in politeness.features.vectorizer and politeness.features.politeness_strategies

- Documents must always be pre-processed with sentences and parses. 
We used nltk's PunktSentenceTokenizer for sentence tokenization and Stanford CoreNLP for dependency parsing. 
To see a sample of the expected format for documents, see politeness.test_documents

- This work focuses on requests, not all kinds of utterances. The model's predictions on non-request utterances (such as imperatives), will be more unpredictable.
Our code includes a simple heuristic to check whether a document looks like a request (see politeness.request_utils)

Requirements: scikit-learn, scipy, numpy, nltk






