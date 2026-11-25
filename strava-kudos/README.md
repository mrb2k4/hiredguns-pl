# Strava – automatyczne kudosy

GitHub Actions codziennie ok. **23:10** i **07:05** (czas polski) otwiera feed
„Obserwowani” na Stravie i klika kudos przy każdej aktywności, która go jeszcze nie ma.

## Konfiguracja (raz)

Konto Strava logowane przez Google → najprościej podać ciasteczko sesji:

1. Zaloguj się na strava.com w przeglądarce na komputerze.
2. F12 → *Application* (Chrome) / *Storage* (Firefox) → *Cookies* → `https://www.strava.com`.
3. Skopiuj wartość `_strava4_session`.
4. GitHub → repo → *Settings → Secrets and variables → Actions → New repository secret*:
   nazwa `STRAVA_COOKIE`, wartość = skopiowany ciąg.

Alternatywa: ustaw hasło w Stravie („Nie pamiętasz hasła?” na swój Gmail) i dodaj
sekrety `STRAVA_EMAIL` + `STRAVA_PASSWORD` (mniej pewne – Strava może pokazać captchę).

Gdy ciasteczko wygaśnie (wylogowanie, zmiana hasła), workflow zakończy się błędem
„Nie zalogowano” – wtedy podmień `STRAVA_COOKIE`.

## Test

*Actions → Strava kudosy → Run workflow* z zaznaczonym „Tylko policz” – pokaże,
ile kudosów by dał. Przy błędzie w artefaktach jest `error-screenshot`.

## Uwagi

- Harmonogram działa tylko z gałęzi domyślnej (`main`).
- GitHub potrafi opóźnić cron o kilka–kilkadziesiąt minut.
- Strava nie ma oficjalnego API do kudosów, więc to klikanie w przeglądarce; automatyzacja
  jest niezgodna z regulaminem Stravy – limit `MAX_KUDOS` (100) i losowe przerwy
  zmniejszają ryzyko, ale go nie eliminują.

## NAS / Docker

Na NAS-ie (x86_64 lub ARM64, min. 1 GB RAM, Docker / Container Manager):

1. Skopiuj katalog `strava-kudos` na NAS (np. `/volume1/docker/strava-kudos`).
2. `cp .env.example .env` i wpisz w nim `STRAVA_COOKIE`.
3. Test: `docker compose run --rm -e DRY_RUN=1 strava-kudos python kudos.py`
4. Start: `docker compose up -d` – logi: `docker logs -f strava-kudos`.

Godziny zmienisz w `RUN_AT` w `docker-compose.yml`.
