#!/bin/bash

sourcedir="/users/mfeys/data/event_mall"
destdir="/work/data/event_mall"

sudo cp /users/mfeys/data/event_mall/bursts /work/data/event_mall/bursts 
sudo cp -r /users/mfeys/evmall/ /work/eventmall/ 
# get batchnode number
clustersize=33
hstnm=$(hostname)
hostid=$(echo ${hstnm:0:18} | egrep -o '[[:digit:]]{1,2}')
padtowidth=2

ENV=/work/eventmall

source $ENV/config
sudo python split_cluto.py $hostid $clustersize 4 2


sudo cp -r "$destdir/splits/*" "$sourcedir/splits/"

#INST="organize events from cluto results"
#log_start $INST
#for year in 2000 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011; do
#    for split in `ls $ENV|grep split-$year`; do
#        echo Organize $split ...
#        ./src/event/organize_cluto.py $ENV $split >$ENV/$split/twords 2> $ENV/$split/error.txt &
#    done
#    wait
#done
#log_finish $INST

#INST="generate events from cluto results"
#log_start $INST
#CMD="./src/event/gen_events.py $ENV -s2 -d.1 -m.1"
#echo $CMD; $CMD
#log_finish $INST


