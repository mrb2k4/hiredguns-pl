"""Daje kudosy aktywnosciom osob obserwowanych na Stravie.

Logowanie:
  STRAVA_COOKIE   - wartosc ciasteczka _strava4_session (zalecane przy logowaniu przez Google)
  albo STRAVA_EMAIL + STRAVA_PASSWORD (jesli ustawisz haslo w Stravie)
Opcje:
  MAX_KUDOS (domyslnie 100), SCROLLS (domyslnie 15), DRY_RUN=1 - tylko liczy, nie klika
"""
import os
import random
import sys
import time

from playwright.sync_api import sync_playwright

FEED_URL = "https://www.strava.com/dashboard?feed_type=following"
MAX_KUDOS = int(os.getenv("MAX_KUDOS", "100"))
SCROLLS = int(os.getenv("SCROLLS", "15"))
DRY_RUN = os.getenv("DRY_RUN", "0") == "1"
# przycisk kudos, ktory jeszcze nie zostal klikniety (pusta ikonka)
UNFILLED = "button[data-testid='kudos_button']:has([data-testid='unfilled_kudos']):not([disabled])"


def pause():
    """Losowa przerwa miedzy kudosami: zwykle 3-12 s, czasem dluzsza (15-45 s)."""
    if random.random() < 0.15:
        time.sleep(random.uniform(15, 45))
    else:
        time.sleep(random.uniform(3, 12))


def login(page, context):
    cookie = os.getenv("STRAVA_COOKIE", "").strip()
    if cookie:
        context.add_cookies([{
            "name": "_strava4_session", "value": cookie,
            "domain": ".strava.com", "path": "/", "secure": True, "httpOnly": True,
        }])
        return
    email, password = os.getenv("STRAVA_EMAIL"), os.getenv("STRAVA_PASSWORD")
    if not (email and password):
        sys.exit("Brak STRAVA_COOKIE lub STRAVA_EMAIL/STRAVA_PASSWORD")
    page.goto("https://www.strava.com/login")
    for sel in ("#onetrust-accept-btn-handler", "button:has-text('Accept All')"):
        if page.locator(sel).count():
            page.locator(sel).first.click()
    page.fill("input[type='email'], #email", email)
    page.fill("input[type='password'], #password", password)
    page.keyboard.press("Enter")
    page.wait_for_load_state("networkidle")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            locale="pl-PL", timezone_id="Europe/Warsaw", viewport={"width": 1280, "height": 1000},
            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"),
        )
        page = context.new_page()
        try:
            login(page, context)
            page.goto(FEED_URL, wait_until="domcontentloaded")
            page.wait_for_timeout(4000)
            if "/login" in page.url or "/onboarding" in page.url:
                sys.exit("Nie zalogowano - ciasteczko wygaslo albo zle dane logowania")

            given = 0
            for _ in range(SCROLLS):
                buttons = page.locator(UNFILLED)
                while buttons.count() and given < MAX_KUDOS:
                    btn = buttons.first
                    btn.scroll_into_view_if_needed()
                    if DRY_RUN:
                        given += 1
                        btn.evaluate("b => b.removeAttribute('data-testid')")  # pomin przy liczeniu
                        continue
                    btn.click()
                    given += 1
                    pause()
                if given >= MAX_KUDOS:
                    break
                page.mouse.wheel(0, 4000)
                page.wait_for_timeout(2500)

            print(f"{'[DRY RUN] znaleziono' if DRY_RUN else 'Dano'} kudosow: {given}")
        except BaseException:
            page.screenshot(path="error.png", full_page=True)
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    main()
