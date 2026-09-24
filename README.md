# Nuovo_progetto

## 📡 Lettore NFC (pagina web)

`index.html` è una pagina web che usa l'API **Web NFC** per leggere e scrivere
tag NFC con il lettore del cellulare.

### Requisiti

- **Chrome su Android** (versione 89 o successiva) — Web NFC non funziona su
  iPhone né su browser desktop
- Telefono con **NFC attivo** (Impostazioni → Dispositivi connessi → NFC)
- La pagina deve essere aperta tramite **HTTPS** (requisito di sicurezza del
  browser)

### Come provarla senza pubblicarla online

Web NFC funziona solo in un contesto sicuro (HTTPS oppure `localhost`), quindi
non basta aprire il file direttamente. Il modo più semplice è servire la
pagina da `localhost` sul telefono stesso con **Termux**:

1. Installa **Termux** dal Play Store (o da F-Droid)
2. Scarica `index.html` da GitHub sul telefono (finisce nella cartella
   Download)
3. In Termux esegui:

   ```sh
   pkg install python
   termux-setup-storage   # consenti l'accesso ai file
   cd storage/downloads
   python -m http.server 8080
   ```

4. Apri **Chrome** sul telefono e vai su `http://localhost:8080/index.html`

### In alternativa: GitHub Pages

Se un giorno il repository diventa **pubblico** (Pages sui repo privati
richiede un piano a pagamento), c'è già il workflow
`.github/workflows/pages.yml`: lancialo dalla scheda **Actions** ("Deploy su
GitHub Pages" → "Run workflow") e la pagina sarà pubblicata su
`https://rudycen67.github.io/Nuovo_progetto/`.

### Funzioni

- **Lettura**: tocca "Avvia scansione" e avvicina un tag NFC al retro del
  telefono; la pagina mostra numero seriale e contenuto (testo, URL, dati)
- **Scrittura**: inserisci un testo, tocca "Scrivi sul tag" e avvicina il tag
- **Storico**: l'elenco dei tag letti nella sessione, con orario

## 💳 Identificare una scheda a contatti (SIM, SAM, pay-TV) con `identifica_scheda.py`

Lo script `identifica_scheda.py` legge l'**ATR** (Answer To Reset) di una
scheda a contatti e lo confronta con il database pubblico
[smartcard_list.txt](https://pcsc-tools.apdu.fr/smartcard_list.txt): dice
la famiglia della scheda (SIM/USIM, SAM MIFARE, Java Card, Irdeto, Nagra,
Conax, Viaccess...) e decodifica protocollo e byte storici. Il database viene
scaricato al primo avvio e salvato accanto allo script.

Serve Python 3. Per la lettura automatica dal lettore serve anche pyscard:

```sh
pip install pyscard
```

### Con lo Smartreader V2 Argolis

Il lettore non è un lettore CCID standard (usa un chip seriale FTDI,
`lsusb` lo mostra come `0403:6001`), quindi:

- **Windows**: installa il driver PC/SC di Argolis, inserisci la scheda ed
  esegui `python identifica_scheda.py`. Lo script elenca i lettori PC/SC,
  legge l'ATR e stampa il risultato.
- **Linux**: il lettore funziona solo con OSCam (`protocol = smartreader`).
  Avvia OSCam con la scheda inserita, poi estrai l'ATR dal log:

  ```sh
  python3 identifica_scheda.py --oscam-log /var/log/oscam.log
  ```

### Con qualsiasi altro lettore CCID (Linux/Windows/macOS)

```sh
sudo apt install pcscd          # solo Linux
python3 identifica_scheda.py
```

### Se hai già l'ATR

```sh
python3 identifica_scheda.py --atr "3B 9F 95 80 1F C7 80 31 E0 73 FE 21 1B 64 ..."
```

Nota: una SIM o un SAM in formato plug-in (ID-000) va inserita in un
adattatore formato carta di credito, altrimenti i contatti non toccano. L'ATR
identifica il sistema operativo/famiglia della scheda, non il produttore del
silicio (Infineon, NXP, ST...), salvo casi noti come JCOP.
