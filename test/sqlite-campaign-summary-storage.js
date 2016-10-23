'use strict';

var expect                 = require('chai').expect;
var CampaignSummaryStorage = require('../lib/storage/sqlite/campaign-summary-storage');

describe('CampaignSummaryStorage', () => {

  var storage = new CampaignSummaryStorage({ path: 'test/data/db.sqlite' });

  describe('#fetchByCampaign', () => {
    it('retrieves the expected record', (done) => {
      storage.fetchByCampaign(1, (err, summaries) => {
        if (err) return done(err);
        expect(summaries[0].campaign_id, 'unexpected campaign_id').to.equal(1);
        expect(summaries[0].summary_level, 'unexpected summary_level').to.equal('10');
        expect(summaries[0].summary_value, 'unexpected summary_value').to.equal(6);
        expect(summaries[0].summary_type, 'unexpected summary_type').to.equal('donation_histogram');
        done();
      });
    });
  });
});
