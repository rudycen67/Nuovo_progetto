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

## 🖼️ Upscaler immagini ×4 (Real-ESRGAN)

`upscaler.html` è una pagina web che ingrandisce le immagini di 4 volte usando
il modello **Real-ESRGAN-General-x4v3** (formato ONNX, nella cartella
`upscaler/`). Il modello viene eseguito **interamente nel browser** con
[onnxruntime-web](https://onnxruntime.ai/docs/tutorials/web/): l'immagine non
viene mai caricata su alcun server.

### Come si usa

1. Apri `upscaler.html` (servita via HTTP/HTTPS, vedi sotto)
2. Scegli o trascina un'immagine (PNG, JPG, WebP...)
3. Tocca **"Ingrandisci ×4"** e attendi: l'elaborazione avviene a blocchi di
   128×128 pixel, con una barra di avanzamento
4. Scarica il risultato in PNG con **"Scarica PNG"**

### Note

- La pagina va servita da un server web (non aperta come `file://`), perché
  deve scaricare i file del modello con `fetch`. Vale lo stesso metodo Termux
  descritto sopra (scarica anche la cartella `upscaler/`), oppure GitHub Pages
- Serve una connessione internet al primo avvio per scaricare il runtime
  onnxruntime-web dal CDN; il modello (~5 MB) invece è servito dal sito stesso
- Le immagini più grandi di 1024 px sul lato lungo vengono ridotte prima
  dell'elaborazione per non esaurire la memoria del browser
- Funziona su qualunque browser moderno, anche desktop (a differenza del
  lettore NFC)
