from flask import Flask, request, jsonify, abort

from app.service.crawling_linkedin import config_to_login
from ..service import CrawlingService
from .config import Config

def create_app():
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def crawling():
        company_name = request.form.get('company_name')
        if company_name is None:
            abort(400, 'A company_name is required')
        #  Todo: inject CrawlingService instead of initiate manually
        crawling_service = CrawlingService()
        apps_info = crawling_service.get_apps_info(company_name)
        return jsonify(apps_info)
    
    @app.route('/sales', methods=['GET'])
    def crawling_linkedin():
        #  Todo: inject CrawlingService instead of initiate manually
        config_to_login()
        return 'OK'

    return app
