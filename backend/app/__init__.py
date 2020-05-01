import json
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    @app.route('/categories', methods=['GET'])
    def get_categories():
        formatted_categories = []
        success = False
        response = {
            'categories': []
        }

        try:
            categories = Category.query.all()
            formatted_categories = {category.id: category.type
                                    for category in categories}
            response['categories'] = formatted_categories
            success = True
        except:
            success = False

        response['success'] = success
        return jsonify(response)

    @app.route('/questions', methods=['GET'])
    def get_questions_paginated():
        success = False
        response = {
            'questions': [],
            'total_questions': 0,
            'current_category': None,
            'categories': []
        }

        try:
            page = request.args.get('page', 1, type=int)

            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE

            questions = Question.query.all()
            formatted_questions = [question.format() for question in questions]

            categories = Category.query.all()
            formatted_categories = {category.id: category.type
                                    for category in categories}

            response['questions'] = formatted_questions[start:end]
            response['total_questions'] = len(questions)
            response['categories'] = formatted_categories
            success = True
        except:
            success = False

        response['success'] = success
        return jsonify(response)

    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):

        success = False
        response = {}

        try:
            question = Question.query.get(question_id)
            question.delete()
            success = True
        except:
            success = False

        response['success'] = success
        return jsonify(response)

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

    @app.route('/questions', methods=['POST'])
    def post_question():
        data = json.loads(request.data)
        success = False
        response = {}

        try:
            question = Question(
                question=data['question'],
                answer=data['answer'],
                category=data['category'],
                difficulty=data['difficulty']
            )

            question.insert()

            success = True
        except:
            success = False

        response['success'] = success
        return jsonify(response)

    @app.route('/questions/search', methods=['POST'])
    def search_questions():

        data = json.loads(request.data)
        success = False
        response = {
            'questions': [],
            'total_questions': 0,
            'current_category': None
        }

        try:
            search_term = data['searchTerm']
            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            formatted_questions = [question.format() for question in questions]

            response['questions'] = formatted_questions
            response['total_questions'] = len(formatted_questions)

            success = True
        except:
            success = False

        response['success'] = success
        return jsonify(response)

    @app.route('/categories/<category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        success = False
        response = {
            'questions': [],
            'total_questions': 0,
            'current_category': None
        }

        try:

            questions = Question.query.filter(Question.category == category_id).all()
            formatted_questions = [question.format() for question in questions]

            response['questions'] = formatted_questions
            response['total_questions'] = len(formatted_questions)

            success = True
        except:
            success = False

        response['success'] = success
        return jsonify(response)

    @app.route('/quizzes', methods=['POST'])
    def post_quiz():
        data = json.loads(request.data)

        previous_questions = data['previous_questions']
        quiz_category = data['quiz_category']
        category_id = int(quiz_category['id'])

        success = False
        response = {
            'question': None
        }
        try:
            if category_id == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter(Question.category == category_id).all()

            random.shuffle(questions)

            for question in questions:
                if question.id not in previous_questions:
                    response['question'] = question.format()
                    break

            success = True
        except:
            success = False


        response['success'] = success
        return jsonify(response)

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error_code': 500,
            'message': 'Internal Server Error'
        }), 500

    return app
