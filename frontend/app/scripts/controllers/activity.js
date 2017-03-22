'use strict';

var app = angular.module('frontendApp');

app.controller('ActivityCtrl', function ($scope, $http) {
  $http
    .get(config.backend_server + '/activity')
    .then(
      function (response) {
        var array = response.data.sort(function (a, b) {
          var x = a.datetime;
          var y = b.datetime;

          if (x == y) {
            return 0;
          } else if (x > y) {
            return 1;
          } else {
            return -1;
          }
        });

        $scope.labels = jQuery.map(array, function (e) {
          return e.identity;
        });
        
        $scope.data = jQuery.map(array, function (e) {
          return e.level;
        });
      },
      function (response) {
        responseErrorHandler(response);
      }
    );

  $scope.series = ['Activity'];
  $scope.labels = [];
  $scope.data = [[]];
});
