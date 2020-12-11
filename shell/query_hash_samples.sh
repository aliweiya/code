for file in `cat md5.txt`;
do
    sample_path=samples/${file:0:4}/${file:4:4}/$file
    if [ -f $sample_path ]
    then
        echo $sample_path
        cp $sample_path hash_samples/
    else
         echo $sample_path not found
    fi
done