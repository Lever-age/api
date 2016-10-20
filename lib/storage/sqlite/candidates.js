'use strict';

/**
 * Sqlite backed implementation
 * of CandidateStorage
 * @file candidates-storage.js
 */

/**
 * @callback candidateProcessor
 * @param {Error} err
 * @param {CandidateInfo} obj
 */

var db = require('sqlite');

var CandidateObj = require('../../objects/candidate');
// var CampaignInfoObj = require('../../objects/campaign-info');

/**
 * Candidate Storage class
 * @class CandidatesStorage
 */
class CandidatesStorage {
  /**
   * Constructor
   * @param {any} cb
   * @memberOf CandidatesStorage
  */
  constructor (params) {
    this.dbpath = params.path;
  }

  /**
   * Fetch an array of Candidate objects by
   * @param {candidateProcessor} callback
   */
  fetchAll (cb) {
    db.open(this.dbpath)
      .then((db) => db.all('SELECT * FROM candidate_info'))
      .then((rows) => {
        rows.forEach((row) => {
          // campaigns
          db.get('SELECT * FROM campaign_info WHERE candidate_id = ?', row.candidate_id)
          .then((campaigns) => {
            row.campaigns = campaigns;
            return row;
          });

          return new CandidateObj(row);
        });
        cb(undefined, rows);
      })
      .catch((err) => cb(err));
  }
}
module.exports = CandidatesStorage;
