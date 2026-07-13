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

## 🖼️ Convertitore JPG → RAW (pagina web)

`jpg-to-raw.html` converte un'immagine JPG (o PNG/WebP) in un file **.raw**
con i dati pixel grezzi, direttamente nel browser: nessuna immagine viene
caricata su internet. Basta aprire il file in un browser qualsiasi (funziona
anche in locale, senza server).

> **Nota:** un vero file RAW fotografico (.CR2, .NEF, .ARW…) contiene i dati
> del sensore della fotocamera, che il JPG ha già scartato in compressione e
> quindi non si possono ricostruire. La pagina esporta i pixel decompressi in
> formato **Photoshop Raw** (dati grezzi senza intestazione).

### Come si usa

1. Apri `jpg-to-raw.html` nel browser
2. Scegli (o trascina) l'immagine
3. Seleziona canali (RGB, RGBA o scala di grigi) e profondità (8 o 16 bit)
4. Tocca "Converti e scarica .raw"

Dopo la conversione la pagina mostra i parametri (larghezza, altezza, canali,
profondità) da inserire per riaprire il file in **Photoshop** o **GIMP**, e il
comando **ImageMagick** già pronto, ad esempio:

```sh
magick -size 1920x1080 -depth 8 rgb:foto.raw foto.png
```
