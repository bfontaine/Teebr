var app = angular.module('tbTimber',
  ['ui.bootstrap', 'tbUtils', 'mgo-mousetrap', 'ngAnimate']);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('_{');
  $interpolateProvider.endSymbol('}_');
});

app.controller('tbHomeCtrl', ['$scope', '$timeout',
    function rmSMSCtrl($scope, $timeout) {

  _scope = $scope; // debug

  /** Alerts *****************************************************************/

  $scope.alerts = [];
  $scope.closeAlert = function(alert) {
    var idx = $scope.alerts.indexOf(alert);
    if (idx < 0) { return; }
    $scope.alerts.splice(idx, 1);
  };

  /*
    Examples:
      addAlert("my message");                // warning msg
      addAlert("my message", "info");        // info msg
      addAlert("my message", "info", 3000);  // fade 3s later
      addAlert("my message", "info", false); // don't fade
  */
  $scope.addAlert = function(msg, type_, timeout) {
    var alert = {msg: msg, type: type_ || 'warning'};
    $scope.alerts.push(alert);

    if (timeout !== false) {
      // hide alerts after 4sec
      $timeout(function() {
        $scope.closeAlert(alert);
      }, timeout || 4000);
    }
  };
}]);
