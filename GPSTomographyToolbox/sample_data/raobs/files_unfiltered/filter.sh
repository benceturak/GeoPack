
for f in `ls *.csv`:
do
	echo $f
	cat -n $f | sort -uk2 | sort -n | cut -f2- >> "../files/"$f
done
