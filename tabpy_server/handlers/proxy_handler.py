import json
import logging
import requests
from tabpy.tabpy_server.handlers import BaseHandler


class ProxyHandler(BaseHandler):
    def initialize(self, app):
        super(ProxyHandler, self).initialize(app)

    def get(self,url):
        if self.should_fail_with_not_authorized():
            self.fail_with_not_authorized()
            return
        self._add_CORS_header()
        the_url = self.request.uri
        print(the_url)
        the_url = the_url.replace('/proxy/','')
        response = requests.get(the_url)
        response = json.loads(response.text)
        print(response.text)
        self.logger.log(logging.DEBUG, f"This is the url to proxy: {the_url}")
        self.write(json.dumps(response))
        self.finish()
        return
