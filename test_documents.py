


"""
Some sample request documents, pre-processed 
and ready for politeness classification.

Shows expected format of documents--
Each document is a dict with fields
'text', 'sentences', and 'parses'

the 'score' field is only required
when training models. 
A score > 0.0 means the request is polite.

"""

TEST_DOCUMENTS = [
    # Polite requests
    # Req 1
    {
        "text": "Have you found the answer for your question? If yes would you please share it?", 
        "sentences": [
            "Have you found the answer for your question?", 
            "If yes would you please share it?"
        ],
        "parses": [
            ["csubj(found-3, Have-1)", "dobj(Have-1, you-2)", "root(ROOT-0, found-3)", "det(answer-5, the-4)", "dobj(found-3, answer-5)", "poss(question-8, your-7)", "prep_for(found-3, question-8)"], 
            ["prep_if(would-3, yes-2)", "root(ROOT-0, would-3)", "nsubj(would-3, you-4)", "ccomp(would-3, please-5)", "nsubj(it-7, share-6)", "xcomp(please-5, it-7)"]
        ],
        "score": 0.7
    }, 
    # Req 2
    {
        "text": "Sorry :) I dont want to hack the system!! :) is there another way?", 
        "sentences": [
            "Sorry :) I dont want to hack the system!!", 
            ":) is there another way?"
        ],
        "parses": [
            ["nsubj(dont-5, I-4)", "xsubj(hack-8, I-4)", "rcmod(-RRB--3, dont-5)", "dep(dont-5, want-6)", "aux(hack-8, to-7)", "xcomp(want-6, hack-8)", "det(!!-11, the-9)", "nn(!!-11, system-10)", "dobj(hack-8, !!-11)"], 
            ["cop(there-4, is-3)", "root(ROOT-0, there-4)", "det(way-6, another-5)", "dep(there-4, way-6)"]
        ],
        "score": 0.8
    },
    # Impolite requests
    # Req 3
    {
        "text": "Ugh, possibly the ugliest Python code I've ever seen. What are you doing?", 
        "sentences": [
            "Ugh, possibly the ugliest Python code I've ever seen.", 
            "What are you doing?"
        ],
        "parses": [
            ["nsubj(seen-11, Ugh-1)", "advmod(ugliest-5, possibly-3)", "det(ugliest-5, the-4)", "dep(seen-11, ugliest-5)", "nn(code-7, Python-6)", "dep(ugliest-5, code-7)", "nsubj(seen-11, I-8)", "aux(seen-11, \'ve-9)", "advmod(seen-11, ever-10)", "root(ROOT-0, seen-11)"], 
            ["dobj(doing-4, What-1)", "aux(doing-4, are-2)", "nsubj(doing-4, you-3)", "root(ROOT-0, doing-4)"]
        ],
        "score": -0.7
    },
    # Req 4
    {
        "text": "My answer would be: What kind of lame ass product searches for palindromes in a string. May I take a closer look at your business plan, please?", 
        "sentences": [
            "My answer would be: What kind of lame ass product searches for palindromes in a string.", 
            "May I take a closer look at your business plan, please?"
        ],
        "parses": [
            ["poss(answer-2, My-1)", "nsubj(be-4, answer-2)", "aux(be-4, would-3)", "dep(kind-7, be-4)", "det(kind-7, What-6)", "root(ROOT-0, kind-7)", "dep(kind-7, of-8)", "amod(searches-12, lame-9)", "nn(searches-12, ass-10)", "nn(searches-12, product-11)", "pobj(of-8, searches-12)", "prep_for(searches-12, palindromes-14)", "det(string-17, a-16)", "prep_in(palindromes-14, string-17)"], 
            ["tmod(take-3, May-1)", "nsubj(take-3, I-2)", "root(ROOT-0, take-3)", "det(look-6, a-4)", "amod(look-6, closer-5)", "dobj(take-3, look-6)", "poss(plan-10, your-8)", "nn(plan-10, business-9)", "prep_at(take-3, plan-10)", "dep(take-3, please-12)"]
        ],
        "score": -0.8
    }
]







