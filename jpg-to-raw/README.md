# 🖼️ Convertitore JPG → RAW

Pagina web che converte un'immagine **JPG** (o PNG/WebP) in un file **.raw**
con i dati pixel grezzi. Tutto avviene nel browser: nessuna immagine viene
caricata su internet.

> **Nota:** un vero file RAW fotografico (.CR2, .NEF, .ARW…) contiene i dati
> del sensore della fotocamera, che il JPG ha già scartato in compressione:
> non si possono ricostruire. Questa pagina esporta i **pixel decompressi**
> in formato **Photoshop Raw** (dati grezzi senza intestazione), apribile in
> Photoshop, GIMP e ImageMagick.

## Come si usa

1. Apri `index.html` in un browser qualsiasi (funziona anche in locale,
   senza server: doppio clic sul file)
2. Scegli l'immagine, oppure trascinala nella pagina
3. Seleziona il formato di uscita:
   - **Canali**: RGB (colore), RGBA (con trasparenza) o scala di grigi
   - **Profondità**: 8 o 16 bit per canale
4. Tocca **"Converti e scarica .raw"**

Dopo la conversione la pagina mostra i parametri da usare per riaprire il
file (larghezza, altezza, canali, profondità, nessuna intestazione, byte
little-endian).

## Riaprire il file .raw

- **Photoshop**: File → Apri → seleziona il `.raw` → inserisci larghezza,
  altezza e numero di canali indicati dalla pagina
- **GIMP**: File → Apri → scegli "Dati immagine grezzi" come tipo di file e
  inserisci gli stessi parametri
- **ImageMagick**: la pagina genera il comando già pronto, ad esempio:

  ```sh
  magick -size 1920x1080 -depth 8 rgb:foto.raw foto.png
  ```
