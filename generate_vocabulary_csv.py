#!/usr/bin/env python3
import csv
import re
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path

try:
    from wordfreq import top_n_list, zipf_frequency
except ImportError:
    print("wordfreq is required: python3 -m pip install --user wordfreq", file=sys.stderr)
    raise


ROOT = Path(__file__).resolve().parent
LEVELS_DIR = ROOT / "levels"
SEEDS_DIR = ROOT / "seeds"
CACHE_DIR = ROOT / ".cache" / "ejdict"
WORDS_PER_LEVEL = 500
SEED_ROWS_PER_LEVEL = 80
TOP_N = 60000
EJDICT_SRC_URL = "https://raw.githubusercontent.com/kujirahand/EJDict/master/src/{letter}.txt"
CSV_FIELDS = ["id", "axis", "level_id", "spelling", "translation", "example", "example_translation"]
WORD_RE = re.compile(r"^[a-z][a-z]{2,15}$")
JAPANESE_RE = re.compile(r"[ぁ-んァ-ン一-龥]")


LEVELS = [
    {"level_id": "toeic-500", "axis": "toeic", "rank_min": 500, "rank_max": 8000, "center": 2800, "min_len": 3, "max_len": 13, "business_min": 1},
    {"level_id": "toeic-700", "axis": "toeic", "rank_min": 1800, "rank_max": 13000, "center": 5600, "min_len": 4, "max_len": 14, "business_min": 1},
    {"level_id": "toeic-850", "axis": "toeic", "rank_min": 4500, "rank_max": 22000, "center": 9800, "min_len": 5, "max_len": 15, "business_min": 1},
    {"level_id": "toeic-990", "axis": "toeic", "rank_min": 7500, "rank_max": 42000, "center": 16000, "min_len": 5, "max_len": 16, "business_min": 1},
    {"level_id": "eiken-3", "axis": "eiken", "rank_min": 450, "rank_max": 4500, "center": 1900, "min_len": 3, "max_len": 12, "academic_min": 0},
    {"level_id": "eiken-pre2", "axis": "eiken", "rank_min": 1500, "rank_max": 7500, "center": 3600, "min_len": 3, "max_len": 14, "academic_min": 0},
    {"level_id": "eiken-2", "axis": "eiken", "rank_min": 2800, "rank_max": 14000, "center": 6200, "min_len": 4, "max_len": 15, "academic_min": 0},
    {"level_id": "eiken-pre1", "axis": "eiken", "rank_min": 5500, "rank_max": 26000, "center": 11500, "min_len": 5, "max_len": 16, "academic_min": 1},
    {"level_id": "eiken-1", "axis": "eiken", "rank_min": 9000, "rank_max": 52000, "center": 21000, "min_len": 6, "max_len": 16, "academic_min": 1},
]

