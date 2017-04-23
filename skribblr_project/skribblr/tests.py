from datetime import datetime, timedelta
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
import json
from skribblr.test_utils import SkribTestUtil
from skribblr.models import Author, Entry
from skribblr.views import (author_portal_home,
                            author_portal_compose,
                            home_page,
                            portal_add_entry,
                            portal_list_entries,
                            portal_update_entry,
                            portal_delete_entry,
                            view_entry)
import pytz

class EntryModelTest(TestCase):

    def test_adding_and_retrieving_authors(self):
        test_util = SkribTestUtil()
        test_author_name = test_util.create_authors(1)
        test_author = Author.objects.first()

        self.assertEqual(test_author.name,
                         test_author_name[0],
                         'author name in db incorrect')

    def test_adding_and_retrieving_entries(self):

        test_util = SkribTestUtil()

        test_authors = test_util.create_authors(3)
        test_entries = test_util.create_entries(3)

        entries = Entry.objects.all()

        self.assertEqual(entries.count(), 3)

        first_saved_entry = entries[0]
        second_saved_entry = entries[1]

        self.assertEqual(first_saved_entry.title,
                         test_entries[0]['title'],
                         'Entry title writing to DB incorrectly')
        self.assertEqual(second_saved_entry.author,
                         test_entries[1]['author'],
                         'Entry author writing to DB incorrectly')
        self.assertEqual(first_saved_entry.date,
                         test_entries[0]['date'],
                         'Entry timestamp writing to DB incorrectly')
        self.assertEqual(second_saved_entry.content,
                         test_entries[1]['content'],
                         'Entry content writing to DB incorrectly')
        self.assertEqual(first_saved_entry.tldr,
                         test_entries[0]['tldr'],
                         'Entry TLDR writing to DB incorrectly')

class AuthorPortalTest(TestCase):

    def correct_view_resolution(self, test_url, test_func):
        """
        Test class wide tool for view resolution checking
        """
        response = resolve(test_url)
        self.assertEqual(response.func,
                         test_func,
                         test_url + ' not resolving correctly')

    def test_does_AuthorPortal_resolve_to_correct_view(self):
        self.correct_view_resolution('/portal',
                                     author_portal_home)

    def test_does_PortalCompose_resolve_correctly(self):
        self.correct_view_resolution('/portal/compose',
                                     author_portal_compose)

    def test_PortalAdd_resolves_correctly(self):
        self.correct_view_resolution('/portal/compose/add',
                                     portal_add_entry)

    def test_PortalList_resolves_correctly(self):
        self.correct_view_resolution('/portal/entry-list',
                                     portal_list_entries)

    def test_PortalEdit_resolves_correctly(self):
        self.correct_view_resolution('/portal/edit/update/1',
                                     portal_update_entry)

    def test_AuthorPortal_returns_correct_html(self):
        response = self.client.get('/portal')
        expected_html = render_to_string('portal-home.html')
        self.assertEqual(response.content,
                         expected_html,
                         'Author Portal rendering incorrect template')

    def test_PortalCompose_writes_entry(self):
        test_util = SkribTestUtil()

        test_author = test_util.create_authors(1)
        entry_data = {'entry_title': 'test_title',
                      'entry_content': 'test_content',
                      'entry_tldr': 'test_tldr'}

        self.client.post(
                         '/portal/compose/add',
                         data=entry_data
                         )
        self.assertEqual(Entry.objects.count(), 1)
        new_entry = Entry.objects.first()
        self.assertEqual(new_entry.title,
                         'test_title',
                         'PortalCompose not writing entry title correctly')
        self.assertEqual(new_entry.author.name,
                         test_author[0],
                         'PortalCompose not writing entry author correctly')
        self.assertEqual(new_entry.content,
                         'test_content',
                         'PortalCompose not writing entry content correctly')
        self.assertEqual(new_entry.tldr,
                         'test_tldr',
                         'PortalCompose not writing entry content correctly')

    def test_PortalUpdate_updates_entry(self):
        test_util = SkribTestUtil()

        test_author = test_util.create_authors(1)
        test_entry = test_util.create_entries(1)

        update_data = {'updated_title': 'updated title 1',
                       'updated_content': 'updated content 1',
                       'updated_tldr': 'updated tldr 1'
        }
        test_entry_id = Entry.objects.latest('id').id

        self.client.post(
                         '/portal/edit/update/' + str(test_entry_id),
                         data=update_data
                         )

        updated_entry = Entry.objects.filter(id=test_entry_id).first()
        self.assertEqual(updated_entry.title,
                         update_data['updated_title'],
                         'PortalUpdate not updating entry title')
        self.assertEqual(updated_entry.content,
                         update_data['updated_content'],
                         'PortalUpdate not updating entry content')
        self.assertEqual(updated_entry.tldr,
                         update_data['updated_tldr'],
                         'PortalUpdate not updating entry tldr')

    def test_PortalDelete_deletes_entry(self):
        test_util = SkribTestUtil()

        total_entries = len(Entry.objects.all())
        #import pdb; pdb.set_trace()

        self.assertEqual(total_entries,
                         0,
                         'Starting total entries not 0')

        test_author = test_util.create_authors(1)
        test_entry = test_util.create_entries(1)

        total_entries = len(Entry.objects.all())
        self.assertEqual(total_entries,
                         1,
                         'Entry not showing up after creation')

        response = self.client.post(
            '/portal/delete/' + str(test_entry[0]['id'])
        )

        self.assertEqual(response.status_code,
                         302,
                         'Delete entry request unsuccessful')
        total_entries = len(Entry.objects.all())
        self.assertEqual(total_entries,
                         0,
                         'PortalDelete Not Deleting Entry')


class EntryPageTest(TestCase):

    def test_does_Entry_resolve_to_correct_view(self):
        test_util = SkribTestUtil()

        test_author = test_util.create_authors(1)
        test_entry = test_util.create_entries(1)

        response = resolve('/entry/' + str(test_entry[0]['id']))
        self.assertEqual(response.func,
                         view_entry,
                         'view entry URL not resolving to view_entry')

    def test_entry_returns_correct_html(self):

        test_util = SkribTestUtil()

        test_author = test_util.create_authors(1)
        test_entry = test_util.create_entries(1)

        response = self.client.get('/entry/' + str(test_entry[0]['id']))
        expected_html = render_to_string('view-entry.html',
            {'entry': {'title': 'entry title 0', 'content': 'entry content 0',
            'tldr': 'tldr 0'}})

        self.assertEqual(response.content,
                         expected_html,
                         'ViewEntry rendering incorrect template')

class HomePageTest(TestCase):

    def test_does_HomePage_resolve_to_correct_view(self):
        response = resolve('/')
        self.assertEqual(response.func,
                         home_page,
                         'root url not resolving to home_page')

    def test_HomePage_returns_correct_html(self):
        response = self.client.get('/')
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content,
                         expected_html,
                         'Homepage rendering incorrect template')
