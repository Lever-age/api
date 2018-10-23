#!/usr/bin/python3
# coding: utf-8

from leverageapi.database import db_session

# -- -----------------------------------------
# -- Set Committee total contributions by year
# -- -----------------------------------------


replacement_dict = {}
replacement_dict['total'] = {'date_start': '2016-12-31', 'date_end': '2019-01-01'}
replacement_dict['2018'] = {'date_start': '2017-12-31', 'date_end': '2019-01-01'}
replacement_dict['2017'] = {'date_start': '2016-12-31', 'date_end': '2018-01-01'}

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

    print(sql_query)

    results = db_session.execute(sql_query)

