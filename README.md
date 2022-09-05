# TRIVIA APP

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience were limited and still needed to be built out.

That's where I came in! I helped them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. This application:

1. Displays questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer.
2. Deletes questions.
3. Adds questions and require that the entries must include question and answer text.
4. Searches for questions based on a text query string.
5. Plays the quiz game, randomizing either all questions or within a specific category.

All backend code follows PEP8 style guidelines.

# Running This App

## Pre-requisites and Local Development

Before utilizing or running this API, developers must have installed python3, pip, and node on their local machine.

## Setting Up The Backend

### Install Dependencies

All required packages are included in the requirements file.
From the backend folder run:

```bash
pip install -r requirements.txt
```

To run the backend run the following commands:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
export FLASK_DEBUG=1 && python -m flask run
```

The first command directs the application as to where to find the main file **init**.py. The second command allows the backend to be initialized in a development environment while the third line runs our app in debugger mode; allowing for automatic refreshes or update to the viewport everytime changes are made in the code. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default.

## Setting Up The Frontend

The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

```bash
npm start
```

By default, the frontend will run on [http://localhost:3000](http://localhost:3000) which can be viewed by your browser. The page will reload if you make edits.

# API Documentation

## Getting Started

Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.

- Authentication: This version of the application does not require authentication or API keys.

## Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```

The API will return two error types when requests fail:

- 404: Resource Not Found
- 422: Not Processable

## Endpoints

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.
- Sample: `curl http://127.0.0.1:5000/categories`

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

`GET '/questions'`

- Fetches a paginated set of questions, a total number of questions, all categories.
- Request Arguments: `page` - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
- Sample: `curl http://127.0.0.1:5000/questions?page=1`

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }
  ],
  "success": true,
  "totalQuestions": 15
}
```

`DELETE '/questions/{question_id}`
Deletes a specified question using the id of the question

- Request Arguments: `question_id` - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question.
  Sample: `curl -X DELETE http://127.0.0.1:5000/questions/12`

```json
{
  "deleted": 2,
  "success": true
}
```

`POST '/questions'`

- Sends a post request in order to add a new question
- Returns the id of the success value, the new question, the answer and difficulty.

- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"question": "Why did the chicken cross the road?", "answer": "Cause it was headed to KFC", "category": 5, "difficulty": 4}' http://127.0.0.1:5000/questions`

```json
{
  "answer": "Cause it was headed to KFC",
  "difficulty": 4,
  "questions": "Why did the chicken cross the road?",
  "success": true
}
```

`POST '/questions/search'`

- Sends a post request in order to search for a specific question by search term
- Returns: success value, any array of questions, a number of total_questions that met the search term and the current category string
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Why"}' http://127.0.0.1:5000/questions`

```json
{
  "questions": [
    {
      "answer": "Cause it was headed to KFC",
      "category": 5,
      "difficulty": 4,
      "id": 26,
      "question": "Why did the chicken cross the road?"
    }
  ],
  "success": true,
  "totalQuestions": 1
}
```

`GET '/categories/{question_category}>'`
Fetches questions for a cateogry specified by id request argument

- Request Arguments: `question_category` - integer
- Returns: Sucess value, An object with questions for the specified category, total number of questions, and title of current category
- Sample: `curl http://127.0.0.1:5000/categories/2`

```json
{
  "currentCategory": "Art",
  "questions": [
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "totalQuestions": 18
}
```

`POST '/quizzes'`

- Sends a post request in order to get the next question
- Takes category and previous question parameters
  and returns success value and a random question within the given category, if provided, and that is not one of the previous questions.
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [5, 9], "quiz_category": {"type": "Art", "id": "2"}}' http://127.0.0.1:5000/quizzes`

```json
{
  "question": {
    "answer": "Mona Lisa",
    "category": 2,
    "difficulty": 3,
    "id": 17,
    "question": "La Giaconda is better known as what?"
  },
  "success": true
}
```

## Deployment N/A

## Authors

Elijah E. Igbokah

## Acknowledgements

Big thanks to the Udacity team, ALX-T programme and the amazing peers who have helped me thus far.
Also, thanks to Valentina Buoro for creating an amazing [Markdown App](https://bigteenzmarkup.netlify.app/); it really helped me alot in understanding how Markdown worked.
