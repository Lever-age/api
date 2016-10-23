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

var Candidate = require('../../objects/candidate');
var CampaignInfo = require('../../objects/campaign-info');

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
    var arrCandidates = [];
    db.open(this.dbpath)
      .then((db) => db.all('SELECT * FROM candidate_info'))
      .then((rows) => {
        var campaignPromises = [];

        rows.forEach((row) => {
          let candidate = new Candidate(row);
          candidate.campaigns = [];
          arrCandidates[row.candidate_id] = candidate;

          // get campaigns
          campaignPromises.push(db.all('SELECT * FROM campaign_info WHERE candidate_id = ?', row.candidate_id)
          .then((campaigns) => campaigns));
        });

        return Promise.all(campaignPromises);
      }).then((campaigns) => {
        var campaignCandidateId;
        // arrCandidates.sort((a, b) => {
          // return a - b;
        // });
        for (let i = 0; i < campaigns.length; i++) {
          campaignCandidateId = campaigns[i][0].candidate_id;
          if (arrCandidates[campaignCandidateId]) {
            arrCandidates[campaignCandidateId].campaigns = campaigns[i];
          }
        }

        console.log(arrCandidates[0]);

        cb(undefined, arrCandidates);
      })
      .catch((err) => cb(err));
  }
}
module.exports = CandidatesStorage;
