#!/usr/bin/env python3
"""
Hired Guns PL - buduje polska wersje gry z oryginalnej instalacji WHDLoad.

Uzycie:
    python3 build.py SCIEZKA_DO_HiredGuns [KATALOG_WYJSCIOWY]

SCIEZKA_DO_HiredGuns - katalog instalacji WHDLoad (zawiera HiredGuns.Slave i game/).
KATALOG_WYJSCIOWY    - domyslnie ./HiredGunsPL

Polskie teksty trafiaja w miejsce wersji niemieckiej (CUSTOM2=2), ikona
HiredGuns.info dostaje CUSTOM2=2. Oryginalny katalog nie jest modyfikowany.
"""
import os, re, shutil, struct, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from texts.messages import PL as MSG_PL, EXTRA as MSG_EXTRA
from texts.items import ITEMS
from texts.world import W as WORLD, LEVELS as WORLD_LEVELS
from texts.outro import OUTRO
from texts.characters import PL as CHARS_PL

# ---------------------------------------------------------------- RNC ------
RNC_BIN = None

def rnc_tool():
    """Zwraca sciezke do rnc_propack (kompiluje z tools/rnc_propack jesli trzeba)."""
    global RNC_BIN
    if RNC_BIN:
        return RNC_BIN
    exe = os.path.join(HERE, 'tools', 'rnc_propack', 'rnc' + ('.exe' if os.name == 'nt' else ''))
    if not os.path.exists(exe):
        src = os.path.join(HERE, 'tools', 'rnc_propack', 'main.c')
        cc = shutil.which('gcc') or shutil.which('cc') or shutil.which('clang')
        if not cc:
            sys.exit('Brak kompilatora C (gcc/clang) do zbudowania tools/rnc_propack. '
                     'Zainstaluj gcc albo wrzuc gotowy plik rnc(.exe) do tools/rnc_propack/.')
        subprocess.run([cc, '-O2', '-o', exe, src], check=True, capture_output=True)
    RNC_BIN = exe
    return exe

def _rnc(mode, data):
    """Uruchamia rnc_propack w katalogu tymczasowym na sciezkach wzglednych
    (narzedzie traktuje sciezki zaczynajace sie od '/' jak opcje)."""
    with tempfile.TemporaryDirectory() as t:
        open(os.path.join(t, 'in.bin'), 'wb').write(data)
        args = [rnc_tool(), mode, 'in.bin', 'out.bin'] + (['-m=1'] if mode == 'p' else [])
        subprocess.run(args, cwd=t, check=True, capture_output=True)
        out = os.path.join(t, 'out.bin')
        if not os.path.exists(out):
            sys.exit('rnc_propack nie utworzyl pliku (%s)' % mode)
        return open(out, 'rb').read()

def rnc_unpack(path):
    data = open(path, 'rb').read()
    return _rnc('u', data) if data[:3] == b'RNC' else data

def rnc_pack(data, dest):
    packed = _rnc('p', data)
    if _rnc('u', packed) != data:
        sys.exit('Blad weryfikacji RNC: ' + dest)
    open(dest, 'wb').write(packed)

# ---------------------------------------------------------- Phrasebook ----
def pb_encode(t):
    big = t.startswith('{BIG}')
    if big:
        t = t[5:]
    t = t.replace('\\n', '\xfe').replace('{C}', '\xfc').replace('{I}', '\xfd')
    b = bytearray()
    for ch in t:
        c = ord(ch)
        if c > 255 or not (32 <= c < 127 or c in (0xfc, 0xfd, 0xfe)):
            raise ValueError('niedozwolony znak %r w: %s' % (ch, t))
        if big and 0x41 <= c <= 0x5f:
            c -= 0x20          # duza czcionka: litery przesuniete o 0x20
        b.append(c)
    return bytes(b)

def build_phrasebook(orig):
    n = struct.unpack('>H', orig[:2])[0] // 2
    offs = [struct.unpack('>H', orig[i*2:i*2+2])[0] for i in range(n)]
    pl = {}
    for ln in open(os.path.join(HERE, 'texts', 'phrasebook.tsv'), encoding='ascii').read().split('\n'):
        if ln:
            k, _, v = ln.partition('\t'); pl[int(k)] = v
    assert sorted(pl) == list(range(n)), 'phrasebook.tsv: brak wpisow'
    new = [pb_encode(pl[i]) for i in range(n)]
    order = sorted(range(n), key=lambda i: offs[i])
    data = bytearray(); pos = {}
    base = n * 2
    for i in order:
        pos[i] = base + len(data); data += new[i] + b'\xf5'
    out = b''.join(struct.pack('>H', pos[i]) for i in range(n)) + data + b'\x00'
    if len(out) % 2:
        out += b'\x00'
    return out

