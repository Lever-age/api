module.exports = function Candidate(){

    var Sequelize = require('sequelize');
    var sequelize = new Sequelize('/srv/leverage/leverage.sqlite', 'u', 'p');

    var Candidate = sequelize.define('candidate', {
        candidate_id: Sequelize.INTEGER,
        candidate_name: Sequelize.TEXT
    });

}