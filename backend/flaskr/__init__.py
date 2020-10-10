import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS , cross_origin
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
  CORS(app, resources={r"/*": {"origins": "*"}})


  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/api/categories', methods=['GET'])
  @cross_origin()
  def get_categories():
    categories = Category.query.order_by(Category.id).all()
    formatted_categories = [category.type for category in categories]
    if len(formatted_categories) == 0:
      abort(404)
    else:
      return jsonify(
        {
          "success": True
          ,"categories":formatted_categories
          ,"total_categories":len(formatted_categories)
        }
      )


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  '''

  @app.route('/api/questions', methods=['GET'])
  @cross_origin()
  def get_questions():
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = Question.query.order_by(Question.id).all()
    formatted_questions = [question.format() for question in questions]
    categories = Category.query.order_by(Category.id).all()
    formatted_categories = [category.type for category in categories]
    if len(formatted_questions) == 0:
      abort(404)
    else:
      return jsonify(
        {
          "success": True
          , "questions": formatted_questions[start:end]
          , "total_questions": len(formatted_questions)
          , "categories": formatted_categories
          , "current_category": None
        }
      )


  '''
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
  '''

  @app.route('/api/questions', methods=['POST'])
  @cross_origin()
  def create_question():
    body = request.get_json()
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_difficulty = body.get('difficulty', None)
    new_category = body.get('category', None)
    try:
      question_item = Question(question=new_question,answer=new_answer,category=new_category,difficulty=new_difficulty)
      question_item.insert()
      return jsonify({
        "success": True
        , "created": question_item.id
      })

    except:
      abort(422)
  '''
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 
  '''

  @app.route('/api/questions/search', methods=['POST'])
  @cross_origin()
  def search_questions():
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    body = request.get_json()
    search_term = body.get('searchTerm', None)
    search_pattern = "%" + search_term + "%"
    questions = Question.query.filter(Question.question.ilike(search_pattern)).all()
    formatted_questions = [question.format() for question in questions]
    categories = Category.query.order_by(Category.id).all()
    formatted_categories = [category.type for category in categories]
    if len(formatted_questions) == 0:
      abort(404)
    else:
      return jsonify(
        {
          "success": True
          , "questions": formatted_questions[start:end]
          , "total_questions": len(formatted_questions)
          , "categories": formatted_categories
          , "current_category": None
        }
      )


  '''
  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 
  '''

  @app.route('/api/category/<category_id>/questions', methods=['GET'])
  @cross_origin()
  def get_questions_by_category(category_id):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = Question.query.filter(Question.category==category_id).order_by(Question.id).all()
    formatted_questions = [question.format() for question in questions]
    categories = Category.query.order_by(Category.id).all()
    formatted_categories = [category.type for category in categories]
    if len(formatted_questions) == 0:
      abort(404)
    else:
      return jsonify(
        {
          "success": True
          , "questions": formatted_questions[start:end]
          , "total_questions": len(formatted_questions)
          , "categories": formatted_categories
          , "current_category": Category.query.get(category_id).type
        }
      )



  '''
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

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Unprocessable Entity"
    }), 422

  return app

    