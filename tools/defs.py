#! usr/bin/env python3
import os
import json


class Defs:
    """
    Hold directory names, files, and keywords necessary to conduct analysis.
    keywords = {
        keyword: [synonym list],
        ...
    }
    papers = [file_name1, file_name2, ...]
    buffer = number of words on each side of keyword to include in concordances
    encoding_type = encoding of research paper files
    """

    def __init__(self):
        self.config_info = {}
        self.paper_titles = []
        self.keywords = {}
        self.paper_dir = ""
        self.results_dir = ""
        self.encoding = ""
        self.concordance_buffer = 0
        # read config files to initialize components
        self.read_config_files()

    def read_config_files(self):
        with open("resources/keywords.json", 'r') as keywords_file:
            self.keywords = json.load(keywords_file)
        with open("resources/project_config.json", 'r') as config_file:
            self.config_info = json.load(config_file)
        self.paper_titles = [str(paper_title) for paper_title in
                             os.listdir(self.config_info["paper directory"])]
        self.paper_dir = self.config_info["paper directory"] + '/'
        self.results_dir = self.config_info["results directory"] + '/'
        self.encoding = self.config_info["encoding"]
        self.concordance_buffer = self.config_info["concordance buffer"]
