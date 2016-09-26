var sqlite = require('sqlite3').verbose(),
db = new sqlite.Database(__dirname + '/leverage.sqlite'),
Campaign = require('../objects/campaign');
//https://github.com/mapbox/node-sqlite3/wiki/API

module.exports = function CampaignDAO(){

    this.getCampaigns = function getAllCampaigns(callback){
        return getAllCampaignInfo().then(function(data){
            addCampaignSummary(data).then(function(){
                
            });
        }).catch(function(err){
                console.log(err);
                return {error: "There has been an error"};
        })
    }

    function getAllCampaignInfo(){
        return new Promise(function(resolve, reject){
            db.all('SELECT * FROM campaign_info', function(err, data){
                if(err){
                    console.log(err);
                    reject(err);
                }else{
                    resolve(data);
                }
                return;
            });
        });
    }

    function makeCampaignObjects(campaigns){

    }

    function getCampaignSummaries(campaignId, cb){
        return db.all("SELECT * FROM campaign_summary WHERE campaign_id = $id", { 
            $id: campaignId
        },
        function(err, data){
        if(err){
                console.log(err);
                return {error: "There was an error."};
        }else{
                return cb(data);
        }
        })
    }

}