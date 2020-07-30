document.addEventListener('DOMContentLoaded', function () {
  var $closeIcons = Array.prototype.slice.call(document.querySelectorAll('.close'), 0);

  if ($closeIcons.length > 0) {
    $closeIcons.forEach(function($el) {
      console.log("adding event listener", $el);

      $el.addEventListener('click', function() {
        var target = $el.dataset.target,
          $target = document.getElementById(target);
        $target.remove();
      });
    });
  }

});
