#!/usr/bin/python3
# coding: utf-8

from leverageapi.database import db_session

# -- -----------------------------------------
# -- Set Committee total donations by year
# -- -----------------------------------------


replacement_dict = {}
replacement_dict['total'] = {'date_start': '2016-12-31', 'date_end': '2019-01-01'}
replacement_dict['2018'] = {'date_start': '2017-12-31', 'date_end': '2019-01-01'}
replacement_dict['2017'] = {'date_start': '2016-12-31', 'date_end': '2018-01-01'}

print('committee -- donations_by_year')

for breakdown in replacement_dict:

    sql_delete = """DELETE FROM `cache_value_amount` 
        WHERE object_name = 'committee'
            AND breakdown_1 = 'donations_by_year'
            AND breakdown_2 = '{}';""".format(breakdown)

    db_session.execute(sql_delete)

    sql_query = """INSERT INTO `cache_value_amount`
        SELECT NULL, committee_id, 'committee', 'donations_by_year', '{}', '', SUM(d.donation_amount)
            FROM political_donation d
        WHERE d.donation_date > '{}'
            AND d.donation_date < '{}'
        GROUP BY d.`committee_id`;""".format(breakdown, replacement_dict[breakdown]['date_start'], replacement_dict[breakdown]['date_end'])

    #print(sql_query)

    results = db_session.execute(sql_query)



# -- -----------------------------------------
# -- Set Committee count of donations by year
# -- -----------------------------------------


replacement_dict = {}
replacement_dict['total'] = {'date_start': '2016-12-31', 'date_end': '2019-01-01'}
replacement_dict['2018'] = {'date_start': '2017-12-31', 'date_end': '2019-01-01'}
replacement_dict['2017'] = {'date_start': '2016-12-31', 'date_end': '2018-01-01'}

print('committee -- count_donations_by_year')

for breakdown in replacement_dict:

    sql_delete = """DELETE FROM `cache_value_amount` 
        WHERE object_name = 'committee'
            AND breakdown_1 = 'count_donations_by_year'
            AND breakdown_2 = '{}';""".format(breakdown)

    db_session.execute(sql_delete)

    sql_query = """INSERT INTO `cache_value_amount`
        SELECT NULL, committee_id, 'committee', 'count_donations_by_year', '{}', '', COUNT(d.donation_amount)
            FROM political_donation d
        WHERE d.donation_date > '{}'
            AND d.donation_date < '{}'
        GROUP BY d.`committee_id`;""".format(breakdown, replacement_dict[breakdown]['date_start'], replacement_dict[breakdown]['date_end'])

    #print(sql_query)

    results = db_session.execute(sql_query)




# -- -----------------------------------------
# -- Set Committee in-district contributions by year for State House races
# -- -----------------------------------------

replacement_dict = {}
replacement_dict['total'] = {'date_start': '2016-12-31', 'date_end': '2019-01-01'}
replacement_dict['2018'] = {'date_start': '2017-12-31', 'date_end': '2019-01-01'}
replacement_dict['2017'] = {'date_start': '2016-12-31', 'date_end': '2018-01-01'}

print('committee (house) -- in_district_donations_by_year')

for breakdown in replacement_dict:

    sql_delete = """DELETE FROM `cache_value_amount` 
        WHERE object_name = 'committee'
            AND breakdown_1 = 'in_district_donations_by_year'
            AND breakdown_2 = '{}';""".format(breakdown)

    db_session.execute(sql_delete)

    sql_query = """INSERT INTO `cache_value_amount`
    SELECT NULL, comm.id, 'committee', 'in_district_donations_by_year', '{}', '', SUM(d.donation_amount)
        FROM political_donation d, committee comm, `candidate_committees` cand_comm, `candidate` cand, `candidacy`, `race`, 
            `contributor`, `contributor_address`, `contributor_address_cicero_district_set` ad_set, `cicero_district`
    WHERE d.committee_id = comm.id
        AND comm.id = cand_comm.committee_id
        AND cand_comm.candidate_id = cand.id
        AND cand.id = `candidacy`.candidate_id
        AND `candidacy`.race_id = `race`.id
        AND d.contributor_id = `contributor`.id
        AND `contributor`.address_id = `contributor_address`.id
        AND `contributor_address`.id = ad_set.address_id
        AND ad_set.cicero_district_id = `cicero_district`.id
        AND `race`.race_name = 'REPRESENTATIVE IN THE GENERAL ASSEMBLY'
        AND `cicero_district`.district_type = 'STATE_LOWER'
        AND `race`.race_district = `cicero_district`.district_id
        AND d.donation_date > '{}'
        AND d.donation_date < '{}'
    GROUP BY d.`committee_id`;""".format(breakdown, replacement_dict[breakdown]['date_start'], replacement_dict[breakdown]['date_end'])

    #print(sql_query)

    results = db_session.execute(sql_query)


