T = "SZACOWANE ZAGROZENIE: {}"
END_ALL = "MISJA WYMAGA, BY WSZYSCY UCZESTNICY OPUSCILI STREFE."
END_FIRST = "WYGRYWA PIERWSZY UCZESTNIK, KTORY DOTRZE DO WYJSCIA."
# (title, threat, description)  description None = keep empty
W = {
1: ("WPIS 1. Sztuczna wyspa.", T.format(1), "WPIS 1. Sztuczna wyspa zbudowana na fundamencie z odpadow przemyslowych. Wymiary ok. 3 na 5 km. UWAGA: zrodlo podczerwieni 54 m ponizej sredniego poziomu morza. KONIEC."),
2: ("WPIS 2. System jaskin.", T.format(2), "WPIS 2. System jaskin. Wyrazna szczelina w skale (12 m szerokosci) moze byc schronieniem. Dziennik pierwszych osadnikow wspomina o \"...ogromnym i zawilym systemie jaskin...\". KONIEC."),
3: ("WPIS 3. Laboratorium doswiadczalne.", T.format(4), "WPIS 3. Laboratorium doswiadczalne. Strefa wysokiego bezpieczenstwa ze stanowiskami badan biomedycznych, terraformowania i warstwowania plaszcza. Ryzyko skazenia minimalne. KONIEC."),
4: ("WPIS 4. Laboratorium.", T.format(6), "WPIS 4. Laboratorium. Laboratorium wysokiego bezpieczenstwa, najwyrazniej specjalizujace sie w bioterraformowaniu. UWAGA: potwierdzono nielegalne rozmieszczenie autostraznikow AVT-789."),
5: ("WPIS 5. Rafineria.", T.format(8), "WPIS 5. Rafineria. Zajmuje wielki obszar i rownie wysoko wznosi sie w powietrze. Szescian z rur i zbiornikow, wokol ktorego roj automatycznych transportow rozwozi produkt po planecie. KONIEC."),
6: ("WPIS 6. Osiedle miejskie.", T.format(6), "WPIS 6. Zamkniete miasto Ghule. Chronione ogromna kopula przed wroga pogoda i wyzszym promieniowaniem tla Graveyard. W obrzezu jest wiele sluz, ale dostepna tylko jedna. KONIEC."),
7: ("WPIS 7. Opuszczony magazyn.", T.format(1), "WPIS 7. Opuszczony magazyn. Przy kurczacym sie rynku dobrych maszyn do terraformowania ten magazyn dlugoterminowy stoi teraz pusty. KONIEC."),
8: ("WPIS 8. Brak w rejestrze.", T.format(8), "WPIS 8. Brak w rejestrze. Obecnie brak informacji o wskazanym miejscu. KONIEC. Drugorzedny cel misji wymaga rozpoznania tego miejsca w celu zebrania danych."),
9: ("WPIS 9. Swiatynia.", T.format(8), "WPIS 9. Swiatynia Horazima. Stosunkowo nowa budowla, w ktorej spoczywa Horazim, zalozyciel religii Duone, a przynajmniej jej glowny propagator. KONIEC."),
10: ("WPIS 10. Sklad amunicji.", T.format(6), "WPIS 10. Sklad amunicji. Silnie oslonieta bunkier, jedyne wejscie wkute w skale u podstawy zwietrzalego wystepu. KONIEC."),
11: ("WPIS 11. Wieza lacznosci satelitarnej.", T.format(9), "WPIS 11. Wieza lacznosci satelitarnej. Glowny zespol anten w najwyzszym punkcie gory, do silnych transmisji na inne zamieszkane swiaty systemu. KONIEC."),
12: ("WPIS 12. Bateria obronna.", T.format(7), "WPIS 12. Bateria obronna. Planetarne lasery obronne. Zainstalowano je na wiekszosci zamieszkanych planet po ostatniej wojnie, w ktorej okazaly sie nieocenione. KONIEC."),
13: ("WPIS 13. Strefa zrzutu.", "BRAK ZAGROZENIA", None),
14: ("WPIS 14. Swiatynia.", T.format(9), "WPIS 14. Swiatynia. Zwana M'aziir Diy Allogh, czyli Siedziba Wybranych, ta budowla religijna jest czesciej znana po prostu jako Swiatynia Duone. KONIEC."),
15: ("WPIS 15. Krypty grobowe.", T.format(10), "WPIS 15. Krypty grobowe. Ten grobowiec nigdy nie dostal nazwy. Zapelnil sie tak szybko, ze trzeba bylo zaczac budowe kolejnego. Spoczywaja w nim glownie ofiary wojny. KONIEC."),
16: ("WPIS 16.", T.format(0), "WPIS 16."),
17: ("WPIS 17. Centrum operacyjne.", T.format(9), "WPIS 17. Centrum operacyjne. Kazda terraformowana planeta ma centrum operacyjne i Graveyard nie jest wyjatkiem. Po wycofaniu funduszy taki obiekt czesto staje sie zbedny. KONIEC."),
18: ("WPIS 18. Reaktor fuzyjny.", T.format(3), "WPIS 18. Reaktor fuzyjny. Obecnie jedyne glowne zrodlo energii planety, odkad wycofano fundusze na program hydroelektryczny. KONIEC."),
19: ("WPIS 19. Odsalarnia.", T.format(3), "WPIS 19. Odsalarnia. Zaprojektowana na kolejne 40 lat ciaglej pracy. Zmniejszy zasolenie wschodniego oceanu Graveyard o 15%, co pozwoli hodowac obce morskie zycie. KONIEC."),
20: ("WPIS 20. Osiedle miejskie.", T.format(9), "WPIS 20. Osiedle miejskie. Duze, rozlegle miasto, zlozone glownie z osrodkow administracyjnych i politycznych. KONIEC."),
21: ("WPIS 21. Port kosmiczny.", T.format(15), "WPIS 21. Port kosmiczny. Wyrzutnia promow to punkt startowy do reszty systemu. Caly ruch kosmiczny kierowany jest tutaj albo na druga strone planety. KONIEC."),
22: ("WPIS 22.", T.format(0), "WPIS 22."),
}
# action / training levels: exact 4 description lines (title/threat empty)
A=["MISJA WYMAGA, BY WSZYSCY UCZESTNICY","OPUSCILI STREFE."]
F=["WYGRYWA PIERWSZY UCZESTNIK,","KTORY DOTRZE DO WYJSCIA."]
LEVELS = {
23: ["*** ZAGRODA DLA ZWIERZAT ***", "Projekt: D. Hally"]+A,
25: ["*** REAKTOR ***", "Projekt: M. Good"]+A,
26: ["*** WIEZIENIE ***", "Projekt: I. Dunlop"]+A,
27: ["*** PRZETRWANIE ***", "Projekt: M. Good"]+A,
28: ["*** OGROD JARRYSA ***", "Projekt: G. Anderson"]+F,
29: ["*** BITWA LEMINGOW - ROZDZIAL PIERWSZY ***", "Projekt: G. Anderson"]+F,
30: ["*** GENERATOR MOCY ***", "Projekt: M. Good"]+F,
31: ["*** PSYCHIATRYK ***", "Projekt: G. Anderson"]+F,
33: ["*** WIELKA SZYCHA ***", "Projekt: G. Anderson"]+F,
34: ["*** DROGA DO SMIERCI ***", "Projekt: M. Good"]+F,
35: ["*** BATMOBIL ***", "Projekt: S. Johnston"]+F,
37: ["*** PARK BUCKMINSTER - DATOWANIE WEGLEM ***", "Projekt: G. Anderson"]+F,
38: ["*** CENTRUM ROZRYWKI ***", "Projekt: S. Hammond"]+F,
39: ["*** SALA SZKIELETOW ***", "Projekt: D. Hally"]+F,
40: ["*** CENTRUM ROZBUDOWY MIASTA ***", "Projekt: S. Hammond"]+F,
41: ["*** CENTRUM HANDLOWE GRAVEYARD ***", "Projekt: M. Good"]+F,
42: ["*** BITWA LEMINGOW - ROZDZIAL DRUGI ***", "Projekt: G. Anderson"]+F,
}
for n in range(43,48): LEVELS[n]=["*** STREFA TRENINGOWA %d ***"%(n-42)]+F+[""]
for n in (24,32,36): W[n]=("WPIS %d."%n, T.format(0), "WPIS %d."%n)
