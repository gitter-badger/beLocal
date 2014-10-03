'use strict';

angular.module('clientApp')
  .controller('MainCtrl', function ($scope, StateService) {

    StateService.getTrendingProducts().then(function() {
      $scope.trendingProducts = StateService.getTrendingProductsList();
    })


  });
