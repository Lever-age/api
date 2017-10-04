# Leverage API

Initially copied from Illinois Sunshine.

## Setup

**Install OS level dependencies:** 

* Python 3.4
* PostgreSQL 9.4 +
* MySQL client libraries + development headers
  + Ubuntu Xenial: `libmysqlclient-dev` package
  + Debian Stretch: `libmariadbclient-dev` package
  + Fedora 26/CentOS 7: `mariadb-devel` package
  + OpenSUSE Leap 42.3: `libmysqlclient-devel` package
  + OS X Sierra: `mysql` homebrew formula

**Install app requirements**

We recommend using [virtualenv](http://virtualenv.readthedocs.org/en/latest/virtualenv.html) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html) for working in a virtualized development environment. [Read how to set up virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

Once you have virtualenvwrapper set up (make sure to initialize as a Python 3 project),

```bash
mkdir leverage
cd leverage
git clone https://github.com/Lever-age/api.git
cd api
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
cp api/app_config.py.example api/app_config.py
```

In `app_config.py`, put your Postgres user in `DB_USER` and password in `DB_PW`.

  NOTE: Mac users might need this [lxml workaround](http://stackoverflow.com/questions/22313407/clang-error-unknown-argument-mno-fused-madd-python-package-installation-fa).

Afterwards, whenever you want to work on leverage-api, cd into the directory

```bash
source venv/bin/activate
```

## Setup your database

For now, load the mysql files from the datadump directory. Load the tables.sql first, then data.sql


## Run the server, then test the api endpoints
```bash
python runserver.py
```

* /api/races (same as /api/races?election_type=general&election_year=2017)
* /api/races?election_type=primary&election_year=2015
* /api/races?race_id=27
* /api/candidates?race_id=27
* /api/candidates?race_id=28
* /api/candidates?candidate_id=47

## Illinois Sunshine DB instructions:

Before we can run the website, we need to create a database.

```bash
createdb leverage_api
```

Then, we run the `etl.py` script to download our data from the IL State Board of Elections and load it into the database.

```bash
python etl.py --download --load_data --recreate_views
```

This command will take between 15-45 min depending on your internet connection.

Doesn't do this: You can run `etl.py` again to get the latest data from the IL State Board of Elections. It is updated daily. Other useful flags are:

```
 --download               Downloading fresh data
 --cache                  Cache downloaded files to S3
 --load_data              Load data into database
 --recreate_views         Recreate database views
 --chunk_size CHUNK_SIZE  Adjust the size of each insert when loading data
 ```

## Running Illinois Sunshine

``` bash
git clone git@github.com:datamade/leverage-api.git
cd leverage-api

# to run locally
python runserver.py
```

navigate to http://localhost:5000/

## Optionally configure PostgreSQL stop words

Uses MySQL for now...

While developing this, we noticed that PostgreSQL treats some names od
individuals and organizations as stop words. We added a custom stop word list
to the repo that can be used to make sure that these names will show up in
search results.

* Create a symbolic link from the stop words list in this repo to the
PostgreSQL shared directory (this example will work on Debian and Ubuntu):

``` bash
sudo ln -s /path/to/this/repo/sunshine.stop /usr/share/postgresql/9.4/tsearch_data/sunshine.stop
```

You'll then need to change the ``STOP_WORD_LIST`` configuration in ``app_config.py`` to ``sunshine``

## Team

* Eric van Zanten - developer
* Derek Eder - developer

## Errors / Bugs

If something is not behaving intuitively, it is a bug, and should be reported.
Report it here: https://github.com/datamade/leverage-api/issues

## Note on Patches/Pull Requests
 
* Fork the project.
* Make your feature addition or bug fix.
* Commit, do not mess with rakefile, version, or history.
* Send a pull request. Bonus points for topic branches.

## Copyright

Copyright (c) 2017 Code for Philly

Copyright (c) 2015 DataMade and Illinois Campaign for Political Reform. Released under the [MIT License](https://github.com/datamade/leverage-api/blob/master/LICENSE).
