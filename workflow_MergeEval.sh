#!/bin/bash

for splitdir in /media/EXTERNE\ HD/event_mall/splits/log_boost_split1540 /media/EXTERNE\ HD/event_mall/splits/log_boost_split2030
 do
	for min_sim in $(seq 0.1 0.1 0.5)
	do
		for min_score in 0.1
		do
			for min_size in 2
			do
				CMD="/home/mfeys/work/EMall/merge_eval.sh $splitdir $min_sim $min_score $min_size"
				echo $CMD;$CMD
			done
		done
	done
done

