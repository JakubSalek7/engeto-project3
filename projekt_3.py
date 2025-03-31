"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: jakub Salek
email: jaku.n.salek@gmail.com
discord: zob3772
"""
import csv
import os
import requests
from bs4 import BeautifulSoup
import sys

def zkontroluj_vstupni_argumenty(argumenty):
    """
    Zkontroluje vlastnosti vstupních argumentů

    """
    if len(argumenty) < 3:
            print("Zadali jste příliš málo argumentů. Zkuste to znovu.")
            sys.exit(1)
    if argumenty[1].endswith(".csv"):
            print("Zdá se, že jste přehodili pořadí argumentů. Zkuste to znovu.")
            sys.exit(1)
    if not argumenty[1].startswith("https://"):
            print("Adresa webové stránky musí začínat https://") 
            print("Zkuste to znovu.")  
            sys.exit(1) 
    if not argumenty[2].endswith(".csv"):
            print("Výstupní soubor nemá správnou příponu. Zkuste to znovu s .csv na konci.")
            sys.exit(1)

def nacti_vstupni_argumenty():          
    """
    Nacte vstupní argumenty

    Returns: 
        str: argument_1
        str: argument_2
    """
    try:
        argument_1 = sys.argv[1]
        argument_2 = os.path.join(r"C:\Users\Milan\Desktop\Projekt_3", sys.argv[2])
    except Exception as e:
        print("Nastala neočekávaná chyba. Ukončuji program.")
        print(e)
        sys.exit(1)
    else:
        return argument_1, argument_2

def nacti_stranku_okresu(adresa_okresu):
    """
    Nacte obsah stranky vybraneho okresu a najde v nich vsechny odkazy ("a")
    
    Return:
        bs: vsechny_url_okresu 
    """
    try:    
        with requests.get(adresa_okresu) as odpoved:
            obsah_stranky_okres = odpoved.text
    except requests.exceptions.RequestException as e:
        print("Chyba při načítání stránky.")
        print(e)
        sys.exit(1)
    else:
        print("STAHUJI DATA Z VYBRANÉHO URL:", adresa_okresu)
        html_okresu = BeautifulSoup(obsah_stranky_okres, "html.parser")
        vsechny_url_okresu = html_okresu.find_all("a")
        return vsechny_url_okresu
 
def dopln_url_obci(vsechny_adresy_okresu):
    """
    Ze vsech odkazu na strance okresu ziska obsah href, a pokud je v nich obsazen text "ps311", prida je do listu doplnek_url_obci

    Return:
        list: doplnek_url_obci 
    """
    doplnek_url_obci = []
    for odkaz in vsechny_adresy_okresu:
        href = odkaz.get('href')
        if href and "ps311" in href:
            doplnek_url_obci.append(href)
    return doplnek_url_obci
    
def ziskej_url_obci(url_obce_1_cast, doplnek_adresy_obci):
    """
    Vytvari url s vysledky vsech obci a z nich ziskava kod obce

    Returns:
        list: url_vsech_obci
    """
    url_vsech_obci = []
    [url_vsech_obci.append(url_obce_1_cast + url_obce_2_cast) for url_obce_2_cast in doplnek_adresy_obci]
    return url_vsech_obci

def jedna_adresa_obce(adresa_obci):
    """
    Ze seznamu vsech nalezenych url obci odstrani duplicity

    Returns:
        list: adresy_vsech_obci
    """
    adresy_vsech_obci = []
    for adresa_obce in adresa_obci:
        if adresa_obce not in adresy_vsech_obci:
            adresy_vsech_obci.append(adresa_obce)

    return adresy_vsech_obci

def nacti_obsah_stranky_obce(adresa_obce):
    """
    Nacte obsah stranky obsahujici vysledky obce

    Return:
        bs: html_obce
    """
    with requests.get(adresa_obce) as odpoved:
        html_obce = BeautifulSoup(odpoved.text, "html.parser")
    return html_obce

def ziskej_kod_obce(adresa_obce, vysledky_obce):
    """
    Ziska kod obce, a pokud jeste neni v seznamu vysledku obce, prida ho do nej

    Returns:
        dict: vysledky_obce
    """
    pomocny_kod_obce = adresa_obce.split("obec=")
    pomocny_kod_obce = pomocny_kod_obce[1].split("&")
    kod_obce = pomocny_kod_obce[0]
    if kod_obce not in vysledky_obce:
        vysledky_obce.update({"code": kod_obce})

    return vysledky_obce

def ziskej_nazev_obce(stranka_obce, vysledky_obce):
    """
    Najde vsechny tagy "h3" a vybere z nich ty obsahujíci slovo "obec".
    Prevede je na text, vybere a ocisti nazev obce a prida ho do listu vysledky_jmena_obci

    Return:
        dict: vysledky_obce
    """
    vsechny_h3 = list(stranka_obce.find_all("h3"))
    
    for obec in vsechny_h3:
        obec = obec.get_text()
        if "Obec:" in obec:
            vybrana_obec = (obec.split(": ")[1:])[0].strip()
    if vybrana_obec not in vysledky_obce:
            vysledky_obce.update({"location": vybrana_obec})

    return vysledky_obce

def ziskej_souhrny_obce(stranka_obce, vysledky_obce):
    """
    V obsahu stranky obce najde podle zadanych kriterii pocet volicu, odevzdanych obalek a platnych hlasu a prida je do vysledky_obce.

    Returns:
        dict: vysledky_obce
    """
    pocet_volicu = stranka_obce.find("td", class_="cislo", headers="sa2").get_text().replace("\xa0", "")
    vysledky_obce.update({"registered": pocet_volicu})

    pocet_obalek = stranka_obce.find("td", class_="cislo", headers="sa5").get_text().replace("\xa0", "")
    vysledky_obce.update({"envelopes": pocet_obalek})

    pocet_platnych = stranka_obce.find("td", class_="cislo", headers="sa6").get_text().replace("\xa0", "")
    vysledky_obce.update({"valid": pocet_platnych})

    return vysledky_obce

def ziskej_strany_a_hlasy(stranky_obce):
    """
    Vytvori list hlasu ze vsech tabulek vysledku voleb v dane obci

    Return:
        ResultSet: strany
        ResultSet: hlasy_obec
    """
    strany = obsah_stranky_obce.find_all("td", class_="overflow_name")

    hlasy_obec = stranky_obce.find_all("td", class_="cislo", headers="t1sa2 t1sb3")
    if len(stranky_obce) > 3:
        hlasy_t2 = stranky_obce.find_all("td", class_="cislo", headers="t2sa2 t2sb3")
        hlasy_obec += hlasy_t2
    if len(stranky_obce) > 4:
        hlasy_t3 = stranky_obce.find_all("td", class_="cislo", headers="t3sa2 t3sb3")
        hlasy_obec += hlasy_t3
        
    return strany, hlasy_obec

def pridej_strany_s_hlasy(nazev_strany, hlasy_V_obci, vysledky_obce):
    """
    Iteruje pres indexy nazev_strany a pridava v kazde iteraci do dictu vysledky_obce nazev strany a pocet hlasu

    Return:
        dict: vysledky_obce
    """
    for j in range(len(nazev_strany)):
          strana_j = nazev_strany[j].get_text()
          hlas_j = hlasy_V_obci[j].get_text().replace("\xa0", "")
          vysledky_obce.update({strana_j: hlas_j})

    return vysledky_obce

def pridej_a_zkontroluj_vysledky(vysledky):
    """
    Prida vysledek obce do finalniho vysledky a vytvori zahlavi pro export

    Return:
        list(dict): vysledky
        list: zahlavi
    """
    zahlavi = []
    vysledky.append(vysledky_obce)
    if vysledky:
        zahlavi = list(vysledky[0].keys())
    else:
        print("Nedošlo k načtení výsledků. Ověřte správnost zadané url adresy. Zkuste to znovu.")
        sys.exit(1)
    return vysledky, zahlavi

def export_do_csv(vystupni_soubor, vysledky, hlavicka):
    """
    Exportuje ziskane vysledky do souboru csv
    """
    print("UKLÁDÁM DO SOUBORU:", vystupni_soubor)
    with open (vystupni_soubor, mode="w", encoding="utf-8", newline="") as vysledky_csv:
        vysledky_writer = csv.DictWriter(vysledky_csv, fieldnames=hlavicka, delimiter=",")
        vysledky_writer.writeheader()
        vysledky_writer.writerows(vysledky)
    print("UKONČUJI:", sys.argv[0])   
     
if __name__ == "__main__":
    
    vysledky = []
    
    zkontroluj_vstupni_argumenty(sys.argv)
    url_okres, vystup_csv = nacti_vstupni_argumenty()
    vsechny_url_okresu = nacti_stranku_okresu(url_okres)
    doplnek_url_obci = dopln_url_obci(vsechny_url_okresu)

    url_obci = ziskej_url_obci("https://volby.cz/pls/ps2017nss/", doplnek_url_obci)

    url_obce = jedna_adresa_obce(url_obci)
            
    i = -1
    for url_kazde_obce in url_obce:
        vysledky_obce = {}
        i += 1

        obsah_stranky_obce = nacti_obsah_stranky_obce(url_kazde_obce)
        cislo_obce = ziskej_kod_obce(url_obce[i], vysledky_obce)
        nazev_obce = ziskej_nazev_obce(obsah_stranky_obce, vysledky_obce)
        ziskej_souhrny_obce(obsah_stranky_obce, vysledky_obce)
        strany, hlasy_obec = ziskej_strany_a_hlasy(obsah_stranky_obce)
        pridej_strany_s_hlasy(strany, hlasy_obec, vysledky_obce)
        vysledky, zahlavi = pridej_a_zkontroluj_vysledky(vysledky)

    export_do_csv(vystup_csv, vysledky, zahlavi)     