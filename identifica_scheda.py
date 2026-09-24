#!/usr/bin/env python3
"""
identifica_scheda.py - identifica una scheda a contatti (SIM, SAM, pay-TV, Java Card...)
a partire dall'ATR (Answer To Reset), usando il database pubblico smartcard_list.txt
di Ludovic Rousseau (https://pcsc-tools.apdu.fr/).

Modi d'uso:

  1) Lettura automatica da un lettore PC/SC (Windows con driver Argolis PC/SC,
     oppure qualunque lettore CCID su Windows/Linux/macOS). Richiede pyscard:
         pip install pyscard
         python identifica_scheda.py

  2) ATR gia' noto (per esempio copiato dal log di OSCam o da pcsc_scan):
         python identifica_scheda.py --atr "3B 9F 95 80 1F C7 80 31 E0 73 FE 21 1B 64 07 ..."

  3) Estrazione dell'ATR da un file di log di OSCam:
         python identifica_scheda.py --oscam-log /var/log/oscam.log

Il database viene scaricato la prima volta e salvato accanto allo script
(smartcard_list.txt); usare --aggiorna per riscaricarlo.
"""

import argparse
import os
import re
import sys
import urllib.request

DB_URL = "https://pcsc-tools.apdu.fr/smartcard_list.txt"
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "smartcard_list.txt")

# Stringhe ASCII che, se compaiono nei byte storici, identificano subito la famiglia.
FIRME_ASCII = [
    ("IRDETO", "pay-TV Irdeto"),
    ("DNASP", "pay-TV Nagravision (Nagra)"),
    ("MIFARE", "SAM NXP MIFARE (Secure Access Module)"),
    ("SAM", "SAM (Secure Access Module)"),
    ("JCOP", "Java Card NXP JCOP"),
    ("JavaCard", "Java Card"),
    ("Java", "Java Card"),
    ("OMNIKEY", "lettore/scheda HID Omnikey"),
    ("SIM", "SIM / USIM"),
    ("USIM", "USIM (UMTS/LTE)"),
    ("Gemplus", "scheda Gemplus/Gemalto"),
    ("Oberthur", "scheda Oberthur/IDEMIA"),
    ("G&D", "scheda Giesecke+Devrient"),
]


def normalizza_atr(testo):
    """Accetta '3B9F95...' o '3b 9f 95' o '3B:9F:95' e restituisce 'AA BB CC ...'."""
    esa = re.sub(r"[^0-9A-Fa-f]", "", testo)
    if len(esa) < 4 or len(esa) % 2:
        raise ValueError("ATR non valido: %r" % testo)
    return " ".join(esa[i:i + 2] for i in range(0, len(esa), 2)).upper()


def carica_db(aggiorna=False):
    if aggiorna or not os.path.exists(DB_FILE):
        print("Scarico il database ATR da %s ..." % DB_URL)
        try:
            with urllib.request.urlopen(DB_URL, timeout=30) as risp, open(DB_FILE, "wb") as f:
                f.write(risp.read())
        except Exception as e:  # noqa: BLE001
            if os.path.exists(DB_FILE):
                print("  scaricamento fallito (%s), uso la copia locale" % e)
            else:
                raise SystemExit("Impossibile scaricare il database: %s" % e)
    voci = []
    pattern, descr = None, []
    with open(DB_FILE, encoding="utf-8", errors="replace") as f:
        for riga in f:
            riga = riga.rstrip("\n")
            if riga.startswith("#"):
                continue
            if riga.startswith("\t"):
                if pattern is not None:
                    descr.append(riga.strip())
            elif riga.strip() == "":
                if pattern is not None:
                    voci.append((pattern, descr))
                pattern, descr = None, []
            else:
                if pattern is not None:
                    voci.append((pattern, descr))
                pattern, descr = riga.strip(), []
    if pattern is not None:
        voci.append((pattern, descr))
    return voci


def cerca(atr, voci):
    trovate = []
    for pattern, descr in voci:
        try:
            if re.fullmatch(pattern, atr, flags=re.IGNORECASE):
                trovate.append((pattern, descr))
        except re.error:
            continue
    return trovate


