var Promise = require('bluebird'),
        sqlite = require('sqlite3').verbose(),
        db = new sqlite.Database('./leverage.sqlite');

module.exports = function Candidate(){

    this.getAll = function getAllCandidateInfo(cb){
        return db.all('SELECT * FROM campaign_info', cb);
    }

}