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
    
    st.button("📌 QFL Ternary Plot", on_click=go_qfl)
    st.button("🧪 Chemical Index of Alteration (CIA)", on_click=go_cia)
    st.button("☔ Rainfall Intensity Plot", on_click=go_rainfall)

# --- Page: QFL Ternary ---
elif st.session_state.page == "qfl":
    st.title("📌 QFL Ternary Plot")
    st.button("⬅️ Back to Home", on_click=go_home)

    import pandas as pd
    import matplotlib.pyplot as plt
    import mpltern
    import io
    
    
    # --- UI Header ---
    st.title("🪨 Lithora – QFL Ternary Diagram Tool")
    st.markdown("Upload or enter **Quartz, Feldspar, Lithics** data to generate ternary diagrams and CSVs.")
    
    # --- Sidebar for input mode ---
    mode = st.sidebar.radio("Select Input Mode", ["📝 Manual Entry", "📁 Upload CSV"])
    
    # --- Helper to clean data ---
    def parse_input_list(data_str):
        return [float(i.strip()) for i in data_str.split(",") if i.strip() != ""]
    
    # --- Compute and return QFL DataFrame ---
    def compute_qfl(quartz, feldspar, lithics):
        df = pd.DataFrame({'Quartz': quartz, 'Feldspar': feldspar, 'Lithics': lithics})
        df['Total'] = df['Quartz'] + df['Feldspar'] + df['Lithics']
        df['%Q'] = df['Quartz'] / df['Total'] * 100
        df['%F'] = df['Feldspar'] / df['Total'] * 100
        df['%L'] = df['Lithics'] / df['Total'] * 100
        df = df.round(2)
        return df
    
    # --- Ternary Plot: Basic ---
    def plot_basic_ternary(df):
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
    
        ax.set_tlabel("Quartz")
        ax.set_llabel("Feldspar")
        ax.set_rlabel("Lithics")
    
        tick_vals = [0, 20, 40, 60, 80, 100]
        ax.taxis.set_ticklabels(tick_vals)
        ax.laxis.set_ticklabels(tick_vals)
        ax.raxis.set_ticklabels(tick_vals)
    
        ax.plot(df['%Q'], df['%F'], df['%L'], 'ko', label='Data Points')
        ax.legend(fontsize='small')
        ax.grid(True, linestyle='--', linewidth=0.5)
    
        return fig
    
    # --- Ternary Plot: Provenance Fields ---
    def plot_provenance_ternary(df):
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
    
        ax.set_tlabel("Quartz")
        ax.set_llabel("Feldspar")
        ax.set_rlabel("Lithics")
    
        tick_vals = [0, 20, 40, 60, 80, 100]
        ax.taxis.set_ticklabels(tick_vals)
        ax.laxis.set_ticklabels(tick_vals)
        ax.raxis.set_ticklabels(tick_vals)
    
        fields = {
            'Basement Uplift': [(100,0,0),(0,100,0),(0,85,15),(96,0,4)],
            'Recycled Orogen': [(25,0,75),(51,40,9),(96,0,4)],
            'Undissected Arc': [(0,50,50),(25,0,75),(0,0,100)],
            'Transitional Arc': [(0,50,50),(25,0,75),(33,12,55),(17,70,13),(0,85,15)],
            'Dissected Arc': [(51,40,9),(17,70,13),(33,12,55)]
        }
        colors = {
            'Basement Uplift': 'lightyellow',
            'Recycled Orogen': 'skyblue',
            'Undissected Arc': 'cyan',
            'Transitional Arc': 'lightgreen',
            'Dissected Arc': 'lightblue'
        }
    
        for label, vertices in fields.items():
            scaled = [(q/100, f/100, l/100) for q, f, l in vertices]
            ax.fill(*zip(*scaled), label=label, alpha=0.3, color=colors[label])
    
        ax.plot(df['%Q'], df['%F'], df['%L'], 'ko', label='Data Points')
        ax.legend(fontsize='small', loc='upper left', bbox_to_anchor=(0.8, 1))
        ax.grid(True, linestyle='--', linewidth=0.5)
    
        return fig
    
    # --- CSV Download helper ---
    def to_csv(df):
        return df.to_csv(index=False).encode('utf-8')
    
    # --- Input Handling ---
    df_result = None
    
    if mode == "📝 Manual Entry":
        st.subheader("Manual Input")
        q_input = st.text_area("Quartz Values (comma-separated)", placeholder="e.g., 30, 40, 35")
        f_input = st.text_area("Feldspar Values (comma-separated)", placeholder="e.g., 50, 40, 45")
        l_input = st.text_area("Lithics Values (comma-separated)", placeholder="e.g., 20, 20, 20")
    
        if st.button("Generate Ternary Plot"):
            try:
                d1 = parse_input_list(q_input)
                d2 = parse_input_list(f_input)
                d3 = parse_input_list(l_input)
    
                if len(d1) != len(d2) or len(d1) != len(d3):
                    st.error("Missing Data!! All input lists must be the same length.")
                else:
                    df_result = compute_qfl(d1, d2, d3)
            except Exception as e:
                st.error(f"Error parsing input: {e}")
    
    else:
        st.subheader("Upload CSV")
        uploaded_file = st.file_uploader("Upload CSV with columns: Quartz, Feldspar, Lithics", type="csv")
    
        if uploaded_file:
            try:
                df_uploaded = pd.read_csv(uploaded_file)
                if all(col in df_uploaded.columns for col in ['Quartz', 'Feldspar', 'Lithics']):
                    df_result = compute_qfl(df_uploaded['Quartz'], df_uploaded['Feldspar'], df_uploaded['Lithics'])
                else:
                    st.error("CSV must contain columns: Quartz, Feldspar, Lithics")
            except Exception as e:
                st.error(f"Error reading CSV: {e}")
    
    # --- Output Results ---
    if df_result is not None:
        st.subheader("📊 Computed QFL Table")
        st.dataframe(df_result)
    
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Ternary Diagram")
            fig = plot_basic_ternary(df_result)
            st.pyplot(fig)
    
        with col2:
            st.subheader("With Provenance Fields")
            fig2 = plot_provenance_ternary(df_result)
            st.pyplot(fig2)
    
        st.download_button("📥 Download CSV", to_csv(df_result), "QFL_data.csv", "text/csv")

