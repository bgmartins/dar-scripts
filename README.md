DAR Scripts
===========

Este é um conjunto de ferramentas desenvolvido no Transparência Hackday Portugal, criadas para lidar especificamente com as transcrições do Parlamento, documentadas no Diário da Assembleia da República (DAR).


darscraper
----------

O script ``dardownloader.py`` descarrega uma transcrição do Parlamento.pt, da seguinte forma:

    python dardownloader.py <legislatura> <sessão legislativa> <número>

Para descarregar vários, alguma magia de linha de comandos trata do assunto:

    for i in `seq 100`; do python dardownloader.py 12 1 $i; done

Este comando descarregará os primeiros 100 números da 1ª Sessão Legislativa da XII Legislatura.


dar2txt
-------

Converte os PDFs do DAR obtidos no site do Parlamento para formato texto e JSON.

    python darjson.py <dir_dos_pdfs> <dir_para_jsons>

O diretório fonte também pode incluir ficheiros de texto (``txt``) em vez de PDF, que será feita a conversão para JSON.

Este é um conjunto bastante complexo de ferramentas que vão executando várias conversões:

* PDF para XML com o pdfminer
* XML para texto
* pós-processamento e normalização do texto
* texto para JSON

Os procedimentos estão comentados irregularmente no código-fonte. Todo o processo daria um paper que um dia iremos escrever.

raspadar
--------

Parser antigo das transcrições do debates.parlamento.pt. Passámos a usar o dar2txt para trabalhar diretamente com os PDFs.

O código é peludo e pouco documentado, mas mantemo-lo por perto para referência.

pdf_urls_hack
-------------

Scripts PHP para determinar os URLs complicados dos PDFs. A lógica destes scripts foi incorporada no darscraper (ver acima).