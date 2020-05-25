#! /bin/bash
NADD="192.168.0."
rm ./ipmac.txt
touch ./ipmac.txt
for HADD in {100..110}
do
    arping -c 2 $NADD$HADD | grep "from"  > ./tmp.txt
    if [ $? -eq 0 ]
    then
        MAC=$(cat ./tmp.txt | awk 'NR==1{print $4}')
        echo "$NADD$HADD $MAC"
        echo "$NADD$HADD $MAC" >> ./ipmac.txt
    fi
        let HADD++
done
