'use strict';

var expect              = require('chai').expect;
var CandidateStorage = require('../lib/storage/sqlite/candidate-storage');

describe('CandidateStorage', () => {

  var storage = new CandidateStorage({ path: 'test/data/db.sqlite' });

  describe('#fetchById', () => {
    it('retrieves the expected record', (done) => {
      storage.fetchById(1, (err, cdt) => {
        if (err) return done(err);
        expect(cdt.candidate_id, 'unexpected candidate_id').to.equal(1);
        expect(cdt.candidate_name, 'unexpected candidate_name').to.equal('Matt Wolfe');
        expect(cdt.campaigns.length, 'invalid type or length of campaigns').to.be.above(0);
        expect(cdt.campaigns[0].campaign_id, 'unexpected campaign_id of campgaigns[0]').to.equal(1);
        expect(cdt.campaigns[0].election_year, 'unexpected election_year of campaigns[0]').to.equal(2015);
        expect(cdt.campaigns[0].election_cycle, 'unexpected election_cycle of campaigns[0]').to.equal('general');
        expect(cdt.campaigns[0].candidate_position, 'unexpected candidate_position of campaigns[0]').to.equal('Council-At-Large');
        expect(cdt.campaigns[0].candidate_party, 'unexpected candidate_party of campaign[0]').to.equal('Made-up party');
        expect(cdt.campaigns[0].campaign_summary.length, 'invalid type or length of campaigns[0].campaign_summary').to.be.above(0);
        expect(cdt.campaigns[0].campaign_summary[0].summary_value, 'unexpected summary_value of campaigns[0].campaign_summary[0]').to.equal(6);
        expect(cdt.campaigns[0].campaign_summary[0].summary_level, 'unexpected summary_level of campaigns[0].campaign_summary[0]').to.equal('10');
        expect(cdt.campaigns[0].campaign_summary[0].summary_type, 'unexpected summary_type of campaigns[0].campaign_summary[0]').to.equal('donation_histogram');
        done();
      });
    });
  });

  describe('#fetchAll', () => {
    it('retrieves the expected record', (done) => {
      storage.fetchAll((err, cdts) => {
        if (err) return done(err);
        expect(cdts[0].candidate_id, 'unexpected candidate_id of cdts[0]').to.equal(1);
        expect(cdts[0].candidate_name, 'unexpected candidate_name of cdts[0]').to.equal('Matt Wolfe');
        expect(cdts[0].campaigns[0].candidate_id, 'unexpected candidate_id of cdts[0].campaigns[0]').to.equal(1);
        expect(cdts[0].campaigns[0].candidate_name, 'unexpected candidate_name of cdts[0].campaigns[0]').to.equal('Matt Wolfe');
        expect(cdts[0].campaigns[0].campaign_id, 'unexpected campaign_id of cdts[0].campaigns[0]').to.equal(1);
        expect(cdts[0].campaigns[0].election_year, 'unexpected election_year of cdts[0].campaigns[0]').to.equal(2015);
        expect(cdts[0].campaigns[0].election_cycle, 'unexpected election_cycle of cdts[0].campaigns[0]').to.equal('general');
        expect(cdts[0].campaigns[0].candidate_position, 'unexpected candidate_position of cdts[0].campaigns[0]').to.equal('Council-At-Large');
        expect(cdts[0].campaigns[0].candidate_party, 'unexpected candidate_party of cdts[0].campaigns[0]').to.equal('Made-up party');
        expect(cdts[0].campaigns[0].campaign_summary.length, 'invalid type or length of cdts[0].campaigns[0].campaign_summary').to.be.above(0);
        expect(cdts[0].campaigns[0].campaign_summary[0].summary_value, 'unexpected summary_value of cdts[0].campaigns[0].campaign_summary[0]').to.equal(6);
        expect(cdts[0].campaigns[0].campaign_summary[0].summary_level, 'unexpected summary_level of cdts[0].campaigns[0].campaign_summary[0]').to.equal('10');
        expect(cdts[0].campaigns[0].campaign_summary[0].summary_type, 'unexpected summary_type of cdts[0].campaigns[0].campaign_summary[0]').to.equal('donation_histogram');
        done();
      });
    });
  });
});
