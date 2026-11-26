
import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Quote Explorer",
    page_icon="💬",
    layout="wide"
)

# ---------------- THEME ----------------
st.markdown("""
<style>
.stApp {
    background: #f5efe6;
    color: #3e2c23;
}
[data-testid="stSidebar"] {
    background: #3e2c23;
}
[data-testid="stSidebar"] * {
    color: #f5efe6 !important;
}
h1, h2, h3 {
    color: #4b3024;
}
div[data-testid="stMetric"] {
    background: #e8d8c5;
    padding: 18px;
    border-radius: 15px;
    border: 1px solid #c7a98b;
}
div.stButton > button {
    background-color: #6f4e37;
    color: white;
    border-radius: 10px;
    border: none;
}
.quote-card {
    background: #fffaf3;
    padding: 22px;
    border-radius: 18px;
    border-left: 5px solid #9b7653;
    margin: 12px 0;
    box-shadow: 0 4px 12px rgba(70, 40, 20, 0.08);
}
.quote-text {
    font-size: 20px;
    font-style: italic;
    color: #493329;
}
.quote-author {
    color: #8b5e3c;
    font-weight: bold;
    margin-top: 12px;
}
.tag {
    background: #e5d2bd;
    color: #5b3b29;
    padding: 4px 10px;
    border-radius: 15px;
    margin-right: 5px;
    display: inline-block;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
CSV_FILE = "data/quotes_data.csv"
JSON_FILE = "data/quotes_data.json"

if not os.path.exists(CSV_FILE):
    st.error("quotes_data.csv not found! Please run your scraping script first.")
    st.stop()

df = pd.read_csv(CSV_FILE)

# Normalize column names
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# Find columns with different possible names
def find_column(possible_names):
    for name in possible_names:
        if name in df.columns:
            return name
    return None

quote_col = find_column(["quote", "text", "quote_text"])
author_col = find_column(["author", "author_name"])
tags_col = find_column(["tags", "tag"])
author_url_col = find_column(["author_url", "url"])
page_url_col = find_column(["page_url", "source_url"])

if quote_col is None or author_col is None:
    st.error("Quote or Author columns were not found in your CSV.")
    st.write("Your columns are:", list(df.columns))
    st.stop()

# Clean basic data
df[quote_col] = df[quote_col].fillna("").astype(str)
df[author_col] = df[author_col].fillna("Unknown").astype(str)

if tags_col:
    df[tags_col] = df[tags_col].fillna("").astype(str)
else:
    df["tags"] = ""
    tags_col = "tags"

# ---------------- SIDEBAR ----------------
st.sidebar.title("💬 Quote Explorer")
st.sidebar.caption("Web Scraping Project • Web 2")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Quote Explorer", "Data & Downloads"]
)

st.sidebar.markdown("---")
st.sidebar.write("📚 Data Source")
st.sidebar.write("Quotes to Scrape")

# ---------------- HEADER ----------------
st.title("💬 Quotes Analytics")
st.markdown("### Explore inspirational quotes, authors and popular topics.")
st.markdown("---")

# ---------------- METRICS ----------------
total_quotes = len(df)
unique_authors = df[author_col].nunique()

def count_tags(tag_text):
    return len([
        t.strip() for t in tag_text.split(",")
        if t.strip()
    ])

total_tags = df[tags_col].apply(count_tags).sum()
average_tags = df[tags_col].apply(count_tags).mean() if len(df) else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("💬 Total Quotes", f"{total_quotes:,}")
col2.metric("✍️ Authors", f"{unique_authors:,}")
col3.metric("🏷️ Tags", f"{total_tags:,}")
col4.metric("📌 Avg Tags / Quote", f"{average_tags:.1f}")

st.markdown("---")

# ---------------- DASHBOARD ----------------
if page == "Dashboard":

    st.subheader("📊 Quotes Overview")

    # Top authors
    author_counts = df[author_col].value_counts().head(10).reset_index()
    author_counts.columns = ["Author", "Quotes"]

    # Top Tags
    tag_list = []
    for tag_string in df[tags_col]:
        for tag in tag_string.split(","):
            tag = tag.strip()
            if tag:
                tag_list.append(tag)

    tag_counts = pd.Series(tag_list).value_counts().head(10).reset_index()
    tag_counts.columns = ["Tag", "Count"]

    left, right = st.columns(2)

    with left:
        st.markdown("#### ✍️ Most Featured Authors")
        fig1 = px.bar(
            author_counts,
            x="Quotes",
            y="Author",
            orientation="h",
            color="Quotes",
            color_continuous_scale=["#c7a98b", "#6f4e37"]
        )
        fig1.update_layout(
            yaxis=dict(autorange="reversed"),
            plot_bgcolor="#fffaf3",
            paper_bgcolor="#f5efe6"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with right:
        st.markdown("#### 🏷️ Popular Tags")
        if len(tag_counts):
            fig2 = px.bar(
                tag_counts,
                x="Tag",
                y="Count",
                color="Count",
                color_continuous_scale=["#d8b99c", "#8b5e3c"]
            )
            fig2.update_layout(
                plot_bgcolor="#fffaf3",
                paper_bgcolor="#f5efe6"
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No tags available.")

    st.markdown("---")
    st.subheader("🌟 Random Quotes")

    sample = df.sample(min(3, len(df)), random_state=None)

    for _, row in sample.iterrows():
        tags = row[tags_col]
        tag_html = "".join(
            f'<span class="tag">{t.strip()}</span>'
            for t in tags.split(",") if t.strip()
        )

        st.markdown(f"""
        <div class="quote-card">
            <div class="quote-text">"{row[quote_col]}"</div>
            <div class="quote-author">— {row[author_col]}</div>
            <div style="margin-top:10px">{tag_html}</div>
        </div>
        """, unsafe_allow_html=True)

# ---------------- QUOTE EXPLORER ----------------
elif page == "Quote Explorer":

    st.subheader("🔎 Search and Explore Quotes")

    search = st.text_input(
        "Search quotes or authors",
        placeholder="Type a quote, author name, or keyword..."
    )

    authors = sorted(df[author_col].unique())
    selected_authors = st.multiselect(
        "Filter by Author",
        authors
    )

    filtered_df = df.copy()

    if search:
        filtered_df = filtered_df[
            filtered_df[quote_col].str.contains(
                search, case=False, na=False
            ) |
            filtered_df[author_col].str.contains(
                search, case=False, na=False
            )
        ]

    if selected_authors:
        filtered_df = filtered_df[
            filtered_df[author_col].isin(selected_authors)
        ]

    st.write(f"Found **{len(filtered_df)} quotes**")

    for _, row in filtered_df.iterrows():

        tags = row[tags_col]
        tag_html = "".join(
            f'<span class="tag">{t.strip()}</span>'
            for t in tags.split(",") if t.strip()
        )

        st.markdown(f"""
        <div class="quote-card">
            <div class="quote-text">"{row[quote_col]}"</div>
            <div class="quote-author">— {row[author_col]}</div>
            <div style="margin-top:10px">{tag_html}</div>
        </div>
        """, unsafe_allow_html=True)

# ---------------- DOWNLOADS ----------------
elif page == "Data & Downloads":

    st.subheader("📁 Dataset & Downloads")

    st.write("Preview of your scraped dataset:")
    st.dataframe(df, use_container_width=True)

    st.markdown("### Download Files")

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download CSV",
        data=csv_data,
        file_name="quotes_data.csv",
        mime="text/csv"
    )

    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            json_data = f.read()

        st.download_button(
            "📥 Download JSON",
            data=json_data,
            file_name="quotes_data.json",
            mime="application/json"
        )
    else:
        st.warning("JSON file was not found.")

    st.markdown("---")
    st.write("### Dataset Information")
    st.write(f"Rows: {len(df)}")
    st.write(f"Columns: {len(df.columns)}")
    st.write("Column Names:", list(df.columns))

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<center>Made with Python, Streamlit & Plotly | Web Scraping Project</center>",
    unsafe_allow_html=True
)