# --- Page: CIA Analysis ---
elif st.session_state.page == "cia":
    st.title("🧪 Chemical Index of Alteration (CIA)")
    st.button("⬅️ Back to Home", on_click=go_home)

    st.markdown("Upload oxide data to compute the CIA index and generate alteration plots.")

    import pandas as pd
    import math
    import base64
    from io import BytesIO
    import matplotlib.pyplot as plt
    import ternary

    def generate_ternary_plot(data, marker="o", color="black", add_labels=True):
        scale = 100
        fig, tax = ternary.figure(scale=scale)
        fig.set_size_inches(6, 6)

        tax.gridlines(color="gray", linestyle='-', linewidth=1)
        tax.boundary(linewidth=2.0)
        tax.left_axis_label("A (Al₂O₃)", fontsize=12)
        tax.right_axis_label("K (K₂O)", fontsize=12)
        tax.bottom_axis_label("CN (CaO + Na₂O)", fontsize=12)
        tax.ticks(axis='lbr', linewidth=1, multiple=10, fontsize=10)

        # Vertical line from (CN=100, A=0, K=0) to (CN=100, A=100, K=-65)
        tax.line([(100, 0, 0), (100, -65, 100)], linewidth=1.5, color="black", linestyle='--')

        points = [(row[1], row[2], row[3]) for row in data]
        tax.scatter(points, marker=marker, color=color)

        if add_labels:
            for row in data:
                label, cn, k, a = row
                tax.annotate(label, position=(cn, k, a), fontsize=10, offset=0.05)

        tax.clear_matplotlib_ticks()
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=300)
        buf.seek(0)
        return buf

    # --- UI ---
    st.title("🧪 CIA Ternary Plot Tool")
    st.markdown("Generate a CIA ternary plot using oxide values: Al₂O₃ (A), CaO + Na₂O (CN), and K₂O (K).")

    # Sample input section
    with st.form("cia_form"):
        use_sample_labels = st.checkbox("🌤️ Add Sample Labels")
        labels = st.text_area("Sample Labels (comma-separated)", disabled=not use_sample_labels)
        cn_input = st.text_area("CN (CaO + Na₂O)", placeholder="e.g., 30, 20, 10")
        k_input = st.text_area("K (K₂O)", placeholder="e.g., 10, 30, 40")
        a_input = st.text_area("A (Al₂O₃)", placeholder="e.g., 60, 50, 50")

        marker = st.selectbox("Select Marker Type", ["o", "s", "^"], index=0)
        color = st.color_picker("Pick Marker Color", "#000000")

        submit = st.form_submit_button("Generate Plot")

    if submit:
        try:
            cn_vals = [float(i.strip()) for i in cn_input.split(",")]
            k_vals = [float(i.strip()) for i in k_input.split(",")]
            a_vals = [float(i.strip()) for i in a_input.split(",")]

            if not (len(cn_vals) == len(k_vals) == len(a_vals)):
                st.error("All input lists must be the same length.")
            else:
                label_list = [f"S{i+1}" for i in range(len(cn_vals))]
                if use_sample_labels and labels:
                    label_list = [l.strip() for l in labels.split(",")] or label_list

                plot_data = list(zip(label_list, cn_vals, k_vals, a_vals))
                img_buf = generate_ternary_plot(plot_data, marker=marker, color=color, add_labels=use_sample_labels)

                st.markdown("<div style='margin-top:40px;'>", unsafe_allow_html=True)
                st.subheader("📈 CIA Ternary Plot")
                st.image(img_buf, caption="CIA Ternary Diagram")
                st.markdown("</div>", unsafe_allow_html=True)

                # Data Table
                df = pd.DataFrame({
                    "Label": label_list,
                    "CN (CaO+Na2O)": cn_vals,
                    "K (K2O)": k_vals,
                    "A (Al2O3)": a_vals
                })
                st.subheader("📄 Data Table")
                st.dataframe(df)
                csv = df.to_csv(index=False).encode()
                st.download_button("📅 Download Data (CSV)", csv, "cia_data.csv", "text/csv")

                # PNG Download
                st.download_button("📅 Download Plot (PNG)", img_buf, file_name="cia_plot.png", mime="image/png")

        except Exception as e:
            st.error(f"Error: {e}")

    

# --- Page: Rainfall Plot ---
elif st.session_state.page == "rainfall":
    st.title("☔ Rainfall Intensity Plot")
    st.button("⬅️ Back to Home", on_click=go_home)

    st.markdown("Upload rainfall data to plot intensity and trend over time.")
    st.info("🔧Comming Soon..")

