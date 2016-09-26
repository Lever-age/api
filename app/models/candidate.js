var sqlite = require('sqlite3').verbose(),
    path = require('path'),
    db = new sqlite.Database(__dirname + '/leverage.sqlite'),
    Candidate = require('../objects/candidate');
        
module.exports = function Candidate(){

    this.getAll = function getAllCandidateInfo(cb){
        return db.all('SELECT * FROM campaign_info', cb);
    }

}