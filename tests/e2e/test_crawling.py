import re
import json
from flask import request
from ..conftest import TestBase

class TestCrawling(TestBase):

    def _find_grab_taxi_app(_, all_results):
        is_taxi_app_available = False
        grab_taxi_regex = r'^Grab: Taxi Ride'
        for result in all_results:
            if re.match(grab_taxi_regex, result['name']):
                is_taxi_app_available = True
                break
        return is_taxi_app_available

    def test_crawling_grab_apps(self):
        form_data = {
            'company_name': 'grab-com',
        }
        api_call_result = self.api_call.get("/", data=form_data)
        response_data = json.loads(api_call_result.get_data(as_text=True))

        # Notice: these assertions could be changed when Grab.com updates its apps
        assert len(response_data) == 4
        assert self._find_grab_taxi_app(response_data) == True

    def test_crawling_from_non_existing_company(self):
        form_data = {
            'company_name': 'non-existing',
        }
        api_call_result = self.api_call.get("/", data=form_data)

        assert api_call_result.status_code == 404
        assert 'company_name not found' in api_call_result.get_data(as_text=True)
