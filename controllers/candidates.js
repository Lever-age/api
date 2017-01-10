'use strict';

/**
 * Controllers for endpoints under /candidates
 * @file candidates.js
 */

/**
 * Return a candidate object
 * of the specified id
 *
 * @param {Object} extern
 * @param {Object} req
 * @param {Object} res
 */
module.exports.candidateById = function (extern, req, res) {
  extern.backend.fetchById(req.params.id, function (err, cdt) {
    if (err) {
      extern.logger.log('error', 'candidateById: %s: %s', err.name, err.message);
      return res.sendStatus(500);
    }
    res.json(cdt);
  });
};

/**
 * Return a campaign info
 * object for the campaign
 * associated with the candidate
 * of the specified id
 *
 * @param {Object} extern
 * @param {Object} req
 * @param {Object} res
 */
module.exports.campaignInfoByCandidate = function (extern, req, res) {
  extern.backend.fetchByCampaign(req.params.id, function (err, ci) {
    if (err) {
      extern.logger.log('error', 'campaignInfoByCandidate: %s: %s', err.name, err.message);
      return res.sendStatus(500);
    }
    res.json(ci);
  });
};

/**
 * Return all Campaign objects
 * associated with the candidate
 * of the specified id
 *
 * @param {Object} extern
 * @param {Object} req
 * @param {Object} res
 */
module.exports.campaignsByCandidate = function (extern, req, res) {
  extern.backend.fetchByCandidate(req.params.id, function (err, cmps) {
    if (err) {
      extern.logger.log('error', 'campaignsByCandidate: %s: %s', err.name, err.message);
      return res.sendStatus(500);
    }
    res.json(cmps);
  });
};

/**
 * Return all candidate objects
 *
 * @param {Object} extern
 * @param {Object} req
 * @param {Object} res
 */
module.exports.candidates = function (extern, req, res) {
  extern.backend.fetchAll(function (err, cmps) {
    if (err) {
      extern.logger.log('error', 'candidates: %s: %s', err.name, err.message);
      return res.sendStatus(500);
    }
    res.json(cmps);
  });
};
