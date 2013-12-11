#!/usr/bin/env bash
DATE_CMD="date +%Y%m%d%H:%M:%S"
log_start() {
    echo -e "* `date +'%Y-%m-%d %H:%M:%S'` \tSTART\t $* @$ENV"
    start_sec=`date +%s`
}

log_finish() {
    echo -e "* `date +'%Y-%m-%d %H:%M:%S'` \tFINISH\t $* @$ENV"
    end_sec=`date +%s`
    echo cost `expr $end_sec - $start_sec` seconds
}
ENV=/work/data/event_mall

INST="organize events from cluto results"
log_start $INST
cd $ENV/splits
for split in *; do
    echo Organize $split ...
    sudo /work/eventmall/src/event/organize_cluto.py $ENV/splits $split >$ENV/splits/$split/twords 2> $ENV/splits/$split/error.txt &
done
log_finish $INST


#INST="generate events from cluto results"
#log_start $INST
#CMD="./src/event/gen_events.py $ENV -s2 -d.1 -m.1"
#echo $CMD; $CMD
#log_finish $INST


