'use strict';

var app = angular.module('frontendApp');

app.controller('PortsFrequencyCtrl', function () {});

app.controller('TCPPortsFrequencyBarCtrl', function ($http) {
  var thisCtrl = this;

  $http
    .get(config.backend_api_base_uri_path + '/ports-frequency')
    .then(
      function (response) {
        if ('tcp' in response.data) {
          var tcpPortsData = response.data.tcp;
          thisCtrl.labels = Object.keys(tcpPortsData);
          thisCtrl.data = Object.values(tcpPortsData);
        }
      },
      function (response) {
        responseErrorHandler(response);
      }
    );

  thisCtrl.labels = [];
  thisCtrl.data = [];
});

app.controller('UDPPortsFrequencyBarCtrl', function ($http) {
  var thisCtrl = this;

  $http
    .get(config.backend_api_base_uri_path + '/ports-frequency')
    .then(
      function (response) {
        if ('udp' in response.data) {
          var udpPortsData = response.data.udp;
          thisCtrl.labels = Object.keys(udpPortsData);
          thisCtrl.data = Object.values(udpPortsData);
        }
      },
      function (response) {
        responseErrorHandler(response);
      }
    );

  thisCtrl.labels = [];
  thisCtrl.data = [];
});
