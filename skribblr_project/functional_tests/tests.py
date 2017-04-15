from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from skribblr.models import Author, Entry
from skribblr.test_utils import SkribTestUtil
from xvfbwrapper import Xvfb

class AuthorPortalBasicFunction(LiveServerTestCase):

    def setUp(self):
        self.xvfb = Xvfb(width=1280, height=720)
        self.xvfb.start()
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
        self.xvfb.stop()

    def test_can_create_an_entry_then_edit_it(self):

        # Create an author in test db for test purpose:
        test_util = SkribTestUtil()
        test_author_name = test_util.create_authors(1)
        import pdb; pdb.set_trace()
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

        # the user clicks the list entries button

        # the user sees the entry they just created in the list

        # The user sees an "edit" link next to their entry

        # The user clicks the edit entry then sees a page load with the
        # entry's title, content and tldr editable.

        # The user edits the title, content, and tldr

        # is brought back to the Author portal

        # views page and sees edits made.
