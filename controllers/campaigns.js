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
  extern.backend.fetch_by_id(req.params.id, function (err, ci) {
    if (err) {
      extern.logger.log('error', 'campaigninfoById: %s: %s', err.name, err.message);
      return res.sendStatus(500);
    }
    res.json(ci);
  });
};
