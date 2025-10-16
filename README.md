# ord_arsins

Ferlið við að velja orð ársins felur í sér að lesa gögn seinustu fimm ára (ýmist úr TEI-skjölum Risamálheildar
eða hreinum textum þess tímabils em ekki er búið að ganga frá í RMH). Upplýsingum um fjölda lemma fyrir hvert ár 
og hvern miðil eru skráðar í töfluna 'ord_arsins_lemmur' í gagnagrunninum risamalheildin á Mímisbrunni.


1) Sækja Risamálheildina.

2) Marka og lemma texta þess tímabil sem RMH nær ekki yfir.

3) Merkja þau textaskjöl sérstaklega sem innihalda erlendan texta (breyta nafni í .erlent.txt)
  merkja_erlent.py

4) Keyra upplýsingar um fjölda lemma úr TEI-skjölum (Risamálheild) í töfluna ord_arsins_lemmur
  python3 ur_tei_i_grunn 

5) Keyra upplýsingar um fjölda lemma úr textaskjölum í töfluna ord_arsins_lemmur 
   python3 ur_hreinir_i_grunn.py

6) Lesa niðurstöður 
   python3 lesa_nidurstodur.py

Við hættum árið 2024 að nota gögn af bland.is. Það er mikil vinna fyrir lítinn ávinning.