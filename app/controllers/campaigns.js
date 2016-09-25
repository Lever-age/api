var express = require('express'),
  router = express.Router(),
  path = require('path'),
  Candidate = require('../models/candidate'),
  CampaignDAO = require('../models/campaign');
  
  var campaign = new CampaignDAO();

  //Do this so that the app can access this file. 
  module.exports = function(app){
      app.use('/campaigns', router);
  }

router.get('/', function(req, res){
    try{
        campaign.getCampaigns().then(function(campaigns){
            console.log(campaigns);
            res.json(campaigns);
        });
    }catch(e){
        console.log(e);
        console.log(e.stack);
        res.json({error: "There has been an error."})
    }
});

router.get('/info', function(req, res){

});