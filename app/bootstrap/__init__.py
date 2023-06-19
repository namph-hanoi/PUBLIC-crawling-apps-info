from flask import Flask, request, jsonify, abort
from ..service import ScrawlingService

def create_app():
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def crawling():
        company_name = request.form.get('company_name')
        if company_name is None:
            abort(400, 'A company_name is required')
        apps_info = ScrawlingService.get_apps_info(company_name)
        return jsonify(apps_info)


    return app
