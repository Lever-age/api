from flask import Blueprint, render_template, abort, request, make_response, redirect, \
    session as flask_session, g
from leverageapi.database import db_session
#from leverageapi.models import Candidate, Committee, Receipt, FiledDoc, Expenditure, D2Report
from leverageapi.cache import cache, make_cache_key, CACHE_TIMEOUT
from leverageapi.app_config import FLUSH_KEY
import sqlalchemy as sa
import json
import time
from datetime import datetime, timedelta
from itertools import groupby
from operator import attrgetter
from dateutil.parser import parse
import csv
import os

views = Blueprint('views', __name__)

@views.route('/')
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=make_cache_key)
def index():

    return render_template('index.html')

