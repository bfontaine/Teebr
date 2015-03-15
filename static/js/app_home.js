app.controller('tbHomeCtrl', ['$scope', '$timeout', '$http',
    function tbHomeCtrl($scope, $timeout, $http) {

  _scope = $scope; // debug

  var endpoints = {
    unrated_sample: '/_ajax/user/statuses/unrated',
    rate: '/_ajax/user/statuses/rate',
    report: '/_ajax/user/statuses/report',
  };

  /** Initialization *********************************************************/

  $.extend(true, $scope, {
    status: null,
    nextStatuses: [],
  });

  function init() {
    $scope.nextStatus();
  }

  /** API ********************************************************************/

  function get(endpoint, data) {
    return $http.get(endpoints[endpoint], data);
  }

  function post(endpoint, data) {
    return $http.post(endpoints[endpoint], data);
  }

  /** Statuses ***************************************************************/

  /*- Fetching --------------------------------------------------------------*/

  $scope.fetchStatuses = function fetchStatuses(fn) {
    get("unrated_sample")
      .success(function(statuses) {
        $scope.nextStatuses = $scope.nextStatuses.concat(statuses);
        (fn || $.noop)();
      });
  };

  $scope.nextStatus = function nextStatus(fn) {
    var restLen = $scope.nextStatuses.length;

    if (restLen === 0) {
      return $scope.fetchStatuses(function() {
        $scope.nextStatus();
        (fn || $.noop)();
      });
    }

    if (restLen < 5) {
      // fetch more statuses if we're running short
      $scope.fetchStatuses();
    }

    $scope.status = $scope.nextStatuses.shift();
    (fn || $.noop)();
  };

  /*- Rating ----------------------------------------------------------------*/

  $scope.rateStatus = function rateStatus(result) {
    post("rate", {
      id: $scope.status.id,
      score: result,
    }).success(function() {
      $scope.nextStatus();
    });
  };

  $scope.skipStatus = function skipStatus() {
    $scope.nextStatus();
  };

  $scope.reportAsSpam = function reportAsSpam() {
    post("report", { id: $scope.status.id });
    $scope.nextStatus();
  };

  // shortcuts
  $scope.rateStatusYes = function y() { return $scope.rateStatus(1); };
  $scope.rateStatusNo = function n() { return $scope.rateStatus(0); };

  init();
}]);
