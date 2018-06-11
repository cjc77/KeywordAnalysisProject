#! usr/bin/env python3

from nltk.stem.wordnet import WordNetLemmatizer


def lower_text(src_tokens: list, dest_tokens: list):
    """
    Take a list of tokens, lowercase the alphabetical tokens.
    Put the result in "dest_tokens"

    :param src_tokens: a list of tokens ['t1', 't2', ...]
    :param dest_tokens: an empty list that will hold lowercase versions of src_tokens
    :return: None
    """
    for w in src_tokens:
        if w.isalpha():
            w = w.lower()
            dest_tokens.append(w)
        # Retain non-alphabetical items
        else:
            dest_tokens.append(w)


def lemmatize_text(src_tokens: list, dest_tokens: list):
    """
    Take a list of tokens, lemmatize the alphabetical tokens,
    and put them in "dest_tokens"
    NOTE: lemmatization does NOT change tense.

    :param src_tokens: a list of tokens ['t1', 't2', ...]
    :param dest_tokens: an empty list that will hold lowercase versions of src_tokens
    :return: None
    """
    lem = WordNetLemmatizer()
    for w in src_tokens:
        # Lemmatize the alphabetical items
        if w.isalpha():
            w = lem.lemmatize(w)
            dest_tokens.append(w)
        # Retain non-alphabetical items
        else:
            dest_tokens.append(w)


def create_frequency_dict(tokens: list, dic: dict):
    """
    Create a frequency distribution for dic based on the number of times
    each key occurs in "tokens".

    :param tokens: a list of tokens ['t1', 't2', ...]
    :param dic: a dictionary of terms whose frequencies must be calculated
    :return: None
    """
    keys = list(dic.keys())
    for w in tokens:
        if w in keys:
            dic[w] += 1


def cross_ref_target_list_concordance(targets: list, lem_tokens: list, reg_tokens: list,
                                      buffer: int, dest: list):
    """
    Create a concordance list of the following structure:
    [(location1, synonym1, concordance1), ...]

    :param targets: list of keywords to be searched for in lem_tokens
    :param lem_tokens: a list of lemmatized tokens
    :param reg_tokens: a list of regular tokens (to be matched with index of appropriate lemmatized token)
    :param buffer: the amount of tokens on either side of the keyword to take on as part
    of the concordance
    :param dest: the destination list to which concordance tuples should be added
    :return: None
    """

    # length of token list
    size = len(lem_tokens)

    # search through each token
    for location in range(size):
        if lem_tokens[location].lower() in targets:
            # Check if we are at very beginning
            if (location - buffer) < 0:
                begin = 0
            else:
                begin = location - buffer + 1

            # Check if at very end
            if (location + buffer) > size:
                end = size
            else:
                end = location + buffer + 1

            # record the context
            context = (reg_tokens[begin:end])
            # Turn the context into a string
            concordance_line = ' '.join(context)
            dest.append((location, lem_tokens[location].lower(), concordance_line))
    # sort the concordances based on the synonyms
    dest.sort(key=lambda tup: tup[1])


def n_gram_counter(tokens: list, target: list, locations: list):
    """
    When a match is found, adds the index of a match to "locations"

    :param tokens: ["t1", "t2", ...]
    :param target: ["w1", "w2", ...]
    :param locations: a list that is added to
    :return: None
    """
    match = False
    start = len(target) - 1
    size = len(tokens)

    # compare each token in target IN ORDER with a corresponding token in tokens:
    # EX:
    # tokens = ["the", "cat", "is", "brown"]
    # target = ["the", "cat"]
    # results in: ([0], ["the", "cat"])

    for i in range(start, size):
        match = False
        for j in range(start + 1):
            # if one of the targets don't match, skip ahead
            if tokens[i - (start - j)] != target[j]:
                break
        else:
            match = True
        if match is True:
            locations.append(i - start)

def bigram_counter(bigrams: list, target: tuple, locations: list):
    """
    When a match is found, adds the index of a match to "locations"

    :param tokens: tokens: ["t1", "t2", ...]
    :param target: ("w1", "w2")
    :param locations: a list that is added to
    :return: None
    """
    found = False
    for token, tup in enumerate(bigrams):
        if target[0].lower() == tup[0] and target[1].lower() == tup[1]:
            found = True
            locations.append(token)

