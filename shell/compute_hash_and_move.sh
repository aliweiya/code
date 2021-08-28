folder=hash_samples
for item in `ls $folder`;
do
    sha256=`sha256sum $folder/$item | awk '{print $1}'`
    mv $folder/$item rescan/${sha256:0:1}/${sha256:1:1}/${sha256:2:1}/$sha256
done