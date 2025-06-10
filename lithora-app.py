import pandas as pd
import matplotlib.pyplot as plt
import mpltern
from io import BytesIO

def clean_commas(input_string):
    cleaned_string = ""
    prev_char = None
    for char in input_string:
        if char == ',' and prev_char == ',':
            continue
        cleaned_string += char
        prev_char = char
    return cleaned_string.rstrip(',')

def create_dataframe(d1, d2, d3):
    df = pd.DataFrame({'Quartz': d1, 'Feldspar': d2, 'Lithics': d3})
    df['Total'] = df['Quartz'] + df['Feldspar'] + df['Lithics']
    df['%Q'] = df['Quartz'] / df['Total'] * 100
    df['%F'] = df['Feldspar'] / df['Total'] * 100
    df['%L'] = df['Lithics'] / df['Total'] * 100
    return df.round(2)

def get_csv_download(df):
    return df.to_csv(index=False).encode('utf-8')

def plot_primary_ternary(df):
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
    ax.grid(True, which='major', linestyle='--', linewidth=0.5, color='gray')
    buf = BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf

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

    provenance_fields = {
        'Basement Uplift': [(100,0,0),(0,100,0),(0,85,15),(96,0,4)],
        'Recycled Orogen': [(25, 0, 75),(51,40,9),(96,0,4)],
        'Undissected Arc': [(0, 50, 50), (25, 0, 75),(0,0,100)],
        'Transitional Arc': [(0, 50, 50), (25, 0, 75),(33,12,55),(17,70,13),(0,85,15)],
        'Dissected Arc'  : [(51,40,9),(17,70,13),(33,12,55)]
    }

    colors = {
        'Basement Uplift': 'lightyellow',
        'Recycled Orogen': 'skyblue',
        'Undissected Arc': 'cyan',
        'Transitional Arc': 'lightgreen',
        'Dissected Arc'  : 'lightblue'
    }

    for label, vertices in provenance_fields.items():
        fill_vertices = [(v[0]/100, v[1]/100, v[2]/100) for v in vertices]
        ax.fill(*zip(*fill_vertices), label=label, alpha=0.3, color=colors.get(label))

    ax.plot(df['%Q'], df['%F'], df['%L'], 'ko', label='Data Points')
    ax.legend(fontsize='small', loc='upper left', bbox_to_anchor=(0.8, 1))
    ax.grid(True, which='major', linestyle='--', linewidth=0.5, color='gray')

    buf = BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf

def extract_QFL_from_csv(uploaded_file):
    content = uploaded_file.read().decode("utf-8").splitlines()
    headers = content[0].split(",")
    try:
        q_idx = headers.index("Quartz")
        f_idx = headers.index("Feldspar")
        l_idx = headers.index("Lithics")
    except ValueError as e:
        return f"ERROR: Missing required column: {e}"

    q_vals, f_vals, l_vals = [], [], []
    for line in content[1:]:
        parts = line.split(",")
        if len(parts) >= 3:
            q_vals.append(parts[q_idx].strip())
            f_vals.append(parts[f_idx].strip())
            l_vals.append(parts[l_idx].strip())

    return ", ".join(q_vals), ", ".join(f_vals), ", ".join(l_vals)
