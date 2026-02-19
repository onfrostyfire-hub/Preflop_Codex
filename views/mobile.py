import random

import streamlit as st

import utils
from spot_config import POSITIONS, get_spot_config


def _safe_pick_spot(pool):
    if not pool:
        return None
    return random.choice(pool)


def _build_new_hand(ranges_db, spot_key):
    src, sc, sp = spot_key.split('|')
    data = ranges_db[src][sc][sp]

    training_range = data.get('training', data.get('source', data.get('full', '')))
    possible_hands = utils.parse_range_to_list(training_range)

    hand = random.choice(possible_hands)
    rng = random.randint(0, 99)

    suits = ['♠', '♥', '♦', '♣']
    s1 = random.choice(suits)
    if 's' in hand:
        s2 = s1
    else:
        s2 = random.choice([x for x in suits if x != s1])

    return {
        'key': spot_key,
        'hand': hand,
        'rng': rng,
        'suits': [s1, s2],
    }


def _get_correct_action(data, hand, rng):
    if 'call' in data or '4bet' in data:
        w_call = utils.get_weight(hand, data.get('call', ''))
        w_4bet = utils.get_weight(hand, data.get('4bet', ''))
        if rng < w_4bet:
            return '4BET'
        if rng < (w_4bet + w_call):
            return 'CALL'
        return 'FOLD'

    if utils.get_weight(hand, data.get('full', '')) > 0:
        return 'RAISE'
    return 'FOLD'


def show():
    st.markdown('## 🎮 Trainer (Mobile)')

    ranges_db = utils.load_ranges()
    if not ranges_db:
        st.error('Нет ренджей. Проверь папку ranges_spots.')
        return

    saved = utils.load_user_settings()

    selected_sources = st.multiselect(
        'Source',
        list(ranges_db.keys()),
        default=saved.get('sources', [list(ranges_db.keys())[0]]),
    )

    available_scenarios = set()
    for source in selected_sources:
        available_scenarios.update(ranges_db[source].keys())
    available_scenarios = sorted(list(available_scenarios))

    selected_scenarios = st.multiselect(
        'Scenario',
        available_scenarios,
        default=saved.get('scenarios', available_scenarios),
    )

    filter_options = utils.get_filter_options()
    selected_mode = st.selectbox('Positions', filter_options, index=0)

    utils.save_user_settings(
        {
            'sources': selected_sources,
            'scenarios': selected_scenarios,
            'mode': selected_mode,
        }
    )

    pool = utils.get_filtered_pool(ranges_db, selected_sources, selected_scenarios, selected_mode)
    if not pool:
        st.warning('Нет спотов под выбранный фильтр.')
        return

    if st.button('🎲 Новая раздача') or 'task' not in st.session_state:
        spot_key = _safe_pick_spot(pool)
        st.session_state['task'] = _build_new_hand(ranges_db, spot_key)

    task = st.session_state['task']
    src, sc, sp = task['key'].split('|')
    data = ranges_db[src][sc][sp]

    cfg = get_spot_config(sp)
    villain = cfg.villain if cfg.villain else '-'

    st.write(f'**Source:** {src}')
    st.write(f'**Scenario:** {sc}')
    st.write(f'**Spot:** {sp}')
    st.write(f'**Hero/Villain/Dealer:** {cfg.hero} / {villain} / {cfg.dealer}')
    st.write(f'**Hand:** `{task["hand"]}` | **RNG:** `{task["rng"]}`')

    actions = ['FOLD', 'CALL', '4BET / RAISE']
    col1, col2, col3 = st.columns(3)

    answer = None
    if col1.button(actions[0]):
        answer = 'FOLD'
    if col2.button(actions[1]):
        answer = 'CALL'
    if col3.button(actions[2]):
        answer = '4BET'

    if answer:
        correct = _get_correct_action(data, task['hand'], task['rng'])
        if correct == 'RAISE':
            is_ok = answer == '4BET'
        else:
            is_ok = answer == correct

        if is_ok:
            st.success(f'✅ Верно: {correct}')
        else:
            st.error(f'❌ Неверно. Правильно: {correct}')

    st.caption(f'Позиции за столом: {", ".join(POSITIONS)}')
