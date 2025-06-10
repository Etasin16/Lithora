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
    from IPython.display import SVG, display
    
    # --- Helper functions ---
    def ternary_to_xy(a, cn, k):
        total = a + cn + k
        a /= total
        cn /= total
        k /= total
        x = 0.5 * (2 * k + cn)
        y = (math.sqrt(3) / 2) * cn
        return x, y
    
    def svg_point(x, y, width=800, height=520, padding=150, scale=400):
        px = padding + x * scale
        py = height - (padding + y * scale)
        return px, py
    
    def generate_svg(points, marker="circle", marker_color="black", add_labels=True):
        width, height, padding, scale = 800, 620, 150, 400
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" style="background:white;">'
            f'<rect width="100%" height="100%" fill="white"/>'
        )
    
        # Triangle outline
        tri_coords = [(0.0, 0.0), (1.0, 0.0), (0.5, math.sqrt(3)/2)]
        svg += '<polygon points="{}" fill="none" stroke="black" stroke-width="2"/>'.format(
            ' '.join(f"{svg_point(x, y)[0]},{svg_point(x, y)[1]}" for x, y in tri_coords))
    
        # Grid lines
        for i in range(1, 10):
            frac = i / 10
    
            ax, ay = ternary_to_xy(frac * 100, 100 - frac * 100, 0)
            bx, by = ternary_to_xy(frac * 100, 0, 100 - frac * 100)
            svg += f'<line x1="{svg_point(ax, ay)[0]}" y1="{svg_point(ax, ay)[1]}" x2="{svg_point(bx, by)[0]}" y2="{svg_point(bx, by)[1]}" stroke="#ccc"/>'
    
            ax, ay = ternary_to_xy(0, frac * 100, 100 - frac * 100)
            bx, by = ternary_to_xy(100 - frac * 100, frac * 100, 0)
            svg += f'<line x1="{svg_point(ax, ay)[0]}" y1="{svg_point(ax, ay)[1]}" x2="{svg_point(bx, by)[0]}" y2="{svg_point(bx, by)[1]}" stroke="#ccc"/>'
    
            ax, ay = ternary_to_xy(100 - frac * 100, 0, frac * 100)
            bx, by = ternary_to_xy(0, 100 - frac * 100, frac * 100)
            svg += f'<line x1="{svg_point(ax, ay)[0]}" y1="{svg_point(ax, ay)[1]}" x2="{svg_point(bx, by)[0]}" y2="{svg_point(bx, by)[1]}" stroke="#ccc"/>'
    
        # Axis labels
        svg += f'''
            <text x="{svg_point(0.5, 0.9)[0]}" y="{svg_point(0.5, 0.9)[1] - 10}" text-anchor="middle" font-size="16">A (Al₂O₃)</text>
            <text x="{svg_point(0.0, 0.0)[0] - 10}" y="{svg_point(0.0, 0.0)[1] + 5}" text-anchor="end" font-size="16">CN (CaO + Na₂O)</text>
            <text x="{svg_point(1.0, 0.0)[0] + 10}" y="{svg_point(1.0, 0.0)[1] + 5}" text-anchor="start" font-size="16">K (K₂O)</text>
        '''
    
        # CN axis ticks
        for i in range(0, 11):
            frac = i / 10
            x, y = ternary_to_xy(0, frac * 100, (1 - frac) * 100)
            px, py = svg_point(x, y)
            svg += f'<line x1="{px - 5}" y1="{py}" x2="{px + 5}" y2="{py}" stroke="black" />'
            svg += f'<text x="{px + 10}" y="{py + 3}" font-size="10" fill="black">{int(frac * 100)}%</text>'
    
        # Plot sample points
        for row in points:
            label, cn, k, a = row
            x, y = ternary_to_xy(a, cn, k)
            sx, sy = svg_point(x, y)
            shape_attrs = f'x="{sx}" y="{sy}" width="10" height="10"' if marker == "rect" else (
                          f'points="{sx},{sy-6} {sx-5},{sy+4} {sx+5},{sy+4}"' if marker == "triangle" else 
                          f'cx="{sx}" cy="{sy}" r="5"')
            svg += f'<{marker} {shape_attrs} fill="{marker_color}"/>'
            if add_labels and label:
                svg += f'<text x="{sx + 6}" y="{sy - 6}" font-size="12">{label}</text>'
    
        svg += '</svg>'
        return svg
    
    def get_svg_download_link(svg, filename="plot.svg"):
        b64 = base64.b64encode(svg.encode()).decode()
        href = f'<a href="data:image/svg+xml;base64,{b64}" download="{filename}">📥 Download SVG</a>'
        return href
    
    # --- UI ---
    st.title("🧪 CIA Ternary Plot Tool")
    st.markdown("Generate a CIA ternary plot using oxide values: Al₂O₃ (A), CaO + Na₂O (CN), and K₂O (K).")
    
    # Sample input section
    with st.form("cia_form"):
        cn_input = st.text_area("CN (CaO + Na₂O)", placeholder="e.g., 30, 20, 10")
        k_input = st.text_area("K (K₂O)", placeholder="e.g., 10, 30, 40")
        a_input = st.text_area("A (Al₂O₃)", placeholder="e.g., 60, 50, 50")
    
        marker = st.selectbox("Select Marker Type", ["circle", "rect", "triangle"], index=0)
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
    
                plot_data = list(zip(label_list, cn_vals, k_vals, a_vals))
                svg = generate_svg(plot_data, marker=marker, marker_color=color)
    
                # Show plot lower
                st.markdown("<div style='margin-top:40px;'>", unsafe_allow_html=True)
                st.subheader("📈 CIA Ternary Plot")
                import streamlit.components.v1 as components
                components.html(svg, height=650)

                st.markdown("</div>", unsafe_allow_html=True)
                # SVG download link
                st.download_button("📥 Download Plot",get_svg_download_link(svg),"cia_plot.svg")
    
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
                st.download_button("📥 Download Data (CSV)", csv, "cia_data.csv", "text/csv")
    
        except Exception as e:
            st.error(f"Error: {e}")

    

# --- Page: Rainfall Plot ---
elif st.session_state.page == "rainfall":
    st.title("☔ Rainfall Intensity Plot")
    st.button("⬅️ Back to Home", on_click=go_home)

    st.markdown("Upload rainfall data to plot intensity and trend over time.")
    st.info("🔧 Rainfall logic will go here.")

