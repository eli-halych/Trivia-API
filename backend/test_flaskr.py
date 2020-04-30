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
        success = data['success']

        questions = Question.query.filter(Question.question.ilike('%Test%')).all()
        for q in questions:
            q.delete()

        self.assertEqual(status_code, 200)
        self.assertTrue(success)

    def test_delete_question(self):
        question = Question(
            question='question',
            answer='answer',
            category='1',
            difficulty='4'
        )

        question.insert()
        question_id = question.id

        res = self.client().delete(
            f'/questions/{question_id}'
        )

        status_code = res.status_code
        data = json.loads(res.data)
        success = data['success']

        question.delete()

        self.assertEqual(status_code, 200)
        self.assertTrue(success)

    def test_search_question(self):
        question = Question(
            question='dummy_question_search',
            answer='answer',
            category='1',
            difficulty='4'
        )

        question.insert()

        search_term = 'dummy_Question'
        body = {
            'searchTerm': search_term
        }
        res = self.client().post(
            f'/questions/search',
            data=json.dumps(body)
        )

        status_code = res.status_code
        data = json.loads(res.data)
        success = data['success']
        questions = data['questions']
        total_questions = data['total_questions']

        question.delete()

        self.assertEqual(status_code, 200)
        self.assertEqual(len(questions), 1)
        self.assertEqual(total_questions, 1)
        self.assertTrue(success)

    def test_get_questions_by_category(self):
        category = Category(
            type='dummy_test_category',
        )
        category.insert()

        question = Question(
            question='dummy_test_question',
            answer='answer',
            category=str(category.id),
            difficulty='4'
        )
        question.insert()

        res = self.client().get(
            f'/categories/{category.id}/questions'
        )
        status_code = res.status_code
        data = json.loads(res.data)
        questions = data['questions']
        total_questions = data['total_questions']

        question.delete()
        category.delete()

        self.assertEqual(status_code, 200)
        self.assertEqual(len(questions), 1)
        self.assertEqual(total_questions, 1)

    def test_post_quiz(self):
        # category ALL
        request_body = {
            'previous_questions': [],
            'quiz_category': {'id': 0},
        }

        res = self.client().post(
            f'/quizzes',
            data=json.dumps(request_body)
        )

        data = json.loads(res.data)

        question = data['question']
        status_code = res.status_code
        success = data['success']

        self.assertEqual(status_code, 200)
        self.assertTrue(question)
        self.assertTrue(success)



        # category 1
        request_body = {
            'previous_questions': [],
            'quiz_category': {'id': 1},
        }

        res = self.client().post(
            f'/quizzes',
            data=json.dumps(request_body)
        )

        data = json.loads(res.data)

        question = data['question']
        status_code = res.status_code
        success = data['success']

        self.assertEqual(status_code, 200)
        self.assertTrue(question)
        self.assertTrue(success)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
