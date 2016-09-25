var Promise = require('bluebird'),
        sqlite = require('sqlite3').verbose(),
        db = new sqlite.Database(__dirname + '/leverage.sqlite'),
        Campaign = require('../models/campaign');

module.exports = function CampaignDAO(){

    this.getAll = function getAllCampaignInfo(cb){
            db.all('SELECT * FROM campaign_info', cb);
    }

}