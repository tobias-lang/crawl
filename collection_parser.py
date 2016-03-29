import traceback
from HTMLParser import HTMLParser
from urllib2 import urlopen
import urlparse
import codecs
import numpy as np

import article_parser


class CollectionParser():

    def __init__(self, article_parser=article_parser.ArticleParser()):
        self.article_parser = article_parser


    def get_filelist(self, dir, maxNumber=None):
        from os import listdir
        from os.path import isfile, join
        filenames = [join(dir, f) for f in listdir(dir) if isfile(join(dir, f))]
        filenames = filter(lambda x: self._is_relevant_file(x), filenames)
        filenames = filenames[:maxNumber]
        return filenames


    def _is_relevant_file(self, filename):
        if filename.endswith("#comments"):
            return False
        return True


    def parse_file(self, filename):
        f = codecs.open(filename, "r", "utf-8")
        lines = f.readlines()
        big_data_string = "".join(lines)
        self.article_parser.reset()
        self.article_parser.feed(big_data_string)
        c = self.article_parser.getContents()
        return c


    def parse_collection(self, filenames):
        contents = set()
        for idx, filename in enumerate(filenames):
            # print "read", filename
            c = self.parse_file(filename)
            if len(c):
                # print "->", len(c)
                contents.add(c)
            # if len(contents) > 10:
            #     break

        contents = list(contents)
        contents.sort()
        return contents


    def parse_and_write_collection(self, input_filenames, output_filename):
        print "write contents to", output_filename
        f = codecs.open(output_filename, "w", "utf-8")
        n = 100
        for i in range(len(input_filenames)/n):
            print i*n,
            batch_filenames = input_filenames[i*n:(i+1)*n]
            batch_contents =self.parse_collection(batch_filenames)
            for c in batch_contents:
                try:
                    # print h
                    # h_ascii = h.encode('ascii', 'ignore')
                    f.write(c + "\n")
                except Exception as e:
                    print(traceback.format_exc())
            f.flush()
        f.close()



    def run_full(self, input_dir, output_filename, maxNumber=None):
        filenames = self.get_filelist(input_dir, maxNumber)
        contents = self.parse_and_write_collection(filenames, output_filename)
        import os
        os.system("wc " + output_filename)

