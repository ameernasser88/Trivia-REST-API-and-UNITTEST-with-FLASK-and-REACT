# Full Stack Trivia API Backend  
## Getting Started  
### Installing Dependencies  
#### Python 3.7  
Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment  
We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies  
Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies  
- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup  With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server  
From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:
#### Mac and Linux

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

To run the server, execute:
#### Windows

```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


## API Endpoints Documentation

### Allowed HTTPs requests :
```   
GET
POST       
DELETE   
```
### Endpoints :
```
GET 'api/categories'
GET 'api/questions'
GET 'api/categories/<category_id>/questions'
POST 'api/questions'
POST 'api/questions/search'
POST 'api/quiz'
DELETE 'api/questions/<question_id>'
```
#### GET  ---   'api/categories'
```
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```
#### GET  ---   'api/questions'
```
- Fetches a JSON object containing one Array of questions , one Array of categories , the current category , the total number of available questions .
- Request Arguments: None
- Returns: 
 1- "questions" : an array where each question in the questions array has values with keys : "id": number , "question" : String , "answer" : String , "difficulty" : number ,"category" : number (which is the category name )
 2- "categories" : an array same as GET 'api/categories
 3- "total_question" : The total number of available questions
 4- "current_category" : the name of the category of question which is null because the request is fetching all questions from all categories
{
"categories":["Science","Art","Geography","History","Entertainment","Sports"],
"current_category":null,
"questions":[{"answer":"Apollo 13","category":5,"difficulty":4,"id":2,"question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"},
..... ],
"total_questions":22
}

```
#### GET  ---   'api/categories/<category_id>/questions'
```
- same as GET ‘api/questions’ but it fetches a list of questions belonging to one category
- Request Arguments: a category id (number) provided in the request url
- Returns: 
 1- "questions" : an array where each question in the questions array has values with keys : "id": number , "question" : String , "answer" : String , "difficulty" : number ,"category" : number (which is the category name )
 2- "categories" : an array same as GET 'api/categories
 3- "total_question" : The total number of available questions
 4- "current_category" : the name of the category of question which is null because the request is fetching all questions from all categories
{
"categories":["Science","Art","Geography","History","Entertainment","Sports"],
"current_category":"Entertainment",
"questions":[{"answer":"Apollo 13","category":5,"difficulty":4,"id":2,"question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"},
..... ],
"total_questions":3
}

```
#### POST  ---   'api/questions'
```
- Fetches a JSON object containing one Array of questions , one Array of categories , the current category , the total number of available questions .
- Request Arguments: a JSON object is provided in the request body in the following format
{
"question" : "question test",
"answer" : "answer text",
"category" : number , // representing the category id
"difficulty": number  
}
- Returns: JSON object { "created": new_question.id }

```
#### POST  ---   'api/questions/search'
```
- Fetches a JSON object containing one Array of questions with question text matching the search term provided in the request body , one Array of categories , the current category , the total number of available questions .
- Request Arguments: a JSON object is provided in the request body in the following format
{
"searchTerm" : "medicine",
}
- Returns: same as GET 'api/questions' but the questions fetched match the search item in question text , or empty questions array if it doesn't match
{
"categories":["Science","Art","Geography","History","Entertainment","Sports"],
"current_category":"Entertainment",
"questions":[{"answer":"Blood","category":1,"difficulty":4,"id":22,"question":"Hematology is a branch of medicine involving the study of what?"}],
"total_questions":1
}

```
#### POST  ---   'api/quiz'
```
- Fetches one random question from a given category provided in the request body , the request body will have an array of previous questions ids in order to fetch a new question
- Request Arguments: a JSON object is provided in the request body in the following format
{
"previous_questions":[2], // array of questions ids
"quiz_category":
{"id": 4 // question category - 1
,"type":"Entertainment"
}
}
- Returns: one question object
{
"question":{"answer":"10","category":5,"difficulty":2,"id":28,"question":"What is th maximum player in among us game ?"}
}

```
#### DELETE  ---   'api/questions/<question_id>'
```
- Deletes the question of id equals thr question id provided in the url
- Request Arguments: a question id provided in the request id
}
- Returns: same as GET 'api/questions' but the questions fetched now don't include the deleted question
{
"categories":["Science","Art","Geography","History","Entertainment","Sports"],
"current_category":null,
"deleted": deleted_question_id
"questions":[{"answer":"Apollo 13","category":5,"difficulty":4,"id":2,"question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"},
..... ],
"total_questions":21
}

```
### Expected errors :
#### 404 Not Founfd
```
- happens if you try to get a resource that doesn't exist , for example if you are trying to GET questions but provide a page number that has no questions
{  
  "success": False,  
    "error": 404,  
    "message": "Not found"  
}
```
#### 400 Bad Request
```
- happens if you try to get a delete a question that doesn't exist or if you are trying to fetch a new question from the POST 'api/quiz' but all the questions have been fetched and no new question to fetch
{  
  "success": False,  
    "error": 400,  
    "message": "Not Bad Request"  
}

```
#### 422 Unprocessable Entity
```
- happens if you send a request with invalid data , for example if you sent a new question in a POST request body with invalid key value pairs
{  
  "success": False,  
    "error": 422,  
    "message": "Unprocessable Entity"  
}

```
## Testing  To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```