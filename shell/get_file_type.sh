dirs='0123456789abcdef'

for ((first=0; first < ${#dirs}; ++first))
do
    for ((second=0; second < ${#dirs}; ++third))
    do
        for ((third=0; third < ${#dirs}; ++third))
        do
            path=/data1/rescan/${dirs:$first:1}/${dirs:$second:1}/${dirs:$third:1}
            ./cde_test.exe $path -p t
        done
    done
done
