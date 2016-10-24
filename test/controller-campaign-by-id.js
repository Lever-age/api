'use strict';

var expect           = require('chai').expect;
var campaignById = require('../controllers/campaigns').campaignById;

describe('campaignById', () => {
  var req = {
    params: {}
  };
  it('sends the retrieved object as a response', (done) => {
    var backend = {
      fetchById: (id, cb) => cb(undefined, 'response content')
    };
    var res = {
      json: (content) => {
        expect(content, 'unexpected response content').to.equal('response content');
        done();
      }
    };
    campaignById({backend: backend}, req, res);
  });
  it('logs and sends error response', (done) => {
    var backend = {
      fetchById: (id, cb) => cb({name: 'test error', message: 'error content'})
    };
    var logger = {
      log: (level, format, name, message) => {
        expect(level, 'incorrect log level specified').to.equal('error');
        expect(format, 'unexpected format string').to.equal('campaignById: %s: %s');
        expect(name, 'unexpected error name').to.equal('test error');
        expect(message, 'unexpected error message').to.equal('error content');
      }
    };
    var res = {
      sendStatus: (rcode) => {
        expect(rcode, 'Unexpected response code').to.equal(500);
        done();
      }
    };
    campaignById({backend: backend, logger: logger}, req, res);
  });
});
