from flask import Blueprint, render_template, abort, request, make_response, redirect, session, g
from leverageapi.database import db_session
from leverageapi.models import Candidate, Committee, Party
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

    commitee = db_session.query(Committee).get(committee_id)
    candidate_name = commitee.candidates[0].name_first + ' ' + commitee.candidates[0].name_last

    return render_template('map_donations.html', boundary_json=boundary_json, api_url=api_url, property_name=property_name,
        hover_description='state house district', map_title='Map of donations to {} by PA State House District'.format(candidate_name))


@views.route('/donations_by_state_senate_district/<committee_id>', methods=['GET'])
#@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=make_cache_key)
def donations_by_state_senate_district(committee_id):

    boundary_json = '/static/FinalSenatePlan2012_tiny.json'
    api_url='/api/donations_by_state_senate_district/{}'.format(committee_id)
    property_name = 'District_1'

    commitee = db_session.query(Committee).get(committee_id)
    candidate_name = commitee.candidates[0].name_first + ' ' + commitee.candidates[0].name_last

    return render_template('map_donations.html', boundary_json=boundary_json, api_url=api_url, property_name=property_name,
        hover_description='state senate district', map_title='Map of donations to {} by PA State Senate District'.format(candidate_name))


@views.route('/donations_by_zipcode/<committee_id>', methods=['GET'])
#@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=make_cache_key)
def donations_by_zipcode(committee_id):

    boundary_json = '/static/tl_2010_42_zcta510_tiny.json'
    api_url='/api/donations_by_zipcode/{}'.format(committee_id)
    property_name = 'ZCTA5CE10'

    commitee = db_session.query(Committee).get(committee_id)
    candidate_name = commitee.candidates[0].name_first + ' ' + commitee.candidates[0].name_last

    return render_template('map_donations.html', boundary_json=boundary_json, api_url=api_url, property_name=property_name,
        hover_description='zipcode', map_title='Map of donations to {} by zipcode'.format(candidate_name))




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




@views.before_request
def before_request():

    session['filter'] = {}

    if 'look_at' in request.args:
        #print ('Found segment')
        session['filter']['look_at'] = request.args['look_at']
    else:
        session['filter']['look_at'] = 'overall'

    session['filter']['look_at_display'] = ' '.join(session['filter']['look_at'].split('_')).title().replace(' Pa', ' PA')

    if 'party' in request.args:
        #print ('Found segment')
        session['filter']['party'] = int(request.args['party'])
    else:
        session['filter']['party'] = 0

    if 'district' in request.args:
        #print ('Found segment')
        session['filter']['district'] = int(request.args['district'])
    else:
        session['filter']['district'] = 0

    if 'min_total' in request.args:
        #print ('Found segment')
        session['filter']['min_total'] = request.args['min_total']
    else:
        session['filter']['min_total'] = ''

    if 'max_total' in request.args:
        #print ('Found segment')
        session['filter']['max_total'] = request.args['max_total']
    else:
        session['filter']['max_total'] = ''

    if 'num_candidates' in request.args:
        #print ('Found segment')
        session['filter']['num_candidates'] = int(request.args['num_candidates'])
    else:
        session['filter']['num_candidates'] = 0

def my_median(a_list):
    my_list = a_list.copy()
    my_list.sort()
    if (len(my_list) % 2) != 0:
        middle_index = len(my_list)//2
        return my_list[middle_index]
    else:
        larger_index = len(my_list)//2
        smaller_index = larger_index - 1
        return (my_list[larger_index] + my_list[smaller_index]) / 2
        

