# WordGate Vocabulary CSV

This repository hosts public CSV files consumed by the WordGate iOS app.

## Columns

- `id`: Stable app-level word identifier.
- `axis`: `toeic` or `eiken`.
- `level_id`: Study level identifier used by the app.
- `spelling`: English word.
- `translation`: Japanese meaning.
- `example`: English example sentence.
- `example_translation`: Japanese translation of the example.

## File Layout

Each level is published as a standalone CSV under `levels/`.

Each level currently contains 80 original entries. Run this command after editing the generator:

```bash
python3 VocabularyCSV/generate_vocabulary_csv.py
```

The app downloads:

```text
https://raw.githubusercontent.com/YujiroOkano/wordgate-vocabulary/main/levels/{level_id}.csv
```

If the download fails, the app uses a cached CSV when available. If no cache is available, it falls back to the bundled vocabulary in the app.
