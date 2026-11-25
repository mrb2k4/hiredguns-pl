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
