#!/usr/bin/env python
# -*- coding: utf-8 -*-

import parse.article_parser

class TitleParser(parse.article_parser.ArticleParser):

    def handle_starttag(self, tag, attrs):
        # We are looking for the begining of a link. Links normally look
        # like <a href="www.someurl.com"></a>
        if tag == 'title':
            self.recording += 1


    def handle_endtag(self, tag):
        if tag == 'title' and self.recording:
            self.recording -= 1


    # Overridable
    def process_contents(self, data):
        i = data.find(u" | ZEIT ONLIN")
        return data[:i].strip()

