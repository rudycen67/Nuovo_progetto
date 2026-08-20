# Nuovo_progetto

## ⚛️ Teorie della meccanica quantistica

In [`docs/teorie-quantistiche.md`](docs/teorie-quantistiche.md) c'è un
quaderno di esplorazione sulle interpretazioni della meccanica
quantistica (Copenaghen, molti mondi, onda pilota, collasso oggettivo,
relazionale, QBism...) e sulle frontiere speculative (gravità
quantistica, principio olografico, ER=EPR), con una tabella comparativa
e letture consigliate.

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
