from multiprocessing import current_process
import os
import re
from unicodedata import category
from unittest import result
from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    db = SQLAlchemy(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    -DONE
    """
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    -DONE
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    -DONE!!!
    """
    @app.route('/categories')
    def get_categories():
        try:
            categories = Category.query.all()

            # Format categories in the right way
            cat_dict = {}
            for category in categories:
                cat_dict[category.id] = category.type

            return jsonify({
                'success': True,
                'categories': cat_dict
            })

        except:
            abort(404)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    -DONE
    """
    @app.route('/questions')
    def get_questions():
        try:
            selection = Question.query.order_by(Question.id).all()
            questions_formatted = [question.format for question in selection]
            categories = Category.query.order_by(Category.id).all()
            cat_dict = {}
            for category in categories:
                cat_dict[category.id] = category.type

            current_questions = paginate_questions(request, selection)

            if len(current_questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'totalQuestions': len(questions_formatted),
                'categories': cat_dict,
                # 'currentCategory': currentCategory
            })
        except:
            abort(404)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    -DONE!!!
    """

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        # filter out question to be deleted
        try:
            question = Question.query.filter(
                question_id == Question.id).one_or_none()
            if question == None:
                abort(404)
            else:
                question.delete()
                # questions = Question.query.all()
                # formatted_question = [question.format()
                #                       for question in questions]
                return jsonify({
                    'success': True,
                    'deleted': question.id,
                    # 'questions': formatted_question,
                    # 'total_questions': len(formatted_question)
                })
        except:
            # db.session.rollback()
            # flash('An error occurred. Venue ' +
            #       question.id + ' could not be deleted.')
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    -DONE!!!
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)

        try:
            new_entry = Question(question=new_question, answer=new_answer,
                                 difficulty=new_difficulty, category=new_category)

            new_entry.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'questions': new_question,
                'answer': new_answer,
                'difficulty': new_difficulty
            })
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    -DONE!!!
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        try:
            body = request.get_json()
            searchTerm = body.get('searchTerm')
            selection = Question.query.filter(
                Question.question.ilike(f'%{searchTerm}%')).all()

            selection_formatted = [result.format() for result in selection]
            # search_results = []
            # for i in selection:
            #     search_results.append({
            #         'id': i.id,
            #         'question': i.question,
            #         'answer': i.answer,
            #         'category': i.category,
            #         'difficulty': i.difficulty
            #     })
            if len(selection_formatted) == 0:
                return abort(404)

            return jsonify({
                'success': True,
                'questions': selection_formatted,
                'totalQuestions': len(selection_formatted)
                # 'currentCategory': result.current_category
            })

        except:
            abort(404)
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    -DONE!!!
    """
    @app.route('/categories/<int:category_id>')
    def get_questions_by_cat(category_id):
        try:
            currentCategory = Category.query.filter(
                category_id == Category.id).one_or_none()
            if currentCategory == None:
                abort(404)
            else:
                totalQuestions = db.session.query(Question).all()
                questions_query = Question.query.filter(
                    Question.category == category_id).order_by(Question.id).all()
                questions = [question.format() for question in questions_query]
                print(questions)
                # else:
                #     table_join = db.session.query(Category, Question).join(
                #         Question, Category.id == Question.category).order_by(Question.id).all()
                return jsonify({
                    'success': True,
                    'questions': questions,
                    'totalQuestions': len(totalQuestions),
                    'currentCategory': currentCategory.type})
        except:
            abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    -DONE!!!
    """

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            body = request.get_json()

            quiz_category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')

            current_category = quiz_category['id']
            if current_category == 0:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter(Question.id.notin_(previous_questions),
                                                  current_category == Question.category).all()

            if len(questions) >= 1:
                question = random.choice(questions)

            return jsonify({
                'success': True,
                'question': question.format()
            })
        except:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    -DONE!!!
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                'success': False,
                'error': 404,
                'message': 'resource not found'
            }), 404
        )

    @app.errorhandler(422)
    def unprocessed(error):
        return (
            jsonify({
                'success': False,
                'error': 422,
                'message': 'error in processing request'
            }), 422
        )

    return app
