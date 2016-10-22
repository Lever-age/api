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

var db = require('sqlite');
var CampaignInfo = require('../../objects/campaign-info');

/** @class */
class CampaignInfoStorage {
  constructor (params) {
    this.dbpath = params.path;
  }
}

/**
 * Fetch a CampaignInfo object by id
 *
 * @param {Number} id
 * @param {campaignInfoProcessor} cb
 */
CampaignInfoStorage.prototype.fetch_by_id = function (id, cb) {
  db.open(this.dbpath)
    .then((db) => db.prepare('SELECT * FROM campaign_info WHERE campaign_id = ?'))
    .then((stmt) => stmt.get(id))
    .then((row) => cb(undefined, new CampaignInfo(row)))
    .catch((err) => cb(err));
};

module.exports = CampaignInfoStorage;
