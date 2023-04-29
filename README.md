# movie-fastAPI
This project is an API created with the FastAPI python framework where it has paths for obtaining, creating, updating and deleting movies with data permanence through a json. 

In order to use the project you must create a folder and install a python virtual environment with the following command:

# Linux
~~~
python3 -m venv venv
~~~

# Windows
~~~
python -m venv venv
~~~

after creating the virtual environment to activate it is the following command in the console:

# Linux
~~~
source venv/bin/activate
~~~
# Windows
~~~
source /venv/Scripts/activate
~~~

now once the virtual environment is activated you must install the required libraries for the project:

~~~
pip install -r requeriments.txt
~~~

to start the application you must be in the root of the project and run:

~~~
uvicorn main:app --reload
~~~

the reload flag is so that every change made to the code is updated in the application without the need to do it manually, and to enter to the interactive documentation is through localhost:8000/docs

and to exit the virtual environment you have to execute the following command in the console:

~~~
deactivate
~~~

I hope this project will serve as a reference in the creation of API with python.
