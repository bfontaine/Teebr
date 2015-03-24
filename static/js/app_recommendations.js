app.controller('tbRecommendationsCtrl', ['$scope', '$http', '$document',
    function tbHomeCtrl($scope, $http, $document) {

  _scope = $scope; // debug

  $document.ready(function() {
    $scope.producers = JSON.parse($("#producers").remove().html());

    // prefetch images
    $.each($scope.producers, function(_, p) {
        new Image(p.profile_background_image_url_https);
        new Image(p.profile_image_url_https);

        p.coverStyle = {
            "background-image": 'url("' + p.profile_background_image_url_https + '")',
        };

        p.textStyle = {
            //"background-color": "#" + p.profile_background_color,
            //"color": "#" + p.profile_text_color,
        };
    });

    $scope.$apply();
  });

}]);
