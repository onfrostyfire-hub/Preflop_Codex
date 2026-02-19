import json
import os
import random
from pathlib import Path
import streamlit as st
from spot_config import SPOT_CONFIGS, get_spot_config

RANGES_DIR = "ranges_spots"
RANKS = "AKQJT98765432"

# 169 рук
ALL_HANDS = []
for i, r1 in enumerate(RANKS):
    for j, r2 in enumerate(RANKS):
        if i < j:
            ALL_HANDS.append(r1 + r2 + "s")
            ALL_HANDS.append(r1 + r2 + "o")
        elif i == j:
            ALL_HANDS.append(r1 + r2)

GROUPS_DEFINITIONS = {
    "Open Raise": [
        "EP open raise", "MP open raise", "CO open raise", "BTN open raise", "SB open raise"
    ],
    "EP OOP vs 3bet": [
        "EP vs 3bet MP", "EP vs 3bet CO/BU"
    ],
    "EP IP vs 3bet": [
        "EP vs 3bet Blinds"
    ],
}

@st.cache_data(ttl=0)
def load_ranges():
    db = {}
    spot_dir = Path(RANGES_DIR)
    if not spot_dir.exists():
        return {}

    for file_path in sorted(spot_dir.glob("*.json")):
        with file_path.open("r", encoding="utf-8") as f:
            payload = json.load(f)

        src = payload.get("source")
        sc = payload.get("scenario")
        sp = payload.get("spot")
        data = payload.get("data")

        if not src or not sc or not sp or data is None:
            continue

        db.setdefault(src, {}).setdefault(sc, {})[sp] = data

    return db

def get_filter_options():
    return ["All"] + list(GROUPS_DEFINITIONS.keys())

def get_filtered_pool(ranges_db, selected_sources, selected_scenarios, filter_mode):
    pool = []
    for src in selected_sources:
        for sc in selected_scenarios:
            if sc not in ranges_db.get(src, {}):
                continue
            for sp in ranges_db[src][sc]:
                if filter_mode == "All":
                    pool.append((src, sc, sp))
                elif filter_mode in GROUPS_DEFINITIONS and sp in GROUPS_DEFINITIONS[filter_mode]:
                    pool.append((src, sc, sp))
    return pool

def get_weight(hand, range_str):
    if not range_str or not isinstance(range_str, str):
        return 0.0

    items = [x.strip() for x in range_str.replace("\n", " ").split(",") if x.strip()]
    for item in items:
        if ":" in item:
            h_part, w_part = item.split(":")
            weight = float(w_part)
            if weight <= 1:
                weight *= 100
        else:
            h_part = item
            weight = 100.0

        # AK -> AKs + AKo
        if len(h_part) == 2 and h_part[0] != h_part[1]:
            if hand in [h_part + "s", h_part + "o"]:
                return weight
        if hand == h_part:
            return weight

    return 0.0

def parse_range_to_list(range_str):
    if not range_str or not isinstance(range_str, str):
        return ALL_HANDS.copy()

    hands = []
    items = [x.strip() for x in range_str.replace("\n", " ").split(",") if x.strip()]
    for item in items:
        h = item.split(":")[0].strip()

        if h in ALL_HANDS:
            hands.append(h)
        elif len(h) == 2:
            if h[0] == h[1]:
                hands.append(h)
            else:
                hands.extend([h + "s", h + "o"])

    return list(set(hands)) if hands else ALL_HANDS.copy()

def choose_task(ranges_db, view_name="Mobile"):
    st.subheader(f"Trainer • {view_name}")

    if not ranges_db:
        st.error("Нет ренджей в папке ranges_spots")
        return

    sources = list(ranges_db.keys())
    src = st.selectbox("Source", sources, index=0)

    scenarios = list(ranges_db[src].keys())
    selected_scenarios = st.multiselect("Scenario", scenarios, default=scenarios)

    filt = st.selectbox("Фильтр", get_filter_options(), index=0)

    pool = get_filtered_pool(ranges_db, [src], selected_scenarios, filt)
    if not pool:
        st.warning("Под этот фильтр нет спотов")
        return

    if st.button("🎲 Новая раздача"):
        st.session_state["new_hand"] = True

    if "task" not in st.session_state or st.session_state.get("new_hand", False):
        src1, sc1, sp1 = random.choice(pool)
        data = ranges_db[src1][sc1][sp1]

        train_range = data.get("training", data.get("source", data.get("full", "")))
        candidates = parse_range_to_list(train_range)
        hand = random.choice(candidates)
        rng = random.randint(0, 99)

        correct = "FOLD"
        if "call" in data or "4bet" in data:
            w4 = get_weight(hand, data.get("4bet", ""))
            wc = get_weight(hand, data.get("call", ""))
            if rng < w4:
                correct = "4BET"
            elif rng < (w4 + wc):
                correct = "CALL"
        else:
            wf = get_weight(hand, data.get("full", ""))
            if wf > 0:
                correct = "RAISE"

        st.session_state["task"] = {
            "src": src1, "sc": sc1, "sp": sp1, "data": data,
            "hand": hand, "rng": rng, "correct": correct
        }
        st.session_state["new_hand"] = False
        st.session_state["answer"] = None

    t = st.session_state["task"]
    cfg = get_spot_config(t["sp"])

    st.markdown("---")
    st.write(f"**Spot:** {t['sp']}")
    st.write(f"**Scenario:** {t['sc']}")
    st.write(f"**Hero:** {cfg.hero} | **Villain:** {cfg.villain or '-'} | **Dealer:** {cfg.dealer}")
    st.write(f"**Hand:** `{t['hand']}` | **RNG:** `{t['rng']}`")

    col1, col2, col3 = st.columns(3)
    if col1.button("FOLD"):
        st.session_state["answer"] = "FOLD"
    if col2.button("CALL"):
        st.session_state["answer"] = "CALL"
    if col3.button("4BET / RAISE"):
        st.session_state["answer"] = "4BET"

    ans = st.session_state.get("answer")
    if ans:
        correct = t["correct"]
        if correct == "RAISE":
            # для open raise приравниваем 4BET/RAISE как правильное "RAISE"
            ok = (ans == "4BET")
        else:
            ok = (ans == correct)

        if ok:
            st.success(f"✅ Верно: {correct}")
        else:
            st.error(f"❌ Неверно. Правильно: {correct}")

        with st.expander("Показать ренджи"):
            st.write("source:", t["data"].get("source", "-"))
            st.write("full:", t["data"].get("full", "-"))
            st.write("training:", t["data"].get("training", "-"))
            st.write("call:", t["data"].get("call", "-"))
            st.write("4bet:", t["data"].get("4bet", "-"))
            st.write("3bet:", t["data"].get("3bet", "-"))
