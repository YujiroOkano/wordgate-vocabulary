#!/usr/bin/env python3
import csv
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
LEVELS_DIR = ROOT / "levels"


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def examples(axis, spelling, translation, part):
    if axis == "toeic":
        patterns = {
            "n": (
                f"The manager reviewed the {spelling} before the meeting.",
                f"マネージャーは会議の前に{translation}を確認しました。"
            ),
            "v": (
                f"The team will {spelling} the details this week.",
                f"チームは今週、詳細を{translation}予定です。"
            ),
            "vi": (
                f"Employees need to {spelling} when the situation changes.",
                f"状況が変わったとき、従業員は{translation}必要があります。"
            ),
            "adj": (
                f"The new process is {spelling} for daily work.",
                f"新しい手順は日々の業務に{translation}です。"
            ),
            "adv": (
                f"The staff responded {spelling} to the request.",
                f"スタッフはその依頼に{translation}対応しました。"
            ),
        }
    else:
        patterns = {
            "n": (
                f"Students discussed the {spelling} in class.",
                f"生徒たちは授業で{translation}について話し合いました。"
            ),
            "v": (
                f"People can {spelling} the problem through careful action.",
                f"人々は慎重な行動でその問題を{translation}ことができます。"
            ),
            "vi": (
                f"The situation may {spelling} over time.",
                f"状況は時間とともに{translation}かもしれません。"
            ),
            "adj": (
                f"The topic was {spelling} for many students.",
                f"その話題は多くの生徒にとって{translation}でした。"
            ),
            "adv": (
                f"She answered {spelling} during the interview.",
                f"彼女は面接で{translation}答えました。"
            ),
        }
    return patterns[part]


