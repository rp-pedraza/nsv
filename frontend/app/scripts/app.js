'use strict';

var app = angular.module('frontendApp', [
  'ngResource',
  'ngRoute',
  'chart.js',
  'angular-advanced-searchbox'
]);

app.config(function ($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'views/main.html',
      controller: 'MainCtrl'
    })
    .when('/scans', {
      templateUrl: 'views/scans.html',
      controller: 'ScansCtrl'
    })
    .when('/scans/:id', {
        templateUrl: 'views/scan-details.html',
        controller: 'ScanDetailsCtrl'
    })
    .when('/ports-frequency', {
      templateUrl: 'views/ports-frequency.html',
      controller: 'PortsFrequencyCtrl'
    })
    .when('/activity', {
      templateUrl: 'views/activity.html',
      controller: 'ActivityCtrl'
    })
    .otherwise({
      redirectTo: '/'
    });
});
