'use strict';

/**
 * Controllers for endpoints under /campaigns
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
