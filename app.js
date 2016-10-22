'use strict';

/* External modules */

var fs = require('fs');
var express = require('express');
var winston = require('winston');

/* Library modules */

var CampaignInfoStorage = require('./lib/storage/sqlite/campaign-info-storage');
var CandidateInfoStorage = require('./lib/storage/sqlite/candidate-info-storage');

/* Controllers */

var campaigninfoById = require('./controllers/campaigns').campaigninfoById;
var candidateinfoByCampaign = require('./controllers/campaigns').candidateinfoByCampaign;
var campaignInfo = require('./controllers/campaigns').campaignInfo;

/* App variables */

var app = express();
var config = JSON.parse(fs.readFileSync('config.json'));
var extern = { logger: winston };

/* Endpoints */

app.get('/campaigns/:id/info', function (req, res) {
  extern.backend = new CampaignInfoStorage(config.storage);
  campaigninfoById(extern, req, res);
});

app.get('/campaigns/:id/candidate', function (req, res) {
  extern.backend = new CandidateInfoStorage(config.storage);
  candidateinfoByCampaign(extern, req, res);
});

app.get('/campaigns/info', function (req, res) {
  extern.backend = new CampaignInfoStorage(config.storage);
  campaignInfo(extern, req, res);
});

/* Initialize */

app.listen(config.listen.port, config.listen.address, function () {
  extern.logger.log('info', 'API listening on port %d', config.listen.port);
});

module.exports = app;
