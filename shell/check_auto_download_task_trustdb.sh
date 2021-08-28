left_cnt=`ps -ef|grep auto_download |grep -v check |grep -v grep |wc -l`
if [ $left_cnt -ne 9 ]
then
    echo -n `date`;
    echo " some process failed, $left_cnt left";
    ps -ef |grep auto_download |grep -v check |awk '{print $2}' |xargs kill
    nohup python /home/cde/cde_service/cde_sample_service/auto_download_task_trustdb.py > /var/log/auto_download_task_trustdb/auto_download_task_trustdb_$(date +\%Y-\%m-\%d-%H-%M-%S).log 2>&1 & 
fi