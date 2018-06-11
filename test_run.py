#! usr/bin/env python3

from tools.paper import Paper
from tools.defs import Defs
import os


def main():
    project_defs = Defs()
    for file_name in project_defs.paper_titles:
        paper_title = project_defs.paper_dir + file_name
        with open(paper_title, encoding=project_defs.encoding) as paper:
            paper_string = paper.read()

            my_paper = Paper(project_defs.keywords, paper_string)
            my_paper.frequency_distribution()
            my_paper.find_concordances(project_defs.concordance_buffer)
            my_paper.find_bigrams()
            # lemmatizer converts "us" -> "u"
            my_paper.search_bigrams("let", "u")
            my_paper.search_n_grams(["you", "and", "i"])

            my_paper.generate_file_string()

            # write out the file string to analysis files
            # NOTE: this program is not multithreaded, so os.path.exists() -> os.makedirs()
            # race condition is not accounted for
            if not os.path.exists(project_defs.results_dir):
                os.makedirs(project_defs.results_dir)
            with open(project_defs.results_dir + "data-" + file_name, "w") as dest_file:
                dest_file.write(my_paper.file_string)



if __name__ == '__main__':
    main()
