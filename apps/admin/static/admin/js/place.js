(function _person_fn() {
    if(django.jQuery) {
        django.jQuery(function($) {
            let $type = $('#id_place_type');
            let $touristicSelects = $('#id_service_type, #id_service_class');
            let $infoSelect = $('#id_turistic_info_office_type');

            $type
                .on('change', function(evt) {
                    let enableTouristicSelects = /serv.*?tur[ií]s/gi.test($type.find('option:selected').text());
                    let enableInfoSelect = /info.*?tur[ií]s/gi.test($type.find('option:selected').text());
                    $touristicSelects
                        .prop('disabled', !enableTouristicSelects)
                        .find('option')
                            .prop('selected', false)
                        .end()
                        .find('option[value=""]')
                            .prop('selected', true)
                        .end()
                        .val('')
                        .trigger('change')
                        .trigger('change.select2')
                    ;

                    $infoSelect
                        .prop('disabled', !enableInfoSelect)
                })
                .trigger('change')


        })
    } else setTimeout(_person_fn, 100)
})();