'use strict';

var expect                  = require('chai').expect;
var candidateinfoByCampaign = require('../controllers/campaigns').candidateinfoByCampaign;

describe('candidateinfoByCampaign', function(){
  var req = {
    params: {}
  };
  it('sends the retrieved object as a response', function(done){
    var backend = {
      fetch_by_campaign: function(id, cb){ cb(undefined, 'response content'); }
    };
    var res = {
      json: function(content){
        expect(content, 'unexpected response content').to.equal('response content');
        done();
      }
    };
    candidateinfoByCampaign({backend: backend}, req, res);
  });
  it('logs and sends error response', function(done){
    var backend = {
      fetch_by_campaign: function(id, cb){ cb({name: 'test error', message: 'error content'}); }
    };
    var logger = {
      log: function(level, format, name, message){
        expect(level, 'incorrect log level specified').to.equal('error');
        expect(format, 'unexpected format string').to.equal('candidateinfoByCampaign: %s: %s');
        expect(name, 'unexpected error name').to.equal('test error');
        expect(message, 'unexpected error message').to.equal('error content');
      }
    };
    var res = {
      sendStatus: function(rcode){
        expect(rcode, 'Unexpected response code').to.equal(500);
        done();
      }
    };
    candidateinfoByCampaign({backend: backend, logger: logger}, req, res);
  });
});
