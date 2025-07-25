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
    
    # ---Pre-prossessing ---
    def parse_input_list(data_str):
        return [float(i.strip()) for i in data_str.split(",") if i.strip() != ""]
    
    # --- Calculate and return QFL DataFrame ---
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
    
    # --- CSV Download ---
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
        st.download_button("📥 Download CSV", to_csv(df_result), "QFL_data.csv", "text/csv")
    
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Ternary Diagram")
            fig = plot_basic_ternary(df_result)
            st.pyplot(fig)

            buf1 = io.BytesIO()
            fig.savefig(buf1, format='png', bbox_inches='tight')
            buf1.seek(0)
            
            st.download_button("📥 Download Plot", buf1, "RAWplot.png", "image/png")
    
        with col2:
            st.subheader("Provenance Fields")
            fig2 = plot_provenance_ternary(df_result)
            st.pyplot(fig2)

            buf2 = io.BytesIO()
            fig.savefig(buf2, format='png', bbox_inches='tight')
            buf2.seek(0)
            st.download_button("📥 Download Plot", buf2, "Prov_plot.png", "image/png")
    
        

# --- Page: CIA Analysis ---
elif st.session_state.page == "cia":
    st.title("🧪 Chemical Index of Alteration (CIA)")
    st.button("⬅️ Back to Home", on_click=go_home)

    st.markdown("Upload oxide data to compute the CIA index and generate alteration plots.")

    import pandas as pd
    import math
    import matplotlib.pyplot as plt
    import io
    
    def ternary_to_xy(a, cn, k):
        total = a + cn + k
        a /= total
        cn /= total
        k /= total
        x = 0.5 * (2 * k + a)
        y = (1) * a
        return x, y

    # --- Plotting function ---
    def plot_ternary(data, marker="o", marker_color="black", show_labels=True):
        fig, ax = plt.subplots(figsize=(8, 7))
        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.1, 1 + 0.1)
        ax.axis('off')

        # Draw triangle
        triangle = [(0, 0), (1, 0), (0.5, 1), (0, 0)]
        x_tri, y_tri = zip(*triangle)
        ax.plot(x_tri, y_tri, 'k-', lw=2)

        # Draw line
        line = [(-0.1, 0), (-0.1, 1), (-0.1, 0)]
        x_li, y_li = zip(*line)
        ax.plot(x_li, y_li, 'k-', lw=2)

        # Mark Lavel and grid
        for i in range(11):
            fcn = i/10
            x_m,y_m = zip((-0.1,1-fcn ), (-0.1, 1))
            ax.plot(x_m, y_m, marker='x', color='black',lw=0)

            for j in range(11):
              ax.text(-0.15,j/10, f"{int(j * 10)}", ha='left', fontsize=8)
            # strong weathering
        lines = [(-0.1, 0.85), (0.57, 0.85)]
        x_li, y_li = zip(*lines)
        ax.plot(x_li, y_li, linestyle='--', color='gray')
        ax.text(-0.001, 0.87, 'Strong\nweathering', ha='center', fontsize=7,color = "gray")
        ax.text(0.6, 1, 'Kaolinite', ha='center', fontsize=7,color = "gray")

             # Intermediate weathering
        lines = [(-0.1, 0.65), (0.68, 0.65)]
        x_li, y_li = zip(*lines)
        ax.plot(x_li, y_li, linestyle='--', color='gray')
        ax.text(-0.001, 0.67, 'Intermediate\nweathering', ha='center', fontsize=7,color = "gray")
        ax.text(0.3, 0.77, 'Smectite', ha='center', fontsize=7,color = "gray")
        ax.text(0.63, 0.77, 'Illite\n \n  Muscovite', ha='left', fontsize=7,color = "gray")

         # Weak weathering
        lines = [(-0.1, 0.5), (0.75, 0.5)]
        x_li, y_li = zip(*lines)
        ax.plot(x_li, y_li, linestyle='--', color='gray')
        ax.text(-0.001, 0.52, 'Weak\nweathering', ha='center', fontsize=7,color = "gray")
        ax.text(0.51, 0.52, 'Average granite', ha='center', fontsize=7,color = "gray")
        ax.text(0.2, 0.52, 'Plahioclase', ha='center', fontsize=7,color = "gray")
        ax.text(0.8, 0.52, 'K-feldspar', ha='center', fontsize=7,color = "gray")
        ax.text(0.35, 0.46, 'Average gabbro', ha='center', fontsize=7,color = "gray")

          # Arrows & Lines
        plt.arrow(0.28, 0.52, 0.145, 0.3, head_width=0.01, head_length=0.01, fc='red', ec='red')
        plt.arrow(0.48, 0.54, 0.115, 0.23, head_width=0.01, head_length=0.01, fc='red', ec='red')

        lineAR = [(0.5375, 0.655), (0.2, 0.62),(0.3525,0.67)]
        x_li, y_li = zip(*lineAR)
        ax.plot(x_li, y_li, linestyle='-', color='gray',lw=1)
        ax.text(0.16, 0.58, 'Weathring\ntrend', ha='center', fontsize=6,color = "gray",fontstyle='italic')

        # Axis labels
        ax.text(0.5, 1 + 0.05, 'A (Al₂O₃)', ha='center', fontsize=14)
        ax.text(-0.05, -0.05, 'CN (CaO + Na₂O)', ha='right', fontsize=14)
        ax.text(1.05, -0.05, 'K (K₂O)', ha='left', fontsize=14)

        # Plot points
        for label, cn, a, k in data:
            x, y = ternary_to_xy(cn, a, k)
            ax.plot(x, y, marker=marker, color=marker_color, markersize=5)
            if show_labels:
                ax.text(x + 0.01, y + 0.01, label, fontsize=10)
        

        return fig

    # --- UI ---
    st.title("🧪 CIA Ternary Plot Tool")

    with st.form("cia_form"):
        a_input = st.text_area("A (Al₂O₃)", placeholder="e.g., 60, 50, 50")
        cn_input = st.text_area("CN (CaO + Na₂O)", placeholder="e.g., 30, 20, 10")
        k_input = st.text_area("K (K₂O)", placeholder="e.g., 10, 30, 40")
       

        marker = st.selectbox("Select Marker Type", ["o", "s", "^","H",], index=0)
        color = st.color_picker("Pick Marker Color", "#000000")

        submit = st.form_submit_button("Generate Plot")

    if submit:
        try:
            a_vals = [float(i.strip()) for i in a_input.split(",")]
            cn_vals = [float(i.strip()) for i in cn_input.split(",")]
            k_vals = [float(i.strip()) for i in k_input.split(",")]
            

            if not (len(cn_vals) == len(k_vals) == len(a_vals)):
                st.error("All input lists must be the same length.")
            else:
                label_list = [f"S{i+1}" for i in range(len(cn_vals))]

                plot_data = list(zip(label_list, a_vals, cn_vals, k_vals))

                # Create figure
                fig = plot_ternary(plot_data, marker=marker, marker_color=color)

                # Save to BytesIO
                buf = io.BytesIO()
                fig.savefig(buf, format='png', bbox_inches='tight')
                buf.seek(0)

                st.markdown("<div style='margin-top:40px;'>", unsafe_allow_html=True)
                st.subheader("📈 CIA Ternary Plot")
                st.image(buf, caption="CIA Ternary Diagram")
                st.markdown("</div>", unsafe_allow_html=True)
                 # PNG download
                st.download_button("📥 Download Plot (PNG)", buf, "cia_plot.png", "image/png")

                # Data Table
                df = pd.DataFrame({
                    "Label": label_list,
                    "A (Al₂O₃)": a_vals,
                    "CN (CaO+Na₂O)": cn_vals,
                    "K (K₂O)": k_vals
                })
                st.subheader("📄 Data Table")
                st.dataframe(df)

                # CSV download
                csv = df.to_csv(index=False).encode()
                st.download_button("📥 Download Data (CSV)", csv, "cia_data.csv", "text/csv")

               

        except Exception as e:
            st.error(f"Error: {e}")

    

# --- Page: Rainfall Plot ---
elif st.session_state.page == "rainfall":
    st.title("☔ Rainfall Intensity Plot")
    st.button("⬅️ Back to Home", on_click=go_home)

    st.markdown("Upload rainfall data to plot intensity and trend over time.")
    st.info("🔧Comming Soon..")