"""
    sql_query = ""SELECT DISTINCT cand.*, race.race_description, party.party_name,
    vc1.value AS total_amount, vc2.value AS total_in_district_amount, (vc2.value/vc1.value) AS percent_in_district, 
    vc3.value AS count_donations, vc4.value AS count_donations_in_district, (vc4.value/vc3.value) AS percent_count_in_district, 
    vc5.value AS total_in_pa_amount, vc6.value AS count_donations_in_pa, (vc5.value/vc1.value) AS percent_in_pa,
    (vc6.value/vc3.value) AS percent_count_in_pa
FROM political_donation d, committee comm, `candidate_committees` cand_comm, `candidate` cand, `candidacy`, `race`, party,
    `contributor`, `contributor_address`, `contributor_address_cicero_district_set` ad_set, `cicero_district`, 
    `cache_value_amount` vc1, `cache_value_amount` vc2, `cache_value_amount` vc3, `cache_value_amount` vc4, 
    `cache_value_amount` vc5, `cache_value_amount` vc6
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
    AND `race`.race_name = '{}'
    AND `cicero_district`.district_type = '{}'
    AND `race`.race_district = `cicero_district`.district_id
    AND comm.id = vc1.object_id AND vc1.object_name = 'committee' 
    AND vc1.breakdown_1 = 'donations_by_year' AND vc1.breakdown_2 = 'total'
    AND comm.id = vc2.object_id AND vc2.object_name = 'committee' 
    AND vc2.breakdown_1 = 'in_district_donations_by_year' AND vc2.breakdown_2 = 'total'

    AND comm.id = vc3.object_id AND vc3.object_name = 'committee' 
    AND vc3.breakdown_1 = 'count_donations_by_year' AND vc3.breakdown_2 = 'total'

    AND comm.id = vc4.object_id AND vc4.object_name = 'committee' 
    AND vc4.breakdown_1 = 'in_district_count_donations_by_year' AND vc4.breakdown_2 = 'total'

    AND comm.id = vc5.object_id AND vc5.object_name = 'committee' 
    AND vc5.breakdown_1 = 'in_pa_donations_by_year' AND vc5.breakdown_2 = 'total'

    AND comm.id = vc6.object_id AND vc6.object_name = 'committee' 
    AND vc6.breakdown_1 = 'in_pa_count_donations_by_year' AND vc6.breakdown_2 = 'total'

    AND {}
    ORDER BY percent_in_district DESC"".format(race_race_name, cicero_district_type, ' AND '.join(additional_where_sql_list))
"""

