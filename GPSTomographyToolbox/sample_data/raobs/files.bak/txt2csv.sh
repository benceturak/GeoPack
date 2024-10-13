

for f in `ls *.txt`
do
	new_name=`echo $f | sed -e 's/.txt/.csv/g'`
	sed 's/\t/,/g' $f >  $new_name 
done
