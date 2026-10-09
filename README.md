# Hired Guns PL

Fanowska polonizacja gry **Hired Guns** (DMA Design / Psygnosis, 1993) na Amigę,
dla instalacji **WHDLoad**.

> Repozytorium **nie zawiera gry** ani jej plików. Zawiera tylko polskie teksty
> i skrypt, który z Twojej własnej kopii gry buduje wersję polską.

## Co jest przetłumaczone

| Element | Plik w grze | Tekst w repo |
|---|---|---|
| Menu, komunikaty, zapis/odczyt | `Languages/Phrasebook.ger` | `texts/phrasebook.tsv` |
| Kwestie najemników w trakcie gry | `Game/Messages.ger` | `texts/messages.py` |
| Nazwy i opisy przedmiotów (114) | `Game/Items.ger` | `texts/items.py` |
| Dziennik lokacji na mapie świata (47) | `World/WorldForeign.dat` | `texts/world.py` |
| Zakończenie (losy 12 postaci) | `Front/Outro.ger` | `texts/outro.py` |
| Opisy postaci na ekranie wyboru | `ChSelect/Characters.dat` | `texts/characters.py` |

Polska wersja zajmuje miejsce wersji niemieckiej, a ikona `HiredGuns.info`
dostaje tooltype `CUSTOM2=2`, więc gra uruchamia się od razu po polsku.

**Jeszcze nie przetłumaczone:** napisy narysowane jako grafika (np. FITNESS,
PHYSIQUE, AGILITY na ekranie statystyk), brak polskich znaków (ą, ę, ł…).

## Jak zbudować

Potrzebne: **Python 3** oraz kompilator C (`gcc`/`clang`, do narzędzia RNC
ProPack; na Windows np. MSYS2/MinGW albo WSL).

```
python3 build.py ŚCIEŻKA/DO/HiredGuns  [KATALOG_WYJŚCIOWY]
```

- `ŚCIEŻKA/DO/HiredGuns` – katalog instalacji WHDLoad (ten z `HiredGuns.Slave`
  i podkatalogiem `game/`).
- wynik trafia do `./HiredGunsPL` (oryginał nie jest zmieniany).

Gotowy katalog `HiredGunsPL` kopiujesz na Amigę / do emulatora i uruchamiasz
ikoną **HiredGuns** (WHDLoad).

> Uwaga: do kopiowania na obrazy HDF używaj WinUAE (katalog podpięty jako dysk)
> albo samej Amigi. Zapis na HDF przez DiskFlashback potrafi uszkodzić system plików.

## Jak poprawiać tłumaczenie

Każdy plik w `texts/` to zwykły tekst. Zasady:

- **bez polskich znaków** (czcionki gry ich nie mają – na razie),
- **długość pól jest ograniczona** – skrypt przerwie budowanie i powie, który
  tekst jest za długi:
  - nazwa przedmiotu: 4 linie po 13 znaków, opis: 10 linii po 16 znaków (łamany automatycznie),
  - dziennik lokacji: tytuł 60 znaków, opis 4 linie po 60 (łamany automatycznie),
  - zakończenie: maks. 48 znaków w linii,
  - ekran postaci: maks. 32 znaki w linii,
- `phrasebook.tsv`: kody `{C}` = wyśrodkuj, `{I}` = pozycja menu, `\n` = nowa
  linia, `{BIG}` = duża czcionka (tylko A–Z i spacja). Pierwsza pozycja menu (F1)
  ma dodatkową spację na początku – tak jak w oryginale.

Po zmianie zbuduj grę, sprawdź w emulatorze i wyślij pull request ze zrzutem ekranu.

## Zgłaszanie błędów

Issues → „Błąd w tłumaczeniu”. Dołącz zrzut ekranu i opis, gdzie w grze to widać.

## Szczegóły techniczne

- Pliki gry są spakowane **RNC ProPack (metoda 1)**. Źródło narzędzia:
  `tools/rnc_propack` (Lab 313, licencja w `tools/rnc_propack/LICENSING`),
  kompiluje się automatycznie przy pierwszym budowaniu.
- Język wybiera tooltype WHDLoad `CUSTOM2` (0 ENG, 1 FRE, 2 GER, 3 ITA, 4 SPA).
- Angielskie kwestie i opisy przedmiotów są wbudowane w `Game/GameFast.dat` –
  skrypt bierze z nich tekst źródłowy, a układ plików z wersji niemieckiej.
- `ChSelect/Characters.dat`: 5 bloków językowych po 12 rekordów; gra czyta linie
  od stałych pozycji 0/33/66/99 w rekordzie.

## Prawa

Hired Guns © 1993 Psygnosis / DMA Design. Projekt jest nieoficjalny, niekomercyjny
i nie rozpowszechnia żadnych plików gry. Do zbudowania polskiej wersji potrzebna
jest własna, legalna kopia gry.

Skrypty i teksty tłumaczenia: licencja MIT (plik `LICENSE`).