BUSINESS_JA = [
    "会社", "企業", "商業", "事業", "仕事", "職業", "職場", "従業員", "雇用", "雇う",
    "管理", "経営", "会計", "財務", "銀行", "市場", "契約", "取引", "販売", "顧客",
    "製品", "製造", "工場", "輸送", "出荷", "旅行", "会議", "報告", "書類", "広告",
    "注文", "支払", "価格", "費用", "利益", "損失", "責任", "権利", "義務", "法律",
    "保険", "税", "通信", "電話", "予約", "出席", "予定", "設備", "店舗", "小売",
    "卸売", "産業", "企画", "提案", "申請", "承認", "許可", "検査", "修理", "保守",
    "供給", "在庫", "給与", "部署", "部門", "担当", "配送", "請求", "領収", "料金",
]
BUSINESS_EN = [
    "account", "advert", "appoint", "audit", "bank", "benefit", "branch", "budget", "business",
    "client", "commerce", "company", "contract", "corporate", "customer", "deliver", "department",
    "employee", "expense", "factory", "finance", "hire", "industry", "invoice", "manage", "market",
    "meeting", "office", "order", "payment", "policy", "price", "product", "profit", "project",
    "proposal", "purchase", "receipt", "recruit", "refund", "report", "reserve", "retail", "revenue",
    "sale", "service", "shipment", "staff", "store", "supplier", "transaction", "travel", "vendor",
]
TOEIC_EXCLUDE_JA = [
    "神", "宗教", "礼拝", "崇拝", "王", "女王", "軍", "砲撃", "爆撃", "兵士", "武器",
    "戦争", "詩", "詩人", "植物", "動物", "鳥", "魚", "病気", "国外追放",
]
TOEIC_EXCLUDE_EN = [
    "worship", "prayer", "religion", "bishop", "monk", "poetry", "poet", "weapon", "rifle",
    "soldier", "battle", "warfare", "bomb", "bombard", "deport", "combustion",
    "junta", "opium", "pizzeria", "tithe",
]
ACADEMIC_JA = [
    "社会", "政治", "経済", "環境", "科学", "研究", "教育", "文化", "歴史", "理論",
    "概念", "現象", "影響", "原因", "結果", "証拠", "分析", "主義", "権利", "法律",
    "倫理", "心理", "哲学", "政策", "国際", "人類", "制度", "格差", "技術", "資源",
]
ACADEMIC_EN = [
    "analysis", "concept", "culture", "economic", "education", "environment", "evidence", "global",
    "history", "human", "legal", "policy", "politic", "psycholog", "research", "resource", "science",
    "social", "society", "theory",
]
SKIP_MEANING_MARKERS = [
    "差別的表現", "俗", "卑", "古", "古語", "方言", "まれ", "人名", "男性名", "女性名", "姓",
    "地名", "商標", "記号", "アルファベット", "短縮形", "略", "接尾辞", "接頭辞", "名の一つ",
]
STOP_WORDS = {
    "the", "and", "for", "that", "this", "with", "from", "have", "has", "had", "was", "were", "are",
    "been", "will", "would", "could", "should", "about", "into", "onto", "over", "under", "than",
    "then", "very", "just", "also", "only", "even", "there", "their", "them", "they", "your", "you",
}
GENERAL_EXCLUDE_WORDS = {
    "africa", "america", "asia", "australia", "broadway", "britain", "california", "canada",
    "chandler", "china", "christmas", "england", "europe", "france", "germany", "henry",
    "descartes", "india", "iraq", "ireland", "israel", "italy", "japan", "jay", "jesus",
    "korea", "latvia", "lincolnshire", "liverpool", "london", "mary", "mexico", "nietzsche",
    "paris", "russia", "shire", "socialise", "spain", "stalin", "texas", "tokyo", "traveller",
    "unesco", "unicef", "washington",
}


@dataclass(frozen=True)
class Entry:
    word: str
    meaning: str
    raw_meaning: str
    rank: int
    zipf: float


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def download_ejdict():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    for code in range(ord("a"), ord("z") + 1):
        letter = chr(code)
        target = CACHE_DIR / f"{letter}.txt"
        if target.exists():
            continue
        url = EJDICT_SRC_URL.format(letter=letter)
        with urllib.request.urlopen(url, timeout=30) as response:
            target.write_bytes(response.read())


def clean_meaning(raw):
    if any(marker in raw for marker in SKIP_MEANING_MARKERS):
        return None
    text = re.sub(r"〈[^〉]*〉|《[^》]*》|{[^}]*}|\[[^\]]*\]", "", raw)
    text = re.sub(r"\([^)]*\)", "", text)
    text = text.replace("『", "").replace("』", "").strip()
    for part in re.split(r"\s*/\s*", text):
        part = part.strip(" ,;、。")
        if not part or part.startswith("="):
            continue
        if not JAPANESE_RE.search(part):
            continue
        part = re.split(r"[;/；]", part)[0].strip(" ,、。")
        part = re.sub(r"^…[をにへが]?", "", part)
        if len(part) > 34:
            part = part[:34].rstrip() + "..."
        return part
    return None


def meaning_quality(meaning):
    score = 0
    if "再び" in meaning:
        score -= 4
    if "…" in meaning:
        score -= 2
    if len(meaning) <= 18:
        score += 1
    if "," in meaning or "、" in meaning:
        score += 1
    return score


