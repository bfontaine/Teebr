var app = angular.module('tbTeebr',
  ['ui.bootstrap', 'tbUtils', 'mgo-mousetrap', 'ngAnimate']);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('_{');
  $interpolateProvider.endSymbol('}_');
});

app.controller('tbHomeCtrl', ['$scope', '$timeout', '$http',
    function tbHomeCtrl($scope, $timeout, $http) {

  _scope = $scope; // debug

  var endpoints = {
    unrated_sample: '/_ajax/user/statuses/unrated',
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
    console.log("rated: " + result); // TODO

    $scope.nextStatus();
  };

  $scope.skipStatus = function skipStatus() {
    $scope.nextStatus();
  };

  $scope.reportAsSpam = function reportAsSpam() {
    console.log("should be spam.");  // TODO

    $scope.nextStatus();
  };

  // shortcuts
  $scope.rateStatusYes = function y() { return $scope.rateStatus(true); };
  $scope.rateStatusNo = function n() { return $scope.rateStatus(false); };

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

  init();
}]);

app.filter("tweet_html", ["$sce", function($sce) {

  var re_hashtag = /(^|\s)#([a-z][^.\s]*)/gi,
      // see:
      // https://github.com/twitter/twitter-text/blob/master/js/pkg/twitter-text-1.9.4.js#L343
      re_stock =  /(^|\s)\$([a-z]{1,6}(?:[._][a-z]{1,2})?)(\s|$)/gi,

      re_mention = /(^|\s)@([a-z]\w*)/gi,

      re_url = /(^|\s)(https?:\/\/)([a-z]+\.[a-z]{2,}\S+)/g;

  function highlightTwitterFeatures(text) {
    return text.replace(re_hashtag, function(_, before, tag) {

      return before + '<span class="status-hashtag">' +
        '<span class="status-hash">#</span>' +
          '<span class="status-hashtag-content">' + tag + '</span></span>';

    }).replace(re_stock, function(_, before, tag, after) {

      return before + '<span class="status-cashtag">' +
        '<span class="status-cash">$</span>' +
          '<span class="status-cashtag-content">' + tag + '</span></span>' +
            after;

    }).replace(re_mention, function(_, before, mention) {

      return before + '<span class="status-mention">' +
        '<span class="status-at">@</span>' +
          '<span class="status-mention-content">' + mention + '</span></span>';

    }).replace(re_url, function(_, before, protocol, url) {
      var full = protocol + url;

      return before + '<a rel="nofollow" target="_blank" ' +
        'class="status-link" href="' + full + '">' +
          '<span class="status-link-protocol">' + protocol + '</span>' +
            '<span class="status-link-url">' + url + '</span></a>';

    });
  }

  return function(text) {
    if (!text) { return text; }

    //text = text.replace(/</, '&lt;').replace(/>/, '&gt;');

    text = highlightTwitterFeatures(text);

    return $sce.trustAsHtml(text);
  };
}]);
