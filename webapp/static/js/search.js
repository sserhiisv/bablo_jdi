$(document).ready(function() {

    $( "#sb-search" ).click(function() {
      $( "#search-form" ).toggle('slow');
      $("#search-input").focus();
    });

});