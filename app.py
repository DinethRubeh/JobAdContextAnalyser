import json

from flask import Flask
from flask import request
from flask_cors import CORS,cross_origin

from basic_search import get_jobs_for_key_word

jobapp = Flask(__name__)

CORS(jobapp, supports_credentials=True)
# CORS(app,  resources={r"/*": {"origins": "*"}}, supports_credentials=True, expose_headers='Authorization')

jobapp.config['CORS_HEADERS'] = 'Content-Type'

@jobapp.route('/')
def home():
    return 'Hello, this is topjobs context analyzer'

# Get all job details for the given keyword
@jobapp.route('/search/')
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def job_search():
    try:
        key_word = request.args.get('keyWord')
        # get job details related to key_word
        job_details = get_jobs_for_key_word(key_word.lower())

        return json.dumps({
            "code":0,
            "message":"success",
            "object":{
                "jobDetails":job_details
            } 
        })
    
    except Exception as e:
        return json.dumps({
            "code":-1,
            "message":str(e)
        })

# start the web scraping process and save job details
# @jobapp.route('/topjobs/scrape')
# @cross_origin(origin='*',headers=['Content-Type','Authorization'])
# def scrape_site():
#     try:
#         # scrape
#         start_process = job_wth_description()

#         return json.dumps({
#             "code":0,
#             "message":"success",
#             "object":{
#                 "scrape":start_process
#             } 
#         })
    
#     except Exception as e:
#         return json.dumps({
#             "code":-1,
#             "message":str(e)
#         })