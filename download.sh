#!/bin/sh

##
## Descarregar dados das iniciativas parlamentares
##
## Mudar para directoria de destino... apagar dados recolhidos anteriormente.
#cd dados/iniciativas
#rm iniciativas.json *.txt

## Descarregar iniciativas parlamentares desde o site do parlamento
#python ../../scripts/scraper-iniciativas/scraper-iniciativas.py --start 00000 --end 199999 --processes 0
#rm -rf cache

## Descarregar ficheiros word com documentos correspondentes a iniciativas parlamentares
#for line in `cat iniciativas.json | grep doc_url | sed s/" "/"_"/g`; do
# echo $line | sed s/".*:_\""/""/  | sed s/"\""/""/ | sed s/"\".*"/""/ | sed s/",_"/""/ | xargs wget --content-disposition
#done

## Converter os ficheiros word para ficheiros de texto, e apagar os ficheiros word
#for file in *.doc; do 
#  antiword $file > $file.txt
#  rm -rf $file
#done

## Voltar a directoria onde se encontra o script
#cd ../..


## *******************

##
## Descarregar dados das transcricoes dos debates no parlamento
##

## Mudar para directoria de destino
cd dados/transcricoes

## Copiar scripts que vamos usar
cp ../../scripts/darscraper/*.py .
cp ../../scripts/dar2txt/*.py .

## Descarregar dados da legislatura i, sessao j e numero k
for i in `seq 11 15`; do
for j in `seq 100`; do
for k in `seq 350`; do
 python dardownloader.py $i $j $k pdf
 python dardownloader.py $i $j $k txt
done
done
done

## Converter os PDFs do diario da republica em ficheiros txt e json
mkdir -p pdf
mv -f *.pdf pdf
mkdir -p txt
mkdir -p json
cd pdf
for file in *.pdf; do
 ../../../scripts/pdfocr/pdfocr.rb -c -i ${file} -o ${file}.tmp
 mv ${file}.tmp ${file}
 cd ..
 python pdf2xml.py -t xml pdf/${file} > txt/${file}.xml
 python xml2txt.py txt/${file}.xml txt/${file}.tmp
 python txtpostproc.py txt/${file}.tmp txt/${file}.txt
 rm txt/${file}.xml txt/${file}.tmp
 python txt2json.py txt/${file}.txt json/${file}.json
 cd pdf
done
cd ..

## Converter os TXTs do diario da republica em ficheiros json
mkdir -p txt
mkdir -p json
for file in *.txt; do
 python txtpostproc.py ${file} txt/${file}
 python txt2json.py txt/${file} json/${file}.json
 rm -rf $file
done

## Remover ficheiros temporarios
rm -rf *.py *.pyc temp
cd ../..
