'use strict';

/**
 * Controllers for endpoints under /campaigns
 * @file campaigns.js
 */

/**
 * Return a campaign info object
 * of the specified id
 *
 * @param {Object} extern
 * @param {Object} req
 * @param {Object} res
 */
module.exports.campaigninfoById = function (extern, req, res) {
  extern.backend.fetchById(req.params.id, function (err, ci) {
    if (err) {
      extern.logger.log('error', 'campaigninfoById: %s: %s', err.name, err.message);
      return res.sendStatus(500);
    }
    res.json(ci);
  });
};

/**
 * Return a candidate info
 * object for the candidate
 * associated with the campaign
 * of the specified id
 *
 * @param {Object} extern
 * @param {Object} req
 * @param {Object} res
 */
module.exports.candidateinfoByCampaign = function (extern, req, res) {
  extern.backend.fetch_by_campaign(req.params.id, function (err, ci) {
    if (err) {
      extern.logger.log('error', 'candidateinfoByCampaign: %s: %s', err.name, err.message);
      return res.sendStatus(500);
    }
    res.json(ci);
  });
};

/**
 * Return all campaigns info objects
 * object for the candidate
 * associated with the campaign
 * of the specified id
 *
 * @param {Object} extern
 * @param {Object} req
 * @param {Object} res
 */
module.exports.campaignInfo = function (extern, req, res) {
  extern.backend.fetchAll(function (err, ci) {
    if (err) {
      extern.logger.log('error', 'campaignInfo: %s: %s', err.name, err.message);
      return res.sendStatus(500);
    }
    res.json(ci);
  });
};

/**
 * Return an array of all
 * campaign summary objects
 * associated with the campaign
 * of the specified id
 *
 * @param {Object} extern
 * @param {Object} req
 * @param {Object} res
 */
module.exports.campaignsummaryById = function (extern, req, res) {
  extern.backend.fetchById(req.params.id, function (err, summaries) {
    if (err) {
      extern.logger.log('error', 'campaignsummaryById: %s: %s', err.name, err.message);
      return res.sendStatus(500);
    }
    res.json(summaries);
  });
};

/**
 * Return the campaign of the specified id
 *
 * @param {Object} extern
 * @param {Object} req
 * @param {Object} res
 */
module.exports.campaignById = function (extern, req, res) {
  extern.backend.fetchById(req.params.id, function (err, cmp) {
    if (err) {
      extern.logger.log('error', 'campaignById: %s: %s', err.name, err.message);
      return res.sendStatus(500);
    }
    res.json(cmp);
  });
};

/**
 * Return all campaign objects
 *
 * @param {Object} extern
 * @param {Object} req
 * @param {Object} res
 */
module.exports.campaigns = function (extern, req, res) {
  extern.backend.fetchAll(function (err, cmps) {
    if (err) {
      extern.logger.log('error', 'campaigns: %s: %s', err.name, err.message);
      return res.sendStatus(500);
    }
    res.json(cmps);
  });
};
