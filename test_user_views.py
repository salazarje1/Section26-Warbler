"""Was not doing very well with testing, couldnt get tests to work. 
    So I went through the section for testing again and rewrote the tests given while 
    working though them. 

"""

import os
from unittest import TestCase

from models import db, connect_db, Message, User, Likes, Follows
from bs4 import BeautifulSoup


os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class MessageViewTestCase(TestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser", email="test@test.com", password="testuser", image_url=None)
        self.testuser_id = 1234
        self.testuser.id = self.testuser_id

        self.u1 = User.signup("user1", "test1@test.com", "password", None)
        self.u1_id = 3456
        self.u1.id = self.u1_id
        self.u2 = User.signup("user2", "test2@test.com", "password", None)
        self.u2_id = 4567
        self.u2.id = self.u2_id
        self.u3 = User.signup("user3", "test3@test.com", "password", None)
        self.u4 = User.signup("user4", "test4@test.com", "password", None)

        db.session.commit()

    def test_users_index(self):
        with self.client as c:
            resp = c.get("/users")

            self.assertIn("@testuser", str(resp.data))
            self.assertIn("@user1", str(resp.data))
            self.assertIn("@user2", str(resp.data))
            self.assertIn("@user3", str(resp.data))
            self.assertIn("@testing", str(resp.data))

    def test_user_show_with_follows(self):

        self.setup_followers()

        with self.client as c:
            resp = c.get(f"/users/{self.testuser_id}")

            self.assertEqual(resp.status_code, 200)

            self.assertIn("@testuser", str(resp.data))
            soup = BeautifulSoup(str(resp.data), 'html.parser')
            found = soup.find_all("li", {"class": "stat"})
            self.assertEqual(len(found), 4)

            self.assertIn("0", found[0].text)
            self.assertIn("2", found[1].text)
            self.assertIn("1", found[2].text)
            self.assertIn("0", found[3].text)

    def test_unauthorized_following_page_access(self):
            self.setup_followers()
            with self.client as c:

                resp = c.get(f"/users/{self.testuser_id}/following", follow_redirects=True)

                self.assertEqual(resp.status_code, 200)
                self.assertNotIn("@user1", str(resp.data))
                self.assertIn("Access unauthorized", str(resp.data))