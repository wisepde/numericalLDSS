#rm result/*
m=8
ii=(0 1 2 3 4)
h=(0.1 0.05 0.025 0.0125 0.00625)
k=(16e-10 8e-10 4e-10 2e-10 1e-10)
#for i in ${ii[@]}
#do
#	nohup python numericLDSS1d.py --m $m --h ${h[i]} --k ${k[i]} &
#done

ii=(0 1 2 3)
for i in ${ii[@]}
do
	python calerr.py --x "result/e1E-03m8_x${h[i]}.csv" --u "result/e1E-03m8_sol${h[i]}.csv" --xr "result/e1E-03m8_x${h[$((i+1))]}.csv"   --ur  "result/e1E-03m8_sol${h[$((i+1))]}.csv"
done	

