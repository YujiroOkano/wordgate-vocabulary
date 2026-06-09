# Vocabulary Selection Notes

The CSV files are original WordGate study data. They are not copied from any single textbook, publisher list, commercial word book, or past exam.

## Selection Policy

- TOEIC levels focus on workplace, office, travel, customer-service, finance, operations, compliance, and high-score business vocabulary.
- EIKEN levels follow the broad ability bands published by EIKEN and gradually move from daily/school vocabulary to social, academic, and abstract vocabulary.
- Each current level contains 500 words. This supports longer study programs while still allowing the app to load only the level selected by the user.
- Curated rows under `seeds/` are treated as seed data so stable word IDs do not churn when the generator is rerun.
- Additional Japanese meanings are derived from EJDict-hand, a public-domain/CC0 English-Japanese dictionary dataset.
- Frequency ordering is used as a rough difficulty proxy, then adjusted by TOEIC business/workplace keywords or EIKEN academic/social-topic keywords.

## Public References

- IIBC, "About the TOEIC Listening & Reading Test": test format, score scale, and workplace/study use context.
- Eiken Foundation of Japan, "EIKEN Grades": grade and CEFR comparison.
- Kaneko, M. "Vocabulary Size of the Eiken Grade Pre-1 Test": public academic reference for the larger vocabulary-size demand at higher EIKEN levels.
- Kujirahand, "EJDict-hand": English-Japanese dictionary data published as Public Domain / CC0.
