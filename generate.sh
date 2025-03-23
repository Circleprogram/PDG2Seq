: <<'mulcomment'
for file in $(find /Users/zzz/Downloads/zzd_dataset -name "*.java" | grep -E 'bugfunc1|nobugfunc1'); do
    joern-parse $file;
    filename=$(basename -- "$file");
    filename="${filename%.*}";
    dir=$(dirname -- "$file");
    joern-export --repr pdg --out $dir/$filename;
done
mulcomment

#! /usr/bin/bash
total=$(cat /mnt/sda/.../Devign/devign_paths.txt | wc -l)
echo "all length : "$total
progress=0

count=0
for file in $(cat /mnt/sda/.../Devign/devign_paths.txt);do
	joern-parse $file > /dev/null;
	filename=$(basename -- "$file");
	filename="${filename%.*}";
	# echo $file
	# echo $filename
	dir=$(dirname -- "$file");
	# dir=/mnt/sdb/zhangyj22/code/zzd/dataset/FFmpeg/vul
	# 我想dot存再上一级的vuldot文件夹中
	dir=${dir}"dot"
	# echo $dir
	joern-export --repr pdg --out $dir/$filename > /dev/null;

	count=$((count+1))
	
	progress=$((progress+1))
        # 计算进度百分比,进度条长度设置100,percent就是已完成长度
        percent=$((100*progress/total))
        # 打印进度条
        # printf "progress: [%-50s] %d%%\r" $(printf "%-{$length}s" "=") $percent
	printf "progress: [%-100s] %d%%\r" $(printf "%0.s=" $(seq 1 $percent)) $percent
done
# 再输出一行，不让命令行盖住进度条
echo

: <<'mulcomment'
# 并行处理
#! /usr/bin/bash

# find /mnt/sdb/zhangyj22/code/zzd/dataset/FFmpeg/test/ -name "*.c" | split -l 1000 -d

for filelist in x*; do
    cat "$filelist" | xargs -P 1 -i {} echo {}
    bash -c '
    for file in "$@"; do 
	joern-parse $file > /dev/null; 
	filename=$(basename -- "$file"); 
	filename="${filename%.*}"; 
	dir=$(dirname -- "$file"); 
	dir=${dir}"dot"; 
	joern-export --repr pdg --out $dir/$filename > /dev/null; 
    done
    ' < {} &
done

# 等待所有进程完成
wait

# 清理临时文件
rm x*
mulcomment
