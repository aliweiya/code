cat requirments.txt |while read line
do
    pip install $line --trusted-host mirrors.aliyun.com 
done
