'use strict';

// var fs = require('fs');
var chai = require('chai');
var expect = require('chai').expect;
var chaiHttp = require('chai-http');
var server = require('../app');
// var config = JSON.parse(fs.readFileSync('config.test.json'));

chai.use(chaiHttp);

describe('candidatesList', () => {
  it('should retreive all candidates on /candidates GET', () => {
    chai.request(server)
    .get('/candidates')
    .end((err, res) => {
      expect(res).have.have.status(200);
      expect(res.body).to.have.length.of.at.least(3);
      expect(res.body).to.be.an('array');
      expect(res.body).to.not.be.empty;
    });
  });

});
