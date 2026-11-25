#!/bin/bash
# Uruchamia kudos.py codziennie o godzinach z RUN_AT (czas wg TZ, domyslnie 23:10 i 07:05).
RUN_AT="${RUN_AT:-23:10 07:05}"
cd "$(dirname "$0")"
python -c "import playwright" 2>/dev/null || pip install -q -r requirements.txt
echo "Start harmonogramu: $RUN_AT ($(date))"
while true; do
  now=$(date +%H:%M)
  for t in $RUN_AT; do
    if [ "$now" = "$t" ]; then
      echo "=== $(date) ==="
      python kudos.py
      sleep 61   # nie uruchamiaj drugi raz w tej samej minucie
    fi
  done
  sleep 20
done
