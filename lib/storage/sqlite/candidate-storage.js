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
    var candidateParams = { campaigns: [] };
    db.open(this.dbpath)
      .then((db) => db.prepare(
        'SELECT * FROM candidate_info cn ' +
        'JOIN campaign_info cp ON cp.candidate_id = cn.candidate_id ' +
        'WHERE cp.candidate_id = ?'
      ))
      .then((stmt) => stmt.all(id))
      .then((rows) => {
        var summaryPromises = [];
        rows.forEach((row) => {
          candidateParams.campaigns.push(row);
          summaryPromises.push(
            db.prepare(
              'SELECT * FROM campaign_summary ' +
              'WHERE campaign_id = ?'
            ).then((stmt) => stmt.all(row.campaign_id))
          );
        });
        return Promise.all(summaryPromises);
      })
      .then((summaries) => {
        for (let i = 0; i < candidateParams.campaigns.length; i++) {
          candidateParams.campaigns[i].campaign_summary = summaries[i];
        }
        candidateParams.candidate_id = candidateParams.campaigns[0].candidate_id;
        candidateParams.candidate_name = candidateParams.campaigns[0].candidate_name;
        cb(undefined, new Candidate(candidateParams));
      })
      .catch((err) => cb(err));
  }
}

module.exports = CandidateStorage;