# -- -----------------------------------------
# -- Set Committee in-district contributions by year for State Senate races
# -- -----------------------------------------

replacement_dict = {}
replacement_dict['total'] = {'date_start': '2016-12-31', 'date_end': '2019-01-01'}
replacement_dict['2018'] = {'date_start': '2017-12-31', 'date_end': '2019-01-01'}
replacement_dict['2017'] = {'date_start': '2016-12-31', 'date_end': '2018-01-01'}

print('committee (senate) -- in_district_donations_by_year')

for breakdown in replacement_dict:

    # Do not delete! These are deleted above!

    sql_query = """INSERT INTO `cache_value_amount`
    SELECT NULL, comm.id, 'committee', 'in_district_donations_by_year', '{}', '', SUM(d.donation_amount)
        FROM political_donation d, committee comm, `candidate_committees` cand_comm, `candidate` cand, `candidacy`, `race`, 
            `contributor`, `contributor_address`, `contributor_address_cicero_district_set` ad_set, `cicero_district`
    WHERE d.committee_id = comm.id
        AND comm.id = cand_comm.committee_id
        AND cand_comm.candidate_id = cand.id
        AND cand.id = `candidacy`.candidate_id
        AND `candidacy`.race_id = `race`.id
        AND d.contributor_id = `contributor`.id
        AND `contributor`.address_id = `contributor_address`.id
        AND `contributor_address`.id = ad_set.address_id
        AND ad_set.cicero_district_id = `cicero_district`.id
        AND `race`.race_name = 'SENATOR IN THE GENERAL ASSEMBLY'
        AND `cicero_district`.district_type = 'STATE_UPPER'
        AND `race`.race_district = `cicero_district`.district_id
        AND d.donation_date > '{}'
        AND d.donation_date < '{}'
    GROUP BY d.`committee_id`;""".format(breakdown, replacement_dict[breakdown]['date_start'], replacement_dict[breakdown]['date_end'])

    #print(sql_query)

    results = db_session.execute(sql_query)








# -- -----------------------------------------
# -- Set Committee in-district count of contributions by year for State House races
# -- -----------------------------------------

replacement_dict = {}
replacement_dict['total'] = {'date_start': '2016-12-31', 'date_end': '2019-01-01'}
replacement_dict['2018'] = {'date_start': '2017-12-31', 'date_end': '2019-01-01'}
replacement_dict['2017'] = {'date_start': '2016-12-31', 'date_end': '2018-01-01'}

print('committee (house) -- in_district_count_donations_by_year')

for breakdown in replacement_dict:

    sql_delete = """DELETE FROM `cache_value_amount` 
        WHERE object_name = 'committee'
            AND breakdown_1 = 'in_district_count_donations_by_year'
            AND breakdown_2 = '{}';""".format(breakdown)

    db_session.execute(sql_delete)

    sql_query = """INSERT INTO `cache_value_amount`
    SELECT NULL, comm.id, 'committee', 'in_district_count_donations_by_year', '{}', '', COUNT(d.donation_amount)
        FROM political_donation d, committee comm, `candidate_committees` cand_comm, `candidate` cand, `candidacy`, `race`, 
            `contributor`, `contributor_address`, `contributor_address_cicero_district_set` ad_set, `cicero_district`
    WHERE d.committee_id = comm.id
        AND comm.id = cand_comm.committee_id
        AND cand_comm.candidate_id = cand.id
        AND cand.id = `candidacy`.candidate_id
        AND `candidacy`.race_id = `race`.id
        AND d.contributor_id = `contributor`.id
        AND `contributor`.address_id = `contributor_address`.id
        AND `contributor_address`.id = ad_set.address_id
        AND ad_set.cicero_district_id = `cicero_district`.id
        AND `race`.race_name = 'REPRESENTATIVE IN THE GENERAL ASSEMBLY'
        AND `cicero_district`.district_type = 'STATE_LOWER'
        AND `race`.race_district = `cicero_district`.district_id
        AND d.donation_date > '{}'
        AND d.donation_date < '{}'
    GROUP BY d.`committee_id`;""".format(breakdown, replacement_dict[breakdown]['date_start'], replacement_dict[breakdown]['date_end'])

    #print(sql_query)

    results = db_session.execute(sql_query)


