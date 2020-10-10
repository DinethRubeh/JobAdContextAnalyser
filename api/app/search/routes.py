from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS,cross_origin

from app.search.basic_search import get_jobs_for_key_word

# Search blueprint
search = Blueprint('search', __name__)

# Health call
@search.route('/')
def home():
    return 'Hello, this is topjobs context analyzer'

# Get all job details for the given keyword (Get by default)
@search.route('/search/', methods=['GET'])   # eg. /search/?keyWord=python
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def job_search():
    try:
        key_word = request.args.get('keyWord')
        # get job details related to key_word
        job_details = get_jobs_for_key_word(key_word.lower())

        return jsonify({
            "code":0,
            "message":"success",
            "object":{
                "jobDetails":job_details
            } 
        })

    except Exception as e:
        return jsonify({
            "code":-1,
            "message":str(e)
        })