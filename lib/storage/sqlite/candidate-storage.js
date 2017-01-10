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
   * Fetch all Candidate objects
   *
   * @param {candidateProcessor} cb
   */
  fetchAll (cb) {
    db.open(this.dbpath)
       // First, build an array of all candidate_info objects
      .then((db) => db.prepare('SELECT * FROM candidate_info'))
      .then((stmt) => stmt.all())
      .then((rows) => rows.map((row) => new Candidate({
        candidate_id: row.candidate_id,
        candidate_name: row.candidate_name
      })))
      /* Then build an array of 2 element arrays
       * in which the elements are
       * [ candidate_info, campaign_info_array ]
       */
       .then((candidates) => Promise.all(
         candidates.map((candidate) => Promise.all([
           Promise.resolve(candidate),
           db.prepare(
             'SELECT * FROM campaign_info ' +
             'WHERE candidate_id = ?'
           ).then((stmt) => stmt.all(candidate.candidate_id))
         ]))
       ))
       /* Then, rebuild the campaign_info_array
        * so that each element within is itself
        * a 2 element array with elements
        * [ campaign_info, campaign_summary_array ]
        */
       .then((candidatesWithCampaignInfo) => Promise.all(
         candidatesWithCampaignInfo.map(
           (candidateWithCampaignInfo) => Promise.all([
             Promise.resolve(candidateWithCampaignInfo[0]), // Candidate object
             Promise.all(
               candidateWithCampaignInfo[1].map( // CampaignInfo objects
                 (campaignInfo) => Promise.all([
                   Promise.resolve(campaignInfo),
                   db.prepare(
                     'SELECT * FROM campaign_summary ' +
                     'WHERE campaign_id = ?'
                   ).then((stmt) => stmt.all(campaignInfo.campaign_id))
                 ])
               )
             )
           ])
         )
       ))
       /* Then reduce all of the 2 element arrays
        * into a flattened array of Candidate objects
        */
      .then((candidatesWithCampaigns) => candidatesWithCampaigns.map(
        (candidateWithCampaigns) => candidateWithCampaigns.reduce(
          (candidate, campaigns) => Object.assign(
            candidate,
            {
              campaigns: campaigns.map((campaign) => campaign.reduce(
                (info, summary) => Object.assign(
                  info,
                  {
                    campaign_summary: summary,
                    candidate_name: candidate.candidate_name
                  }
                )
              ))
            }
          )
        )
      ))
      .then((candidates) => cb(undefined, candidates))
      .catch((err) => cb(err));
  }
}

module.exports = CandidateStorage;
