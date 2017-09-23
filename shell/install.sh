cat requirments.txt |while read line
do
    pip install $line -i https://pypi.tuna.tsinghua.edu.cn/simple
done
