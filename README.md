# Blood bank
App to help people blood donors to requestors.

Setup instructions:
=> Python 3.9 required.

=> Install all the dependencies.

=> directly run main.py, then goto the following APIs, preferably use Chrome:

1. http://127.0.0.1:5000/:                                      
This opens a normal HTML page which has direct link to register page.

2. http://127.0.0.1:5000/register:                              
Fill the form that comes up to complete the registration.

3. http://127.0.0.1:5000//nearest_users/<int:user_id>/<int:d> : 
This API return a JSON with all the nearest donors available.

TODO:
Create a dependencies file to add all dependencies.
Decouple main.py so that it becomes more functional and less cluttered. 
