'use strict';

/**
 * Sqlite backed implementation
 * of CandidateStorage
 * @file candidate-storage.js
 */

/**
 * @callback candidateProcessor
 * @param {Error} err
 * @param {Candidate} obj
 */

var db = require('sqlite');
var Candidate = require('../../objects/candidate');

/** @class */
class CandidateStorage {
  constructor (params) {
    this.dbpath = params.path;
  }

  /**
  * Fetch a CandidateInfo object by
  * an associated campaign id
  *
  * @param {Number} id
  * @param {candidateProcessor} cb
  */
  fetchById (id, cb) {
    db.open(this.dbpath)
      .then((db) => db.prepare(
        'SELECT * FROM candidate_info cn ' +
        'JOIN campaign_info cp ON cp.candidate_id = cn.candidate_id ' +
        'WHERE cp.candidate_id = ?'
      ))
      .then((stmt) => stmt.all(id))
      .then((rows) => Promise.all(
        rows.map((row) => Promise.all([
          Promise.resolve(row),
          db.prepare(
            'SELECT * FROM campaign_summary ' +
            'WHERE campaign_id = ?'
          ).then((stmt) => stmt.all(row.campaign_id))
        ]))
      ))
      .then((campaignsData) => campaignsData.map(
        (campaignParts) => campaignParts.reduce(
          (campaign, summary) => Object.assign(campaign, {campaign_summary: summary})
        )
      ))
      .then((campaigns) => cb(
        undefined,
        new Candidate({
          candidate_id: campaigns[0].candidate_id,
          candidate_name: campaigns[0].candidate_name,
          campaigns: campaigns
        })
      ))
      .catch((err) => cb(err));
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
          arrCandidates[row.candidate_id] = candidate;

          // get campaigns
          campaignPromises.push(db.all('SELECT * FROM campaign_info WHERE candidate_id = ?', row.candidate_id)
          .then((campaigns) => campaigns));
        });

        return Promise.all(campaignPromises);
      }).then((campaigns) => {
        var campaignCandidateId;
        for (let i = 0; i < campaigns.length; i++) {
          campaignCandidateId = campaigns[i][0].candidate_id;
          if (arrCandidates[campaignCandidateId]) {
            arrCandidates[campaignCandidateId].campaigns = campaigns[i];
          }
        }

        // remove arrCandidates index of null
        arrCandidates.splice(0, 1);

        cb(undefined, arrCandidates);
      })
      .catch((err) => cb(err));
  }
}

module.exports = CandidateStorage;
