import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia-test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', os.getenv('postgres_pw'), 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def test_get_paginated_questions(self):
        res = self.client().get('api/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_paginated_questions_invalid_page(self):
        res = self.client().get('api/questions?page=10000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_post_new_question(self):
        res = self.client().post('api/questions',json={'question':"What was Tom Hanks's name in Cast Away ?", "answer":"Chuck Noland" , "difficulty":2 , "category":5})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_delete_question(self):
        question_id = Question.query.first().id
        res = self.client().delete('api/questions/'+str(question_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'],str(question_id))

    def test_400_delete_non_existing_question(self):
        res = self.client().delete('api/questions/5000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_search_questions(self):
        res = self.client().post('api/questions/search', json={"searchTerm":"Tom Hanks"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_search_questions(self):
        res = self.client().post('api/questions/search', json={"searchTerm":".@#$"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_404_paginated_questions_invalid_page(self):
        res = self.client().get('api/questions?page=10000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_questions_by_category(self):
        res = self.client().get('api/categories/5/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], "Entertainment")

    def test_404_questions_by_category(self):
        res = self.client().get('api/categories/10/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_play_quiz(self):
        res = self.client().post('api/quiz',json={"previous_questions":[],"quiz_category":{"id":4,"type":"Entertainment"}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_400_play_quiz(self):
        res = self.client().post('api/quiz',json={"previous_questions":[],"quiz_category":{"id":10,"type":"Science"}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)





    def tearDown(self):
        """Executed after reach test"""
        pass


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()