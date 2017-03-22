'use strict';

function addFormattedFields(scan) {
  scan.datetimeString = moment(scan.datetime * 1000).utc().format('YYYY-MM-DD hh:mm:ss.SSS');
  scan.addressesString = Object.values(scan.addresses).join(' ');
  scan.hostnamesString = jQuery.map(scan.hostnames, function (e) {
    if (e.type === 'user') {
      return e.name;
    } else {
      return e.type + ":" + e.name;
    }
  }).join(' ');
  scan.tcpPortsSring = 'tcp' in scan ? Object.keys(scan.tcp).join(' ') : '';
  scan.udpPortsSring = 'udp' in scan ? Object.keys(scan.udp).join(' ') : '';
  return scan;
}

function responseErrorHandler(response) {
  alert("Server response error.");
}

function getType(o) { return o && o.constructor && o.constructor.name; }
function log(msg) { console.log("[" + window.performance.now() + "] " + msg); }
