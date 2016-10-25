'use strict';

var expect              = require('chai').expect;
var CampaignStorage = require('../lib/storage/sqlite/campaign-storage');

describe('CampaignStorage', () => {

  var storage = new CampaignStorage({ path: 'test/data/db.sqlite' });

  describe('#fetchById', () => {
    it('retrieves the expected record', (done) => {
      storage.fetchById(1, (err, cmp) => {
        if (err) return done(err);
        expect(cmp.candidate_id, 'unexpected candidate_id').to.equal(1);
        expect(cmp.candidate_name, 'unexpected candidate_name').to.equal('Matt Wolfe');
        expect(cmp.campaign_id, 'unexpected campaign_id').to.equal(1);
        expect(cmp.election_year, 'unexpected election_year').to.equal(2015);
        expect(cmp.election_cycle, 'unexpected election_cycle').to.equal('general');
        expect(cmp.candidate_position, 'unexpected candidate_position').to.equal('Council-At-Large');
        expect(cmp.candidate_party, 'unexpected candidate_party').to.equal('Made-up party');
        expect(cmp.campaign_summary.length, 'invalid type or length of campaign_summary').to.be.above(0);
        expect(cmp.campaign_summary[0].summary_value, 'unexpected summary_value of campaign_summary[0]').to.equal(6);
        expect(cmp.campaign_summary[0].summary_level, 'unexpected summary_level of campaign_summary[0]').to.equal('10');
        expect(cmp.campaign_summary[0].summary_type, 'unexpected summary_type of campaign_summary[0]').to.equal('donation_histogram');
        done();
      });
    });
  });

  describe('#fetchAll', () => {
    it('retrieves the expected record', (done) => {
      storage.fetchAll((err, cmps) => {
        if (err) return done(err);
        expect(cmps[0].candidate_id, 'unexpected candidate_id of cmps[0]').to.equal(1);
        expect(cmps[0].candidate_name, 'unexpected candidate_name of cmps[0]').to.equal('Matt Wolfe');
        expect(cmps[0].campaign_id, 'unexpected campaign_id of cmps[0]').to.equal(1);
        expect(cmps[0].election_year, 'unexpected election_year of cmps[0]').to.equal(2015);
        expect(cmps[0].election_cycle, 'unexpected election_cycle of cmps[0]').to.equal('general');
        expect(cmps[0].candidate_position, 'unexpected candidate_position of cmps[0]').to.equal('Council-At-Large');
        expect(cmps[0].candidate_party, 'unexpected candidate_party of cmps[0]').to.equal('Made-up party');
        expect(cmps[0].campaign_summary.length, 'invalid type or length of cmps[0].campaign_summary').to.be.above(0);
        expect(cmps[0].campaign_summary[0].summary_value, 'unexpected summary_value of cmps[0].campaign_summary[0]').to.equal(6);
        expect(cmps[0].campaign_summary[0].summary_level, 'unexpected summary_level of cmps[0].campaign_summary[0]').to.equal('10');
        expect(cmps[0].campaign_summary[0].summary_type, 'unexpected summary_type of cmps[0].campaign_summary[0]').to.equal('donation_histogram');
        done();
      });
    });
  });
});
