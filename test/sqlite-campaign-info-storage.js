'use strict';

var expect              = require('chai').expect;
var CampaignInfoStorage = require('../lib/storage/sqlite/campaign-info-storage');

describe('CampaignInfoStorage', function(){

  var storage = new CampaignInfoStorage({ path: 'test/data/db.sqlite' });

  describe('#fetch_by_id', function(){
    it('retrieves the expected record', function(done){
      storage.fetch_by_id(1, function(err, cinfo){
        if (err) return done(err);
        expect(cinfo.campaign_id, 'unexpected campaign_id').to.equal(1);
        expect(cinfo.election_year, 'unexpected election_year').to.equal(2015);
        expect(cinfo.election_cycle, 'unexpected election_cycle').to.equal('general');
        expect(cinfo.candidate_id, 'unexpected candidate_id').to.equal(1);
        expect(cinfo.candidate_position, 'unexpected candidate_position').to.equal('Council-At-Large');
        expect(cinfo.candidate_party, 'unexpected candidate_party').to.equal('Made-up party');
        done();
      });
    });
  });
});
