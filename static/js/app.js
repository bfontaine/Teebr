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

app.controller('tbUserSettingsCtrl', ['$scope', '$http', '$document',
    function tbHomeCtrl($scope, $http, $document) {

  _scope = $scope; // debug

  $document.ready(function() {
    $scope.user = JSON.parse($("#user").html());
    $scope.languages = JSON.parse($("#languages").html());

    $scope.$apply();
  });

  $scope.resetAccount = function resetAccount() {
    $http.post("/_ajax/user/reset-account")
         .success(function() { $scope.user.rated_statuses = 0; });
  };

  $scope.$watch("user", function(oldUser, newUser) {
      console.log("TODO");
  }, true);

}]);

/*== Filters ================================================================*/

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
