import importlib

import streamlit as st

import utils

st.set_page_config(page_title="Preflop Trainer", layout="wide")


def show_stats_inline() -> None:
    st.subheader("Stats")
    df = utils.load_history()

    if df.empty:
        st.info("История пока пустая")
        return

    total = len(df)
    correct = int(df["Result"].sum())
    acc = int((correct / total) * 100) if total else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Всего рук", total)
    c2.metric("Верных", correct)
    c3.metric("Точность", f"{acc}%")

    st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True, hide_index=True)

    if st.button("Очистить историю"):
        utils.delete_history(days=None)
        st.success("История очищена")


def main() -> None:
    st.sidebar.title("Preflop Trainer")
    mode = st.sidebar.radio("Раздел", ["🎮 Trainer", "🔬 Range Lab", "📊 Stats"])

    if mode == "🎮 Trainer":
        view = st.sidebar.radio("Вид", ["Mobile", "Desktop"], index=0)
        if view == "Mobile":
            importlib.import_module("views.mobile").show()
        else:
            importlib.import_module("views.desktop").show()
    elif mode == "🔬 Range Lab":
        importlib.import_module("views.compare").show()
    else:
        show_stats_inline()


if __name__ == "__main__":
    main()
