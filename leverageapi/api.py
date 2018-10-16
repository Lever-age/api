import sqlalchemy as sa
from leverageapi.database import db_session
from leverageapi.models import *
from leverageapi.cache import cache, make_cache_key, CACHE_TIMEOUT
from leverageapi.app_config import DEFAULT_RACE, DEFAULT_YEAR
from flask import Blueprint, render_template, request, make_response, g, abort
import json
from datetime import datetime, date
from collections import OrderedDict
from operator import attrgetter, itemgetter
from itertools import groupby
from string import punctuation
import re
import sqlalchemy as sa
from io import StringIO, BytesIO
import csv
import zipfile

api = Blueprint('api', __name__)

dthandler = lambda obj: obj.isoformat() if isinstance(obj, date) else None

operator_lookup = {
    'ge': '>=',
    'gt': '>',
    'le': '<=',
    'lt': '<'
}

def return_amount_donated_from_race_id(race_id):

    """

    """
    donations = db_session.query(PoliticalDonation)\
        .join(PoliticalDonation.committee)\
        .join(Committee.candidates)\
        .join(Candidate.candidacies)\
        .join(PoliticalDonation.contribution_type)\
        .filter(PoliticalDonationContributionType.is_donation==1)\
        .filter(Candidacy.race_id==race_id)

    #print (donations)

    #for d in donations:
    #    #print(dir(d.donation_amount))
    #    print(d.donation_amount, float(d.donation_amount))

    #print([d.donation_amount for d in donations])

    return sum([float(d.donation_amount) for d in donations])

def return_error(message):

    resp = {
        'status': 'error',
        'message': message,
        'meta': {},
        'objects': {},
    }
    status_code = 400
    valid = False

    response_str = json.dumps(resp, sort_keys=False, default=dthandler)
    response = make_response(response_str, status_code)
    response.headers['Content-Type'] = 'application/json'

    return response

@api.route('/races', methods=['GET'])
#@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=make_cache_key)
def races():

    #print('In races')

    if 'election_type' in request.args:
        election_type = request.args['election_type']
    else:
        election_type = DEFAULT_RACE

    if 'election_year' in request.args:
        election_year = request.args['election_year']
    else:
        election_year = DEFAULT_YEAR

    # If race_id is in request.args, only return that race
    if 'race_id' in request.args:
        races = db_session.query(Race)\
            .filter(Race.id==request.args['race_id'])

    elif 'race_slug' in request.args:
        races = db_session.query(Race)\
            .filter(Race.slug==request.args['race_slug'])

    else:

        races = db_session.query(Race)\
            .filter(Race.election_type==election_type)\
            .filter(Race.election_year==election_year)

    #print (races)

    objs = []

    for r in races:

        #donations_2016 = sum([(sum([float(c.donations_2016)]) for c in cands.candidate.committees) for cands in r.candidacies])
        #donations_2017 = sum([(sum([float(c.donations_2017)]) for c in cands.candidate.committees) for cands in r.candidacies])

        """
        donations_2016 = 0
        donations_2017 = 0
        donations_in_philly = 0
        donations_in_pa = 0
        donations_out_pa = 0

        for cands in r.candidacies:
            for c in cands.candidate.committees:
                #print (c.id, c.donations_2017)
                donations_2016 += float(c.donations_2016)
                donations_2017 += float(c.donations_2017)
                donations_in_philly += float(c.donations_in_philly)
                donations_in_pa += float(c.donations_in_pa)
                donations_out_pa += float(c.donations_out_pa)

        donations_2016 = round(donations_2016, 2)
        donations_2017 = round(donations_2017, 2)
        donations_in_philly = round(donations_in_philly, 2)
        donations_in_pa = round(donations_in_pa, 2)
        donations_out_pa = round(donations_out_pa, 2)
        """

        #donations_2016 = round(sum([float(c.donations_2016) for c in cands.candidate.committees for cands in r.candidacies]), 2)
        #donations_2017 = round(sum([float(c.donations_2017) for c in cands.candidate.committees for cands in r.candidacies]), 2)
        #donations_2017 = sum([(float(c.donations_2017) for c in cands.candidate.committees) for cands in r.candidacies])
        #donations_2017 = 0

        race = r.as_dict()

        cache_values = r.sum_committee_cache_value_amounts_dict()
        
        for breakdown1 in cache_values:
            race[breakdown1] = cache_values[breakdown1]

        race['num_candidates'] = len(r.candidacies)
        #race['total_money_donated'] = round(donations_2016 + donations_2017, 2)
        #race['total_money_donated_by_year'] = {2016: donations_2016, 2017: donations_2017}
        #race['donations_by_year'] = r.aggregate_race_cache_value_amounts_dict('donations_by_year')
        #race['total_money_in_philly'] = donations_in_philly
        #race['total_money_out_philly'] = round(donations_2016 + donations_2017 - donations_in_philly, 2)
        #race['total_money_in_pa'] = donations_in_pa
        #race['total_money_out_pa'] = donations_out_pa 
        #race['total_money_spent'] = 0
        race['top_donors'] = {}

        objs.append(race)

    resp = {}
    resp['metadata'] = {}
    resp['data'] = objs
    """
    resp['meta']['query'] = {
        'limit': limit,
        'offset': offset,
        'sort_order': sort_order,
        'order_by': order_by,
    })

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    """

    response_str = json.dumps(resp, sort_keys=False, default=dthandler)
    response = make_response(response_str, 200)
    response.headers['Content-Type'] = 'application/json'
    # response.headers['Access-Control-Allow-Origin'] = '*'

    return response


