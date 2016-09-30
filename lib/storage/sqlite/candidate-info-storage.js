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

var sqlite3 = require('sqlite3');
var CandidateInfo = require('../../objects/candidate-info');

/** @class */
function CandidateInfoStorage (params) {
  this.db = new sqlite3.Database(params.path);
}

/**
 * Fetch a CandidateInfo object by
 * an associated campaign id
 *
 * @param {Number} id
 * @param {candidateInfoProcessor} cb
 */
CandidateInfoStorage.prototype.fetch_by_campaign = function (id, cb) {
  var stmt = this.db.prepare(
    'SELECT cd.candidate_id, cd.candidate_name FROM candidate_info AS cd ' +
    'JOIN campaign_info AS cp ON cd.candidate_id = cp.candidate_id ' +
    'WHERE cp.campaign_id = ?'
    , function (err) {
    if (err) cb(err);
  });
  stmt.get(id, function (err, row) {
    if (err) return cb(err);
    cb(undefined, new CandidateInfo(row));
  });
};

module.exports = CandidateInfoStorage;
