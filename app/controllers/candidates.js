var express = require('express'),
  router = express.Router(),
  path = require('path'),
  CampaignInfo = require('../models/campaignInfo'),
  Candidate = require('../models/candidate'),
  CampaignSummary = require('../models/campaignSummary');
  
  //Do this so that the app can access this file. 
  module.exports = function(app){
      app.use('/candidates', router);
  }

  //We're gonna return a list of all users'
  router.get('/', function(req, res){    
      res.json({"x": "y"});
      res.end();
  });

  //We send the ID
  router.get('/:id', function(req, res){ 
      var id = req.params.id;

      res.json({id: id});
      res.end();
  });