def donation_table(candidate_type, race_race_name, cicero_district_type, districts, action_url, map_url):

    additional_where_sql_list = ['1']

    description = 'Basic stats for PARTY candidates running for the PA {} NUM_CANDS'.format(candidate_type)

    if session['filter']['party'] > 0:
        additional_where_sql_list.append('`candidacy`.party_id = {}'.format(session['filter']['party']))
        party = db_session.query(Party).get(session['filter']['party'])
        description = description.replace('PARTY', party.party_name)
    else:
        description = description.replace('PARTY', 'all')

    if session['filter']['min_total']:
        additional_where_sql_list.append('d.party_id = {}'.format(session['filter']['min_total']))

    if session['filter']['max_total']:
        additional_where_sql_list.append('d.party_id = {}'.format(session['filter']['max_total']))

    if session['filter']['num_candidates'] > 0:
        additional_where_sql_list.append('`race`.num_candidates = {}'.format(session['filter']['num_candidates']))
        if session['filter']['num_candidates'] == 1:
            description = description.replace('NUM_CANDS', 'where only one candidate is running')
        else:
            description = description.replace('NUM_CANDS', 'where {} candidates are running'.format(session['filter']['num_candidates']))
    else:
        description = description.replace('NUM_CANDS', '')

    if session['filter']['district'] > 0:
        additional_where_sql_list.append('`race`.race_district = {}'.format(session['filter']['district']))
        description = description.replace('DISTRCT', 'in district number {}'.format(session['filter']['district']))

    else:
        description = description.replace('DISTRCT', '')

    description = description.strip()

    print('additional_where_sql_list:', additional_where_sql_list)



    # Top business donors
    sql_query = """SELECT DISTINCT cand.*, comm.id AS 'committee_id', race.race_description, party.party_name,
    vc1.value AS total_amount, vc2.value AS total_in_district_amount, (vc2.value/vc1.value) AS percent_in_district, 
    vc3.value AS count_donations, vc4.value AS count_donations_in_district, (vc4.value/vc3.value) AS percent_count_in_district 

FROM political_donation d, committee comm, `candidate_committees` cand_comm, `candidate` cand, `candidacy`, `race`, party,
    `cache_value_amount` vc1, `cache_value_amount` vc2, `cache_value_amount` vc3, `cache_value_amount` vc4
WHERE d.committee_id = comm.id
    AND comm.id = cand_comm.committee_id
    AND cand_comm.candidate_id = cand.id
    AND cand.id = `candidacy`.candidate_id
    AND `candidacy`.race_id = `race`.id

    AND `candidacy`.party_id = party.id
    AND `race`.race_name = '{}'

    AND comm.id = vc1.object_id AND vc1.object_name = 'committee' 
    AND vc1.breakdown_1 = 'donations_by_year' AND vc1.breakdown_2 = 'total'
    AND comm.id = vc2.object_id AND vc2.object_name = 'committee' 
    AND vc2.breakdown_1 = 'in_district_donations_by_year' AND vc2.breakdown_2 = 'total'

    AND comm.id = vc3.object_id AND vc3.object_name = 'committee' 
    AND vc3.breakdown_1 = 'count_donations_by_year' AND vc3.breakdown_2 = 'total'

    AND comm.id = vc4.object_id AND vc4.object_name = 'committee' 
    AND vc4.breakdown_1 = 'in_district_count_donations_by_year' AND vc4.breakdown_2 = 'total'

    AND {}
    ORDER BY percent_in_district DESC""".format(race_race_name, ' AND '.join(additional_where_sql_list))

    """
    `contributor`, `contributor_address`, `contributor_address_cicero_district_set` ad_set, `cicero_district`, 

    AND d.contributor_id = `contributor`.id
    AND `contributor`.address_id = `contributor_address`.id
    AND `contributor_address`.id = ad_set.address_id
    AND ad_set.cicero_district_id = `cicero_district`.id

    AND `cicero_district`.district_type = '{}'
    AND `race`.race_district = `cicero_district`.district_id

    ORDER BY percent_in_district DESC"".format(race_race_name, cicero_district_type, ' AND '.join(additional_where_sql_list))

    """

    #print(sql_query); return

    results = db_session.execute(sql_query)

    candidates_in_district_percent = [dict(r) for r in results]

    total_amounts = []
    in_district_amounts = []
    count_donations = []
    count_donations_in_district = []

    """
    in_pa_amounts = []
    count_donations_in_pa = []
    """


    for c in candidates_in_district_percent:

        if not c['count_donations']:
            c['count_donations'] = 0

        if not c['count_donations_in_district']:
            c['count_donations_in_district'] = 0

        c['total_amount'] = int(round(float(c['total_amount']), 2))
        c['count_donations'] = int(c['count_donations'])
        c['avg_donation'] = int(round(c['total_amount']/c['count_donations'], 2))

        c['total_in_district_amount'] = int(round(float(c['total_in_district_amount']), 2))
        c['percent_in_district'] = int(float(100 * c['percent_in_district']))

        c['count_donations_in_district'] = int(c['count_donations_in_district'])
        c['percent_count_in_district'] = int(float(100 * c['percent_count_in_district']))

        c['avg_in_district_donation'] = int(round(c['total_in_district_amount']/c['count_donations_in_district'], 2))

        """
        c['total_in_pa_amount'] = round(float(c['total_in_pa_amount']), 2)
        c['percent_in_pa'] = float(100 * c['percent_in_pa'])

        c['count_donations_in_pa'] = int(c['count_donations_in_pa'])
        c['percent_count_in_pa'] = float(100 * c['percent_count_in_pa'])

        c['avg_in_pa_donation'] = round(c['total_in_pa_amount']/c['count_donations_in_pa'], 2)
        """


        total_amounts.append(c['total_amount'])
        in_district_amounts.append(c['total_in_district_amount'])
        count_donations.append(c['count_donations'])
        count_donations_in_district.append(c['count_donations_in_district'])

        """
        in_pa_amounts.append(c['total_in_pa_amount'])
        count_donations_in_pa.append(c['count_donations_in_pa'])
        """



    # "${:,.0f}".format(value).

    if len(total_amounts):
        avg_amount = "${:,.0f}".format(round(sum(total_amounts)/len(total_amounts), 2))
    else:
        avg_amount = 0

    avg_in_dist_amount = "${:,.0f}".format(round(sum(in_district_amounts)/len(in_district_amounts), 2))
    avg_count_of_donations = "{:,.0f}".format(round(sum(count_donations)/len(count_donations), 2))
    avg_count_of_in_district_donations = "{:,.0f}".format(round(sum(count_donations_in_district)/len(count_donations_in_district), 2))

    avg_donation = "${:,.0f}".format(round((sum(total_amounts)/len(total_amounts))/(sum(count_donations)/len(count_donations)), 2))
    avg_in_district_donation = "${:,.0f}".format(round((sum(in_district_amounts)/len(in_district_amounts))/(sum(count_donations_in_district)/len(count_donations_in_district)), 2))

    median_amount = "${:,.0f}".format(my_median(total_amounts))
    median_in_dist_amount = "${:,.0f}".format(my_median(in_district_amounts))

    percent_count_in_district = "{:,.0f}".format(round(100 * (sum(count_donations_in_district)/len(count_donations_in_district))/(sum(count_donations)/len(count_donations)), 2))
    percent_amount_in_district = "{:,.0f}".format(round(100 * (sum(in_district_amounts)/len(in_district_amounts))/(sum(total_amounts)/len(total_amounts)), 2))

    # Include in PA
    """
    avg_in_pa_amount = "${:,.0f}".format(round(sum(in_pa_amounts)/len(in_pa_amounts), 2))
    avg_count_of_in_pa_donations = "{:,.0f}".format(round(sum(count_donations_in_pa)/len(count_donations_in_pa), 2))
    avg_in_pa_donation = "${:,.0f}".format(round((sum(in_pa_amounts)/len(in_pa_amounts))/(sum(count_donations_in_pa)/len(count_donations_in_pa)), 2))
    median_in_pa_amount = "${:,.0f}".format(my_median(in_pa_amounts))
    percent_count_in_pa = "{:,.0f}".format(round(100 * (sum(count_donations_in_pa)/len(count_donations_in_pa))/(sum(count_donations)/len(count_donations)), 2))
    percent_amount_in_pa = "{:,.0f}".format(round(100 * (sum(in_pa_amounts)/len(in_pa_amounts))/(sum(total_amounts)/len(total_amounts)), 2))
    """


    #print(candidates_in_district_percent)

    #districts = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50]

    if session['filter']['look_at'] == 'overall':
        template_name = 'table_overall.html'
    elif session['filter']['look_at'] == 'in_district':
        template_name = 'table_in_district.html'
    elif session['filter']['look_at'] == 'in_pa':
        template_name = 'table_in_pa.html'

    """
    ,
        avg_in_pa_amount=avg_in_pa_amount, avg_count_of_in_pa_donations=avg_count_of_in_pa_donations, avg_in_pa_donation=avg_in_pa_donation,
        median_in_pa_amount=median_in_pa_amount, percent_count_in_pa=percent_count_in_pa, percent_amount_in_pa=percent_amount_in_pa
    """

    return render_template(template_name, candidates_in_district_percent=candidates_in_district_percent,
        action_url=action_url, map_url=map_url, candidate_type=candidate_type, description=description, avg_amount=avg_amount, 
        avg_in_dist_amount=avg_in_dist_amount, median_amount=median_amount, median_in_dist_amount=median_in_dist_amount,
        avg_count_of_donations=avg_count_of_donations, avg_count_of_in_district_donations=avg_count_of_in_district_donations,
        avg_donation=avg_donation, avg_in_district_donation=avg_in_district_donation, districts=districts, 
        percent_count_in_district=percent_count_in_district, percent_amount_in_district=percent_amount_in_district)




