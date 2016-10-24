'use strict';

/**
 * Sqlite backed implementation
 * of CampaignStorage
 * @file campaign-storage.js
 */

/**
 * @callback campaignProcessor
 * @param {Error} err
 * @param {Campaign} obj
 */

var db = require('sqlite');
var Campaign = require('../../objects/campaign');

/** @class */
class CampaignStorage {

  constructor (params) {
    this.dbpath = params.path;
  }

  /**
  * Fetch a Campaign object by id
  *
  * @param {Number} id
  * @param {candidateProcessor} cb
  */
  fetchById (id, cb) {
    db.open(this.dbpath)
      .then((db) => db.prepare(
        'SELECT * FROM candidate_info cn ' +
        'JOIN campaign_info cp ON cp.candidate_id = cn.candidate_id ' +
        'WHERE cp.campaign_id = ?'
      ))
      .then((smt) => smt.get(id))
      .then((row) => Promise.all([
        Promise.resolve(row),
        db.prepare('SELECT * FROM campaign_summary WHERE campaign_id = ?')
        .then((stmt) => stmt.all(id))
      ]))
      .then((campaignParts) => campaignParts.reduce(
        (campaign, summary) => Object.assign(campaign, {campaign_summary: summary})
      ))
      .then((params) => cb(undefined, new Campaign(params)))
      .catch((err) => cb(err));
  }

}

module.exports = CampaignStorage;
