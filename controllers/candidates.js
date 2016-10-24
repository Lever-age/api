'use strict';

/**
 * Controllers for endpoints under /candidates
 * @file candidates.js
 */

/**
 * Return an array of candidates object
 *
 * @param {Object} extern
 * @param {Object} req
 * @param {Object} res
 */
module.exports.candidatesList = (extern, req, res) => {
  extern.backend.fetchAll((err, allCandidates) => {
    if (err) {
      extern.logger.log('error', 'candidatesList: %s: %s', err.name, err.message);
      return res.sendStatus(500);
    }
    res.json(allCandidates);
  });
};

/**
 * Return an candidate object of the specified id
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
