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
    st.session_state.page = "qfl"

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
    
    # Use one wide column
    col = st.container()
    
    with col:
        st.markdown("### 📌 QFL Ternary Plot")
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Ternary_plot_QFL_diagram.svg/400px-Ternary_plot_QFL_diagram.svg.png", width=300)
        st.markdown("Analyze sandstone composition using Quartz, Feldspar, and Lithics.")
        st.button("Go to QFL Module", on_click=go_qfl)
    
        st.markdown("---")
    
        st.markdown("### 🧪 CIA (Chemical Index of Alteration)")
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Weathering_CIA_plot.svg/400px-Weathering_CIA_plot.svg.png", width=300)
        st.markdown("Calculate CIA index from oxide data to evaluate chemical weathering.")
        st.button("Go to CIA Module", on_click=go_cia)
    
        st.markdown("---")
    
        st.markdown("### ☔ Rainfall Intensity Plot")
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Rainfall_plot.svg/400px-Rainfall_plot.svg.png", width=300)
        st.markdown("Visualize rainfall trends and intensity over time.")
        st.button("Go to Rainfall Module", on_click=go_rainfall)

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

