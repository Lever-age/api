
-- Set total contributions by year

UPDATE `committee` c
SET donations_2017 = (
    SELECT SUM(d.donation_amount) as total_donation
        FROM `political_donation` d 
        WHERE d.committee_id = c.id
            AND donation_date > '2016-12-31'
            AND donation_date < '2018-01-01'
    );


UPDATE `committee` c
SET donations_2017 = 0 
WHERE donations_2017 IS NULL;


UPDATE `committee` c
SET donations_2016 = (
    SELECT SUM(d.donation_amount) as total_donation
        FROM `political_donation` d 
        WHERE d.committee_id = c.id
            AND donation_date > '2015-12-31'
            AND donation_date < '2017-01-01'
    );


UPDATE `committee` c
SET donations_2016 = 0 
WHERE donations_2016 IS NULL;


UPDATE `committee` c
SET donations_2015 = (
    SELECT SUM(d.donation_amount) as total_donation
        FROM `political_donation` d 
        WHERE d.committee_id = c.id
            AND donation_date > '2014-12-31'
            AND donation_date < '2016-01-01'
    );


UPDATE `committee` c
SET donations_2015 = 0 
WHERE donations_2015 IS NULL;


-- Set total contributions by address (in Philly, in PA, out PA)

UPDATE `committee` c
SET donations_in_philly = (
    SELECT SUM(d.donation_amount) AS total_donation
        FROM `political_donation` d 
            LEFT JOIN `contributor` ON d.contributor_id = contributor.id
            LEFT JOIN `contributor_address` a ON contributor.address_id = a.id
        WHERE d.committee_id = c.id
            AND a.city LIKE 'Phil%' AND a.city NOT LIKE '%rg' 
            AND a.state = 'PA'
    );


UPDATE `committee` c
SET donations_in_philly = 0 
WHERE donations_in_philly IS NULL;


UPDATE `committee` c
SET donations_in_pa = (
    SELECT SUM(d.donation_amount) AS total_donation
        FROM `political_donation` d 
            LEFT JOIN `contributor` ON d.contributor_id = contributor.id
            LEFT JOIN `contributor_address` a ON contributor.address_id = a.id
        WHERE d.committee_id = c.id
            AND a.state = 'PA'
    );


UPDATE `committee` c
SET donations_in_pa = 0 
WHERE donations_in_pa IS NULL;


UPDATE `committee` c
SET donations_out_pa = (
    SELECT SUM(d.donation_amount) AS total_donation
        FROM `political_donation` d 
            LEFT JOIN `contributor` ON d.contributor_id = contributor.id
            LEFT JOIN `contributor_address` a ON contributor.address_id = a.id
        WHERE d.committee_id = c.id
            AND a.state != 'PA'
    );


UPDATE `committee` c
SET donations_out_pa = 0 
WHERE donations_out_pa IS NULL;