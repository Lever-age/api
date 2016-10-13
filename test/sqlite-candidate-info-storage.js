'use strict';

var expect              = require('chai').expect;
var CandidateInfoStorage = require('../lib/storage/sqlite/candidate-info-storage');

describe('CandidateInfoStorage', () => {

  var storage = new CandidateInfoStorage({ path: 'test/data/db.sqlite' });

  describe('#fetch_by_campaign', () => {
    it('retrieves the expected record', (done) => {
      storage.fetch_by_campaign(1, (err, cinfo) => {
        if (err) return done(err);
        expect(cinfo.candidate_id, 'unexpected candidate_id').to.equal(1);
        expect(cinfo.candidate_name, 'unexpected candidate_name').to.equal('Matt Wolfe');
        done();
      });
    });
  });
});
