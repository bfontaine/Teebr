angular.module('tbUtils', [])

  /**
   * rmL10n
   * ======
   *
   * l10n/i18n utilities
   **/
  .service('tbL10n', function() {

    /**
     * .getString
     * ----------
     *
     * Return a string from the template. This should be used instead of
     * hard-coded strings. To include translatable strings in the HTML with
     * Jinja/Babel, use:
     *    <script type="text/x-strings" id="_strings">
     *    key1:{{ _("the string 1") }}
     *    key2:{{ _("the string 2") }}
     *    </script>
     * Each string should have an unique key, which you'll give to `getString`.
     **/
    this.getString = (function() {
      var strs = {};

      $(function() {
        var lines = $('#_strings').html().split(/\n+/);
        $.each(lines, function(_, line) {
          var kv = line.split(/^([^:]+):/);
          if (kv) {
            strs[kv[1]] = kv[2];
          }
        });
      });

      return function(k) { return strs[k]; };
    })();
  })

  ;
