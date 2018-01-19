# -*- coding: utf-8 -*-
import webapp2
import os
from google.appengine.ext.webapp.template import render
import logging
from compute_functions import represent_as_3primes, rwh_primes2
import json


class ComputeNumbersHandler(webapp2.RequestHandler):
    def post(self):
        numbers = [int(i) for i in json.loads(self.request.get('numbers'))]
        primes = set(rwh_primes2(max(numbers)))
        for number in numbers:
            is_prime = number in primes
            if not is_prime and number > 20:
                res1, res2 = represent_as_3primes(number, primes)
                self.response.out.write("{},{},{},{}\n".format(number,
                                                                 str(is_prime).upper(),
                                                                 "+".join([str(j) for j in res1]),
                                                                 "+".join([str(j) for j in res2])))
            else:
                self.response.out.write("{},{}\n".format(number, str(is_prime).upper()))


app = webapp2.WSGIApplication([
    ('/compute_numbers', ComputeNumbersHandler)
], debug=True)