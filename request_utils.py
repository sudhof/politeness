

from features.politeness_strategies import check_elems_for_strategy, initial_polar, aux_polar


def check_is_request(document):
    """
    Heuristic to determine whether a document
    looks like a request

    :param document- pre-processed document
        that might be a request
    :type document- dict with fields 
        'sentences' and 'parses', as
        in other parts of the system
    """
    for sentence, parse in zip(document['sentences'], document['parses']):
        if "?" in sentence:
            return True
        if check_elems_for_strategy(parse, initial_polar) or check_elems_for_strategy(parse, aux_polar):
            return True
    return False




if __name__ == "__main__":


    from test_documents import TEST_DOCUMENTS

    for doc in TEST_DOCUMENTS:
        print "\nText: ", doc['text']
        print "Is request: ", check_is_request(doc)

    print "\n"



