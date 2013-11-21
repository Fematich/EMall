#!/bin/bash


for i in {0..111}
do
  echo "Processing dat$i"
  # take action on each file. $f store current file name
  java -Djava.class.path=/home/mfeys/work/EMall/Segmenter/lib/IKAnalyzer2012_u6.jar converter.parse('dat'$i)
done
echo "Done!!!"
