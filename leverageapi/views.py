from flask import Blueprint, render_template, abort, request, make_response, redirect, \
    session as flask_session, g
from leverageapi.database import db_session
from leverageapi.models import Candidate, Committee
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




@views.route('/donations_by_state_house_district/<committee_id>', methods=['GET'])
#@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=make_cache_key)
def donations_by_state_house_district(committee_id):

    boundary_json = '/static/House2012Final_tiny.json'
    api_url='/api/donations_by_state_house_district/{}'.format(committee_id)
    property_name = 'District_1'

    return render_template('map_donations.html', boundary_json=boundary_json, api_url=api_url, property_name=property_name)


@views.route('/donations_by_state_senate_district/<committee_id>', methods=['GET'])
#@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=make_cache_key)
def donations_by_state_senate_district(committee_id):

    boundary_json = '/static/FinalSenatePlan2012_tiny.json'
    api_url='/api/donations_by_state_senate_district/{}'.format(committee_id)
    property_name = 'District_1'

    return render_template('map_donations.html', boundary_json=boundary_json, api_url=api_url, property_name=property_name)


@views.route('/donations_by_zipcode/<committee_id>', methods=['GET'])
#@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=make_cache_key)
def donations_by_zipcode(committee_id):

    boundary_json = '/static/tl_2010_42_zcta510_tiny.json'
    api_url='/api/donations_by_zipcode/{}'.format(committee_id)
    property_name = 'ZCTA5CE10'

    return render_template('map_donations.html', boundary_json=boundary_json, api_url=api_url, property_name=property_name)




@views.route('/committee_summary/<committee_id>', methods=['GET'])
#@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=make_cache_key)
def committee_summary(committee_id):

    committee = db_session.query(Committee).get(committee_id)

    # Top business donors
    sql_query = """SELECT c.*, COUNT(c.id) AS num_donations, SUM(d.donation_amount) as total_amount FROM `contributor` c, political_donation d 
WHERE c.id = d.contributor_id AND c.is_business = 1 
    AND d.committee_id = {}
GROUP BY c.id
ORDER BY total_amount DESC
LIMIT 10""".format(committee_id)

    top_biz_donors = db_session.execute(sql_query)

    """    
    result_dict = {} 

    for r in results:
        print(r)
        result_dict[r.district_id] = {'district': r.district_id, 'donation_amount': round(float(r.district_amount), 2)}
    """


    return render_template('committee_summary.html', committee=committee, top_biz_donors=top_biz_donors)


@views.route('/state_house_in_district', methods=['GET'])
#@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=make_cache_key)
def state_house_in_district():

    # Top business donors
    sql_query = """SELECT DISTINCT cand.*, race.race_description, party.party_name,
    vc1.value AS total_amount, vc2.value AS in_district_amount, (vc2.value/vc1.value) AS percent_in_district
FROM political_donation d, committee comm, `candidate_committees` cand_comm, `candidate` cand, `candidacy`, `race`, party,
    `contributor`, `contributor_address`, `contributor_address_cicero_district_set` ad_set, `cicero_district`, 
    `cache_value_amount` vc1, `cache_value_amount` vc2
WHERE d.committee_id = comm.id
    AND comm.id = cand_comm.committee_id
    AND cand_comm.candidate_id = cand.id
    AND cand.id = `candidacy`.candidate_id
    AND `candidacy`.race_id = `race`.id
    AND d.contributor_id = `contributor`.id
    AND `contributor`.address_id = `contributor_address`.id
    AND `contributor_address`.id = ad_set.address_id
    AND ad_set.cicero_district_id = `cicero_district`.id
    AND `candidacy`.party_id = party.id
    AND `race`.race_name = 'REPRESENTATIVE IN THE GENERAL ASSEMBLY'
    AND `cicero_district`.district_type = 'STATE_LOWER'
    AND `race`.race_district = `cicero_district`.district_id
    AND comm.id = vc1.object_id AND vc1.object_name = 'committee' 
    AND vc1.breakdown_1 = 'donations_by_year' AND vc1.breakdown_2 = 'total'
    AND comm.id = vc2.object_id AND vc2.object_name = 'committee' 
    AND vc2.breakdown_1 = 'in_district_donations_by_year' AND vc2.breakdown_2 = 'total'
ORDER BY percent_in_district DESC"""

    results = db_session.execute(sql_query)

    candidates_in_district_percent = [dict(r) for r in results]

    for c in candidates_in_district_percent:
        c['total_amount'] = round(float(c['total_amount']), 2)
        c['in_district_amount'] = round(float(c['in_district_amount']), 2)
        c['percent_in_district'] = float(100 * c['percent_in_district'])

    print(candidates_in_district_percent)

    """    
    result_dict = {} 

    for r in results:
        print(r)
        result_dict[r.district_id] = {'district': r.district_id, 'donation_amount': round(float(r.district_amount), 2)}
   
    """


    return render_template('state_house_in_district.html', candidates_in_district_percent=candidates_in_district_percent)



@views.route('/state_senate_in_district', methods=['GET'])
#@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=make_cache_key)
def state_senate_in_district():

    # Top business donors
    sql_query = """SELECT DISTINCT cand.*, race.race_description, party.party_name,
    vc1.value AS total_amount, vc2.value AS in_district_amount, (vc2.value/vc1.value) AS percent_in_district
FROM political_donation d, committee comm, `candidate_committees` cand_comm, `candidate` cand, `candidacy`, `race`, party,
    `contributor`, `contributor_address`, `contributor_address_cicero_district_set` ad_set, `cicero_district`, 
    `cache_value_amount` vc1, `cache_value_amount` vc2
WHERE d.committee_id = comm.id
    AND comm.id = cand_comm.committee_id
    AND cand_comm.candidate_id = cand.id
    AND cand.id = `candidacy`.candidate_id
    AND `candidacy`.race_id = `race`.id
    AND d.contributor_id = `contributor`.id
    AND `contributor`.address_id = `contributor_address`.id
    AND `contributor_address`.id = ad_set.address_id
    AND ad_set.cicero_district_id = `cicero_district`.id
    AND `candidacy`.party_id = party.id
    AND `race`.race_name = 'SENATOR IN THE GENERAL ASSEMBLY'
    AND `cicero_district`.district_type = 'STATE_UPPER'
    AND `race`.race_district = `cicero_district`.district_id
    AND comm.id = vc1.object_id AND vc1.object_name = 'committee' 
    AND vc1.breakdown_1 = 'donations_by_year' AND vc1.breakdown_2 = 'total'
    AND comm.id = vc2.object_id AND vc2.object_name = 'committee' 
    AND vc2.breakdown_1 = 'in_district_donations_by_year' AND vc2.breakdown_2 = 'total'
ORDER BY percent_in_district DESC"""

    results = db_session.execute(sql_query)

    candidates_in_district_percent = [dict(r) for r in results]

    for c in candidates_in_district_percent:
        c['total_amount'] = round(float(c['total_amount']), 2)
        c['in_district_amount'] = round(float(c['in_district_amount']), 2)
        c['percent_in_district'] = float(100 * c['percent_in_district'])

    print(candidates_in_district_percent)

    """    
    result_dict = {} 

    for r in results:
        print(r)
        result_dict[r.district_id] = {'district': r.district_id, 'donation_amount': round(float(r.district_amount), 2)}
   
    """


    return render_template('state_senate_in_district.html', candidates_in_district_percent=candidates_in_district_percent)

