'use strict';

/* External modules */

var fs = require('fs');
var express = require('express');
var winston = require('winston');

/* Library modules */

var CampaignInfoStorage = require('./lib/storage/sqlite/campaign-info-storage');
var CandidateInfoStorage = require('./lib/storage/sqlite/candidate-info-storage');
var CandidateStorage = require('./lib/storage/sqlite/candidate-storage');
var CampaignSummaryStorage = require('./lib/storage/sqlite/campaign-summary-storage');
var CampaignStorage = require('./lib/storage/sqlite/campaign-storage');

/* Controllers */

var campaigninfoById = require('./controllers/campaigns').campaigninfoById;
var candidateinfoByCampaign = require('./controllers/campaigns').candidateinfoByCampaign;
var campaignInfo = require('./controllers/campaigns').campaignInfo;
var campaignInfoByCandidate = require('./controllers/candidates').campaignInfoByCandidate;
var candidateById = require('./controllers/candidates').candidateById;
var campaignsummaryById = require('./controllers/campaigns').campaignsummaryById;
var campaignById = require('./controllers/campaigns').campaignById;
var campaigns = require('./controllers/campaigns').campaigns;
var candidates = require('./controllers/candidates').candidates;

/* App variables */

var cfgPath = process.env.LEVERAGE_API_CFG || process.argv[2] || 'config.json';
var app = express();
var config = JSON.parse(fs.readFileSync(cfgPath));
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

app.get('/candidates/:id/campaigns/info', function (req, res) {
  extern.backend = new CampaignInfoStorage(config.storage);
  campaignInfoByCandidate(extern, req, res);
});

app.get('/candidates/:id', function (req, res) {
  extern.backend = new CandidateStorage(config.storage);
  candidateById(extern, req, res);
});

app.get('/campaigns/:id/summary', function (req, res) {
  extern.backend = new CampaignSummaryStorage(config.storage);
  campaignsummaryById(extern, req, res);
});

app.get('/campaigns/:id', function (req, res) {
  extern.backend = new CampaignStorage(config.storage);
  campaignById(extern, req, res);
});

app.get('/campaigns', function (req, res) {
  extern.backend = new CampaignStorage(config.storage);
  campaigns(extern, req, res);
});

app.get('/candidates', function (req, res) {
  extern.backend = new CandidateStorage(config.storage);
  candidates(extern, req, res);
});

/* Initialize */

app.listen(config.listen.port, config.listen.address, function () {
  extern.logger.log('info', 'API listening on port %d', config.listen.port);
});

module.exports = app;
