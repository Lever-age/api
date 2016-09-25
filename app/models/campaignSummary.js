var Promise = require('bluebird'),
        sqlite = require('sqlite3').verbose(),
        db = new sqlite.Database(__dirname + '/leverage.sqlite');

module.exports = function CampaignSummary(){

    this.getAll = function getAllSummaryInfo(cb){
        return db.all('SELECT * FROM campaign_info', cb);
    }

}