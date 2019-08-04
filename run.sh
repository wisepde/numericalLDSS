mkdir result
rm result/*.csv result/*.png
for m in 1 2 8
do
    nohup python numericLDSS1d.py --m  $m &
done

for m in 1 2 8
do
<<<<<<< HEAD
    nohup python python numericLDSS2d.py --m $m &
=======
    nohup python numericLDSS2d.py --m $m &
>>>>>>> c88d387d8359bb9036e3c7a258802422f9e674d9
done

#for m in 1 2 8
#do 
#    python postpossing.py --m $m
#done

#for m in 1 2 8
#do 
#    python postpossing2d.py --m $m
#done
