$(document).ready(function () {
    $("#id_tags").autocomplete({
        source: '/ajax/tag/autocomplete/',
        minLength: 2,
        open: function(){
            setTimeout(function () {
                $('.ui-autocomplete').css('z-index', 99);
            }, 0);
        }
    });
    });