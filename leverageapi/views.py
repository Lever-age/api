from flask import Blueprint, render_template, abort, request, make_response, redirect, \
    session as flask_session, g
from leverageapi.database import db_session
#from leverageapi.models import Candidate, Committee, Receipt, FiledDoc, Expenditure, D2Report
from leverageapi.cache import cache, make_cache_key, CACHE_TIMEOUT
from leverageapi.app_config import FLUSH_KEY, API_BASE_URL
import sqlalchemy as sa
import json
"""
import time
from datetime import datetime, timedelta
from itertools import groupby
from operator import attrgetter
from dateutil.parser import parse
import csv
import os
"""
import requests

views = Blueprint('views', __name__)

@views.route('/')
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=make_cache_key)
def races():

    api_url = '{}{}'.format(API_BASE_URL, 'races')

    #print('api url:', api_url)

    r = requests.get(api_url)

    races = json.loads(r.text)

    #print(races['metadata'])

    return render_template('races.html', api_url=api_url, races=races['data'])



@views.route('/race/<race_slug>')
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=make_cache_key)
def race(race_slug):

    api_url_race = '{}{}{}'.format(API_BASE_URL, 'races?race_slug=', race_slug)

    #print('api url:', api_url)

    r = requests.get(api_url_race)

    races = json.loads(r.text)

    race = races['data'][0]


    api_url = '{}{}{}'.format(API_BASE_URL, 'candidates?race_slug=', race_slug)

    #print('api url:', api_url)

    r = requests.get(api_url)

    candidates = json.loads(r.text)

    #print(races['metadata'])

    return render_template('race.html', api_url_race=api_url_race, api_url=api_url, race=race, candidates=candidates['data'])




@views.route('/candidate/<candidate_slug>')
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=make_cache_key)
def candidate(candidate_slug):

    api_url = '{}{}{}'.format(API_BASE_URL, 'candidates?candidate_slug=', candidate_slug)

    #print('api url:', api_url)

    r = requests.get(api_url)

    candidates = json.loads(r.text)

    candidate = candidates['data'][0]

    api_url = '{}{}{}'.format(API_BASE_URL, 'contributions?candidate_slug=', candidate_slug)

    #print('api url:', api_url)

    r = requests.get(api_url)

    contributions = json.loads(r.text)

    #print(races['metadata'])

    return render_template('candidate.html', api_url=api_url, candidate=candidate, contributions=contributions['data'])



