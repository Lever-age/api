var express = require('express'),
  router = express.Router(),
  path = require('path'),
  mongoose = require('mongoose');


module.exports = function (app) {
  app.use('/', router);
};

router.get('/', function (req, res, next) {
  res.sendFile(path.dirname(require.main.filename) + "/index.html");
});
