import nltk
from tools import text_analysis as ta


class Paper:
    """
    Hold data about an academic paper.
    freq_dict_tup_ls = [(keyword, {synonym1: 0, ...}), ...]
    concordance_tup_ls = [(keyword, [concordance_ls])]
    bigrams = [(w1, w2), (w2, w3), ...] *** Lemmatized tokens only
    n_grams = [([loc1, loc2, ...], [gram1, gram2, ...]), ...]
    """

    def __init__(self, keywords: dict, paper_str: str):
        """
        :param keywords: {'keyword': [synonym1, ...], ...}
        :param paper_str: a string version of a paper
        """

        # Initialize tuple lists to be empty
        self.freq_dict_tup_ls = []
        self.concordance_tup_ls = []

        # string version of paper being analyzed
        self.paper_str = paper_str

        # initialize all tokens to empty lists
        self.paper_tokens = []
        self.lc_paper_tokens = []
        self.lc_lem_paper_tokens = []

        # initialize a place for bigrams & n-grams to be recorded
        self.bigrams = []
        self.bigram_queries = []
        self.n_gram_queries = []

        # this will be how paper data will be written out
        self.file_string = ""

        # initialize the frequencies of the keyword synonyms
        self.make_freq_dicts(keywords)
        self.initialize_tokens()

    def generate_file_string(self):
        """
        Generate a string containing all desired information for the purpose of being
        written to a text file.

        :return: None
        """
        present_keys_str = ""
        frequency_str = ""
        n_gram_str = ""
        bigram_str = ""
        concordance_str = ""

        # check what is actually present in this paper (of the user's desired queries)
        present_keys = [tup[0] for tup in self.freq_dict_tup_ls if sum(tup[1].values()) > 0]
        for key in present_keys:
            present_keys_str += (key + '\n')

        # format the frequency distributions
        for tup in self.freq_dict_tup_ls:
            frequency_str += "Keyword: {} (occurrences: {})\n".format(tup[0], str(sum(tup[1].values())))
            frequency_str += "{}\n\n".format(str(tup[1]))

        # format the n-grams
        for tup in self.n_gram_queries:
            n_gram_str += "N-Gram: {}\n".format(' '.join(tup[1]))
            if len(tup[0]) > 0:
                n_gram_str += "Found at Token(s): {}\n\n".format(str(tup[0]))
            else:
                n_gram_str += "Not found\n\n"

        for tup in self.bigram_queries:
            bigram_str += "Bi-Gram: {}\n".format(' '.join(tup[1]))
            if len(tup[0]) > 0:
                bigram_str += "Found at Token(s): {}\n\n".format(str(tup[0]))
            else:
                bigram_str += "Not found\n\n"

        # format the concordances
        for tup in self.concordance_tup_ls:
            # only include terms that actually occur
            if len(tup[1]) > 0:
                concordance_str += "--- Keyword: {} ------------------------------\n\n".format(tup[0])
                for conc in tup[1]:
                    concordance_str += "[{}, {}]:\n{}\n\n".format(conc[1], conc[0], conc[2])


        self.file_string += "[This Paper References]: \n\n{}\n\n".format(present_keys_str)
        self.file_string += "[Frequencies]: \n\n{}\n\n".format(frequency_str)
        self.file_string += "[N-Gram Queries]: \n\n{}\n\n".format(n_gram_str)
        self.file_string += "[Bi-Gram Queries]: \n\n{}\n\n".format(bigram_str)
        self.file_string += "[Concordances]: \n\n{}\n\n".format(concordance_str)

    def make_freq_dicts(self, keywords: dict):
        """
        Make word frequency dictionaries for each keyword's synonyms.
        Store as a tuple: (keyword, {syn1: freq, syn2: freq, ...}).
        Append this tuple to self.freq_dict_tup_ls.

        :param keywords:  {'keyword': [synonym1, ...], ...}
        :return: None
        """
        for key_wd, synonyms in keywords.items():
            # give each synonym an initial frequency of 0
            word_freq = {}
            for syn in synonyms:
                word_freq[syn] = 0
            self.freq_dict_tup_ls.append((key_wd, word_freq))

    def initialize_tokens(self):
        """
        Initialize...
        -- self.paper_tokens: all tokens in paper
        -- self.lc_paper_tokens: lowercase of all tokens in paper (numerical tokens remain
        unchanged)
        -- self.lem_paper_tokens: lowercase and lemmatization of all tokens in paper (numerical
        entries remain unchanged)

        :return: None
        """
        # Create tokens from the paper string
        self.paper_tokens = nltk.word_tokenize(self.paper_str)
        # Create version of tokens where all tokens are lower cased
        ta.lower_text(self.paper_tokens, self.lc_paper_tokens)
        # Create version of tokens where all lemmatized & lower cased
        ta.lemmatize_text(self.lc_paper_tokens, self.lc_lem_paper_tokens)

    def frequency_distribution(self):
        """
        Fill in the frequency distribution dictionaries for each of the keywords
        in self.freq_dict_tup_ls.

        :return: None
        """
        # iterate through all items in the freq_dict_tup_ls
        for tup in self.freq_dict_tup_ls:
            # fill in the frequency dictionary for the current tuple
            # tup[1] = the dictionary
            ta.create_frequency_dict(self.lc_lem_paper_tokens, tup[1])

    def find_concordances(self, buffer: int):
        """
        Create concordance lists for each tracked keyword.

        :param buffer: the amount of tokens on either side of the keyword to take on as part
        of the concordance
        :return: None
        """
        for tup in self.freq_dict_tup_ls:
            # make a (sorted) list of the synonym keys for the current keyword
            keyword_ls = [key for key in tup[1]]
            # make a temporary concordance list to be stored with the
            # current keyword: (keyword, [(location, synonym, concordance), ...])
            key_concordances = []
            # find concordances for all synonyms of current keyword
            ta.cross_ref_target_list_concordance(keyword_ls, self.lc_lem_paper_tokens,
                                                 self.paper_tokens, buffer, key_concordances)
            self.concordance_tup_ls.append((tup[0], key_concordances))

    def find_bigrams(self):
        """
        Create bigrams of the lemmatized tokens

        :return: None
        """

        self.bigrams = nltk.bigrams(self.lc_lem_paper_tokens)

    def search_bigrams(self, target1: str, target2: str):
        """
        Check to see whether queried bigram is present in the bigrams for this paper.

        :param target1: a string, part 1 of the bigram
        :param target2: a string, part 2 of the bigram
        """
        temp_locks = []
        ta.bigram_counter(self.bigrams, (target1, target2), temp_locks)
        self.bigram_queries.append((temp_locks, [target1, target2]))

    def search_n_grams(self, targets: list):
        """
        Search through the paper text for location of target n-gram.
        This will be added to:
        self.n_grams = [ ([loc1, loc2, ...], ["t1", "t2", ...]), ...]

        :param targets: a list of targets... ["t1", "t2", ...]
        :return: None
        """

        temp_locs = []
        ta.n_gram_counter(self.lc_paper_tokens, targets, temp_locs)
        self.n_gram_queries.append((temp_locs, targets))
