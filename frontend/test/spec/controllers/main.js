'use strict';

describe('Controller: MainCtrl', function () {
  beforeEach(module('frontendApp'));

  let MainCtrl, scope;

  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();

    MainCtrl = $controller('MainCtrl', {
      $scope: scope
    });
  }));

  it('should be defined', function() {
    expect(MainCtrl).toBeTruthy();
  });
});
