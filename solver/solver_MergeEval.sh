#!/bin/bash
split_name=$1
min_msim=$2
max_msim=$3
diff=0.2

max_digits=4
max_iter=4
min_diff=0.01
for splitdir in /home/mfeys/work/data/splits2/$split_name
 do
	#for min_score in 0.1
	#do
	#	for min_size in 2
	#	do
	#		CMD="/home/mfeys/work/EMall/merge_eval.sh $splitdir $min_msim $min_score $min_size"
	#		echo $CMD;$CMD	
	#		CMD="/home/mfeys/work/EMall/merge_eval.sh $splitdir $max_msim $min_score $min_size"
	#		echo $CMD;$CMD
	#	done
	#done
	iter=0
	while [ $iter -lt $max_iter ] && [ $(echo $diff'>'$min_diff | bc -l) -eq  1 ]
	do
	iter=$(($iter+1))
	min_sim=$(python calc_next_msim.py $split_name $min_msim $max_msim)
		for min_score in 0.1
		do
			for min_size in 2
			do
				CMD="/home/mfeys/work/EMall/merge_eval.sh $splitdir $min_sim $min_score $min_size"
				echo $CMD;$CMD
				max_msim=$(python calc_max_msim.py $split_name $min_sim $min_msim $max_msim)
				min_msim=$(python calc_min_msim.py $split_name $min_sim $min_msim $max_msim)
				diff=$(python calc_diff.py $split_name $min_sim)
				
			done
		done
	done
done
#loop until max_iter or diff<min_diff or digits=max_digits
#next_value:
	# select min and max (first time generated), otherwise select such that last_diff*other_diff<0
	# use average of min and max:
	# cut off to certain degree (given by max number of digits of min and max)
	# if cut off equals to min or max:
		# don't cut off...
