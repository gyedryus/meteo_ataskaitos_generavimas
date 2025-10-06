# Meteorologinių Rodiklių Analizė ir Ataskaitos Generavimas

Šis įrankis buvo parengta, siekiant automatizuoti meteorologinių duomenų nuskaitymą, šių duomenų analizę ir apibendrinančios ataskaitos generavimą.

---

## 1. Duomenų Šaltinis ir Nuskaitymas

Modulyje naudojami **api.meteo.lt** viešai prieinami duomenys.

* **Duomenų Nuskaitymo Programa:** Sukurtas modulis atsakingas už duomenų nuskaitymą ir surinkimą. Programa surenka **istorinius duomenis** pasirinktam (nurodytos trukmės) laiko intervalui.
* **Laiko Eilučių Tvarkymas:** Visi surinkti duomenys apdorojami, užtikrinant teisingą laiko eilučių tvarką ir tikslumą.

---

## 2. Istorinių Duomenų Analizė ir Skaičiavimai

Remiantis surinktu istoriniu duomenų masyvu, atliekami šie pagrindiniai rodiklių skaičiavimai:

1.  **Vidutinė Temperatūra:** Apskaičiuojama bendra laikotarpio vidutinė oro temperatūra.
2.  **Vidutinė Oro Drėgmė:** Apskaičiuojama bendra laikotarpio vidutinė oro drėgmė.
3.  **Dienos ir Nakties Temperatūra:** Apskaičiuojama atskira vidutinė temperatūra **dienos** ir **nakties** laikotarpiams. Skaičiavimai atliekami atsižvelgiant į **Lietuvos laiko zoną (LT)**.
4.  **Kritulių Prognozės Įvertinimas:** Įvertinamas ir suskaičiuojamas savaitgalių (Šeštadienis/Sekmadienis) skaičius per visą analizuojamą laikotarpį, kuriam buvo prognozuotas lietus.

---

## 3. Duomenų Vizualizacija ir Sujungimas su Prognoze

* **Grafiko Generavimas:** Parengiamas linijinis grafikas, atvaizduojantis **interpoliuotus paskutinės savaitės stebėtus duomenis** ir **ilgalaikę prognozę**. Grafikas vizualiai sujungia istorinius duomenis ir prognozę į vieną vientisą kreivę.
* **Grafiko Įkėlimas:** Grafikas išsaugomas PNG formatu tame pačiame aplanke, vėliau panaudojant jį rengiant ataskaitą.

---

## 4. Ataskaitos Generavimas (Automatizacija)

Visi apskaičiuoti rodikliai ir sugeneruotas grafikas yra automatiškai pateikiami vartotojui naudojant iš anksto paruoštą ataskaitos šabloną:

* **Šablonų Variklis:** Naudojamas **Jinja2** šablonų variklis HTML ataskaitos struktūrai paruošti.
* **Duomenų Perdavimas:** Visi skaičiavimų rezultatai bei parengta vizualizacija perduodama į šabloną.
* **PDF Konvertavimas:** Galutinė ataskaita iš HTML konvertuojama į **PDF formatą** naudojant **WeasyPrint** biblioteką, užtikrinant tvarkingą ir reprezentatyvų ataskaitos pateikimą.