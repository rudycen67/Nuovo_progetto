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

### Come provarla

Il modo più semplice è pubblicarla con **GitHub Pages**:

1. Su GitHub vai in **Settings → Pages**
2. In "Source" scegli il branch e la cartella root (`/`)
3. Apri l'indirizzo `https://<utente>.github.io/Nuovo_progetto/` con Chrome
   sul telefono

### Funzioni

- **Lettura**: tocca "Avvia scansione" e avvicina un tag NFC al retro del
  telefono; la pagina mostra numero seriale e contenuto (testo, URL, dati)
- **Scrittura**: inserisci un testo, tocca "Scrivi sul tag" e avvicina il tag
- **Storico**: l'elenco dei tag letti nella sessione, con orario
