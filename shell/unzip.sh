SHARE_FOLDER=/home/cde_self_sample/

function get_share_folder {
    folder=$1
    # 把下划线替换为横杠
    folder=${folder//_/\-}
    today=`date +%Y%m%d`
    # 最长20个字符
    target=${SHARE_FOLDER}cde_self-samples_${folder:0:20}_${today}_01
    # 通过echo返回值
    echo $target
}

zip_filename=$1
# 从路径中获取文件名
unzip_folder=`basename ${zip_filename%.*}`

if [ -f $zip_filename ]
then
    echo "filename: $zip_filename"
else
    echo "$zip_filename not found" >&2
    exit 1
fi

if [ -d $unzip_folder ]
then
    echo "folder $unzip_folder exists, not going to unzip"
else
    echo "unzipping $zip_filename to $unzip_folder"
    7za x -pcde9527 $zip_filename -oc:$unzip_folder
fi

target_folder="${unzip_folder}_target"
if [ -d $target_folder ]
then
    echo "target folder $target_folder exists"
else
    mkdir $target_folder
fi

for item in `find $unzip_folder`
do
    if [ -f $item ]
    then
        mv $item $target_folder/
    fi
done

share_folder=`get_share_folder $unzip_folder`

echo "move $target_folder to $share_folder"
mv $target_folder $share_folder

echo "delete $zip_filename"
rm -f $zip_filename

echo "delete $unzip_folder"
rm -rf $unzip_folder
