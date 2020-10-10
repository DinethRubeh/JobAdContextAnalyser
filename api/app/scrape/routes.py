from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS,cross_origin

from .web_scraper import start_scrape

# Web scrape blueprint
scrape = Blueprint('scrape', __name__)

# start the web scraping process and save job details
@scrape.route('/scrape', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def scrape_site():
    try:
        # scrape
        scrape_ = start_scrape()

        return jsonify({
            "code":0,
            "message":"success",
            "object":{
                "scrape":scrape_
            } 
        })
    
    except Exception as e:
        return jsonify({
            "code":-1,
            "message":str(e)
        })