# ------------------------------------------------------------ Messages ----
def msg_parse(d):
    H = lambda o: struct.unpack('>H', d[o:o+2])[0]
    pairs = [struct.unpack('>HH', d[i*4:i*4+4]) for i in range(25)]
    slots = []
    for g, (n, off) in enumerate(pairs):
        for k in range(n):
            slots.append(((g, k), H(off+2*k)))
    slots += [(('w', 100), H(100)), (('w', 102), H(102))]
    recs = {o: (d[o:o+8], d[o+8:d.index(b'\x00', o+8)]) for _, o in slots}
    return pairs, slots, recs

def msg_translate(b):
    for k, v in MSG_EXTRA.items():
        b = b.replace(k, v)
    def rep(m):
        t = m.group(1).decode('latin1')
        if t not in MSG_PL:
            raise KeyError('Brak tlumaczenia kwestii: ' + t)
        return b'"' + MSG_PL[t].encode('ascii') + b'"'
    return re.sub(rb'"([^"]*)"', rep, b)

def build_messages(ger, gamefast):
    # angielskie kwestie siedza w GameFast.dat w tym samym formacie
    i = gamefast.find(ger[:16])
    if i < 0:
        sys.exit('Nie znaleziono angielskich kwestii w GameFast.dat')
    eng = gamefast[i:i+len(ger)+4096]
    pe, se, re_ = msg_parse(eng)
    pg, sg, rg = msg_parse(ger)
    slot_en = {k: re_[o][1] for k, o in se}
    first = {}
    for k, o in sg:
        first.setdefault(o, k)
    order = sorted(first)
    hdr = order[0]
    body = bytearray(); newoff = {}
    for o in order:
        newoff[o] = hdr + len(body)
        rec = rg[o][0] + msg_translate(slot_en[first[o]]) + b'\x00'
        if len(rec) % 2:
            rec += b'\x00'
        body += rec
    out = bytearray(ger[:hdr])
    H = lambda o: struct.unpack('>H', ger[o:o+2])[0]
    for n, off in pg:
        for k in range(n):
            p = off + 2*k; out[p:p+2] = struct.pack('>H', newoff[H(p)])
    for w in (100, 102):
        out[w:w+2] = struct.pack('>H', newoff[H(w)])
    return bytes(out + body)

# --------------------------------------------------------------- Items ----
def item_groups(b):
    out = []; last = -1
    for m in re.finditer(rb'\xf7([t!])([^\x00]*)\x00', b):
        if m.start() != last:
            out.append([])
        out[-1].append((m.start(), m.group(1), m.group(2))); last = m.end()
    return out

def wrap(text, width):
    lines = []; cur = ''
    for w in text.split():
        while len(w) > width:
            room = width - (len(cur) + 1 if cur else 0)
            if room >= 4:
                part = w[:room-1] + '-'
                cur = (cur + ' ' + part) if cur else part
                lines.append(cur); cur = ''; w = w[room-1:]
            else:
                lines.append(cur); cur = ''
        if not cur:
            cur = w
        elif len(cur) + 1 + len(w) <= width:
            cur += ' ' + w
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

def build_items(ger):
    d = bytearray(ger); errs = []
    for i, g in enumerate(item_groups(ger)):
        titles, desc = ITEMS[i]
        tl = [x for x in g if x[1] == b't']; dl = [x for x in g if x[1] == b'!']
        for (pos, _, old), t in zip(tl, titles):
            if len(t) > len(old):
                errs.append('przedmiot %d: nazwa "%s" za dluga (max %d)' % (i, t, len(old))); continue
            d[pos+2:pos+2+len(old)] = t.encode('ascii') + b'~' * (len(old) - len(t))
        lines = wrap(desc, 16)
        if len(lines) > len(dl):
            errs.append('przedmiot %d: opis za dlugi (%d linii, max %d)' % (i, len(lines), len(dl))); continue
        lines += [''] * (len(dl) - len(lines))
        for (pos, _, old), l in zip(dl, lines):
            d[pos+2:pos+2+len(old)] = l.replace(' ', '\x7f').encode('ascii') + b'~' * (len(old) - len(l))
    if errs:
        sys.exit('\n'.join(errs))
    return bytes(d)

# ------------------------------------------------------- WorldForeign -----
def build_world(orig):
    w = bytearray(orig); sec = len(w) // 4          # 4 jezyki: fre, ger, ita, spa
    pos = [sec + m.start() for m in re.finditer(rb'\xfb..\x00.\xfc', orig[sec:2*sec], re.S)]
    assert len(pos) == 282
    errs = []
    def put(idx, text):
        if len(text) > 60:
            errs.append('lokacja: linia za dluga (%d): %s' % (len(text), text)); return
        p = pos[idx] + 6
        w[p:p+60] = text.encode('ascii') + b'~' * (60 - len(text))
    for n in range(1, 48):
        b = (n - 1) * 6
        if n in WORLD:
            t, th, desc = WORLD[n]
            put(b, t); put(b+1, th)
            lines = wrap(desc, 60) if desc else []
            if len(lines) > 4:
                errs.append('lokacja %d: opis za dlugi' % n); continue
            for k, l in enumerate(lines + [''] * (4 - len(lines))):
                put(b+2+k, l)
        else:
            L = WORLD_LEVELS[n]; put(b, ''); put(b+1, '')
            for k, l in enumerate(L + [''] * (4 - len(L))):
                put(b+2+k, l)
    if errs:
        sys.exit('\n'.join(errs))
    return bytes(w)

