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

  $scope.$watch("user", function(newUser, oldUser) {
    if (!oldUser || !newUser) { return; }

    $http.post("/_ajax/user/settings", {"settings": newUser})
         .success(function(data) {
           if (data.reload) {
             document.location.reload(true);
           }
         });
  }, true);

}]);
