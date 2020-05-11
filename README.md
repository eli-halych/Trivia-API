# Full Stack API - Trivia Game, version 1.0

## Functionalities
1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

## Documentation
#### Endpoints
```
GET '/categories'
GET '/categories/<category_id>/questions'
GET '/questions'
POST '/questions/search'
DELETE '/questions/<question_id>'
POST '/questions'
POST '/quizzes'
```
#### Error handlers
```
Return objects of a success status, error_code, message. Error codes.

500 Internal Server Error
{
    'success': False,
    'error_code': 500,
    'message': 'Internal Server Error'
}, 500
```
```
400 Bad Request
- Returns
{
    'success': False,
    'error_code': 400,
    'message': 'Bad Request'
}, 400
```
```
404 Not Found
- Returns
{
    'success': False,
    'error_code': 404,
    'message': 'Not Found'
}, 404
```
```
422 Unprocessable Entity
- Returns
{
    'success': False,
    'error_code': 422,
    'message': 'Unable To Process Contained Instructions In The Request'
}, 422
```
#### Endpoint descriptions
```
GET '/categories'

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Body: None
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs
 and a success status. 
{
    categories: {
                    '1' : "Science",
                    '2' : "Art",
                    '3' : "Geography",
                    '4' : "History",
                    '5' : "Entertainment",
                    '6' : "Sports"
                },
    success: True
}
```
```
GET '/categories/<category_id>/questions'

- Fetches a list of questions in a related category given by a category ID.
- Request Arguments: None
- Request Body: None
- Returns: An object containing a list of questions, total number of questions returned, current category
 and a success status.
{
    'questions': [
        {
            'answer': 'Arctic Circle', 
            'category': 3, 'difficulty': 2, 
            'id': 245, 
            'question': 'Where do polar bears live?'
        }
    ],
    'total_questions': 1,
    'current_category': None,
    'success': True
}
```
```
GET '/questions'

- Fetches a list of questions within a specified range which is a number of questions per page.
- Request Arguments: ?page=1
- Request Body: None
- Returns: An object containing a list of questions, total number of questions returned, 
current category, a list of all categories and a success status.
{
    'questions': [
        {
            'answer': 'Arctic Circle', 
            'category': 3, 'difficulty': 2, 
            'id': 245, 
            'question': 'Where do polar bears live?'
        }

    ],
    'total_questions': 1,
    'current_category': None,
    categories: {
                    '1' : "Science",
                    '2' : "Art",
                    '3' : "Geography",
                    '4' : "History",
                    '5' : "Entertainment",
                    '6' : "Sports"
                },
    'success': True
}
```
```
POST '/questions/search'

- Fetch all questions whose question containes a specified search term (case insensitive).
- Request Arguments: None
- Request Body: {'searchTerm': 'value'}
- Returns: An object containing a list of questions, total number of questions returned, current category
 and a success status.
{
    'questions': [
        {
            'answer': 'Arctic Circle', 
            'category': 3, 'difficulty': 2, 
            'id': 245, 
            'question': 'Where do polar bears live?'
        }
    ],
    'total_questions': 1,
    'current_category': None,
    'success': True
}
```
```
DELETE '/questions/<question_id>'

- Removes a question given by a question ID,
- Request Arguments: None
- Request Body: None
- Returns: success status.
{
    'success': True
}
```
```
POST '/questions'

- Create a new question.
- Request Arguments: None
- Request Body: {
                    'answer': 'Arctic Circle', 
                    'category': 3, 
                    'difficulty': 2, 
                    'question': 'Where do polar bears live?'
                }
- Returns: success status.
{
    'success': True
}
```
```
POST '/quizzes'

- Initiates a new game with questions a user didn't see before in current category if any was given.
- Request Arguments: None
- Request Body: {
                    'previous_questions': [], 
                    'quiz_category': {
                                        'id': 3,
                                        'type': 'Geography
                                     }
                }
- Returns: a question and a success status.
{  
    'question': {
                    'answer': 'Arctic Circle', 
                    'category': 3, 
                    'difficulty': 2, 
                    'question': 'Where do polar bears live?'
                },
    'success': True
}

```