# --------------------------------------------------------------- Outro ----
def build_outro(ger):
    offs = [struct.unpack('>I', ger[i:i+4])[0] for i in range(0, 48, 4)] + [len(ger)]
    segs = []
    for k in range(12):
        seg = ger[offs[k]:offs[k+1]]
        lines = [(struct.unpack('>H', m.group(1))[0], struct.unpack('>H', m.group(2))[0])
                 for m in re.finditer(rb'\xfb(..)(..)\xfc', seg, re.S)]
        x0, y0 = lines[0]
        pl = OUTRO[k]
        y0 += (len(lines) - len(pl)) * 5            # zachowaj srodek bloku
        body = b'\xf8\x02'
        for i, t in enumerate(pl):
            if len(t) > 48:
                sys.exit('zakonczenie: linia za dluga: ' + t)
            body += b'\xfb' + struct.pack('>HH', x0, y0 + 10*i) + b'\xfc' + t.encode('ascii')
        segs.append(body + b'\x00')
    hdr = b''; p = 48
    for s in segs:
        hdr += struct.pack('>I', p); p += len(s)
    out = hdr + b''.join(segs)
    return out + (b'\x00' if len(out) % 2 else b'')

# ---------------------------------------------------------- Characters ----
def build_characters(orig):
    d = bytearray(orig); B, R, LANG, SLOT = 3264, 272, 2, 33   # blok 2 = niemiecki
    for c in range(12):
        o = LANG*B + c*R; rec = orig[o:o+R]
        at = lambda off: rec[off:rec.index(b'\x00', off)]
        origin = at(0).strip().replace(b'ursprung unbekannt', b'pochodzenie nieznane')
        race, prof = CHARS_PL[c]
        region = b''
        for t in (origin, at(33).strip(), race.encode('ascii'), prof.encode('ascii')):
            if len(t) > SLOT - 1:
                sys.exit('postac %d: tekst za dlugi: %s' % (c, t))
            seg = t + b'\x00'
            region += seg + b' ' * (SLOT - len(seg))
        d[o:o+132] = region            # gra czyta linie od stalych pozycji 0/33/66/99
    return bytes(d)

# ---------------------------------------------------------------- Icon ----
def build_icon(orig):
    old = b'\x00\x00\x00\x0c(CUSTOM2=X)\x00'
    if old not in orig:
        return orig
    return orig.replace(old, b'\x00\x00\x00\x0aCUSTOM2=2\x00', 1)

# ---------------------------------------------------------------- main ----
def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = os.path.abspath(sys.argv[1])
    dst = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.getcwd(), 'HiredGunsPL'))
    g = lambda *p: os.path.join(src, 'game', *p)
    if not os.path.exists(g('Languages', 'Phrasebook.ger')):
        sys.exit('To nie wyglada na instalacje Hired Guns (brak game/Languages/Phrasebook.ger): ' + src)
    if os.path.exists(dst):
        sys.exit('Katalog wyjsciowy juz istnieje: ' + dst)
    shutil.copytree(src, dst)
    o = lambda *p: os.path.join(dst, 'game', *p)

    print('Menu i komunikaty...')
    pb = build_phrasebook(rnc_unpack(g('Languages', 'Phrasebook.eng')))
    rnc_pack(pb, o('Languages', 'Phrasebook.ger'))
    rnc_pack(pb, o('Languages', 'Phrasebook.eng'))
    print('Kwestie najemnikow...')
    rnc_pack(build_messages(rnc_unpack(g('Game', 'Messages.ger')),
                            rnc_unpack(g('Game', 'GameFast.dat'))), o('Game', 'Messages.ger'))
    print('Przedmioty...')
    rnc_pack(build_items(rnc_unpack(g('Game', 'Items.ger'))), o('Game', 'Items.ger'))
    print('Dziennik lokacji...')
    rnc_pack(build_world(rnc_unpack(g('World', 'WorldForeign.dat'))), o('World', 'WorldForeign.dat'))
    print('Zakonczenie...')
    rnc_pack(build_outro(rnc_unpack(g('Front', 'Outro.ger'))), o('Front', 'Outro.ger'))
    print('Ekran wyboru postaci...')
    rnc_pack(build_characters(rnc_unpack(g('ChSelect', 'Characters.dat'))), o('ChSelect', 'Characters.dat'))
    print('Ikona (CUSTOM2=2)...')
    ic = os.path.join(src, 'HiredGuns.info')
    if os.path.exists(ic):
        open(os.path.join(dst, 'HiredGuns.info'), 'wb').write(build_icon(open(ic, 'rb').read()))
    print('Gotowe: ' + dst)

if __name__ == '__main__':
    main()
