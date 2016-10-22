'use strict';

var chai = require('chai');
var expect = require('chai').expect;
var chaiHttp = require('chai-http');
var server = require('../app');

chai.use(chaiHttp);

describe('campaignInfo', () => {
  it('should retreive all candidate campaigns info on /candidates/:id/campaigns GET', () => {
    chai.request(server)
    .get('/candidates/5/campaigns')
    .end((err, res) => {
      expect(err).to.be.an('undefined');
      expect(res).have.have.status(200);
      expect(res.body).to.have.length.of.at.least(1);
      expect(res.body).to.be.an('array');
      expect(res.body).to.not.be.empty;

      expect(res.body[0].campaign_year).to.equal(2015);
      expect(res.body[0].candidate_party).to.equal('Made-up party');
    });
  });
});