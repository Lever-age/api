var sqlite = require('sqlite3').verbose(),
db = new sqlite.Database(__dirname + '/leverage.sqlite'),
Campaign = require('../objects/campaign');


module.exports = function CampaignDAO(){

    this.getCampaigns = function getAllCampaignInfo(){
        return getCampaignInfo().then(function(data){
                return data;
        }).catch(function(err){
                console.log(err);
                return {error: "There has been an error"};
        })
    }

    function getCampaignInfo(){
        return new Promise(function(resolve, reject){
            db.all('SELECT * FROM campaign_info', function(err, data){
                if(err){
                    console.log(err);
                    reject(err);
                }else{
                    console.log(JSON.stringify(data));
                    resolve(data);
                }
                return;
            });
        });
    }

}