# -- -----------------------------------------
# -- Set Committee in-district count of contributions by year for State Senate races
# -- -----------------------------------------

replacement_dict = {}
replacement_dict['total'] = {'date_start': '2016-12-31', 'date_end': '2019-01-01'}
replacement_dict['2018'] = {'date_start': '2017-12-31', 'date_end': '2019-01-01'}
replacement_dict['2017'] = {'date_start': '2016-12-31', 'date_end': '2018-01-01'}

print('committee (senate) -- in_district_count_donations_by_year')

for breakdown in replacement_dict:

    # Do not delete! These are deleted above!

    sql_query = """INSERT INTO `cache_value_amount`
    SELECT NULL, comm.id, 'committee', 'in_district_count_donations_by_year', '{}', '', COUNT(d.donation_amount)
        FROM political_donation d, committee comm, `candidate_committees` cand_comm, `candidate` cand, `candidacy`, `race`, 
            `contributor`, `contributor_address`, `contributor_address_cicero_district_set` ad_set, `cicero_district`
    WHERE d.committee_id = comm.id
        AND comm.id = cand_comm.committee_id
        AND cand_comm.candidate_id = cand.id
        AND cand.id = `candidacy`.candidate_id
        AND `candidacy`.race_id = `race`.id
        AND d.contributor_id = `contributor`.id
        AND `contributor`.address_id = `contributor_address`.id
        AND `contributor_address`.id = ad_set.address_id
        AND ad_set.cicero_district_id = `cicero_district`.id
        AND `race`.race_name = 'SENATOR IN THE GENERAL ASSEMBLY'
        AND `cicero_district`.district_type = 'STATE_UPPER'
        AND `race`.race_district = `cicero_district`.district_id
        AND d.donation_date > '{}'
        AND d.donation_date < '{}'
    GROUP BY d.`committee_id`;""".format(breakdown, replacement_dict[breakdown]['date_start'], replacement_dict[breakdown]['date_end'])

    #print(sql_query)

    results = db_session.execute(sql_query)












# -- -----------------------------------------
# -- Set Committee in-pa contributions by year
# -- -----------------------------------------

replacement_dict = {}
replacement_dict['total'] = {'date_start': '2016-12-31', 'date_end': '2019-01-01'}
replacement_dict['2018'] = {'date_start': '2017-12-31', 'date_end': '2019-01-01'}
replacement_dict['2017'] = {'date_start': '2016-12-31', 'date_end': '2018-01-01'}

print('committee -- in_pa_donations_by_year')

for breakdown in replacement_dict:

    sql_delete = """DELETE FROM `cache_value_amount` 
        WHERE object_name = 'committee'
            AND breakdown_1 = 'in_pa_donations_by_year'
            AND breakdown_2 = '{}';""".format(breakdown)

    db_session.execute(sql_delete)

    sql_query = """INSERT INTO `cache_value_amount`
    SELECT NULL, comm.id, 'committee', 'in_pa_donations_by_year', '{}', '', SUM(d.donation_amount)
        FROM political_donation d, committee comm, `contributor`, `contributor_address`
    WHERE d.committee_id = comm.id
        AND d.contributor_id = `contributor`.id
        AND `contributor`.address_id = `contributor_address`.id
        AND `contributor_address`.state = 'pa'
        AND d.donation_date > '{}'
        AND d.donation_date < '{}'
    GROUP BY d.`committee_id`;""".format(breakdown, replacement_dict[breakdown]['date_start'], replacement_dict[breakdown]['date_end'])

    #print(sql_query)

    results = db_session.execute(sql_query)



# -- -----------------------------------------
# -- Set Committee count of in-pa contributions by year
# -- -----------------------------------------

replacement_dict = {}
replacement_dict['total'] = {'date_start': '2016-12-31', 'date_end': '2019-01-01'}
replacement_dict['2018'] = {'date_start': '2017-12-31', 'date_end': '2019-01-01'}
replacement_dict['2017'] = {'date_start': '2016-12-31', 'date_end': '2018-01-01'}

