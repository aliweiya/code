file_type=(pe pdf elf lnk bash powershell webshell doc)

for i in $(seq -5 -1);
do
    current_date=`date +"%Y-%m-%d" -d "$i days"`
    for f in ${file_type[@]};
    do
        python3 cde_${f}_filehash_service.py -t insert -d $current_date > /var/log/cde_filehash_service/temp/${f}_${current_date}.log 2>&1 &
    done
done
