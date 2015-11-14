#!/bin/sh
cd dados/iniciativas
rm iniciativas.json
python ../../scripts/scraper-iniciativas/scraper-iniciativas.py --start 38000 --end 38150 --processes 3
for line in `cat iniciativas.json | grep doc_url | sed s/" "/"_"/g`; do
 echo $line | sed s/".*:_\""/""/  | sed s/"\""/""/ | sed s/"\".*"/""/ | sed s/",_"/""/ | xargs wget --content-disposition
done
#for file in *.doc; do 
#  echo $file
#  antiword -w 0 ${f} > ${f.txt}
#done
rm *.doc
rm -rf cache
cd ../..

