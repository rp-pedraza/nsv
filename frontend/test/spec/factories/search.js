'use strict';

describe('Factory: Search', function () {
  beforeEach(module('frontendApp'));

  var Search, httpBackend;

  const mockIdentity = "pao7s";
  const mockRequestUri = config.backend_api_base_uri_path + '/search?query=' + mockIdentity
  const mockResponse = [{"status":{"state":"up","reason":"user-set"},"addresses":{"ipv4":"38.233.183.136"},"tcp":{"80":{"product":"","state":"open","version":"","name":"http","conf":"3","extrainfo":"","reason":"syn-ack","cpe":""},"443":{"product":"","state":"open","version":"","name":"https","conf":"3","extrainfo":"","reason":"syn-ack","cpe":""}},"datetime":1475585472.587352,"hostnames":[{"type":"user","name":"www.pao7s.com"}],"identity":mockIdentity,"id":"32"}];

  beforeEach(inject(function ($injector) {
    Search = $injector.get('Search');
    httpBackend = $injector.get('$httpBackend');
    httpBackend.when('GET', mockRequestUri).respond(mockResponse);

    // Avoid 'Error: Unexpected request: GET views/main.html'
    // See https://stackoverflow.com/a/41138710/10580490
    // Using https://github.com/karma-runner/karma-ng-html2js-preprocessor doesn't work.
    // The generated function in that library never gets triggered.
    httpBackend.whenGET(new RegExp('[.]html$')).respond(function() { return [200, 'XXX', {}] });
  }));

  it('should be defined', function() {
    expect(Search).toBeTruthy();
  });

  it('should return a valid search result', async function() {
    httpBackend.expectGET(mockRequestUri);
    Search.query({ query: mockIdentity }, function (response) {
      expect(response.length).toEqual(1);
      const responseKeys = Object.keys(mockResponse[0])
      response = response.map(resource => _.pick(resource, responseKeys));
      expect(response).toEqual(mockResponse);
    });
    httpBackend.flush();
  });
});
