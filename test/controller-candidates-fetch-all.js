'use strict';

var fs = require('fs');
// var winston = require('winston');
var chai = require('chai');
var expect = require('chai').expect;
var chaiHttp = require('chai-http');
var server = require('../app');
// var config = JSON.parse(fs.readFileSync('config.test.json'));
// var extern = { logger: winston };
// var CandidateStorage = require('../lib/storage/sqlite/candidates');
// var candidatesList = require('../controllers/candidates').candidatesList;

chai.use(chaiHttp);

describe('candidatesList', () => {
  var req = {
    params: {}
  };

  it('should retreive all candidates on /candidates GET', () => {
    chai.request(server)
    .get('/candidates/all')
    .end((err, res) => {
      res.should.have.status(200);
      expect(res.body).to.be.an('object');
      expect(res.body).to.not.be.empty;
      done();
    });
  });

});
