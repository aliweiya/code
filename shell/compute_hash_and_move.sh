for item in `ls hash_samples`;
do
    sha256=`sha256sum hash_samples/$item | awk '{print $1}'`
    mv hash_samples/$item rescan/${sha256:0:1}/${sha256:1:1}/${sha256:2:1}/$sha256
done