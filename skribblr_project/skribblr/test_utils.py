from datetime import datetime, timedelta
from django.core.urlresolvers import resolve
from django.test import TestCase
import json
from skribblr.models import Author, Entry
from skribblr.views import (author_portal_home,
                            author_portal_compose,
                            home_page,
                            portal_add_entry,
                            portal_list_entries)
import pytz


class SkribTestUtil():

    def create_authors(self, author_num):
        """
        generates a number of author objects as defined by author_num param
        then returns list of author names generated

        """
        i = 0
        author_names = []
        while i < author_num:
            test_author = Author()
            author_name = 'test_author' + str(i)
            test_author.name = author_name
            test_author.save()
            author_names.append(author_name)
            i += 1

        return author_names

    def create_entries(self, entries_num):
        """
        generates a number of author objects as defined by entries_num,
        then returns a dictionary of their values
        """

        i = 0
        entries = {}
        while i < entries_num:
            # generate values for entries
            title = 'entry title ' + str(i)
            author = Author.objects.filter(name='test_author' + str(i))
            author = author[0]
            date = pytz.utc.localize(datetime.now())
            content = 'etnry content ' + str(i)
            tldr = 'tldr ' + str(i)

            # load values into model:
            test_entry = Entry()
            test_entry.title = title
            test_entry.author = author
            test_entry.date = date
            test_entry.content = content
            test_entry.tldr = tldr
            test_entry.save()

            #load values into return dict:
            entries[i] = {'title': title,
                          'author': author,
                          'date': date,
                          'content': content,
                          'tldr': tldr}

            i +=1

        return entries
