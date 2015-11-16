Programas para acesso a dados da Assembleia da República
========================================================

Este é um conjunto de ferramentas para lidar com as transcrições do Parlamento, documentadas no Diário da Assembleia da República (DAR), assim como para descaregar informação sobre iniciativas legislativas. As ferramentas disponíveis neste repositório resultam de adaptações feitas sobre scripts desenvolvidos originalmente no contexto do Transparência Hackday Portugal.

darscraper
----------

O script ``dardownloader.py`` descarrega uma transcrição do Parlamento.pt, da seguinte forma:

    python dardownloader.py <legislatura> <sessão legislativa> <número>

Para descarregar vários documentos, alguma magia de linha de comandos trata do assunto:

    for i in `seq 100`; do python dardownloader.py 12 1 $i; done

Este comando descarregará os PDFs correspondentes aos primeiros 100 números da 1ª Sessão Legislativa da XII Legislatura.


dar2txt
-------

Programas para conversão dos PDFs do DAR, obtidos no site do Parlamento, para os formatos texto e JSON.
Este é um conjunto bastante complexo de ferramentas que vão executando várias conversões:

* OCR desde PDFs com a ferramenta [OCRmyPDF](https://github.com/jbarlow83/OCRmyPDF)
* PDF para XML com o pdfminer
* XML para texto
* pós-processamento e normalização do texto
* texto para JSON

Os procedimentos estão comentados irregularmente no código-fonte.

raspadar
--------

Parser antigo das transcrições do debates.parlamento.pt. Passámos a usar o dar2txt para trabalhar diretamente com os PDFs. O código é antigo e pouco documentado, mas mantemo-lo por perto para referência.

pdf_urls_hack
-------------

Scripts PHP para determinar os URLs complicados dos PDFs. A lógica destes scripts foi incorporada no darscraper (ver acima). O código é antigo e pouco documentado, mas mantemo-lo por perto para referência.


scraper-iniciativas
-------------------

Este scraper recolhe as iniciativas legislativas a partir do [site do Parlamento](http://www.parlamento.pt). O site do Parlamento foi programado em ASP, o que dificulta muito a tarefa de recolher a informação (_scraping_). Assim, adotámos uma técnica bruta, recorrendo aos ID's numéricos de cada documento. 

O endereço de uma iniciativa específica é algo como

    http://www.parlamento.pt/ActividadeParlamentar/Paginas/DetalheIniciativa.aspx?BID=38526

Ao alterar o valor da variável BID, podemos chegar a cada documento individual. Mas como não sabemos quais os ID's a pesquisar, batemos à porta de todos e apanhamos o que vem à rede. 

Isto faz com que o processo seja muito mais demorado do que o necessário, já que existem milhares de ID's vazios e os mais recentes estão na ordem dos 38000, significando que temos de fazer mais de 38000 pedidos ao site para assegurar que temos tudo. Mas graças a um cache inteligente (obrigado @medecau), a descarga só é feita uma vez e todos os processamentos subsequentes usam uma cópia local da página HTML original. Assim, não há risco de sobrecarregar desnecessariamente o site do Parlamento.

Para a ajuda dos comandos do script:

    python scraper-iniciativas.py --help

Para experimentar sacando apenas 10 documentos a partir do 38000:

    python scraper-iniciativas.py --start 38000 --end 38010

Para fazer a mesma coisa usando 4 processos (mais rápido mas puxa mais pelo CPU):

    python scraper-iniciativas.py --start 38000 --end 38010 --processes 4

Os campos que podem ser encontrados no JSON resultante são os seguintes:

  * `title` -- Título da iniciativa (_Proposta de Lei 231/XII_)
  * `summary` -- Sumário da iniciativa 
  * `id` -- Número de identificação do documento no Parlamento.pt (_38526_)
  * `authors` -- Lista dos autores do documento
  * `parlgroup` -- Grupo parlamentar responsável pelo documento (_PSD, CDS-PP_)
  * `events` -- Lista com as várias fases do processo legislativo. Contém objetos com os seguintes atributos:
    * `date` -- Data do evento (_2014-05-29_)
    * `type` -- Tipo de evento (_Envio para promulgação_)
    * `info` -- Pormenores do evento como links e detalhes das comissões e votações. Este campo só está expresso em texto, um dos afazeres é processá-lo para uma lista de links e outras informações.
  * `doc_url` -- URL do ficheiro Word com o texto integral do documento
  * `pdf_url` -- URL do ficheiro PDF com o texto integral do documento
  * `pdf_url` -- URL do ficheiro PDF com o texto integral do documento
  * `url` -- URL da iniciativa no Parlamento.pt
  * `scrape_date` -- Data e hora completa de quando o documento foi raspado

O JSON apenas inclui o sumário da iniciativa, mas o texto completo permite análises bem mais potentes. O campo `doc_url` aponta-nos para um ficheiro Word, por isso primeiro tratamos de encontrar todos esses campos e fazer uma lista de URLs; depois usarmos o `wget` para os descarregar. 

Os ficheiros Word podem ser facilmente convertidos para texto usando o fantástico `antiword`:

    for f in *.doc; do antiword -w 0 ${f} > ${f/doc/txt}; done

Lista de melhorias a introduzir nos vários programas
----------------------------------------------------

  * No scrapper das iniciativas, processar corretamente os campos `info` dos eventos para determinar links e outras informações que lá existem
  * No scrapper das iniciativas, detetar entradas sobre a substituição do texto original ([exemplo](http://www.parlamento.pt/ActividadeParlamentar/Paginas/DetalheIniciativa.aspx?BID=38526))
