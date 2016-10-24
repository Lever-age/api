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
});
