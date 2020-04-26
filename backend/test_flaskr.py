import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from app import create_app, QUESTIONS_PER_PAGE
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'admin', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            engine = create_engine(self.app.config['SQLALCHEMY_DATABASE_URI'])
            if not database_exists(engine.url):
                create_database(engine.url)

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        res = self.client().get(
            '/categories'
        )
        status_code = res.status_code
        data = json.loads(res.data)

        self.assertEqual(status_code, 200)

    def test_get_questions_paginated(self):
        total_questions = len(Question.query.all())
        # total // per_page gives all full pages
        # +1 for possible not full page
        # +1 for a definite failing page
        failing_page = total_questions // QUESTIONS_PER_PAGE + 2

        # failing page number provided
        res = self.client().get(
            f'/questions?page={failing_page}'
        )
        data = json.loads(res.data)
        status_code = res.status_code

        # status code is always 200, only questions are empty
        self.assertEqual(status_code, 200)
        self.assertTrue(len(data['questions']) == 0)

    def test_post_question(self):
        request_body = {
            'question': 'Test',
            'answer': 'Answer',
            'difficulty': 4,
            'category': 1
        }
        res = self.client().post(
            '/questions',
            data=json.dumps(request_body)
        )
        status_code = res.status_code
        data = json.loads(res.data)
        # print(data)
        success = data['success']

        self.assertEqual(status_code, 200)
        self.assertTrue(success)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
