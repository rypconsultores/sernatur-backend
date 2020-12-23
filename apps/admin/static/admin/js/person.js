(function _person_fn() {
    if(django.jQuery) {
        django.jQuery(function($) {
            let inputID = 'id_id';
            let $originalID = $('#' + inputID)
                .attr({
                    'id': inputID +'-shadow',
                    'readonly': 'readonly'
                })
                .css('font-style', 'italic')
            let $hiddenID = $('<input type="hidden" />')
                .attr({
                    'name': $originalID.attr('name'),
                    'id': inputID
                })
                .val($originalID.val())
            ;

            $originalID
                .val('')
                .attr('placeholder', gettext('Automatic'))
                .removeAttr('name')
            ;

            $hiddenID.insertAfter($originalID)
        })
    } else setTimeout(_person_fn, 100)
})();