@views.route('/state_house_in_district', methods=['GET'])
#@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=make_cache_key)
def state_house_in_district():

    #districts = [i for i in range(1, 203)]

    districts = [2, 3, 5, 7, 9, 10, 11, 13, 14, 15, 16, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 39, 40, 41, 42, 43, 44, 45, 46, 48, 49, 50, 51, 52, 53, 54, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 73, 74, 76, 77, 78, 79, 80, 81, 82, 84, 85, 86, 87, 88, 89, 91, 92, 94, 95, 96, 97, 98, 99, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 118, 119, 121, 122, 125, 127, 128, 129, 131, 132, 133, 134, 135, 138, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 160, 161, 162, 163, 164, 165, 166, 167, 168, 170, 171, 172, 175, 176, 177, 178, 181, 182, 183, 184, 188, 189, 192, 194, 195, 199, 200, 201, 202]

    #AND `race`.race_name = 'REPRESENTATIVE IN THE GENERAL ASSEMBLY'
    #AND `cicero_district`.district_type = 'STATE_LOWER'

    return donation_table(candidate_type='State House', race_race_name = 'REPRESENTATIVE IN THE GENERAL ASSEMBLY',
        cicero_district_type = 'STATE_LOWER', districts=districts, action_url='/state_house_in_district',
        map_url='.donations_by_state_house_district')


