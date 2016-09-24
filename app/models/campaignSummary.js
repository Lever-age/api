module.exports = function CampaignSummary(){

    var Sequelize = require('sequelize');
    var sequelize = new Sequelize('leverage', null, null, {
        // sqlite! now!
        dialetc: 'sqlite',
        storage: 'leverage.sqlite'
    });

    var CampaignSummary = sequelize.define('campaign_summary', {
        campaign_id: Sequelize.INTEGER,
        donation_amount: Sequelize.REAL,
        donation_count: Sequelize.INTEGER
    });

}