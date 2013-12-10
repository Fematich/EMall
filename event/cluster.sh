#!/bin/bash

cd /home/mfeys/work/data/event_mall/splits
for dir in *
do
echo $dir
cd /home/mfeys/work/data/event_mall/splits/$dir
sudo chmod 666 *
read ndocs filename <<< $(wc -l docids)
nclusters=$(python -c "import numpy as np; print 4*np.sqrt($ndocs)")
sudo /home/mfeys/work/eventmall/bin/vcluster matrix $nclusters -clustfile=clust -cltreefile=tree -showtree -zscores -colmodel=none -showfeatures > features
done

