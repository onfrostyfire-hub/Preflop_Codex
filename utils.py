import json
import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st


RANGES_DIR = Path("ranges_spots")
RANGES_FILE = Path("ranges.json")
HISTORY_FILE = Path("history_log.csv")

RANKS = "AKQJT98765432"
ALL_HANDS = []
for i, a in enumerate(RANKS):
    for j, b in enumerate(RANKS):
        if i == j:
            ALL_HANDS.append(a + b)
        elif i < j:
            ALL_HANDS.append(a + b + "s")
            ALL_HANDS.append(a + b + "o")


GROUPS_DEFINITIONS = {
    "Open Raise": ["EP open raise", "MP open raise", "CO open raise", "BTN open raise", "SB open raise"],
    "EP OOP vs 3bet": ["EP vs 3bet MP", "EP vs 3bet CO/BU"],
    "EP IP vs 3bet": ["EP vs 3bet Blinds"],
}


@st.cache_data(ttl=0)
def load_ranges() -> dict:
    db: dict = {}

    if RANGES_DIR.exists():
        for file_path in sorted(RANGES_DIR.glob("*.json")):
            with file_path.open("r", encoding="utf-8") as f:
                payload = json.load(f)
            src = payload.get("source")
            scenario = payload.get("scenario")
            spot = payload.get("spot")
            data = payload.get("data")
            if src and scenario and spot and isinstance(data, dict):
                db.setdefault(src, {}).setdefault(scenario, {})[spot] = data

    if db:
        return db

    if RANGES_FILE.exists():
        with RANGES_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)

    return {}


def get_weight(hand: str, range_str: str) -> float:
    if not range_str:
        return 0.0

    for token in [x.strip() for x in range_str.split(",") if x.strip()]:
        if ":" in token:
            combo, raw_w = token.split(":", 1)
            weight = float(raw_w)
            if weight <= 1:
                weight *= 100
        else:
            combo = token
            weight = 100.0

        if len(combo) == 2 and combo[0] != combo[1]:
            if hand in (combo + "s", combo + "o"):
                return weight
        elif hand == combo:
            return weight

    return 0.0


def parse_range_to_list(range_str: str) -> list[str]:
    if not range_str:
        return ALL_HANDS.copy()

    out: list[str] = []
    for token in [x.strip() for x in range_str.split(",") if x.strip()]:
        combo = token.split(":", 1)[0].strip()
        if combo in ALL_HANDS:
            out.append(combo)
        elif len(combo) == 2 and combo[0] != combo[1]:
            out.extend([combo + "s", combo + "o"])
        elif len(combo) == 2 and combo[0] == combo[1]:
            out.append(combo)

    return list(dict.fromkeys(out)) if out else ALL_HANDS.copy()


def choose_random_task(ranges_db: dict, source: str, scenarios: list[str], filter_mode: str):
    pool = []
    for scenario in scenarios:
        for spot in ranges_db.get(source, {}).get(scenario, {}):
            if filter_mode == "All":
                pool.append((scenario, spot))
            elif filter_mode in GROUPS_DEFINITIONS and spot in GROUPS_DEFINITIONS[filter_mode]:
                pool.append((scenario, spot))
            elif spot == filter_mode:
                pool.append((scenario, spot))

    if not pool:
        return None

    scenario, spot = random.choice(pool)
    data = ranges_db[source][scenario][spot]
    train_range = data.get("training") or data.get("source") or data.get("full") or ""
    hand = random.choice(parse_range_to_list(train_range))
    rng = random.randint(0, 99)

    if "call" in data or "4bet" in data:
        w4 = get_weight(hand, data.get("4bet", ""))
        wc = get_weight(hand, data.get("call", ""))
        if rng < w4:
            correct = "4BET"
        elif rng < w4 + wc:
            correct = "CALL"
        else:
            correct = "FOLD"
    elif "3bet" in data:
        w3 = get_weight(hand, data.get("3bet", ""))
        wc = get_weight(hand, data.get("call", ""))
        if rng < w3:
            correct = "3BET"
        elif rng < w3 + wc:
            correct = "CALL"
        else:
            correct = "FOLD"
    else:
        correct = "RAISE" if get_weight(hand, data.get("full", "")) > 0 else "FOLD"

    return {
        "scenario": scenario,
        "spot": spot,
        "data": data,
        "hand": hand,
        "rng": rng,
        "correct": correct,
    }


def load_history() -> pd.DataFrame:
    if HISTORY_FILE.exists():
        return pd.read_csv(HISTORY_FILE)
    return pd.DataFrame(columns=["Date", "Spot", "Hand", "Result", "CorrectAction"])


def save_to_history(spot: str, hand: str, result: int, correct_action: str) -> None:
    row = pd.DataFrame([
        {
            "Date": datetime.now().isoformat(timespec="seconds"),
            "Spot": spot,
            "Hand": hand,
            "Result": result,
            "CorrectAction": correct_action,
        }
    ])
    if HISTORY_FILE.exists():
        row.to_csv(HISTORY_FILE, mode="a", index=False, header=False)
    else:
        row.to_csv(HISTORY_FILE, index=False)


def delete_history(days: int | None = None) -> None:
    if not HISTORY_FILE.exists():
        return
    df = pd.read_csv(HISTORY_FILE)
    if df.empty:
        return
    if days is None:
        df.iloc[0:0].to_csv(HISTORY_FILE, index=False)
        return
    df["Date"] = pd.to_datetime(df["Date"])
    cutoff = datetime.now() - timedelta(days=days)
    df = df[df["Date"] < cutoff]
    df.to_csv(HISTORY_FILE, index=False)
