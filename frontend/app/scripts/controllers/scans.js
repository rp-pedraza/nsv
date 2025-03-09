'use strict';

var app = angular.module('frontendApp');

app.factory('Scan', function ($resource) {
  return $resource(config.backend_api_base_uri_path + '/scans/:id', { id: '@id' }, {
    get: {
      method: 'GET',
      transformResponse: function (data) {
        data = data ? data : {};
        var scan = angular.fromJson(data);
        addFormattedFields(scan);
        return scan;
      },
      interceptor : {
        responseError : responseErrorHandler
      }
    }
  });
});

app.factory('Scans', function ($resource) {
  return $resource(config.backend_api_base_uri_path + '/scans', {}, {
    query: {
      method: 'GET',
      transformResponse: function (data) {
        data = data ? data : {};

        var array = angular.fromJson(data);

        array.sort(function (a, b) {
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

        array.forEach(function (scan) {
          addFormattedFields(scan);
        });

        return array;
      },
      isArray: true,
      interceptor: {
        responseError : responseErrorHandler
      }
    }
  });
});

app.controller('ScansCtrl', function ($scope, Scans) {
  $scope.scans = Scans.query();
});

app.controller('ScanDetailsCtrl', function ($scope, Scan, $routeParams) {
  $scope.scan = Scan.get({ id: $routeParams.id });
});