LEVELS = {
    "toeic-500": {
        "axis": "toeic",
        "entries": [
            ("attend", "出席する", "v"), ("confirm", "確認する", "v"), ("depart", "出発する", "vi"), ("invoice", "請求書", "n"),
            ("receipt", "領収書", "n"), ("deadline", "締め切り", "n"), ("survey", "調査", "n"), ("deliver", "配達する", "v"),
            ("repair", "修理する", "v"), ("expense", "費用", "n"), ("available", "利用できる", "adj"), ("request", "依頼する", "v"),
            ("appointment", "予約", "n"), ("schedule", "予定", "n"), ("customer", "顧客", "n"), ("client", "取引先", "n"),
            ("order", "注文", "n"), ("purchase", "購入する", "v"), ("refund", "返金", "n"), ("exchange", "交換", "n"),
            ("payment", "支払い", "n"), ("budget", "予算", "n"), ("report", "報告書", "n"), ("file", "ファイル", "n"),
            ("document", "書類", "n"), ("copy", "写し", "n"), ("print", "印刷する", "v"), ("submit", "提出する", "v"),
            ("update", "更新する", "v"), ("arrange", "手配する", "v"), ("reserve", "予約する", "v"), ("cancel", "取り消す", "v"),
            ("delay", "遅延", "n"), ("arrive", "到着する", "vi"), ("leave", "出発する", "vi"), ("rent", "借りる", "v"),
            ("hire", "雇う", "v"), ("train", "研修する", "v"), ("staff", "職員", "n"), ("branch", "支店", "n"),
            ("manager", "管理者", "n"), ("employee", "従業員", "n"), ("office", "事務所", "n"), ("factory", "工場", "n"),
            ("product", "製品", "n"), ("service", "サービス", "n"), ("price", "価格", "n"), ("discount", "割引", "n"),
            ("advertisement", "広告", "n"), ("notice", "通知", "n"), ("sign", "掲示", "n"), ("entrance", "入口", "n"),
            ("floor", "階", "n"), ("aisle", "通路", "n"), ("cafeteria", "食堂", "n"), ("luggage", "荷物", "n"),
            ("form", "用紙", "n"), ("address", "住所", "n"), ("contact", "連絡先", "n"), ("warranty", "保証", "n"),
            ("package", "小包", "n"), ("machine", "機械", "n"), ("equipment", "設備", "n"), ("supply", "供給品", "n"),
            ("material", "資材", "n"), ("instruction", "指示", "n"), ("safety", "安全", "n"), ("total", "合計", "n"),
            ("weekly", "週ごとの", "adj"), ("monthly", "月ごとの", "adj"), ("local", "地元の", "adj"), ("foreign", "外国の", "adj"),
            ("convenient", "便利な", "adj"), ("busy", "忙しい", "adj"), ("empty", "空の", "adj"), ("full", "満員の", "adj"),
            ("ready", "準備できた", "adj"), ("closed", "閉まっている", "adj"), ("open", "開いている", "adj"), ("nearby", "近くの", "adj"),
        ],
    },
    "toeic-700": {
        "axis": "toeic",
        "entries": [
            ("allocate", "割り当てる", "v"), ("negotiate", "交渉する", "v"), ("inventory", "在庫", "n"), ("comply", "従う", "vi"),
            ("postpone", "延期する", "v"), ("venue", "会場", "n"), ("evaluate", "評価する", "v"), ("defect", "欠陥", "n"),
            ("shipment", "出荷", "n"), ("revenue", "収益", "n"), ("briefing", "説明会", "n"), ("extend", "延長する", "v"),
            ("agenda", "議題", "n"), ("proposal", "提案", "n"), ("contract", "契約", "n"), ("estimate", "見積もり", "n"),
            ("approval", "承認", "n"), ("applicant", "応募者", "n"), ("benefit", "福利厚生", "n"), ("commute", "通勤", "n"),
            ("complaint", "苦情", "n"), ("competitor", "競合相手", "n"), ("consultant", "コンサルタント", "n"), ("department", "部署", "n"),
            ("distribution", "流通", "n"), ("efficiency", "効率", "n"), ("facility", "施設", "n"), ("feedback", "意見", "n"),
            ("headquarters", "本社", "n"), ("inspection", "検査", "n"), ("maintenance", "保守", "n"), ("manufacturer", "製造業者", "n"),
            ("marketing", "販売促進", "n"), ("performance", "業績", "n"), ("personnel", "人事", "n"), ("policy", "方針", "n"),
            ("procedure", "手順", "n"), ("promotion", "昇進", "n"), ("questionnaire", "アンケート", "n"), ("recommendation", "推薦", "n"),
            ("registration", "登録", "n"), ("reservation", "予約", "n"), ("representative", "担当者", "n"), ("requirement", "要件", "n"),
            ("supervisor", "上司", "n"), ("transaction", "取引", "n"), ("workshop", "研修会", "n"), ("advertise", "宣伝する", "v"),
            ("assign", "割り当てる", "v"), ("attach", "添付する", "v"), ("collaborate", "協力する", "vi"), ("complete", "完了する", "v"),
            ("conduct", "実施する", "v"), ("demonstrate", "実演する", "v"), ("distribute", "配布する", "v"), ("expand", "拡大する", "vi"),
            ("improve", "改善する", "v"), ("install", "設置する", "v"), ("launch", "開始する", "v"), ("notify", "通知する", "v"),
            ("participate", "参加する", "vi"), ("process", "処理する", "v"), ("recruit", "採用する", "v"), ("reduce", "削減する", "v"),
            ("relocate", "移転する", "vi"), ("replace", "交換する", "v"), ("resolve", "解決する", "v"), ("ship", "発送する", "v"),
            ("supervise", "監督する", "v"), ("transfer", "転送する", "v"), ("accurate", "正確な", "adj"), ("annual", "年1回の", "adj"),
            ("competitive", "競争力のある", "adj"), ("domestic", "国内の", "adj"), ("electronic", "電子の", "adj"), ("flexible", "柔軟な", "adj"),
            ("immediate", "即時の", "adj"), ("limited", "限定された", "adj"), ("qualified", "資格のある", "adj"), ("reliable", "信頼できる", "adj"),
        ],
    },
    "toeic-850": {
        "axis": "toeic",
        "entries": [
            ("accommodate", "対応する", "v"), ("consecutive", "連続した", "adj"), ("substantial", "かなりの", "adj"), ("constraint", "制約", "n"),
            ("eligible", "資格がある", "adj"), ("procurement", "調達", "n"), ("reimburse", "払い戻す", "v"), ("turnover", "離職率", "n"),
            ("feasible", "実行可能な", "adj"), ("authorize", "承認する", "v"), ("premises", "敷地", "n"), ("discrepancy", "不一致", "n"),
            ("acquisition", "買収", "n"), ("affiliate", "関連会社", "n"), ("asset", "資産", "n"), ("liability", "負債", "n"),
            ("logistics", "物流", "n"), ("memorandum", "覚書", "n"), ("objective", "目的", "n"), ("obligation", "義務", "n"),
            ("outcome", "結果", "n"), ("productivity", "生産性", "n"), ("quota", "割り当て", "n"), ("retailer", "小売業者", "n"),
            ("vendor", "販売業者", "n"), ("wholesale", "卸売", "n"), ("depreciation", "減価償却", "n"), ("deduction", "控除", "n"),
            ("merger", "合併", "n"), ("patent", "特許", "n"), ("projection", "予測", "n"), ("relocation", "移転", "n"),
            ("subsidiary", "子会社", "n"), ("surplus", "余剰", "n"), ("profitability", "収益性", "n"), ("compliance", "法令遵守", "n"),
            ("certification", "認証", "n"), ("database", "データベース", "n"), ("evaluation", "評価", "n"), ("delegation", "委任", "n"),
            ("implementation", "実施", "n"), ("facilitate", "促進する", "v"), ("delegate", "委任する", "v"), ("implement", "実施する", "v"),
            ("forecast", "予測する", "v"), ("outsource", "外部委託する", "v"), ("diversify", "多角化する", "v"), ("expedite", "迅速化する", "v"),
            ("audit", "監査する", "v"), ("approve", "承認する", "v"), ("restructure", "再編する", "v"), ("coordinate", "調整する", "v"),
            ("verify", "検証する", "v"), ("revise", "改訂する", "v"), ("specialize", "専門化する", "vi"), ("confidential", "機密の", "adj"),
            ("considerable", "かなりの", "adj"), ("mandatory", "必須の", "adj"), ("preliminary", "予備的な", "adj"), ("strategic", "戦略的な", "adj"),
            ("sustainable", "持続可能な", "adj"), ("technical", "技術的な", "adj"), ("valid", "有効な", "adj"), ("versatile", "多用途の", "adj"),
            ("comprehensive", "包括的な", "adj"), ("compatible", "互換性のある", "adj"), ("insufficient", "不十分な", "adj"), ("outstanding", "未払いの", "adj"),
            ("prospective", "見込みのある", "adj"), ("recurrent", "再発する", "adj"), ("stable", "安定した", "adj"), ("tentative", "仮の", "adj"),
            ("thorough", "徹底的な", "adj"), ("annually", "毎年", "adv"), ("approximately", "およそ", "adv"), ("accordingly", "それに応じて", "adv"),
            ("mutually", "相互に", "adv"), ("promptly", "迅速に", "adv"), ("efficiently", "効率的に", "adv"), ("substantially", "大幅に", "adv"),
        ],
    },
    "toeic-990": {
        "axis": "toeic",
        "entries": [
            ("streamline", "効率化する", "v"), ("contingency", "不測の事態", "n"), ("consolidate", "統合する", "v"), ("provisional", "暫定的な", "adj"),
            ("scrutinize", "詳細に調べる", "v"), ("mitigate", "軽減する", "v"), ("lucrative", "利益の大きい", "adj"), ("convene", "招集する", "vi"),
            ("inadvertently", "うっかり", "adv"), ("revamp", "刷新する", "v"), ("stringent", "厳格な", "adj"), ("ratify", "正式承認する", "v"),
            ("abide", "従う", "vi"), ("accolade", "称賛", "n"), ("aggregate", "総計", "n"), ("anomaly", "異常", "n"),
            ("appraisal", "評価", "n"), ("benchmark", "基準", "n"), ("bottleneck", "障害", "n"), ("catalyst", "きっかけ", "n"),
            ("concession", "譲歩", "n"), ("consensus", "合意", "n"), ("deterioration", "悪化", "n"), ("divest", "売却する", "v"),
            ("embargo", "禁輸", "n"), ("entitlement", "権利", "n"), ("excerpt", "抜粋", "n"), ("forfeiture", "没収", "n"),
            ("incumbent", "現職者", "n"), ("indemnity", "補償", "n"), ("litigation", "訴訟", "n"), ("offset", "相殺する", "v"),
            ("precedent", "前例", "n"), ("redundancy", "余剰人員", "n"), ("requisition", "請求書", "n"), ("stakeholder", "利害関係者", "n"),
            ("statute", "法令", "n"), ("stipulation", "条件", "n"), ("threshold", "基準値", "n"), ("underwriting", "引受業務", "n"),
            ("volatility", "変動性", "n"), ("waiver", "権利放棄", "n"), ("ascertain", "突き止める", "v"), ("curtail", "削減する", "v"),
            ("defer", "延期する", "v"), ("disclose", "開示する", "v"), ("enforce", "施行する", "v"), ("formulate", "策定する", "v"),
            ("nullify", "無効にする", "v"), ("overhaul", "全面的に見直す", "v"), ("preclude", "妨げる", "v"), ("reconcile", "調整する", "v"),
            ("subsidize", "補助金を出す", "v"), ("supersede", "取って代わる", "v"), ("suspend", "一時停止する", "v"), ("undergo", "経験する", "v"),
            ("validate", "検証する", "v"), ("autonomous", "自律的な", "adj"), ("binding", "拘束力のある", "adj"), ("conducive", "役立つ", "adj"),
            ("detrimental", "有害な", "adj"), ("dormant", "休止状態の", "adj"), ("exhaustive", "徹底的な", "adj"), ("imminent", "差し迫った", "adj"),
            ("intrinsic", "本質的な", "adj"), ("meticulous", "細心の", "adj"), ("nominal", "名目上の", "adj"), ("obsolete", "時代遅れの", "adj"),
            ("proprietary", "独自の", "adj"), ("tangible", "有形の", "adj"), ("uniformly", "一律に", "adv"), ("retrospectively", "遡って", "adv"),
            ("unequivocally", "明確に", "adv"), ("fiscally", "財政的に", "adv"), ("marginally", "わずかに", "adv"), ("subsequently", "その後", "adv"),
            ("interim", "暫定の", "adj"), ("fiduciary", "信認上の", "adj"), ("moratorium", "一時停止", "n"), ("remuneration", "報酬", "n"),
        ],
    },
    "eiken-3": {
        "axis": "eiken",
        "entries": [
            ("abroad", "海外へ", "adv"), ("culture", "文化", "n"), ("environment", "環境", "n"), ("habit", "習慣", "n"),
            ("invite", "招待する", "v"), ("neighbor", "隣人", "n"), ("practice", "練習する", "v"), ("promise", "約束する", "v"),
            ("suddenly", "突然", "adv"), ("traffic", "交通", "n"), ("accident", "事故", "n"), ("advice", "助言", "n"),
            ("airport", "空港", "n"), ("answer", "答え", "n"), ("birthday", "誕生日", "n"), ("bridge", "橋", "n"),
            ("camera", "カメラ", "n"), ("chance", "機会", "n"), ("classroom", "教室", "n"), ("club", "部活動", "n"),
            ("college", "大学", "n"), ("country", "国", "n"), ("doctor", "医師", "n"), ("dream", "夢", "n"),
            ("event", "行事", "n"), ("festival", "祭り", "n"), ("future", "将来", "n"), ("garbage", "ごみ", "n"),
            ("garden", "庭", "n"), ("health", "健康", "n"), ("hobby", "趣味", "n"), ("holiday", "休日", "n"),
            ("hospital", "病院", "n"), ("island", "島", "n"), ("kitchen", "台所", "n"), ("library", "図書館", "n"),
            ("message", "伝言", "n"), ("museum", "博物館", "n"), ("nature", "自然", "n"), ("noise", "騒音", "n"),
            ("opinion", "意見", "n"), ("picnic", "ピクニック", "n"), ("plan", "計画", "n"), ("problem", "問題", "n"),
            ("question", "質問", "n"), ("reason", "理由", "n"), ("restaurant", "レストラン", "n"), ("rule", "規則", "n"),
            ("season", "季節", "n"), ("station", "駅", "n"), ("ticket", "切符", "n"), ("trip", "旅行", "n"),
            ("village", "村", "n"), ("volunteer", "ボランティア", "n"), ("weather", "天気", "n"), ("weekend", "週末", "n"),
            ("activity", "活動", "n"), ("beautiful", "美しい", "adj"), ("careful", "注意深い", "adj"), ("clean", "清潔な", "adj"),
            ("famous", "有名な", "adj"), ("favorite", "お気に入りの", "adj"), ("friendly", "親しみやすい", "adj"), ("important", "重要な", "adj"),
            ("interested", "興味がある", "adj"), ("kind", "親切な", "adj"), ("popular", "人気のある", "adj"), ("quiet", "静かな", "adj"),
            ("simple", "簡単な", "adj"), ("useful", "役に立つ", "adj"), ("visit", "訪れる", "v"), ("borrow", "借りる", "v"),
            ("choose", "選ぶ", "v"), ("collect", "集める", "v"), ("decide", "決める", "v"), ("enjoy", "楽しむ", "v"),
            ("explain", "説明する", "v"), ("join", "参加する", "v"), ("learn", "学ぶ", "v"), ("protect", "守る", "v"),
        ],
    },
    "eiken-pre2": {
        "axis": "eiken",
        "entries": [
            ("affect", "影響を与える", "v"), ("benefit", "利益", "n"), ("community", "地域社会", "n"), ("consider", "よく考える", "v"),
            ("efficient", "効率的な", "adj"), ("factor", "要因", "n"), ("provide", "提供する", "v"), ("reduce", "減らす", "v"),
            ("solution", "解決策", "n"), ("actually", "実際に", "adv"), ("advantage", "利点", "n"), ("article", "記事", "n"),
            ("behavior", "行動", "n"), ("communication", "意思疎通", "n"), ("comparison", "比較", "n"), ("condition", "状態", "n"),
            ("confidence", "自信", "n"), ("custom", "習慣", "n"), ("development", "発展", "n"), ("education", "教育", "n"),
            ("experience", "経験", "n"), ("generation", "世代", "n"), ("government", "政府", "n"), ("information", "情報", "n"),
            ("knowledge", "知識", "n"), ("population", "人口", "n"), ("purpose", "目的", "n"), ("research", "研究", "n"),
            ("responsibility", "責任", "n"), ("society", "社会", "n"), ("technology", "技術", "n"), ("tradition", "伝統", "n"),
            ("waste", "廃棄物", "n"), ("ability", "能力", "n"), ("challenge", "課題", "n"), ("opportunity", "機会", "n"),
            ("relationship", "関係", "n"), ("skill", "技能", "n"), ("support", "支援", "n"), ("allow", "許す", "v"),
            ("avoid", "避ける", "v"), ("continue", "続く", "vi"), ("create", "作り出す", "v"), ("depend", "依存する", "vi"),
            ("describe", "説明する", "v"), ("discover", "発見する", "v"), ("discuss", "話し合う", "v"), ("encourage", "励ます", "v"),
            ("increase", "増える", "vi"), ("introduce", "紹介する", "v"), ("offer", "提供する", "v"), ("prepare", "準備する", "v"),
            ("receive", "受け取る", "v"), ("recycle", "リサイクルする", "v"), ("share", "共有する", "v"), ("succeed", "成功する", "vi"),
            ("understand", "理解する", "v"), ("improve", "改善する", "v"), ("produce", "生産する", "v"), ("active", "活発な", "adj"),
            ("common", "一般的な", "adj"), ("correct", "正しい", "adj"), ("effective", "効果的な", "adj"), ("necessary", "必要な", "adj"),
            ("natural", "自然な", "adj"), ("possible", "可能な", "adj"), ("public", "公共の", "adj"), ("serious", "深刻な", "adj"),
            ("similar", "似ている", "adj"), ("social", "社会の", "adj"), ("traditional", "伝統的な", "adj"), ("recently", "最近", "adv"),
            ("especially", "特に", "adv"), ("probably", "おそらく", "adv"), ("clearly", "はっきりと", "adv"), ("gradually", "徐々に", "adv"),
            ("global", "世界的な", "adj"), ("available", "利用できる", "adj"), ("independent", "自立した", "adj"), ("regularly", "定期的に", "adv"),
        ],
    },
    "eiken-2": {
        "axis": "eiken",
        "entries": [
            ("acquire", "習得する", "v"), ("alternative", "代替案", "n"), ("analyze", "分析する", "v"), ("contribute", "貢献する", "v"),
            ("estimate", "見積もる", "v"), ("impact", "影響", "n"), ("maintain", "維持する", "v"), ("perspective", "視点", "n"),
            ("resource", "資源", "n"), ("significant", "重要な", "adj"), ("access", "利用機会", "n"), ("agriculture", "農業", "n"),
            ("aspect", "側面", "n"), ("assumption", "仮定", "n"), ("climate", "気候", "n"), ("consequence", "結果", "n"),
            ("economy", "経済", "n"), ("employment", "雇用", "n"), ("evidence", "証拠", "n"), ("habitat", "生息地", "n"),
            ("income", "収入", "n"), ("industry", "産業", "n"), ("issue", "問題", "n"), ("majority", "大多数", "n"),
            ("method", "方法", "n"), ("minority", "少数派", "n"), ("policy", "政策", "n"), ("pollution", "汚染", "n"),
            ("poverty", "貧困", "n"), ("quality", "質", "n"), ("region", "地域", "n"), ("risk", "危険", "n"),
            ("shortage", "不足", "n"), ("source", "源", "n"), ("trend", "傾向", "n"), ("value", "価値", "n"),
            ("vehicle", "乗り物", "n"), ("welfare", "福祉", "n"), ("adapt", "適応する", "vi"), ("adopt", "採用する", "v"),
            ("compare", "比較する", "v"), ("conduct", "実施する", "v"), ("connect", "つなぐ", "v"), ("consume", "消費する", "v"),
            ("debate", "討論する", "v"), ("define", "定義する", "v"), ("demand", "要求する", "v"), ("develop", "発展させる", "v"),
            ("examine", "調査する", "v"), ("exist", "存在する", "vi"), ("focus", "集中する", "vi"), ("ignore", "無視する", "v"),
            ("manage", "管理する", "v"), ("observe", "観察する", "v"), ("occur", "起こる", "vi"), ("prevent", "防ぐ", "v"),
            ("publish", "出版する", "v"), ("require", "必要とする", "v"), ("respond", "反応する", "vi"), ("seek", "求める", "v"),
            ("support", "支える", "v"), ("achieve", "達成する", "v"), ("complex", "複雑な", "adj"), ("current", "現在の", "adj"),
            ("economic", "経済の", "adj"), ("environmental", "環境の", "adj"), ("essential", "不可欠な", "adj"), ("individual", "個々の", "adj"),
            ("likely", "ありそうな", "adj"), ("major", "主要な", "adj"), ("modern", "現代の", "adj"), ("particular", "特定の", "adj"),
            ("private", "私的な", "adj"), ("rapid", "急速な", "adj"), ("recent", "最近の", "adj"), ("various", "さまざまな", "adj"),
            ("widely", "広く", "adv"), ("directly", "直接に", "adv"), ("generally", "一般に", "adv"), ("eventually", "最終的に", "adv"),
        ],
    },
    "eiken-pre1": {
        "axis": "eiken",
        "entries": [
            ("ambiguous", "曖昧な", "adj"), ("coherent", "一貫した", "adj"), ("deteriorate", "悪化する", "vi"), ("elaborate", "詳しく述べる", "v"),
            ("impose", "課す", "v"), ("inevitable", "避けられない", "adj"), ("notion", "概念", "n"), ("preliminary", "予備的な", "adj"),
            ("undermine", "弱体化させる", "v"), ("viable", "実行可能な", "adj"), ("abstract", "抽象的な", "adj"), ("adversity", "逆境", "n"),
            ("allocation", "配分", "n"), ("bias", "偏見", "n"), ("burden", "負担", "n"), ("consensus", "合意", "n"),
            ("controversy", "論争", "n"), ("deficiency", "不足", "n"), ("disparity", "格差", "n"), ("domain", "領域", "n"),
            ("emission", "排出", "n"), ("incentive", "動機づけ", "n"), ("infrastructure", "インフラ", "n"), ("innovation", "革新", "n"),
            ("integrity", "誠実さ", "n"), ("legislation", "法律制定", "n"), ("phenomenon", "現象", "n"), ("premise", "前提", "n"),
            ("priority", "優先事項", "n"), ("resilience", "回復力", "n"), ("scrutiny", "精査", "n"), ("sovereignty", "主権", "n"),
            ("transition", "移行", "n"), ("transparency", "透明性", "n"), ("advocate", "主張する", "v"), ("clarify", "明確にする", "v"),
            ("compensate", "補償する", "v"), ("comprise", "構成する", "v"), ("contradict", "矛盾する", "v"), ("cultivate", "育む", "v"),
            ("diminish", "減少する", "vi"), ("enforce", "施行する", "v"), ("enhance", "高める", "v"), ("fluctuate", "変動する", "vi"),
            ("justify", "正当化する", "v"), ("manipulate", "操作する", "v"), ("perceive", "認識する", "v"), ("prohibit", "禁止する", "v"),
            ("reinforce", "強化する", "v"), ("restore", "回復する", "v"), ("sustain", "維持する", "v"), ("tolerate", "許容する", "v"),
            ("transform", "変える", "v"), ("yield", "生み出す", "v"), ("arbitrary", "恣意的な", "adj"), ("chronic", "慢性的な", "adj"),
            ("compatible", "相性がよい", "adj"), ("compelling", "説得力のある", "adj"), ("credible", "信頼できる", "adj"), ("crucial", "極めて重要な", "adj"),
            ("deliberate", "意図的な", "adj"), ("diverse", "多様な", "adj"), ("empirical", "経験に基づく", "adj"), ("ethical", "倫理的な", "adj"),
            ("fundamental", "根本的な", "adj"), ("implicit", "暗黙の", "adj"), ("marginal", "わずかな", "adj"), ("mutual", "相互の", "adj"),
            ("persistent", "持続的な", "adj"), ("plausible", "もっともらしい", "adj"), ("practical", "実用的な", "adj"), ("prominent", "著名な", "adj"),
            ("rational", "合理的な", "adj"), ("reluctant", "気が進まない", "adj"), ("subtle", "微妙な", "adj"), ("unprecedented", "前例のない", "adj"),
            ("vulnerable", "弱い立場の", "adj"), ("consequently", "その結果", "adv"), ("deliberately", "意図的に", "adv"), ("virtually", "事実上", "adv"),
        ],
    },
    "eiken-1": {
        "axis": "eiken",
        "entries": [
            ("alleviate", "緩和する", "v"), ("contemplate", "熟考する", "v"), ("detrimental", "有害な", "adj"), ("exacerbate", "悪化させる", "v"),
            ("foster", "促進する", "v"), ("imperative", "不可欠な", "adj"), ("meticulous", "細心の", "adj"), ("proliferation", "急増", "n"),
            ("subsidize", "補助金を出す", "v"), ("tenacious", "粘り強い", "adj"), ("aberration", "逸脱", "n"), ("acclaim", "称賛", "n"),
            ("acquiescence", "黙認", "n"), ("austerity", "緊縮", "n"), ("benevolence", "慈悲", "n"), ("catastrophe", "大惨事", "n"),
            ("coercion", "強制", "n"), ("conjecture", "推測", "n"), ("contempt", "軽蔑", "n"), ("convergence", "収束", "n"),
            ("deprivation", "剥奪", "n"), ("dissent", "反対意見", "n"), ("doctrine", "教義", "n"), ("erosion", "侵食", "n"),
            ("fallacy", "誤った考え", "n"), ("fortitude", "不屈の精神", "n"), ("grievance", "不満", "n"), ("hierarchy", "階層", "n"),
            ("hostility", "敵意", "n"), ("implication", "含意", "n"), ("jurisprudence", "法理学", "n"), ("leniency", "寛大さ", "n"),
            ("monopoly", "独占", "n"), ("paradigm", "枠組み", "n"), ("persecution", "迫害", "n"), ("philanthropy", "慈善活動", "n"),
            ("predicament", "苦境", "n"), ("prosperity", "繁栄", "n"), ("reciprocity", "相互関係", "n"), ("rhetoric", "美辞麗句", "n"),
            ("sanction", "制裁", "n"), ("skepticism", "懐疑", "n"), ("solidarity", "連帯", "n"), ("turmoil", "混乱", "n"),
            ("upheaval", "激変", "n"), ("vulnerability", "脆弱性", "n"), ("abdicate", "放棄する", "v"), ("admonish", "戒める", "v"),
            ("aggravate", "悪化させる", "v"), ("corroborate", "裏付ける", "v"), ("curtail", "抑制する", "v"), ("debunk", "誤りを暴く", "v"),
            ("denounce", "非難する", "v"), ("elicit", "引き出す", "v"), ("eradicate", "根絶する", "v"), ("formulate", "練り上げる", "v"),
            ("galvanize", "活気づける", "v"), ("impede", "妨げる", "v"), ("instigate", "扇動する", "v"), ("lament", "嘆く", "v"),
            ("legitimize", "正当化する", "v"), ("ostracize", "排斥する", "v"), ("perpetuate", "永続させる", "v"), ("refute", "論破する", "v"),
            ("relinquish", "手放す", "v"), ("suppress", "抑圧する", "v"), ("transcend", "超越する", "v"), ("affluent", "裕福な", "adj"),
            ("austere", "質素な", "adj"), ("clandestine", "秘密の", "adj"), ("complacent", "自己満足した", "adj"), ("conspicuous", "目立つ", "adj"),
            ("dogmatic", "独断的な", "adj"), ("elusive", "捉えにくい", "adj"), ("formidable", "手ごわい", "adj"), ("impartial", "公平な", "adj"),
            ("indigenous", "先住の", "adj"), ("inherent", "固有の", "adj"), ("insidious", "陰湿な", "adj"), ("precarious", "不安定な", "adj"),
        ],
    },
}


def generate():
    LEVELS_DIR.mkdir(exist_ok=True)
    for level_id, config in LEVELS.items():
        entries = config["entries"]
        if len(entries) != 80:
            raise ValueError(f"{level_id} must contain 80 entries, got {len(entries)}")
        axis = config["axis"]
        seen = set()
        path = LEVELS_DIR / f"{level_id}.csv"
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "axis", "level_id", "spelling", "translation", "example", "example_translation"])
            for spelling, translation, part in entries:
                if spelling in seen:
                    raise ValueError(f"Duplicate word in {level_id}: {spelling}")
                seen.add(spelling)
                example, example_translation = examples(axis, spelling, translation, part)
                writer.writerow([
                    f"{level_id}-{slug(spelling)}",
                    axis,
                    level_id,
                    spelling,
                    translation,
                    example,
                    example_translation,
                ])


if __name__ == "__main__":
    generate()
