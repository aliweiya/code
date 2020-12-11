base_path="/home/cde/share_write/hot_samples"

function get_source_cnt {
    total=0
    for i in $(seq -7 -1);
    do
        sample_path=$base_path/$1/`date +"%Y-%m" -d "$i days"`  
        if [ -d $sample_path ]
        then
            date_filter=`date "+%Y%m%d" -d "$i days"`
            cnt=`ls -l --time-style '+%Y%m%d' $sample_path |grep $date_filter |wc -l`
        else
            cnt=0
        fi
        echo source: $1, date: `date +'%Y-%m-%d'`, cnt: $cnt
        total=$[$total + $cnt]
    done
    echo source: $1, total: $total
}

for folder in `ls $base_path`;
do
    if [ -d $base_path/$folder ]
    then
        get_source_cnt $folder
    fi
done
