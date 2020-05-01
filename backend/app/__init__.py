import json
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)

    # get all categories
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
            abort(422)

        response['success'] = success
        return jsonify(response)

    # get all questions
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
        except:
            success = False
            abort(400)

        try:
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
            abort(500)

        response['success'] = success
        return jsonify(response)

    # get a question by ID
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
            abort(500)

        response['success'] = success
        return jsonify(response)

    # post a question
    @app.route('/questions', methods=['POST'])
    def post_question():
        success = False
        data = {}
        response = {}

        try:
            data = json.loads(request.data)
        except:
            success = False
            abort(400)

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
            abort(422)

        response['success'] = success
        return jsonify(response)

    # search for a question
    @app.route('/questions/search', methods=['POST'])
    def search_questions():

        data = {}
        success = False
        response = {
            'questions': [],
            'total_questions': 0,
            'current_category': None
        }

        try:
            data = json.loads(request.data)
        except:
            success = False
            abort(400)

        try:
            search_term = data['searchTerm']

            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            formatted_questions = [question.format() for question in questions]

            response['questions'] = formatted_questions
            response['total_questions'] = len(formatted_questions)

            success = True
        except:
            success = False
            abort(404)

        response['success'] = success
        return jsonify(response)

    # get questions by a category ID
    @app.route('/categories/<category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        success = False
        response = {
            'questions': [],
            'total_questions': 0,
            'current_category': None
        }

        if category_id is None:
            abort(400)

        try:

            questions = Question.query.filter(Question.category == category_id).all()
            formatted_questions = [question.format() for question in questions]

            response['questions'] = formatted_questions
            response['total_questions'] = len(formatted_questions)

            success = True
        except:
            success = False
            abort(404)

        response['success'] = success
        return jsonify(response)

    # play a quiz
    @app.route('/quizzes', methods=['POST'])
    def post_quiz():
        data = {}
        success = False
        response = {
            'question': None
        }

        try:
            data = json.loads(request.data)
        except:
            success = False
            abort(400)

        previous_questions = data['previous_questions']
        quiz_category = data['quiz_category']
        category_id = int(quiz_category['id'])

        try:

            # ALL vs a specific category
            if category_id == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter(Question.category == category_id).all()

            # randomize the order of questions
            random.shuffle(questions)

            # find a new question
            for question in questions:
                if question.id not in previous_questions:
                    response['question'] = question.format()
                    break

            success = True
        except:
            success = False
            abort(500)

        response['success'] = success
        return jsonify(response)

    # error handler
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error_code': 500,
            'message': 'Internal Server Error'
        }), 500

    # error handler
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error_code': 400,
            'message': 'Bad Request'
        }), 400

    # error handler
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error_code': 404,
            'message': 'Not Found'
        }), 404

    # error handler
    @app.errorhandler(422)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error_code': 422,
            'message': 'Unable To Process Contained Instructions In The Request'
        }), 422

    return app
