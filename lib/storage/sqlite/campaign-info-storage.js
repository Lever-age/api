'use strict';

/**
 * Sqlite backed implementation
 * of CampaignInfoStorage
 * @file campaign-info-storage.js
 */

/**
 * @callback campaignInfoProcessor
 * @param {Error} err
 * @param {CampaignInfo} obj
 */

var sqlite3 = require('sqlite3');
var CampaignInfo = require('../../objects/campaign-info');

/** @class */
function CampaignInfoStorage (params) {
  this.db = new sqlite3.Database(params.path);
}

/**
 * Fetch a CampaignInfo object by id
 *
 * @param {Number} id
 * @param {campaignInfoProcessor} cb
 */
CampaignInfoStorage.prototype.fetch_by_id = function (id, cb) {
  var stmt = this.db.prepare('SELECT * FROM campaign_info WHERE campaign_id = ?');
  stmt.get(id, function (err, row) {
    if (err) return cb(err);
    cb(undefined, new CampaignInfo(row));
  });
};

module.exports = CampaignInfoStorage;
