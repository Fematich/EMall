#!/bin/bash
#parameters: splitname min-sim min-score
splitsource=/home/mfeys/work/data/splits/$1

splitdir=/home/mfeys/work/data/event_mall/splits
ENV="/home/mfeys/work/data/event_mall"
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

unlink $splitdir
ln -s $splitsource $splitdir

INST="generate events from cluto results"
log_start $INST
CMD="/home/mfeys/work/eventmall/src/event/gen_events.py $ENV -s$4 -d$2 -m$3"
echo $CMD; $CMD
log_finish $INST

INST="evaluate events vs the gold events"
log_start $INST
event_name="$1"d"$2"m"$3"s"$4"
CMD="python /home/mfeys/work/EMall/evaluate.py $event_name splitname=$1 min_sim=$2 min_score=$3 min_size=$4"
echo $CMD; $CMD
log_finish $INST

INST="move the generated event-files to the event-directory and rename it"
log_start $INST
EVENT_DIR="/home/mfeys/work/data/events/"$event_name
mkdir $EVENT_DIR
mv /home/mfeys/work/data/event_mall/earticles $EVENT_DIR/earticles
mv /home/mfeys/work/data/event_mall/events $EVENT_DIR/events
mv /home/mfeys/work/data/event_mall/events_index $EVENT_DIR/events_index
mv /home/mfeys/work/data/event_mall/aevents $EVENT_DIR/aevents
log_finish $INST
