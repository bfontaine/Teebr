app.controller('tbHomeCtrl', ['$scope', '$timeout', '$http', 'tbDOM',
    function tbHomeCtrl($scope, $timeout, $http, DOM) {

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

  $scope.rateStatus = function rateStatus(result, ev) {
    $scope.validate(result);

    post("rate", {
      id: $scope.status.id,
      score: result,
    }).success(function() {
      $scope.nextStatus();
    });

    return DOM.stopEvent(ev);
  };

  $scope.skipStatus = function skipStatus(ev) {
    $scope.nextStatus();
    return DOM.stopEvent(ev);
  };

  $scope.reportAsSpam = function reportAsSpam(ev) {
    post("report", { id: $scope.status.id });
    $scope.nextStatus();
    return DOM.stopEvent(ev);
  };

  // shortcuts
  $scope.rateStatusYes = function y(e) { return $scope.rateStatus(1, e); };
  $scope.rateStatusNo = function n(e) { return $scope.rateStatus(0, e); };

  /*-- Validation -----------------------------------------------------------*/

  $scope.predictions = { count: 0, matched: 0 };

  $scope.validate = function validate(result) {
    var t = 0.3,
        ok = result == 1,

        // this is enabled with beta features in the settings
        expected = $scope.status.expected;

    $scope.predictions.count++;

    if ((ok && expected < t) || (!ok && expected > t)) {
        $scope.predictions.matched++;
    }
  };

  /*-------------------------------------------------------------------------*/

  init();
}]);
