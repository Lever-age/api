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
var Campaign = require('../../objects/campaign-info');
var CampaignSummary = require('../../objects/campaign-summary');

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
          row,
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
    let summaryPromises = [];
    db.open(this.dbpath)
      .then((db) => db.all('SELECT * FROM candidate_info'))
      .then((rows) => rows.map((row) => Promise.all([
         row,
         db.prepare('SELECT * FROM campaign_info WHERE candidate_id = ?')
         .then((stmt) => stmt.all(row.candidate_id))
       ])
      ))
      .then((allCandidates) => {
        allCandidates.map((cnd) =>
          cnd.then((candidateParts) => {
            candidateParts.reduce((candidate, cmp) => Object.assign(candidate, {campaigns: cmp}));
            // remove last index that's no longer needed.
            candidateParts.pop();

            /*candidateParts.map((cnds) => {
              cnds.campaigns.map((campaign) => {
                let campaign_summary = Promise.resolve(db.prepare('SELECT * FROM campaign_summary WHERE campaign_id = ?')
                .then((stmt) => stmt.all(campaign.campaign_id)));
                return Object.assign(campaign, { campaign_summary });
              });
            });
            */
        }
        ));
        return Promise.all(allCandidates);
        }
      )
      .then((candidatesRes) => {
        return candidatesRes.map((candidate) => {
          // flatten it out
           return new Candidate(candidate.reduce((a,b) => a));
        });
      }).then((candidates) => {
        cb(undefined, candidates);
      })
      .catch((err) => cb(err));
  }
}

module.exports = CandidateStorage;
