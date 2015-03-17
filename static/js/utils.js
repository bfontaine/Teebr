angular.module('tbUtils', [])

  .service('tbDOM', function() {

    this.stopEvent = function($ev) {
      $ev.preventDefault();
      $ev.stopPropagation();
      return false;
    };

  })

  ;
