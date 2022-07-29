#!/bin/bash

DIR=$(pwd)			# 現在のディレクトリ
WORKDIR=$DIR/._latex		# 現在のディレクトリの下に作業用ディレクトリを作成
if [ -e $WORKDIR ]; then	# 事前にディレクトリがあった場合は消すか確認したほうがいいかも
    rm -ri $WORKDIR
fi
mkdir $WORKDIR

compile_latex () {
    TEX=$1
    NAME_TEX=${TEX##*/}		# 別のディレクトリから指定している場合名前に'/'が入っているので、それをもとにファイル名だけにする
    NAME=${NAME_TEX%.*}		# .texを削除する。これはPDFを同じ名前にするため

    cp $NAME_TEX $WORKDIR/hoge.tex
    cp -r $DIR/sources $WORKDIR/sources
    cd $WORKDIR

    				# Dockerコンテナを用いてコンパイルを行う

    docker run -itd --name latex_ mf220061/my_repository:latexv1.1
    				# Dockerコンテナを作成する

    docker cp ./ latex_:/root/result
    				# 作業用ディレクトリの中身をコンテナにコピーする


    if [ "$2" = 'platex' ]; then
        docker exec latex_ platex hoge
        docker exec latex_ dvipdfmx hoge

    elif [ "$2" = 'lualatex' ]; then
        docker exec latex_ lualatex hoge

    else
        docker exec latex_ platex hoge
        docker exec latex_ dvipdfmx hoge

    fi 				# コンパイルを行う
				# できればここはオプションで選択できるようにしたい

    docker cp latex_:/root/result/ ./
    				# コンパイル結果を作業用ディレクトリにコピーする

    docker rm -f latex_		# コンテナを削除する
    
    cd $DIR
    cp -i $WORKDIR/result/hoge.pdf $DIR/$NAME.pdf
    				# 作業用ディレクトリから現在のディレクトリにPDFファイルをコピーする
				# 上書きされるので注意
				# 確認を取るようにする
    rm -r $WORKDIR		# 作業用ディレクトリを削除する
}

CMDNAME=`basename $0`

while getopts c:f: OPT
do
    case $OPT in
        "c" ) FLG_C="TRUE" ; VALUE_C="$OPTARG" ;;
        "f" ) FLG_F="TRUE" ; VALUE_F="$OPTARG" ;;
          * ) echo "Usage: $CMDNAME [-c VALUE] [-f VALUE]" 1>&2
	    exit 1 ;;
    esac
done

shift $(expr $OPTIND - 1)

compile_latex $VALUE_F $VALUE_C

exit 0
