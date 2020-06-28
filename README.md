# JobAdContextAnalyser
Job Advertisement Context Analyser for local recruitment website topjobs.lk

### Prerequisites
Create a new virtual environment and install the dependencies from the requirements.txt file.
```
  pip install -r requirements.txt
```

### Run the service
To run the flask server, use the following commands:
```
  set FLASK_APP=app.py
  flask run
```
The backend server will now be running in the background. To start the frontend, use the following commands:
```
  cd angular-frontend
  ng serve -o
```
This will open up a page in the browser and display the frontend of the service.

If you have not installed Angular CLI, follow [these instructions](https://angular.io/guide/setup-local) and try to run the frontend again.
