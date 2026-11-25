"""Uruchamia kudos.py raz w kazdym oknie czasowym, o losowej porze.

WINDOWS - okna "HH:MM-HH:MM" oddzielone spacja (moga przechodzic przez polnoc),
          domyslnie "07:00-09:00 23:00-01:00". Czas wg zmiennej TZ.
"""
import os
import random
import subprocess
import sys
import time
from datetime import datetime, timedelta

WINDOWS = os.getenv("WINDOWS", "07:00-09:00 23:00-01:00").split()


def windows_around(now):
    """Zwraca (start, koniec) wszystkich okien z wczoraj, dzis i jutro."""
    for day in (-1, 0, 1):
        base = (now + timedelta(days=day)).replace(second=0, microsecond=0)
        for w in WINDOWS:
            a, b = w.split("-")
            start = base.replace(hour=int(a[:2]), minute=int(a[3:]))
            end = base.replace(hour=int(b[:2]), minute=int(b[3:]))
            if end <= start:
                end += timedelta(days=1)
            yield start, end


def next_run(now, done):
    """Najblizsze okno, w ktorym jeszcze nie bylo uruchomienia -> losowa chwila w nim."""
    start, end = min((s, e) for s, e in windows_around(now) if e > now and s not in done)
    lo = max(start, now)
    return start, lo + timedelta(seconds=random.uniform(0, (end - lo).total_seconds()))


def main():
    done = set()
    while True:
        window, at = next_run(datetime.now(), done)
        print(f"Nastepne uruchomienie: {at:%Y-%m-%d %H:%M:%S} (okno od {window:%H:%M})", flush=True)
        time.sleep(max(0, (at - datetime.now()).total_seconds()))
        print(f"=== {datetime.now():%Y-%m-%d %H:%M:%S} ===", flush=True)
        subprocess.run([sys.executable, "kudos.py"])
        done = {window} | {w for w in done if w > datetime.now() - timedelta(days=2)}


if __name__ == "__main__":
    main()