print('committee -- in_pa_count_donations_by_year')

for breakdown in replacement_dict:

    sql_delete = """DELETE FROM `cache_value_amount` 
        WHERE object_name = 'committee'
            AND breakdown_1 = 'in_pa_count_donations_by_year'
            AND breakdown_2 = '{}';""".format(breakdown)

    db_session.execute(sql_delete)

    sql_query = """INSERT INTO `cache_value_amount`
    SELECT NULL, comm.id, 'committee', 'in_pa_count_donations_by_year', '{}', '', COUNT(d.donation_amount)
        FROM political_donation d, committee comm, `contributor`, `contributor_address`
    WHERE d.committee_id = comm.id
        AND d.contributor_id = `contributor`.id
        AND `contributor`.address_id = `contributor_address`.id
        AND `contributor_address`.state = 'pa'
        AND d.donation_date > '{}'
        AND d.donation_date < '{}'
    GROUP BY d.`committee_id`;""".format(breakdown, replacement_dict[breakdown]['date_start'], replacement_dict[breakdown]['date_end'])

    #print(sql_query)

    results = db_session.execute(sql_query)



# -- -----------------------------------------
# -- Set Committee out-of-pa contributions by year
# -- -----------------------------------------

replacement_dict = {}
replacement_dict['total'] = {'date_start': '2016-12-31', 'date_end': '2019-01-01'}
replacement_dict['2018'] = {'date_start': '2017-12-31', 'date_end': '2019-01-01'}
replacement_dict['2017'] = {'date_start': '2016-12-31', 'date_end': '2018-01-01'}

print('committee -- out_of_pa_donations_by_year')

for breakdown in replacement_dict:

    sql_delete = """DELETE FROM `cache_value_amount` 
        WHERE object_name = 'committee'
            AND breakdown_1 = 'out_of_pa_donations_by_year'
            AND breakdown_2 = '{}';""".format(breakdown)

    db_session.execute(sql_delete)

    sql_query = """INSERT INTO `cache_value_amount`
    SELECT NULL, comm.id, 'committee', 'out_of_pa_donations_by_year', '{}', '', SUM(d.donation_amount)
        FROM political_donation d, committee comm, `contributor`, `contributor_address`
    WHERE d.committee_id = comm.id
        AND d.contributor_id = `contributor`.id
        AND `contributor`.address_id = `contributor_address`.id
        AND `contributor_address`.state != 'pa'
        AND d.donation_date > '{}'
        AND d.donation_date < '{}'
    GROUP BY d.`committee_id`;""".format(breakdown, replacement_dict[breakdown]['date_start'], replacement_dict[breakdown]['date_end'])

    #print(sql_query)

    results = db_session.execute(sql_query)













# -- -----------------------------------------
# -- Set Race total contributions by year
# -- -----------------------------------------


replacement_dict = {}
replacement_dict['total'] = {'date_start': '2016-12-31', 'date_end': '2019-01-01'}
replacement_dict['2018'] = {'date_start': '2017-12-31', 'date_end': '2019-01-01'}
replacement_dict['2017'] = {'date_start': '2016-12-31', 'date_end': '2018-01-01'}

print('race -- donations_by_year')

for breakdown in replacement_dict:

    sql_delete = """DELETE FROM `cache_value_amount` 
    WHERE object_name = 'race'
        AND breakdown_1 = 'donations_by_year'
        AND breakdown_2 = '{}';""".format(breakdown)

    db_session.execute(sql_delete)

    sql_query = """INSERT INTO `cache_value_amount`
    SELECT NULL, candidacy.race_id, 'race', 'donations_by_year', '{}', '', SUM(d.donation_amount)
        FROM political_donation d, committee comm, `candidate_committees` cc, `candidate` cand, candidacy
    WHERE d.committee_id = comm.id
        AND comm.id = cc.committee_id
        AND cc.candidate_id = cand.id
        AND cand.id = candidacy.candidate_id
        AND d.donation_date > '{}'
        AND d.donation_date < '{}'
    GROUP BY `candidacy`.`race_id`;""".format(breakdown, replacement_dict[breakdown]['date_start'], replacement_dict[breakdown]['date_end'])

    #print(sql_query)

    results = db_session.execute(sql_query)




