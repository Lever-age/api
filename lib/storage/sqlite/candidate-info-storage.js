'use strict';

/**
 * Sqlite backed implementation
 * of CandidateInfoStorage
 * @file candidate-info-storage.js
 */

/**
 * @callback candidateInfoProcessor
 * @param {Error} err
 * @param {CandidateInfo} obj
 */

var db = require('sqlite');
var CandidateInfo = require('../../objects/candidate-info');

/** @class */
class CandidateInfoStorage {
  constructor (params) {
    this.dbpath = params.path;
  }
}

/**
 * Fetch a CandidateInfo object by
 * an associated campaign id
 *
 * @param {Number} id
 * @param {candidateInfoProcessor} cb
 */
CandidateInfoStorage.prototype.fetch_by_campaign = function (id, cb) {
  db.open(this.dbpath)
    .then((db) => db.prepare(
      'SELECT cd.candidate_id, cd.candidate_name FROM candidate_info AS cd ' +
      'JOIN campaign_info AS cp ON cd.candidate_id = cp.candidate_id ' +
      'WHERE cp.campaign_id = ?'
    ))
    .then((stmt) => stmt.get(id))
    .then((row) => cb(undefined, new CandidateInfo(row)))
    .catch((err) => cb(err));
};

module.exports = CandidateInfoStorage;
