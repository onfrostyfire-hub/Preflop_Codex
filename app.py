import importlib

import streamlit as st

st.set_page_config(page_title="Preflop Trainer", layout="wide")


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
        importlib.import_module("views.stats").show()


if __name__ == "__main__":
    main()