@api.route('/candidates', methods=['GET'])
#@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=make_cache_key)
def candidates():

    if 'race_id' in request.args:
        race_id = request.args['race_id']

        candidates = db_session.query(Candidate)\
            .join(Candidate.candidacies)\
            .filter(Candidacy.race_id==race_id)

    elif 'race_slug' in request.args:

        candidates = db_session.query(Candidate)\
            .join(Candidate.candidacies)\
            .join(Candidacy.race)\
            .filter(Race.slug==request.args['race_slug'])

    elif 'candidate_id' in request.args:
        candidate_id = request.args['candidate_id']

        candidates = db_session.query(Candidate)\
            .join(Candidate.candidacies)\
            .filter(Candidate.id==candidate_id)

    elif 'candidate_slug' in request.args:

        candidates = db_session.query(Candidate)\
            .join(Candidate.candidacies)\
            .filter(Candidate.slug==request.args['candidate_slug'])

    else:
        return return_error('Either race_slug, race_id, candidate_slug, or candidate_id must be sent to candidates endpoint.')


    #print (races)

    objs = []

    for c in candidates:

        """
        donations_2016 = round(float(c.primary_committee().donations_2016), 2)
        donations_2017 = round(float(c.primary_committee().donations_2017), 2)
        donations_in_philly = round(float(c.primary_committee().donations_in_philly), 2)
        donations_in_pa = round(float(c.primary_committee().donations_in_pa), 2)
        donations_out_pa = round(float(c.primary_committee().donations_out_pa), 2)
        """

        candidate = c.as_dict()

        #candidate['total_money_donated'] = round(donations_2016 + donations_2017, 2)

        cache_values = c.cache_value_amounts_dict()

        for breakdown1 in cache_values:
            candidate[breakdown1] = cache_values[breakdown1]


        #candidate['total_money_donated_by_year'] = {2016: donations_2016, 2017: donations_2017}

        #candidate['donations_by_year'] = c.aggregate_committee_cache_value_amounts_dict('donations_by_year')
        #candidate['in_district_donations_by_year'] = c.aggregate_committee_cache_value_amounts_dict('in_district_donations_by_year')
        #candidate['in_pa_donations_by_year'] = c.aggregate_committee_cache_value_amounts_dict('in_pa_donations_by_year')
        #candidate['out_of_pa_donations_by_year'] = c.aggregate_committee_cache_value_amounts_dict('out_of_pa_donations_by_year')

        """
        candidate['total_money_in_philly'] = donations_in_philly
        candidate['total_money_out_philly'] = round(donations_2016 + donations_2017 - donations_in_philly , 2) 
        candidate['total_money_in_pa'] = donations_in_pa
        candidate['total_money_out_pa'] = donations_out_pa     
        candidate['total_money_spent'] = 0
        #candidate['previous_races'] = {}
        """

        #for comm in c.committees:
        #    print(comm.donations_2015, comm.donations_2016, comm.donations_2017)

        objs.append(candidate)

    resp = {}
    resp['metadata'] = {}
    resp['data'] = objs
    """
    resp['meta']['query'] = {
        'limit': limit,
        'offset': offset,
        'sort_order': sort_order,
        'order_by': order_by,
    })

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    """

    response_str = json.dumps(resp, sort_keys=False, default=dthandler)
    response = make_response(response_str, 200)
    response.headers['Content-Type'] = 'application/json'
    # response.headers['Access-Control-Allow-Origin'] = '*'

    return response




