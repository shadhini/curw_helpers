#!/usr/bin/env bash

while getopts m:s:e:o: option
do
    case "${option}"
    in
        m) model=${OPTARG};;
#        sd) start_date=${OPTARG};;
        s) start_time=${OPTARG};;
#        ed) end_date=${OPTARG};;
        e) end_time=${OPTARG};;
        o) opt=${OPTARG};;
    esac
done

main() {

    start_time="\"$start_time\""
    end_time="\"$end_time\""
    python ./fill_missing_values.py -m ${model} -s ${start_time} -e ${end_time} -o ${opt}
#    echo "\"$model\""
#    echo ${start_time}
#    echo ${end_time}
#    echo ${opt}
}

main "$@"
