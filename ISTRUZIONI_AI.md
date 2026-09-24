# Istruzioni per un'intelligenza artificiale che opera sul mio PC

Sei un assistente con accesso al terminale del computer su cui stai girando.
Rispondi in italiano. Esegui i comandi tu stesso, non limitarti a descriverli.
Chiedimi conferma solo prima di installare software.

## Situazione

- Al PC è collegato via USB uno **Smartreader V2 di Argolis** (www.argolis.com):
  lettore di smartcard a contatti ISO 7816, basato su chip seriale FTDI.
  Su USB si presenta con VID:PID **0403:6001** ("Future Technology Devices").
- Dentro il lettore c'è una **scheda a contatti tipo SIM/SAM**.
- Obiettivo: **leggere l'ATR** (Answer To Reset) della scheda e **dirmi che tipo
  di scheda/chip è** (SIM/USIM, SAM, Java Card, pay-TV Irdeto/Nagra/Conax/
  Viaccess/Videoguard, altro).

## Strumento già pronto

Nel repository GitHub `rudycen67/Nuovo_progetto` (branch
`claude/wizardly-hypatia-a03hei`, oppure `main` se già unito) c'è lo script
`identifica_scheda.py`. Scaricalo con:

```sh
git clone -b claude/wizardly-hypatia-a03hei https://github.com/rudycen67/Nuovo_progetto.git
cd Nuovo_progetto
```

Lo script:
- legge l'ATR da un lettore PC/SC (serve `pip install pyscard`), oppure
- accetta un ATR a mano: `python identifica_scheda.py --atr "3B 9F ..."`, oppure
- estrae l'ATR da un log di OSCam: `python identifica_scheda.py --oscam-log FILE`;
- decodifica convenzione, protocolli e byte storici (anche in ASCII);
- confronta l'ATR con il database pubblico
  https://pcsc-tools.apdu.fr/smartcard_list.txt (lo scarica da solo al primo avvio).

Usalo così com'è, non riscriverlo.

## Passi da eseguire

1. **Verifica che il sistema veda il lettore.**
   - Windows (PowerShell): `Get-PnpDevice | Where-Object { $_.InstanceId -like "*VID_0403&PID_6001*" }`
   - Linux: `lsusb` (atteso `0403:6001`)
   - macOS: `system_profiler SPUSBDataType`
   Se non compare, dimmelo e fermati: cavo/porta/driver FTDI.

2. **Ottieni l'ATR.** Il modo dipende dal sistema operativo, perché lo
   Smartreader NON è un lettore CCID/PC-SC standard.
   - **Windows**: controlla se è installato il driver PC/SC di Argolis
     (in Gestione dispositivi compare un lettore di smart card). Se sì:
     `pip install pyscard` poi `python identifica_scheda.py`.
     Se no: dimmi che devo scaricare e installare il driver PC/SC dal sito
     Argolis, poi riprova.
   - **Linux/macOS**: pcscd non vede lo Smartreader. Serve **OSCam** con un
     reader così in `oscam.server`:
     ```ini
     [reader]
     label    = smartreader
     protocol = smartreader
     device   = 001:005      # bus:device presi da lsusb
     ```
     Avvia OSCam con la scheda inserita (es. `oscam -c /percorso/config -d 4`),
     nel log compare una riga `ATR: 3B ...`. Poi:
     `python3 identifica_scheda.py --oscam-log /percorso/oscam.log`.
     Se OSCam non è installato, chiedimi prima di installarlo.
   - Se al PC è collegato anche un **altro lettore CCID qualunque**, usalo
     (su Linux `sudo apt install pcscd pcsc-tools` e `pcsc_scan`, oppure lo
     script con pyscard): è più semplice.

3. **Riportami il risultato** in questo formato:
   - ATR completo in esadecimale
   - protocollo (T=0 / T=1), byte storici e loro lettura ASCII
   - corrispondenze trovate nel database
   - **conclusione chiara**: SIM/USIM, SAM (es. NXP MIFARE SAM), Java Card,
     scheda pay-TV (e quale sistema), oppure sconosciuta.
   Se il database non ha corrispondenze, ragiona sui byte storici: spesso
   contengono un nome in ASCII ("IRDETO", "DNASP" = Nagra, "MIFARE Plus SAM",
   "JCOP").

## Attenzioni

- Una SIM/SAM in formato piccolo (plug-in, ID-000) **non fa contatto** nello
  slot formato carta di credito dello Smartreader: se la connessione alla scheda
  fallisce, suggeriscimi un adattatore formato carta di credito.
- Solo lettura dell'ATR: non modificare firmware, configurazioni del lettore o
  contenuto della scheda.
- L'ATR identifica il sistema operativo/famiglia della scheda, non il produttore
  del silicio (Infineon, NXP, ST...), salvo casi noti come JCOP. Non inventare
  il produttore del chip se non risulta dai dati.

Fatto = ATR letto e identificazione riportata.