def load_dictionary():
    download_ejdict()
    entries = {}
    for path in sorted(CACHE_DIR.glob("*.txt")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if "\t" not in line:
                continue
            head, raw_meaning = line.split("\t", 1)
            meaning = clean_meaning(raw_meaning)
            if not meaning:
                continue
            for variant in head.split(","):
                word = variant.strip().lower()
                if not WORD_RE.fullmatch(word) or word in STOP_WORDS:
                    continue
                quality = meaning_quality(meaning)
                if word not in entries or quality > entries[word][2]:
                    entries[word] = (meaning, raw_meaning, quality)
    return entries


def build_ranked_entries(dictionary):
    ranked_words = top_n_list("en", TOP_N)
    entries = []
    for index, word in enumerate(ranked_words, start=1):
        normalized = word.lower()
        if normalized not in dictionary:
            continue
        meaning, raw_meaning, _ = dictionary[normalized]
        entries.append(Entry(normalized, meaning, raw_meaning, index, zipf_frequency(normalized, "en")))
    return entries


def score_keywords(entry, ja_keywords, en_stems, suffix_bonus=False):
    score = 0
    score += sum(2 for keyword in ja_keywords if keyword in entry.meaning or keyword in entry.raw_meaning)
    score += sum(2 for stem in en_stems if stem in entry.word)
    if suffix_bonus and entry.word.endswith(("tion", "ment", "ance", "ence", "ity", "ism")):
        score += 1
    return score


def excluded_from_toeic(entry):
    text = entry.meaning + entry.raw_meaning
    return any(keyword in text for keyword in TOEIC_EXCLUDE_JA) or any(stem in entry.word for stem in TOEIC_EXCLUDE_EN)


def excluded_generally(entry):
    return entry.word in GENERAL_EXCLUDE_WORDS


def row_from_entry(entry, config, ordinal):
    return {
        "id": f"{config['level_id']}-{slug(entry.word)}",
        "axis": config["axis"],
        "level_id": config["level_id"],
        "spelling": entry.word,
        "translation": entry.meaning,
        **example_fields(config["axis"], ordinal, entry.word, entry.meaning),
    }


def example_fields(axis, ordinal, word, translation):
    templates = TOEIC_EXAMPLES if axis == "toeic" else EIKEN_EXAMPLES
    example, example_translation = templates[ordinal % len(templates)]
    return {
        "example": example.format(word=word),
        "example_translation": example_translation.format(translation=translation),
    }


TOEIC_EXAMPLES = [
    ('The team reviewed "{word}" before making a decision.', 'チームは決定前に「{translation}」を確認しました。'),
    ('The manager used "{word}" in the monthly report.', 'マネージャーは月次報告で「{translation}」を使いました。'),
    ('Employees should understand "{word}" in business documents.', '従業員は業務文書で「{translation}」を理解する必要があります。'),
    ('The notice mentioned "{word}" for all staff members.', 'その通知は全スタッフ向けに「{translation}」に触れていました。'),
    ('The client asked about "{word}" after the meeting.', '顧客は会議後に「{translation}」について尋ねました。'),
]
EIKEN_EXAMPLES = [
    ('Students learned "{word}" while reading the article.', '生徒たちは記事を読みながら「{translation}」を学びました。'),
    ('The speaker used "{word}" to explain the idea.', '話し手は考えを説明するために「{translation}」を使いました。'),
    ('This passage includes "{word}" as an important word.', 'この文章には重要語として「{translation}」が含まれています。'),
    ('The class discussed "{word}" during the lesson.', 'その授業では「{translation}」について話し合いました。'),
    ('Learners should understand "{word}" in context.', '学習者は文脈の中で「{translation}」を理解する必要があります。'),
]


def read_seed_rows(config):
    path = SEEDS_DIR / f"{config['level_id']}.csv"
    if not path.exists():
        path = LEVELS_DIR / f"{config['level_id']}.csv"
    if not path.exists():
        return []
    rows = []
    with path.open(newline="", encoding="utf-8") as file:
        for index, row in enumerate(csv.DictReader(file)):
            if index >= SEED_ROWS_PER_LEVEL:
                break
            spelling = row.get("spelling", "").strip().lower()
            translation = row.get("translation", "").strip()
            if not WORD_RE.fullmatch(spelling) or not translation:
                continue
            normalized = {
                "id": row.get("id", "").strip() or f"{config['level_id']}-{slug(spelling)}",
                "axis": config["axis"],
                "level_id": config["level_id"],
                "spelling": spelling,
                "translation": translation,
                **example_fields(config["axis"], index, spelling, translation),
            }
            rows.append(normalized)
    return rows


def candidate_sort_key(entry, config):
    center_distance = abs(entry.rank - config["center"])
    if config["axis"] == "toeic":
        topic_score = score_keywords(entry, BUSINESS_JA, BUSINESS_EN)
    else:
        topic_score = score_keywords(entry, ACADEMIC_JA, ACADEMIC_EN, suffix_bonus=True)
    return (-topic_score, center_distance, entry.rank, entry.word)


def is_candidate(entry, config, strict=True):
    if not (config["min_len"] <= len(entry.word) <= config["max_len"]):
        return False
    if excluded_generally(entry):
        return False
    if config["axis"] == "toeic" and excluded_from_toeic(entry):
        return False
    if strict and not (config["rank_min"] <= entry.rank <= config["rank_max"]):
        return False
    if config["axis"] == "toeic" and strict:
        return score_keywords(entry, BUSINESS_JA, BUSINESS_EN) >= config["business_min"]
    if config["axis"] == "eiken" and strict:
        return score_keywords(entry, ACADEMIC_JA, ACADEMIC_EN, suffix_bonus=True) >= config["academic_min"]
    return True


def choose_rows(config, ranked_entries):
    selected = []
    seen_words = set()

    for row in read_seed_rows(config):
        word = row["spelling"]
        if word in seen_words:
            continue
        selected.append(row)
        seen_words.add(word)
        if len(selected) == WORDS_PER_LEVEL:
            return selected

    if config["axis"] == "toeic":
        passes = [
            [entry for entry in ranked_entries if is_candidate(entry, config, strict=True)],
            [
                entry
                for entry in ranked_entries
                if config["rank_min"] * 0.65 <= entry.rank <= config["rank_max"] * 1.35
                and is_candidate(entry, config, strict=False)
                and score_keywords(entry, BUSINESS_JA, BUSINESS_EN) >= config["business_min"]
            ],
            [
                entry
                for entry in ranked_entries
                if is_candidate(entry, config, strict=False)
                and score_keywords(entry, BUSINESS_JA, BUSINESS_EN) >= config["business_min"]
            ],
        ]
    else:
        passes = [
            [entry for entry in ranked_entries if is_candidate(entry, config, strict=True)],
            [entry for entry in ranked_entries if config["rank_min"] * 0.65 <= entry.rank <= config["rank_max"] * 1.35 and is_candidate(entry, config, strict=False)],
            [entry for entry in ranked_entries if is_candidate(entry, config, strict=False)],
        ]

    ordinal = len(selected)
    for pool in passes:
        for entry in sorted(pool, key=lambda item: candidate_sort_key(item, config)):
            if entry.word in seen_words:
                continue
            selected.append(row_from_entry(entry, config, ordinal))
            seen_words.add(entry.word)
            ordinal += 1
            if len(selected) == WORDS_PER_LEVEL:
                return selected

    raise ValueError(f"{config['level_id']} only reached {len(selected)} words")


def validate_rows(level_id, rows):
    if len(rows) != WORDS_PER_LEVEL:
        raise ValueError(f"{level_id} must contain {WORDS_PER_LEVEL} rows, got {len(rows)}")
    ids = set()
    words = set()
    for row in rows:
        missing = [field for field in CSV_FIELDS if not row.get(field)]
        if missing:
            raise ValueError(f"{level_id} has missing fields for {row.get('spelling')}: {missing}")
        if row["id"] in ids:
            raise ValueError(f"{level_id} has duplicate id: {row['id']}")
        if row["spelling"] in words:
            raise ValueError(f"{level_id} has duplicate spelling: {row['spelling']}")
        ids.add(row["id"])
        words.add(row["spelling"])


def generate():
    LEVELS_DIR.mkdir(exist_ok=True)
    dictionary = load_dictionary()
    ranked_entries = build_ranked_entries(dictionary)
    for config in LEVELS:
        rows = choose_rows(config, ranked_entries)
        validate_rows(config["level_id"], rows)
        path = LEVELS_DIR / f"{config['level_id']}.csv"
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        print(f"{config['level_id']}: {len(rows)} words")


if __name__ == "__main__":
    generate()
