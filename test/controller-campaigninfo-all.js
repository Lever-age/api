'use strict';

var chai = require('chai');
var expect = require('chai').expect;
var chaiHttp = require('chai-http');
var server = require('../app');

chai.use(chaiHttp);

describe('campaignInfo', () => {
  it('should retreive all campaigns info on /campaigns/info GET', () => {
    chai.request(server)
    .get('/campaigns/info')
    .end((err, res) => {
      expect(err).to.be.an('undefined');
      expect(res).have.have.status(200);
      expect(res.body).to.have.length.of.at.least(3);
      expect(res.body).to.be.an('array');
      expect(res.body).to.not.be.empty;
    });
  });
});
