Stanford Politeness API
=======================
 Version 1.01 (released October 2014)

Python implementation of a politeness classifier for requests, based on the work described in:

	A computational approach to politeness with application to social factors.  	
	Cristian Danescu-Niculescu-Mizil, Moritz Sudhof, Dan Jurafsky, Jure Leskovec, Christopher Potts.  
	Proceedings of ACL, 2013.


We release this code hoping that others will use and improve on our work.

NOTE: If you use this API in your work please send an email to cristiand@cs.stanford.edu so we can add you to our list of users.  Thanks!


**Further resources:**

    Info about our work: http://www.mpi-sws.org/~cristian/Politeness.html

    A web interface to the politeness model: http://politeness.mpi-sws.org/

    The Stanford Politeness Corpus: http://www.mpi-sws.org/~cristian/Politeness_files/Stanford_politeness_corpus.zip


**Using this API you can:**

- classify requests using politeness.model.score  (using the provided pre-trained model)

- train new models on new data using politeness.scripts.train_model

- experiment with new politeness features in politeness.features.vectorizer and politeness.features.politeness_strategies


**Input:** Requests must be pre-processed with sentences and dependency parses.  We used nltk's [PunktSentenceTokenizer](http://www.nltk.org/api/nltk.tokenize.html#module-nltk.tokenize.punkt) for sentence tokenization and [Stanford CoreNLP](http://nlp.stanford.edu/software/corenlp.shtml) [version 1.3.3](http://nlp.stanford.edu/software/stanford-corenlp-2012-07-09.tgz) for dependency parsing.  A sample of the expected format for documents is given in politeness.test_documents


**Caveat:** This work focuses on requests, not all kinds of utterances. The model's predictions on non-request utterances will be less accurate. As a bonus, our code also includes a very simple heuristic to check whether a document looks like a request (see politeness.request_utils).


**Requirements:** 

python package requirements are listed in requirements.txt. We recommend setting up a new python environment using virtualenv and installing the dependencies by running

    pip install -r requirements.txt

Additionally, since the code uses nltk.word_tokenize to tokenize text, you will need to download the  tokenizers/punkt/english.pickle nltk resource. If you've worked with nltk before, there's a good chance you've already downloaded this model. Otherwise, open the python interpreter and run:

    import nltk
    nltk.download()

In the window that opens, navigate to Models and download the Punkt Tokenizer Models.


**Sanity Check:**

To make sure everything's working, navigate to the code directory and run

    python model.py

This should print out the politeness probabilities for 4 test documents.


**Contact:** Please email any questions to: cristiand@cs.stanford.edu (Cristian Danescu-Niculescu-Mizil) and sudhof@stanford.edu (Moritz Sudhof)