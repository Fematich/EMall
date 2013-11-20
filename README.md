EMall
=====

toolkit to transform EventMall dataset into a usable format for burst-detection

steps:
1) Segment the data from dat-files and use correct encoding
2) Generate a:
	- dates file
		#dates = open(sys.argv[1]+"/dates").read().strip().split()
		* lijst van dates
	- daily_volumes file:
		#while True:
        	#line = fin.readline()
        	#if not line: break
        	#tokens = line.split()
        	#term = tokens[0]
        	#cnt = int(tokens[1])
        	#tvols = map(int, tokens[2:])
		#  date1, date2, .... dateN
		#  vol1,  vol2,  .... volN
		#  term1, v1, v2, .... vN
		#  term2, v1, v2, .... vN
		#  ...
		#  termK, v1, v2, .... vN
		* docfreq of tf per dag per term
	- gross_daily_volumes file
		#vols = map(int, open(sys.argv[1]+'/gross_daily_volumes').read().strip().split())
		* total # terms during day

