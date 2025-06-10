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
    
    st.set_page_config(page_title="Lithora – QFL Ternary Analysis", layout="wide")
    
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
                    st.error("All input lists must be the same length.")
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
    import math
    from IPython.display import SVG, display
    
    def ternary_to_xy(a, cn, k):
        total = a + cn + k
        a /= total
        cn /= total
        k /= total
        x = 0.5 * (2 * k + cn)
        y = (math.sqrt(3) / 2) * cn
        return x, y
    
    def generate_svg(points, filename="ternary_plot.svg"):
        width = 800  # made wider
        height = 520
        padding = 150  # more padding to shift right
        scale = 400
    
        def svg_point(x, y):
            px = padding + x * scale
            py = height - (padding + y * scale)
            return px, py
    
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" style="background:white;">
            <rect width="100%" height="100%" fill="white"/>'''
    
        # Triangle outline
        tri_coords = [
            (0.0, 0.0),
            (1.0, 0.0),
            (0.5, math.sqrt(3)/2),
        ]
        svg += '<polygon points="{}" fill="none" stroke="black" stroke-width="2"/>'.format(
            ' '.join(f"{svg_point(x, y)[0]},{svg_point(x, y)[1]}" for x, y in tri_coords)
        )
    
        # Grid lines and ticks
        for i in range(1, 10):
            frac = i / 10
    
            # Grid lines
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
    
        # Vertical CN axis line (center top)
        top_x, top_y = ternary_to_xy(0, 100, 0)
        bottom_x, bottom_y = ternary_to_xy(0, 0, 100)
        top_px, top_py = svg_point(top_x, top_y)
        bot_px, bot_py = svg_point(bottom_x, bottom_y)
        svg += f'<line x1="{bot_px}" y1="{bot_py}" x2="{top_px}" y2="{top_py}" stroke="black" stroke-width="1.5" stroke-dasharray="0"/>'
    
        # CN ticks on vertical line
        for i in range(0, 11):
            frac = i / 10
            x, y = ternary_to_xy(0, frac * 100, (1 - frac) * 100)
            px, py = svg_point(x, y)
            svg += f'<line x1="{px - 5}" y1="{py}" x2="{px + 5}" y2="{py}" stroke="black" />'
            svg += f'<text x="{px + 10}" y="{py + 3}" font-size="10" fill="black">{int(frac * 100)}%</text>'
    
        # Plot sample points
        for label, cn, k, a in points:
            x, y = ternary_to_xy(a, cn, k)
            sx, sy = svg_point(x, y)
            svg += f'''
                <circle cx="{sx}" cy="{sy}" r="5" fill="red"/>
                <text x="{sx + 6}" y="{sy - 6}" font-size="12">{label}</text>
            '''
    
        svg += '</svg>'
        with open(filename, "w") as f:
            f.write(svg)
    
    # Sample data
    sample_points = [
        ("Sample 1", 30, 10, 60),
        ("Sample 2", 20, 30, 50),
        ("Sample 3", 10, 40, 50),
        ("Sample 4", 25, 25, 50),
    ]
    
    generate_svg(sample_points)
    st.display(SVG(filename="ternary_plot.svg"))

# --- Page: Rainfall Plot ---
elif st.session_state.page == "rainfall":
    st.title("☔ Rainfall Intensity Plot")
    st.button("⬅️ Back to Home", on_click=go_home)

    st.markdown("Upload rainfall data to plot intensity and trend over time.")
    st.info("🔧 Rainfall logic will go here.")

