# -*- coding: utf-8 -*-
import webapp2
import os
from google.appengine.ext.webapp.template import render
from google.appengine.api import urlfetch
import logging
import urllib
import csv


class UploadHandler(webapp2.RequestHandler):
    def get(self):
        data = {}
        template = os.path.join(os.path.dirname(__file__), 'templates/upload_from.html')
        self.response.out.write(render(template, data))


class UploadCompleteHandler(webapp2.RequestHandler):
    def post(self):
        numbers = self.request.get('myfile')

        numbers = [int(y) for y in (x.strip() for x in numbers.splitlines()) if y]

        try:
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            form_data = urllib.urlencode({"numbers": numbers})
            result = urlfetch.fetch(
                url='https://number2threeprimes.appspot.com/compute_numbers',
                payload=form_data,
                method=urlfetch.POST,
                headers=headers)

            self.response.headers['Content-Type'] = 'text/csv'
            self.response.headers['Content-Disposition'] = 'attachment; filename=numbers_with_parameters.csv'
            writer = csv.writer(self.response.out)
            for parameters in result.content.splitlines():
                writer.writerow(parameters.split(","))
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')

        data = {}
        template = os.path.join(os.path.dirname(__file__), 'templates/upload_conplete.html')
        self.response.out.write(render(template, data))


app = webapp2.WSGIApplication([
    ('/upload_form', UploadHandler),
    ('/upload_conplete', UploadCompleteHandler)
], debug=True)