import streamlit as st

# --- Page config ---
st.set_page_config(page_title="Lithora Geoscience Tools", layout="wide")

# --- Page state manager ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- Navigation functions ---
def go_home():
    st.session_state.page = "home"

def go_qfl():
    st.session_state.page = "qft-ternary-model.py"

def go_cia():
    st.session_state.page = "cia"

def go_rainfall():
    st.session_state.page = "rainfall"

# --- Page: Home Interface ---
if st.session_state.page == "home":
    st.title("🌍 Lithora Geoscience Toolkit")
    st.markdown("Welcome to **Lithora**, an integrated geoscience app for plotting and analyzing geological data.")

    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Ternary_plot_QFL_diagram.svg/1024px-Ternary_plot_QFL_diagram.svg.png", width=600)

    st.subheader("🧭 Choose an analysis module:")
        col1, col2 = st.columns(2)

    with col1:
        st.button("📌 QFL Ternary Plot", on_click=go_qfl)
        st.button("🧪 Chemical Index of Alteration (CIA)", on_click=go_cia)
        st.button("☔ Rainfall Intensity Plot", on_click=go_rainfall)
    with col2:
        
# --- Page: QFL Ternary ---
elif st.session_state.page == "qfl":
    st.title("📌 QFL Ternary Plot")
    st.button("⬅️ Back to Home", on_click=go_home)

    # You can insert your previous QFL plotting code here
    st.markdown("🪨 Upload or input Quartz, Feldspar, Lithics data to generate ternary plots.")

    # Placeholder for your QFL logic
    st.info("🔧 QFL logic goes here.")

# --- Page: CIA Analysis ---
elif st.session_state.page == "cia":
    st.title("🧪 Chemical Index of Alteration (CIA)")
    st.button("⬅️ Back to Home", on_click=go_home)

    st.markdown("Upload oxide data to compute the CIA index and generate alteration plots.")
    st.info("🔧 CIA logic will go here.")

# --- Page: Rainfall Plot ---
elif st.session_state.page == "rainfall":
    st.title("☔ Rainfall Intensity Plot")
    st.button("⬅️ Back to Home", on_click=go_home)

    st.markdown("Upload rainfall data to plot intensity and trend over time.")
    st.info("🔧 Rainfall logic will go here.")

