'use strict';

var app = angular.module('frontendApp');

app.factory('Search', function ($resource) {
  return $resource(config.backend_api_base_uri_path + '/search', {},
    {
      query: {
        method: 'GET',
        transformResponse: function (data) {
          if (data == null) {
            return [];
          }

          var array = angular.fromJson(data);

          array.forEach(function (scan) {
            addFormattedFields(scan);
          });

          return array;
        },
        isArray: true,
        interceptor : {
          responseError : responseErrorHandler
        },
        responseType: "json",
        headers: {
          "Content-Type": "application/json"
        }
      }
    });
});

app.controller('MainCtrl', function ($scope, Search) {
  $scope.availableSearchParams = [
    { key: "identity", name: "Identity", placeholder: "Identity..." },
    { key: "address", name: "Address", placeholder: "Address..." },
    { key: "hostname", name: "Hostname", placeholder: "Hostname..." },
    { key: "state", name: "State", placeholder: "State..." },
    { key: "tcpports", name: "TCP Ports", placeholder: "TCP Ports..." },
    { key: "udpports", name: "UDP Ports", placeholder: "UDP Ports..." }
  ];

  $scope.$on('advanced-searchbox:modelUpdated', function (event, model) {
    var params = $scope.searchParams;
    $scope.scans = Search.query(params);
  });
});
