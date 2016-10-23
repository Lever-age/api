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
