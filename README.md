# projekt_3.py
Třetí projekt Engeto Python akademie.

# Popis projektu
Projekt slouží k získání výsledků voleb do poslanecké sněmovny v roce 2017 v libovolném okrese.

# Instalace knihoven
Knihovny použité v kódu obsahuje soubor `requirements.txt`.
Jejich instalace je doporučena ve virtuálním prostředí s nainstalovaným manažerem.
```
pip3 --version                    # zjisteni verze manazeru
pip3 install requirements.txt     # instalace poutzitych knihoven
``` 
# Spuštění projektu
Pro spuštění projektu `projekt_3.py` z příkazového řádku jsou vyžadovány dva vstupní parametry:<br>  
`python projekt_3.py <odkaz-uzemniho-celku> <vysledny-soubor>`<br>   
Výsledky se uloží do souboru `.csv`

# Ukázka projektu
Výsledky hlasování pro okres Břeclav:
1. argument `https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6204`
2. argument `vysledky_breclav.csv`

Spuštění programu:<br>   
`python projekt_3.py https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6204 vysledky_breclav.csv`  

Průběh stahování:  
```
STAHUJI DATA Z VYBRANÉHO URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6204
UKLÁDÁM DO SOUBORU: D:\Privat_doma\Python_Engeto\Moje_cviceni\Projekt_3\vysledky_breclav.csv
UKONČUJI: projekt_3.py
```
Částečný výstup:  
```
code,location,registered,envelopes,valid,Občanská demokratická strana,Řád národa - Vlastenecká unie...
584304,Bavory,334,236,236,42,0...
584321,Boleradice,737,487,483,47,3...
...
```

