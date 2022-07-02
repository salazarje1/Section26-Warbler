"""Was not doing very well with testing, couldnt get tests to work. 
    So I went through the section for testing again and rewrote the tests given while 
    working though them. 

"""

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows, Likes


os.environ["DATABASE_URL"] = "postgresql:///warbler-test"


from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """Test views for messages"""

    def setUP(self):
        db.drop_all()
        db.create_all()

        self.uid = 12345
        u = User.signup("testing", "testing@text.com","password", None)
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res


    def test_message_model(self):
        """Does basic model work"""

        msg = Message(text="a test", user_id=self.uid)

        db.session.add(msg)
        db.session.commit()

        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(self.u.messages[0].text, 'a test')

    def test_message_likes(self):

        msg = Message(text='message 1', user_id=self.uid)
        msg2 = Message(text='message 2', user_id=self.uid)

        u = User.signup("Anothertest", "anothertest@text.com", 'password', None)
        uid = 67890
        u.id = uid
        db.session.add_all([msg, msg2, u])
        db.session.commit()

        u.likes.append(msg)

        db.session.commit()

        l = Likes.quey.filter(Likes.user_id == uid).all()
        self.assertEqual(len(1), 1)
        self.assertEqual(l[0].message_id, msg.id)