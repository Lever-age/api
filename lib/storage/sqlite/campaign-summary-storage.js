'use strict';

/**
 * Sqlite backed implementation
 * of CampaignSummaryStorage
 * @file campaign-summary-storage.js
 */

/**
 * @callback campaignSummaryProcessor
 * @param {Error} err
 * @param {CampaignSummary} obj
 */

var db = require('sqlite');
var CampaignSummary = require('../../objects/campaign-summary');

/** @class */
class CampaignSummaryStorage {

  constructor (params) {
    this.dbpath = params.path;
  }

  /**
   * Fetch all CampaignSummary objects
   * associated with the campaign of
   * the specified id
   *
   * @param {Number} id
   * @param {campaignSummaryProcessor} cb
   */
  fetchById (id, cb) {
    db.open(this.dbpath)
    .then((db) => db.prepare('SELECT *  FROM campaign_summary WHERE campaign_id = ?'))
    .then((stmt) => stmt.all(id))
    .then((rows) => rows.map((row) => new CampaignSummary(row)))
    .then((summaries) => cb(undefined, summaries))
    .catch((err) => cb(err));
  }

}

module.exports = CampaignSummaryStorage;
