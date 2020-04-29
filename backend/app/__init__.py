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

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

    '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        formatted_categories = {category.id: category.type
                                for category in categories}

        return jsonify(formatted_categories)

    '''
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

    @app.route('/questions', methods=['GET'])
    def get_questions_paginated():
        page = request.args.get('page', 1, type=int)

        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions]

        categories = Category.query.all()
        formatted_categories = {category.id: category.type
                                for category in categories}

        return jsonify({
            'questions': formatted_questions[start:end],
            'total_questions': len(questions),
            'current_category': None,
            'categories': formatted_categories
        })

    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

    @app.route('/questions/<question_id>', methods=['DELETE'])
    def post_question(question_id):

        success = False

        try:
            question = Question.query.get(question_id)
            question.delete()
            success = True
        except:
            success = False

        return jsonify({
            'success': success
        })

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
    def delete_question():
        data = json.loads(request.data)
        success = False

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

        return jsonify({
            'success': success
        })

    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

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
            success = True
            response['questions'] = formatted_questions
            response['total_questions'] = len(formatted_questions)
        except:
            success = False
        finally:
            response['success'] = success

        return jsonify(response)

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    return app