def decodifica(atr):
    """Decodifica minima dell'ATR: convenzione, protocolli, byte storici."""
    b = [int(x, 16) for x in atr.split()]
    out = []
    ts = b[0]
    out.append("TS = %02X : %s" % (ts, {0x3B: "convenzione diretta", 0x3F: "convenzione inversa"}.get(ts, "sconosciuta")))
    t0 = b[1]
    n_storici = t0 & 0x0F
    y = t0 >> 4
    i = 2
    protocolli = set()
    while y:
        if y & 1:
            i += 1  # TA
        if y & 2:
            i += 1  # TB
        if y & 4:
            i += 1  # TC
        if y & 8:  # TD
            if i < len(b):
                td = b[i]
                protocolli.add(td & 0x0F)
                y = td >> 4
                i += 1
            else:
                break
        else:
            y = 0
    if not protocolli:
        protocolli = {0}
    out.append("protocolli: " + ", ".join("T=%d" % p for p in sorted(protocolli)))
    storici = b[i:i + n_storici]
    ascii_ = "".join(chr(x) if 32 <= x < 127 else "." for x in storici)
    out.append("byte storici (%d): %s   ascii: \"%s\"" % (n_storici, " ".join("%02X" % x for x in storici), ascii_))
    firme = []
    testo_ascii = "".join(chr(x) if 32 <= x < 127 else " " for x in b)
    for chiave, significato in FIRME_ASCII:
        if chiave.lower() in testo_ascii.lower():
            firme.append("%s -> %s" % (chiave, significato))
            if chiave in ("MIFARE", "JCOP", "IRDETO", "DNASP"):
                break
    if firme:
        out.append("firme ASCII riconosciute: " + "; ".join(firme))
    return out


def leggi_da_lettore(nome_lettore=None):
    try:
        from smartcard.System import readers
        from smartcard.util import toHexString
    except ImportError:
        raise SystemExit(
            "Modulo pyscard non installato. Installa con:  pip install pyscard\n"
            "Su Linux serve anche pcscd in esecuzione (sudo apt install pcscd pcsc-tools).\n"
            "In alternativa passa l'ATR a mano con --atr \"3B ...\"."
        )
    lista = readers()
    if not lista:
        raise SystemExit(
            "Nessun lettore PC/SC trovato.\n"
            "- Smartreader V2 Argolis: su Windows installa il driver PC/SC Argolis; su Linux\n"
            "  il lettore non e' PC/SC, usa OSCam (protocol = smartreader) e poi --oscam-log.\n"
            "- Qualsiasi lettore CCID: verifica che pcscd sia avviato (Linux)."
        )
    print("Lettori trovati:")
    for k, r in enumerate(lista):
        print("  [%d] %s" % (k, r))
    scelto = None
    if nome_lettore:
        for r in lista:
            if nome_lettore.lower() in str(r).lower():
                scelto = r
                break
        if scelto is None:
            raise SystemExit("Nessun lettore contiene '%s' nel nome" % nome_lettore)
    else:
        scelto = lista[0]
    print("Uso: %s" % scelto)
    conn = scelto.createConnection()
    try:
        conn.connect()
    except Exception as e:  # noqa: BLE001
        raise SystemExit("Impossibile connettersi alla scheda (inserita? contatti puliti? adattatore SIM?): %s" % e)
    return toHexString(conn.getATR())


def atr_da_log_oscam(percorso):
    ultimo = None
    with open(percorso, encoding="utf-8", errors="replace") as f:
        for riga in f:
            m = re.search(r"ATR:\s*((?:[0-9A-Fa-f]{2}\s*)+)", riga)
            if m:
                ultimo = m.group(1)
    if not ultimo:
        raise SystemExit("Nessuna riga 'ATR: ...' trovata in %s" % percorso)
    return ultimo


def main():
    ap = argparse.ArgumentParser(description="Identifica una scheda a contatti dal suo ATR")
    ap.add_argument("--atr", help="ATR in esadecimale, es. \"3B 9F 95 80 1F ...\"")
    ap.add_argument("--oscam-log", help="file di log di OSCam da cui estrarre l'ATR")
    ap.add_argument("--lettore", help="parte del nome del lettore PC/SC da usare")
    ap.add_argument("--aggiorna", action="store_true", help="riscarica il database ATR")
    args = ap.parse_args()

    if args.atr:
        atr = normalizza_atr(args.atr)
    elif args.oscam_log:
        atr = normalizza_atr(atr_da_log_oscam(args.oscam_log))
    else:
        atr = normalizza_atr(leggi_da_lettore(args.lettore))

    print("\nATR: %s\n" % atr)
    for riga in decodifica(atr):
        print("  " + riga)

    voci = carica_db(args.aggiorna)
    trovate = cerca(atr, voci)
    print("\nCorrispondenze nel database (%d voci caricate):" % len(voci))
    if not trovate:
        print("  nessuna. Puoi contribuire l'ATR su https://smartcard-atr.apdu.fr/")
        print("  Prova comunque la decodifica sopra: le firme ASCII spesso bastano.")
    for pattern, descr in trovate:
        print("  pattern: %s" % pattern)
        for d in descr:
            print("      - %s" % d)
    return 0


if __name__ == "__main__":
    sys.exit(main())