@views.route('/state_senate_in_district', methods=['GET'])
#@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=make_cache_key)
def state_senate_in_district():

    #districts = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50]

    districts = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 46, 48]

    #AND `race`.race_name = 'SENATOR IN THE GENERAL ASSEMBLY'
    #AND `cicero_district`.district_type = 'STATE_UPPER'

    return donation_table(candidate_type='State Senate', race_race_name = 'SENATOR IN THE GENERAL ASSEMBLY',
        cicero_district_type = 'STATE_UPPER',  districts=districts, action_url='/state_senate_in_district',
        map_url='.donations_by_state_senate_district')





@views.route('/governor_in_district', methods=['GET'])
#@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=make_cache_key)
def governor_in_district():

    districts = []

    #AND `race`.race_name = 'SENATOR IN THE GENERAL ASSEMBLY'
    #AND `cicero_district`.district_type = 'STATE_UPPER'

    return donation_table(candidate_type='Governor', race_race_name = 'GOVERNOR',
        cicero_district_type = 'STATE_UPPER',  districts=districts, action_url='/governor_in_district')


"""
@views.route('/state_house_in_district', methods=['GET'])
#@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=make_cache_key)
def state_house_in_district():

    additional_where_sql_list = ['1']

    description = 'Basic stats for PARTY candidates running for the PA State House NUM_CANDS DISTRCT'

    if session['filter']['party'] > 0:
        additional_where_sql_list.append('`candidacy`.party_id = {}'.format(session['filter']['party']))
        party = db_session.query(Party).get(session['filter']['party'])
        description = description.replace('PARTY', party.party_name)
    else:
        description = description.replace('PARTY', 'all')

    if session['filter']['min_total']:
        additional_where_sql_list.append('d.party_id = {}'.format(session['filter']['min_total']))

    if session['filter']['max_total']:
        additional_where_sql_list.append('d.party_id = {}'.format(session['filter']['max_total']))

    if session['filter']['num_candidates'] > 0:
        additional_where_sql_list.append('`race`.num_candidates = {}'.format(session['filter']['num_candidates']))
        if session['filter']['num_candidates'] == 1:
            description = description.replace('NUM_CANDS', 'where only one candidate is running')
        else:
            description = description.replace('NUM_CANDS', 'where {} candidates are running'.format(session['filter']['num_candidates']))
    else:
        description = description.replace('NUM_CANDS', '')

    if session['filter']['district'] > 0:
        additional_where_sql_list.append('`race`.race_district = {}'.format(session['filter']['district']))
        description = description.replace('DISTRCT', 'in district number {}'.format(session['filter']['district']))

    else:
        description = description.replace('DISTRCT', '')

    description = description.strip().replace('  ', ' ')

    print('additional_where_sql_list:', additional_where_sql_list)


    #sql_query = ""SELECT DISTINCT cand.*, race.race_description, party.party_name,
    vc1.value AS total_amount, vc2.value AS total_in_district_amount, (vc2.value/vc1.value) AS percent_in_district, 
    vc3.value AS count_donations, vc4.value AS count_donations_in_district, (vc4.value/vc3.value) AS percent_count_in_district 
FROM political_donation d, committee comm, `candidate_committees` cand_comm, `candidate` cand, `candidacy`, `race`, party,
    `contributor`, `contributor_address`, `contributor_address_cicero_district_set` ad_set, `cicero_district`, 
    `cache_value_amount` vc1, `cache_value_amount` vc2, `cache_value_amount` vc3, `cache_value_amount` vc4
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

    AND comm.id = vc3.object_id AND vc3.object_name = 'committee' 
    AND vc3.breakdown_1 = 'count_donations_by_year' AND vc3.breakdown_2 = 'total'

    AND comm.id = vc4.object_id AND vc4.object_name = 'committee' 
    AND vc4.breakdown_1 = 'in_district_count_donations_by_year' AND vc4.breakdown_2 = 'total'

    AND {}
    #ORDER BY percent_in_district DESC"".format(' AND '.join(additional_where_sql_list))

    print(sql_query)

    results = db_session.execute(sql_query)

    candidates_in_district_percent = [dict(r) for r in results]

    total_amounts = []
    in_district_amounts = []
    count_donations = []
    count_donations_in_district = []

    for c in candidates_in_district_percent:
        c['total_amount'] = round(float(c['total_amount']), 2)
        c['total_in_district_amount'] = round(float(c['total_in_district_amount']), 2)
        c['percent_in_district'] = float(100 * c['percent_in_district'])

        c['count_donations'] = int(c['count_donations'])
        c['count_donations_in_district'] = int(c['count_donations_in_district'])
        c['percent_count_in_district'] = float(100 * c['percent_count_in_district'])

        c['avg_donation'] = round(c['total_amount']/c['count_donations'], 2)
        c['avg_in_district_donation'] = round(c['total_in_district_amount']/c['count_donations_in_district'], 2)

        total_amounts.append(c['total_amount'])
        in_district_amounts.append(c['total_in_district_amount'])
        count_donations.append(c['count_donations'])
        count_donations_in_district.append(c['count_donations_in_district'])

    # "${:,.0f}".format(value).

    avg_amount = "${:,.0f}".format(round(sum(total_amounts)/len(total_amounts), 2))
    avg_in_dist_amount = "${:,.0f}".format(round(sum(in_district_amounts)/len(in_district_amounts), 2))
    avg_count_of_donations = "{:,.0f}".format(round(sum(count_donations)/len(count_donations), 2))
    avg_count_of_in_district_donations = "{:,.0f}".format(round(sum(count_donations_in_district)/len(count_donations_in_district), 2))

    avg_donation = "${:,.0f}".format(round((sum(total_amounts)/len(total_amounts))/(sum(count_donations)/len(count_donations)), 2))
    avg_in_district_donation = "${:,.0f}".format(round((sum(in_district_amounts)/len(in_district_amounts))/(sum(count_donations_in_district)/len(count_donations_in_district)), 2))

    median_amount = "${:,.0f}".format(my_median(total_amounts))
    median_in_dist_amount = "${:,.0f}".format(my_median(in_district_amounts))

    percent_count_in_district = "{:,.0f}".format(round(100 * (sum(count_donations_in_district)/len(count_donations_in_district))/(sum(count_donations)/len(count_donations)), 2))
    percent_amount_in_district = "{:,.0f}".format(round(100 * (sum(in_district_amounts)/len(in_district_amounts))/(sum(total_amounts)/len(total_amounts)), 2))


    #print(candidates_in_district_percent)

    districts = [i for i in range(1, 203)]


    return render_template('table_in_district.html', candidates_in_district_percent=candidates_in_district_percent,
        action_url='/state_house_in_district', candidate_type='State House', description=description, avg_amount=avg_amount, 
        avg_in_dist_amount=avg_in_dist_amount, median_amount=median_amount, median_in_dist_amount=median_in_dist_amount,
        avg_count_of_donations=avg_count_of_donations, avg_count_of_in_district_donations=avg_count_of_in_district_donations,
        avg_donation=avg_donation, avg_in_district_donation=avg_in_district_donation, districts=districts, 
        percent_count_in_district=percent_count_in_district, percent_amount_in_district=percent_amount_in_district)



@views.route('/state_senate_in_district', methods=['GET'])
#@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=make_cache_key)
def state_senate_in_district():

    additional_where_sql_list = ['1']

    description = 'Basic stats for PARTY candidates running for the PA State Senate NUM_CANDS'

    if session['filter']['party'] > 0:
        additional_where_sql_list.append('`candidacy`.party_id = {}'.format(session['filter']['party']))
        party = db_session.query(Party).get(session['filter']['party'])
        description = description.replace('PARTY', party.party_name)
    else:
        description = description.replace('PARTY', 'all')

    if session['filter']['min_total']:
        additional_where_sql_list.append('d.party_id = {}'.format(session['filter']['min_total']))

    if session['filter']['max_total']:
        additional_where_sql_list.append('d.party_id = {}'.format(session['filter']['max_total']))

    if session['filter']['num_candidates'] > 0:
        additional_where_sql_list.append('`race`.num_candidates = {}'.format(session['filter']['num_candidates']))
        if session['filter']['num_candidates'] == 1:
            description = description.replace('NUM_CANDS', 'where only one candidate is running')
        else:
            description = description.replace('NUM_CANDS', 'where {} candidates are running'.format(session['filter']['num_candidates']))
    else:
        description = description.replace('NUM_CANDS', '')

    if session['filter']['district'] > 0:
        additional_where_sql_list.append('`race`.race_district = {}'.format(session['filter']['district']))
        description = description.replace('DISTRCT', 'in district number {}'.format(session['filter']['district']))

    else:
        description = description.replace('DISTRCT', '')

    description = description.strip()

    print('additional_where_sql_list:', additional_where_sql_list)



    # Top business donors
    #sql_query = ""SELECT DISTINCT cand.*, race.race_description, party.party_name,
    vc1.value AS total_amount, vc2.value AS total_in_district_amount, (vc2.value/vc1.value) AS percent_in_district, 
    vc3.value AS count_donations, vc4.value AS count_donations_in_district, (vc4.value/vc3.value) AS percent_count_in_district 
FROM political_donation d, committee comm, `candidate_committees` cand_comm, `candidate` cand, `candidacy`, `race`, party,
    `contributor`, `contributor_address`, `contributor_address_cicero_district_set` ad_set, `cicero_district`, 
    `cache_value_amount` vc1, `cache_value_amount` vc2, `cache_value_amount` vc3, `cache_value_amount` vc4
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

    AND comm.id = vc3.object_id AND vc3.object_name = 'committee' 
    AND vc3.breakdown_1 = 'count_donations_by_year' AND vc3.breakdown_2 = 'total'

    AND comm.id = vc4.object_id AND vc4.object_name = 'committee' 
    AND vc4.breakdown_1 = 'in_district_count_donations_by_year' AND vc4.breakdown_2 = 'total'

    AND {}
    #ORDER BY percent_in_district DESC"".format(' AND '.join(additional_where_sql_list))


    results = db_session.execute(sql_query)

    candidates_in_district_percent = [dict(r) for r in results]

    total_amounts = []
    in_district_amounts = []
    count_donations = []
    count_donations_in_district = []

    for c in candidates_in_district_percent:
        c['total_amount'] = round(float(c['total_amount']), 2)
        c['total_in_district_amount'] = round(float(c['total_in_district_amount']), 2)
        c['percent_in_district'] = float(100 * c['percent_in_district'])

        c['count_donations'] = int(c['count_donations'])
        c['count_donations_in_district'] = int(c['count_donations_in_district'])
        c['percent_count_in_district'] = float(100 * c['percent_count_in_district'])

        c['avg_donation'] = round(c['total_amount']/c['count_donations'], 2)
        c['avg_in_district_donation'] = round(c['total_in_district_amount']/c['count_donations_in_district'], 2)

        total_amounts.append(c['total_amount'])
        in_district_amounts.append(c['total_in_district_amount'])
        count_donations.append(c['count_donations'])
        count_donations_in_district.append(c['count_donations_in_district'])

    # "${:,.0f}".format(value).

    avg_amount = "${:,.0f}".format(round(sum(total_amounts)/len(total_amounts), 2))
    avg_in_dist_amount = "${:,.0f}".format(round(sum(in_district_amounts)/len(in_district_amounts), 2))
    avg_count_of_donations = "{:,.0f}".format(round(sum(count_donations)/len(count_donations), 2))
    avg_count_of_in_district_donations = "{:,.0f}".format(round(sum(count_donations_in_district)/len(count_donations_in_district), 2))

    avg_donation = "${:,.0f}".format(round((sum(total_amounts)/len(total_amounts))/(sum(count_donations)/len(count_donations)), 2))
    avg_in_district_donation = "${:,.0f}".format(round((sum(in_district_amounts)/len(in_district_amounts))/(sum(count_donations_in_district)/len(count_donations_in_district)), 2))

    median_amount = "${:,.0f}".format(my_median(total_amounts))
    median_in_dist_amount = "${:,.0f}".format(my_median(in_district_amounts))

    percent_count_in_district = "{:,.0f}".format(round(100 * (sum(count_donations_in_district)/len(count_donations_in_district))/(sum(count_donations)/len(count_donations)), 2))
    percent_amount_in_district = "{:,.0f}".format(round(100 * (sum(in_district_amounts)/len(in_district_amounts))/(sum(total_amounts)/len(total_amounts)), 2))


    #print(candidates_in_district_percent)

    districts = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50]


    return render_template('table_in_district.html', candidates_in_district_percent=candidates_in_district_percent,
        action_url='/state_senate_in_district', candidate_type='State Senate', description=description, avg_amount=avg_amount, 
        avg_in_dist_amount=avg_in_dist_amount, median_amount=median_amount, median_in_dist_amount=median_in_dist_amount,
        avg_count_of_donations=avg_count_of_donations, avg_count_of_in_district_donations=avg_count_of_in_district_donations,
        avg_donation=avg_donation, avg_in_district_donation=avg_in_district_donation, districts=districts, 
        percent_count_in_district=percent_count_in_district, percent_amount_in_district=percent_amount_in_district)

"""