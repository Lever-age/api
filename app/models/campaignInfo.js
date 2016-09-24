module.exports = function CampaignInfo(){

    var Sequelize = require('sequelize');
    var sequelize = new Sequelize('/srv/leverage/leverage.sqlite', 'u', 'p');

    var CampaignInfo = sequelize.define('campaign_info', {
        campaign_id: Sequelize.INTEGER,
        election_year: Sequelize.TEXT,
        election_cycle: Sequelize.TEXT,
        candidate_id: Sequelize.TEXT,
        candidate_position: Sequelize.TEXT,
        candidate_party: Sequelize.TEXT
    });

}