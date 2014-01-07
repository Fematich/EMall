#!/bin/bash

DATE_CMD="date +%Y%m%d%H:%M:%S"
sourcedir="/users/mfeys/data/event_mall"
destdir="/work/data/event_mall"
ENV="/work/data/event_mall"
lines=13706
padtowidth=2
# get batchnode number
clustersize=33
hstnm=$(hostname)
hostid=$(echo ${hstnm:0:18} | egrep -o '[[:digit:]]{1,2}')


dirs=$(python -c 'from gmths import get_months;get_months($hostid, $clustersize)')
for dir in dirs;
do;
	rsync -rvz /users/mfeys/data/event_mall/vectors/$dir /work/data/event_mall/vectors/$dir;
done;
