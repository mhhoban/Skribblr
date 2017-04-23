from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from skribblr.models import Author, Entry
from skribblr.test_utils import SkribTestUtil
from xvfbwrapper import Xvfb

import requests

class AuthorPortalBasicFunction(LiveServerTestCase):
    fixtures = ['test_authors.yaml']

    def setUp(self):
        self.xvfb = Xvfb(width=1280, height=720)
        self.xvfb.start()
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)
        self.context = {}

    def tearDown(self):

        self.browser.quit()
        self.xvfb.stop()



    def test_can_create_an_entry_then_edit_it(self):

        # Create an author in test db for test purpose:
        test_util = SkribTestUtil()
        test_author_name = test_util.create_authors(1)
        #import pdb; pdb.set_trace()
        # Load the Author portal

        self.browser.get('localhost:8000/portal')

        # See a compose and list entries button

        compose_btn = self.browser.find_element_by_id('compose-btn')
        entries_btn = self.browser.find_element_by_id('view-entries-btn')

        self.assertTrue(compose_btn)
        self.assertTrue(entries_btn)

        # click the compose button
        compose_btn.click()

        # The compose entry page loads
        self.assertIn('Skribblr Author Portal: Compose',
                      self.browser.title,
                      'Compose button not leading to right page')

        # Then the user sees the Title, TLDR, and Content fields:
        title_field = self.browser.find_element_by_id('title-field')
        tldr_field = self.browser.find_element_by_id('tldr-field')
        content_field = self.browser.find_element_by_id('content-field')
        # The user also sees a submit button
        submit_btn = self.browser.find_element_by_id('submit-btn')



        # The user enters the data to create a new entry
        title_field.send_keys('functional test title')
        tldr_field.send_keys('functional test tldr')
        content_field.send_keys('functional test content')

        # The user saves the entry by clicking the submit button
        submit_btn.click()

        # The user is brought back to the Author portal
        self.assertIn('Skribblr Author Portal',
                      self.browser.title,
                      'User not redirecting to portal home after composing')

        compose_btn = self.browser.find_element_by_id('compose-btn')
        entries_btn = self.browser.find_element_by_id('view-entries-btn')

        # the user clicks the list entries button, then sees the previous
        # entries page

        entries_btn.click()
        self.assertIn('Previous Entries',
                      self.browser.title,
                      'Edit btn not leading to previous entries page')

        # the user sees the entry they just created in the list

        row_num = len(self.browser.find_elements_by_xpath("//div[@class='row']"))
        row = []
        edit_link = None
        for i in range(0, row_num):
            x_path_query='//div[@class="row"][' + str(i+1) + ']/div'
            row = self.browser.find_elements_by_xpath(x_path_query)
            if (row[0].text == 'functional test title'):
                edit_link = self.browser.find_element_by_xpath(
                    x_path_query + '[4]/a'
                    )
                break

        try:
            self.assertEqual('functional test title',
                          row[0].text,
                          'Test entry not in previous entries page after composing')
        except IndexError:
            self.fail('Test entry not in previous entries page after composing [index fail]')

        # The user sees an "edit" link next to their entry
        self.assertEqual('Edit',
                         row[3].text,
                         'Test entry not in previous entries page after composing')

        # The user clicks the edit entry then sees a page load with the
        # entry's title, content and tldr editable.

        edit_link.click()

        self.assertEqual(self.browser.title,
                         'Skribblr Author Portal: Edit Entry',
                         'Page Edit Page not loading')

        # Then the user sees the Title, TLDR, and Content fields ready for
        # editing:

        title_field = self.browser.find_element_by_id('title-field')
        tldr_field = self.browser.find_element_by_id('tldr-field')
        content_field = self.browser.find_element_by_id('content-field')
        # The user also sees a submit button
        submit_btn = self.browser.find_element_by_id('submit-btn')


        # The user edits the title, content, and tldr

        title_field.send_keys(' - EDITED')
        tldr_field.send_keys(' - EDITED')
        content_field.send_keys(' - EDITED')

        # and submits the changes
        submit_btn.click()


        # and is redirected to the home portal
        self.assertIn('Skribblr Author Portal',
                      self.browser.title,
                      'User not redirecting to portal home after updating')

        compose_btn = self.browser.find_element_by_id('compose-btn')
        entries_btn = self.browser.find_element_by_id('view-entries-btn')


        # and when they check the list of previous entries
        entries_btn.click()


        # they see that title has changed
        row_num = len(self.browser.find_elements_by_xpath("//div[@class='row']"))
        row = []
        view_link = None
        for i in range(0, row_num):
            x_path_query='//div[@class="row"][' + str(i+1) + ']/div'
            row = self.browser.find_elements_by_xpath(x_path_query)
            if (row[0].text == 'functional test title - EDITED'):
                view_link = self.browser.find_element_by_xpath(
                    x_path_query + '[3]/a'
                    )
                break

        self.assertEqual(row[0].text,
                         'functional test title - EDITED',
                         'entry title not updating')

        # and when they click the "view" link,

        view_link.click()

        # they see the content had changed.

        entry_tldr = self.browser.find_element_by_id('entry-tldr').text
        entry_content = self.browser.find_element_by_id('entry-content').text

        self.assertEqual(entry_tldr,
                         'functional test tldr - EDITED',
                         'functional test tldr not saving edits')
        self.assertEqual(entry_content,
                         'functional test content - EDITED',
                         'functional test content not saving edits')



        # return to the Author portal - Entries List

        self.browser.get('localhost:8000/portal/entry-list')

        # clicks the delete entry link for the entry

        row_num = len(self.browser.find_elements_by_xpath("//div[@class='row']"))
        row = []
        delete_link = None
        for i in range(0, row_num):
            x_path_query='//div[@class="row"][' + str(i+1) + ']/div'
            row = self.browser.find_elements_by_xpath(x_path_query)
            if (row[0].text == 'functional test title - EDITED'):
                delete_link = self.browser.find_element_by_xpath(
                    x_path_query + '[4]/a'
                    )
                break

        delete_link.click()

        # and see that the entry is gone

        row_num = len(self.browser.find_elements_by_xpath("//div[@class='row']"))
        row = []
        entry_title = None
        for i in range(0, row_num):
            x_path_query='//div[@class="row"][' + str(i+1) + ']/div'
            row = self.browser.find_elements_by_xpath(x_path_query)
            if (row[0].text == 'functional test title - EDITED'):
                entry_title = self.browser.find_element_by_xpath(
                    x_path_query + '[0]'
                    )
                break

        self.assertEqual(entry_title,
                         None,
                         'Entry not deleting after deletion.')