@api.route('/contributions', methods=['GET'])
#@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=make_cache_key)
def contributions():

    if 'race_id' in request.args:
        race_id = request.args['race_id']

        candidates = db_session.query(Candidate)\
            .join(Candidate.candidacies)\
            .filter(Candidacy.race_id==race_id)

    elif 'race_slug' in request.args:

        candidates = db_session.query(Candidate)\
            .join(Candidate.candidacies)\
            .join(Candidacy.race)\
            .filter(Race.slug==request.args['race_slug'])

    elif 'candidate_id' in request.args:
        candidate_id = request.args['candidate_id']

        candidates = db_session.query(Candidate)\
            .join(Candidate.candidacies)\
            .filter(Candidate.id==candidate_id)

    elif 'candidate_slug' in request.args:

        candidates = db_session.query(Candidate)\
            .join(Candidate.candidacies)\
            .filter(Candidate.slug==request.args['candidate_slug'])

    else:
        return return_error('Either race_slug, race_id, candidate_slug, or candidate_id must be sent to candidates endpoint.')


    """
    donations_2016 = 0
    donations_2017 = 0
    donations_in_philly = 0
    donations_in_pa = 0
    donations_out_pa = 0

    for cands in candidates:
        for c in cands.committees:
            #print (c.id, c.donations_2017)
            donations_2016 += round(float(c.donations_2016), 2)
            donations_2017 += round(float(c.donations_2017), 2)
            donations_in_philly += round(float(c.donations_in_philly), 2)
            donations_in_pa += round(float(c.donations_in_pa), 2)
            donations_out_pa += round(float(c.donations_out_pa), 2)

    donations_in_philly = round(donations_in_philly, 2)
    """

    #print (races)

    obj = {}
    #obj['total_money_donated'] = round(donations_2016 + donations_2017, 2)
    #obj['total_money_donated_by_year'] = {2016: donations_2016, 2017: donations_2017}
    #obj['total_money_in_philly'] = donations_in_philly
    #obj['total_money_out_philly'] = round(donations_2016 + donations_2017 - donations_in_philly, 2)
    #obj['total_money_in_pa'] = donations_in_pa
    #obj['total_money_out_pa'] = donations_out_pa
    #obj['total_money_spent'] = 0
    obj['top_donors'] = {}
    obj['donations_by_zipcode'] = {}
    obj['donations_by_ward'] = {}

    #obj['cache_values'] = r.sum_committee_cache_value_amounts_dict()


    resp = {}
    resp['metadata'] = {}
    resp['data'] = obj

    response_str = json.dumps(resp, sort_keys=False, default=dthandler)
    response = make_response(response_str, 200)
    response.headers['Content-Type'] = 'application/json'
    # response.headers['Access-Control-Allow-Origin'] = '*'

    return response



@api.route('/donations_by_state_house_district/<committee_id>', methods=['GET'])
#@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=make_cache_key)
def donations_by_state_house_district(committee_id):

    sql_query = """SELECT cd.district_type, cd.district_id, SUM(d.donation_amount) AS district_amount 
FROM `cicero_district` cd, `contributor_address_cicero_district_set` ad_set, `contributor_address`, 
    `contributor`, political_donation d
WHERE d.contributor_id = `contributor`.id
        AND `contributor`.address_id = `contributor_address`.id
        AND `contributor_address`.id = ad_set.address_id
        AND ad_set.cicero_district_id = cd.id
        AND cd.district_type = 'STATE_LOWER'
        AND d.committee_id = {}
GROUP BY cd.district_type, cd.district_id
ORDER BY district_amount DESC""".format(committee_id)

    results = db_session.execute(sql_query)
    
    result_dict = {} 

    for r in results:
        print(r)
        result_dict[r.district_id] = {'district': r.district_id, 'donation_amount': round(float(r.district_amount), 2)}


    resp = {}
    resp['metadata'] = {}
    resp['data'] = result_dict

    response_str = json.dumps(resp, sort_keys=False, default=dthandler)
    response = make_response(response_str, 200)
    response.headers['Content-Type'] = 'application/json'
    # response.headers['Access-Control-Allow-Origin'] = '*'

    return response


