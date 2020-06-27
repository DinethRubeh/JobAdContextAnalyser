# JobAdContextAnalyser
Job Advertisement Context Analyser for local recruitment website topjobs.lk

### Prerequisites
Create a new virtual environment and install the dependencies from the requirements.txt file.
```
  pip install requirements.txt
```

### Run the service
To run the flask server, use the following commands:
```
  set FLASK_APP=app.py
  flask run
```
The backend server will now be running in the background. To start the frontend, use the following commands:
```
  npm install -g @angular/cli
  cd angular-frontend
  ng serve -o
```
This will open up a page in the browser and display the frontend of the service.
