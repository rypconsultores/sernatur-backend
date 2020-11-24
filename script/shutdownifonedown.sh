#!/bin/sh

process_needed="$1"

var_parser() {

    while [ "$#" -ne "0" ]; do
        var="$(echo "$1" | cut -d: -f1)"
        val="$(echo "$1" | cut -d: -f2)"

        case $var in
            "eventname")
                ( [ "$val" = "PROCESS_STATE_FATAL" ] || [ "$val" = "PROCESS_STATE_EXITED" ] ) \
                    && is_dying=1
            ;;
            "processname")
                [ "$val" = "${process_needed}" ] \
                    && is_the_process=1
            ;;
            *)
            ;;
        esac

        shift
    done

    # if [ "${is_dying}${is_the_process}" = "11" ]; then
    if [ ! -z "${is_dying}" ]; then
        pkill -15 -f supervisord &
        exit 0
    fi
}

while echo -ne "READY\n" && read line; do
    var_parser $line
    echo -ne "RESULT 2\nOK"
done < /dev/stdin