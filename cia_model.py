import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt
import io

def ternary_to_xy(a, cn, k):
    total = a + cn + k
    a /= total
    cn /= total
    k /= total
    x = 5 * (2 * k + cn)
    y = (10) * cn
    return x, y

# --- Plotting function ---
def plot_ternary(data, marker="o", marker_color="black", show_labels=False):
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 10 + 1)
    ax.axis('off')

    # Draw triangle
    triangle = [(0, 0), (10, 0), (5, 10), (0, 0)]
    x_tri, y_tri = zip(*triangle)
    ax.plot(x_tri, y_tri, 'k-', lw=2)

    # Draw line
    line = [(-1, 0), (-1, 10), (-1, 0)]
    x_li, y_li = zip(*line)
    ax.plot(x_li, y_li, 'k-', lw=2)

    # Mark Lavel and grid
    for i in range(11):
        fcn = i/10
        x_m,y_m = zip((-1,10-fcn ), (-1, 10))
        ax.plot(x_m, y_m, marker='x', color='black',lw=0)

        for j in range(11):
            ax.text(-1.5,j/10, f"{int(j * 10)}", ha='left', fontsize=8)
        # strong weathering
    lines = [(-1, 8.5), (5.7, 8.5)]
    x_li, y_li = zip(*lines)
    ax.plot(x_li, y_li, linestyle='--', color='gray')
    ax.text(-0.5, 9.2, 'strong\nweathering', ha='center', fontsize=7,color = "gray")

            # Intermediate weathering
    lines = [(-1, 6.5), (6.8, 6.5)]
    x_li, y_li = zip(*lines)
    ax.plot(x_li, y_li, linestyle='--', color='gray')
    ax.text(-0.5, 7.2, 'Intermediate\nweathering', ha='center', fontsize=7,color = "gray")

        # Weak weathering
    lines = [(-1, 5), (7.5, 5)]
    x_li, y_li = zip(*lines)
    ax.plot(x_li, y_li, linestyle='--', color='gray')
    ax.text(-0.5, 5.2, 'Weak\nweathering', ha='center', fontsize=7,color = "gray")

    # Axis labels
    ax.text(5, 10 + 0.5, 'A (Al₂O₃)', ha='center', fontsize=14)
    ax.text(-0.5, -0.5, 'CN (CaO + Na₂O)', ha='right', fontsize=14)
    ax.text(10.05, -0.5, 'K (K₂O)', ha='left', fontsize=14)

    # Plot points
    for label, cn, k, a in data:
        x, y = ternary_to_xy(a, cn, k)
        ax.plot(x, y, marker=marker, color=marker_color, markersize=8)
        if show_labels:
            ax.text(x + 0.1, y + 0.1, label, fontsize=10)

    return fig

# --- UI ---
st.title("🧪 CIA Ternary Plot Tool")

with st.form("cia_form"):
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

            plot_data = list(zip(label_list, cn_vals, k_vals, a_vals))

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

            # Data Table
            df = pd.DataFrame({
                "Label": label_list,
                "CN (CaO+Na₂O)": cn_vals,
                "K (K₂O)": k_vals,
                "A (Al₂O₃)": a_vals
            })
            st.subheader("📄 Data Table")
            st.dataframe(df)

            # CSV download
            csv = df.to_csv(index=False).encode()
            st.download_button("📥 Download Data (CSV)", csv, "cia_data.csv", "text/csv")

            # PNG download
            st.download_button("📥 Download Plot (PNG)", buf, "cia_plot.png", "image/png")

    except Exception as e:
        st.error(f"Error: {e}")