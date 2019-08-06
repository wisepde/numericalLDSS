#rm result/*
m=8
ii=(0 1 2 3 4)
h=(0.1 0.05 0.025 0.0125 0.00625)
k=(0.5e-9 0.25e-9 1.25e-10 0.625e-10 3.125e-11)
for i in ${ii[@]}
do
	nohup python numericLDSS2d.py --m $m --h ${h[i]} --k ${k[i]} &
done

#ii=(0 1 2 3)
#for i in ${ii[@]}
#do
#	python calerr2d.py --x "result/e2d1E-03m8_x${h[i]}.csv" --u "result/e2d1E-03m8_sol${h[i]}.csv" --xr "result/e2d1E-03m8_x${h[$((i+1))]}.csv"   --ur  "result/e2d1E-03m8_sol${h[$((i+1))]}.csv"
#done	

