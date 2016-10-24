'use strict';

var chai = require('chai');
var expect = require('chai').expect;
var chaiHttp = require('chai-http');
var server = require('../app');

chai.use(chaiHttp);

describe('candidatesList', () => {
  it('should retreive all candidates on /candidates GET', () => {
    chai.request(server)
    .get('/candidates')
    .end((err, res) => {
      expect(res).have.have.status(200);
      expect(res.body).to.be.an('array');
      expect(res.body).to.not.be.empty;
      expect(res.body).to.have.length.of.at.least(3);
      expect(res.body[0].candidate_name).to.equal('Matt Wolfe');
    });
  });

});
