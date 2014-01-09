#!/bin/bash

for splitdir in /home/mfeys/work/data/splits2/tf1_log_boost_splits1530 /home/mfeys/work/data/splits2/tf1_splits2020
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

