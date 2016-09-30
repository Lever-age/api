
/* External modules */

var fs = require('fs')
var express = require('express');
var winston = require('winston');

/* Library modules */

var CampaignInfoStorage = require('./lib/storage/sqlite/campaign-info-storage');

/* Controllers */

var campaigninfo_by_id = require('./controllers/campaigns').campaigninfo_by_id;

/* App variables */

var app = express();
var config = JSON.parse(fs.readFileSync('config.json'));
var extern = new Object();

extern.logger = winston;

/* Endpoints */

app.get('/campaigns/:id/info', function (req, res) {
  extern.backend = new CampaignInfoStorage(config.storage);
  campaigninfo_by_id(extern, req, res);
});

/* Initialize */

app.listen(config.bind.port, config.bind.address, function () {
  extern.logger.log('info', 'API listening on port %d', config.bind.port)
});
