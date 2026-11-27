from pathlib import Path
from io import BytesIO

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ------------------------------------------------------------
# EduPro | Learner Analytics Dashboard
# ------------------------------------------------------------
st.set_page_config(
    page_title="EduPro | Learner Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Premium dark interface
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #08111f;
        --panel: #101d30;
        --panel2: #14243a;
        --text: #e8f0fb;
        --muted: #9aacc4;
        --cyan: #36c5f0;
        --blue: #5687ff;
        --line: rgba(150, 180, 220, .16);
    }
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    .stApp {
        background:
          radial-gradient(circle at 78% 0%, rgba(29, 113, 170, .20), transparent 32%),
          radial-gradient(circle at 0% 30%, rgba(57, 83, 171, .13), transparent 28%),
          #08111f;
        color: var(--text);
    }
    [data-testid="stHeader"] { background: rgba(8,17,31,.82); }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1b30 0%, #101f36 100%);
        border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] * { color: #e8f0fb; }
    [data-testid="stSidebar"] .stMultiSelect span {
        color: #e8f0fb !important;
    }
    h1, h2, h3, h4, p, label { color: var(--text); }
    .hero {
        position: relative;
        overflow: hidden;
        padding: 28px 32px;
        border: 1px solid rgba(91, 190, 255, .28);
        border-radius: 22px;
        background: linear-gradient(115deg, #122b4a 0%, #12577c 54%, #087f9f 100%);
        box-shadow: 0 18px 50px rgba(0,0,0,.28);
        margin: 4px 0 22px 0;
        animation: fadeUp .75s ease both;
    }
    .hero:after {
        content: "";
        position: absolute;
        width: 250px; height: 250px;
        right: -65px; top: -125px;
        border: 1px solid rgba(255,255,255,.22);
        border-radius: 50%;
        box-shadow: 0 0 0 28px rgba(255,255,255,.045),
                    0 0 0 58px rgba(255,255,255,.035);
    }
    .hero h1 { font-size: 2rem; font-weight: 800; margin: 0; color: white; }
    .hero p { color: #d4efff; margin: 8px 0 0 0; font-size: .98rem; }
    .eyebrow {
        text-transform: uppercase; letter-spacing: 2px;
        font-size: .70rem; font-weight: 700; color: #9cecff;
        margin-bottom: 8px;
    }
    .section-head {
        font-size: 1.28rem; font-weight: 750;
        margin: 20px 0 3px 0; color: #edf5ff;
    }
    .section-sub { color: #94a9c4; font-size: .88rem; margin-bottom: 15px; }
    .kpi {
        background: linear-gradient(145deg, rgba(22,40,64,.98), rgba(14,28,46,.98));
        border: 1px solid rgba(112,157,211,.20);
        border-radius: 17px;
        padding: 18px 19px;
        min-height: 122px;
        box-shadow: 0 10px 28px rgba(0,0,0,.18);
        transition: transform .25s ease, border-color .25s ease, box-shadow .25s ease;
        animation: fadeUp .65s ease both;
    }
    .kpi:hover {
        transform: translateY(-5px);
        border-color: rgba(54,197,240,.65);
        box-shadow: 0 16px 35px rgba(0,0,0,.30), 0 0 22px rgba(54,197,240,.10);
    }
    .kpi-label { color: #9fb3cd; font-size: .76rem; font-weight: 700; letter-spacing: .7px; text-transform: uppercase; }
    .kpi-value { color: #f3f8ff; font-size: 2rem; font-weight: 800; margin-top: 7px; line-height: 1.1; }
    .kpi-note { color: #8da5c1; font-size: .74rem; margin-top: 7px; }
    .insight {
        background: linear-gradient(120deg, rgba(20,48,72,.95), rgba(17,34,56,.95));
        border: 1px solid rgba(54,197,240,.25);
        border-left: 4px solid #36c5f0;
        padding: 14px 17px; border-radius: 12px;
        margin: 8px 0; color: #dcecff;
        animation: fadeUp .55s ease both;
    }
    .pill {
        display: inline-block; padding: 5px 10px; border-radius: 20px;
        background: rgba(54,197,240,.13); color: #8de8ff;
        border: 1px solid rgba(54,197,240,.25); font-size: .72rem;
        font-weight: 700; margin-right: 6px;
    }
    div[data-testid="stPlotlyChart"] {
        background: rgba(16,29,48,.72);
        border: 1px solid rgba(112,157,211,.14);
        border-radius: 16px; padding: 8px;
        box-shadow: 0 8px 25px rgba(0,0,0,.12);
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid var(--line); border-radius: 12px; overflow: hidden;
    }
    .footer {
        color: #7187a4; font-size: .75rem; text-align: center;
        padding: 25px 0 8px 0; border-top: 1px solid var(--line); margin-top: 30px;
    }
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @media (prefers-reduced-motion: reduce) {
        *, *:before, *:after { animation: none !important; transition: none !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

PLOT_TEMPLATE = "plotly_dark"
PLOT_BG = "rgba(16,29,48,0)"
GRID = "rgba(150,180,220,.13)"
PALETTE = ["#36c5f0", "#5687ff", "#8b7cff", "#46d6b2", "#f3b65c",
           "#ed83bd", "#70a6d8", "#a8d978", "#f18f70", "#9cafd0"]


def style_fig(fig, height=390):
    fig.update_layout(
        template=PLOT_TEMPLATE,
        paper_bgcolor=PLOT_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(family="DM Sans, sans-serif", color="#dce8f7", size=12),
        title=dict(font=dict(size=15, color="#edf5ff"), x=0.02, xanchor="left"),
        height=height,
        margin=dict(l=28, r=22, t=55, b=35),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#bdcce0")),
        hoverlabel=dict(bgcolor="#14243a", font_color="#ffffff"),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor=GRID, tickfont_color="#a9bbd1")
    fig.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False, tickfont_color="#a9bbd1")
    return fig


def kpi_card(label, value, note):
    st.markdown(
        f"""<div class="kpi">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-note">{note}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def key_insight(message):
    st.markdown(
        f'<div class="insight"><b>✦ Key Insight</b><br>{message}</div>',
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner="Loading and integrating the master workbook...")
def load_data():
    base = Path(__file__).resolve().parent
    candidates = [
        base.parent / "EduPro_Online_Platform_Master.xlsx",
        base / "EduPro_Online_Platform_Master.xlsx",
        base.parent / "EduPro Online Platform (1).xlsx",
        base / "EduPro Online Platform (1).xlsx",
    ]
    workbook = next((p for p in candidates if p.exists()), None)
    if workbook is None:
        raise FileNotFoundError(
            "Master workbook not found. Keep EduPro_Online_Platform_Master.xlsx "
            "in the project root (one folder above 04_Streamlit_Dashboard)."
        )

    users = pd.read_excel(workbook, sheet_name="Users")
    courses = pd.read_excel(workbook, sheet_name="Courses")
    transactions = pd.read_excel(workbook, sheet_name="Transactions")
    teachers = pd.read_excel(workbook, sheet_name="Teachers")

    required = {
        "Users": {"UserID", "Age", "Gender"},
        "Courses": {"CourseID", "CourseCategory", "CourseType", "CourseLevel"},
        "Transactions": {"TransactionID", "UserID", "CourseID", "TeacherID"},
        "Teachers": {"TeacherID"},
    }
    for name, cols in required.items():
        frame = {"Users": users, "Courses": courses,
                 "Transactions": transactions, "Teachers": teachers}[name]
        missing = cols - set(frame.columns)
        if missing:
            raise ValueError(f"{name} sheet is missing columns: {sorted(missing)}")

    merged = transactions.merge(users, on="UserID", how="left", validate="many_to_one")
    merged = merged.merge(courses, on="CourseID", how="left", validate="many_to_one")
    age_bins = [0, 17, 25, 35, 45, np.inf]
    age_labels = ["Below 18", "18–25", "26–35", "36–45", "Above 45"]
    merged["Age Group"] = pd.cut(
        merged["Age"], bins=age_bins, labels=age_labels, include_lowest=True
    )
    return users, courses, transactions, teachers, merged, workbook.name


try:
    users, courses, transactions, teachers, integrated, workbook_name = load_data()
except Exception as exc:
    st.error(f"Unable to load project data: {exc}")
    st.info(
        "Check that the master Excel workbook is in the project root, "
        "beside the 04_Streamlit_Dashboard folder."
    )
    st.stop()


# Sidebar navigation and filters
with st.sidebar:
    st.markdown("## 🎓 EduPro")
    st.caption("LEARNER INTELLIGENCE PLATFORM")
    st.markdown("---")
    page = st.radio(
        "NAVIGATION",
        ["Overview", "Demographics", "Course Preferences",
         "Learner Behaviour", "Data & Export"],
        index=0,
    )
    st.markdown("---")
    st.markdown("### 🎛️ Dashboard Filters")
    st.caption("Filters update the analysis across all sections.")

    if st.button("↺ Reset all filters", use_container_width=True):
        for key in ["age_filter", "gender_filter", "category_filter", "level_filter"]:
            st.session_state.pop(key, None)
        st.rerun()

    age_options = ["Below 18", "18–25", "26–35", "36–45", "Above 45"]
    gender_options = sorted(integrated["Gender"].dropna().unique().tolist())
    category_options = sorted(integrated["CourseCategory"].dropna().unique().tolist())
    level_options = sorted(integrated["CourseLevel"].dropna().unique().tolist())

    selected_ages = st.multiselect("Age Group", age_options, default=age_options[:3], key="age_filter")
    selected_genders = st.multiselect("Gender", gender_options, default=gender_options, key="gender_filter")
    selected_categories = st.multiselect("Course Category", category_options, default=category_options, key="category_filter")
    selected_levels = st.multiselect("Course Level", level_options, default=level_options, key="level_filter")
    st.markdown("---")
    st.markdown(
        f'<span class="pill">Workbook connected</span><br><small style="color:#8fa6c2">{workbook_name}</small>',
        unsafe_allow_html=True,
    )

filtered = integrated[
    integrated["Age Group"].astype(str).isin(selected_ages)
    & integrated["Gender"].isin(selected_genders)
    & integrated["CourseCategory"].isin(selected_categories)
    & integrated["CourseLevel"].isin(selected_levels)
].copy()

if filtered.empty:
    st.warning("No records match the selected filters. Please adjust or reset your filters.")
    st.stop()

n_learners = filtered["UserID"].nunique()
n_enrolments = len(filtered)
n_courses = filtered["CourseID"].nunique()
avg_enrolments = n_enrolments / n_learners if n_learners else 0

# Shared hero header
st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">EDUPRO • LEARNER INTELLIGENCE</div>
      <h1>🎓 Learner Analytics</h1>
      <p>Understand learner demographics, course preferences and enrollment behaviour — all in one view.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Overview page
if page == "Overview":
    st.markdown('<div class="section-head">Dashboard Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Key indicators for the currently selected filters.</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    with cols[0]: kpi_card("Learners in view", f"{n_learners:,}", "Unique learners matching filters")
    with cols[1]: kpi_card("Total enrollments", f"{n_enrolments:,}", "Filtered transaction records")
    with cols[2]: kpi_card("Courses represented", f"{n_courses:,}", "Unique courses in this view")
    with cols[3]: kpi_card("Avg. enrollments / learner", f"{avg_enrolments:.2f}", "Within the filtered view")

    st.markdown('<div class="section-head">Learner Demographics</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Explore enrollment distribution across age groups and gender.</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        age_df = filtered.groupby("Age Group", observed=False).size().reindex(age_options, fill_value=0).reset_index(name="Enrollments")
        age_df = age_df.rename(columns={"Age Group": "Age Group"})
        fig = px.bar(age_df, x="Age Group", y="Enrollments", color="Age Group",
                     color_discrete_sequence=PALETTE, text_auto=True, title="Enrollments by Age Group")
        fig.update_layout(showlegend=False)
        st.plotly_chart(style_fig(fig, 370), use_container_width=True)
        key_insight('The tallest bar identifies the age group contributing the most enrollments in the selected data.')
    with c2:
        gender_df = filtered["Gender"].value_counts().rename_axis("Gender").reset_index(name="Enrollments")
        fig = px.pie(gender_df, names="Gender", values="Enrollments", hole=.66,
                     color_discrete_sequence=["#ed83bd", "#36c5f0", "#8b7cff"],
                     title="Gender Participation by Enrollment")
        fig.update_traces(textposition="inside", textinfo="label+percent")
        st.plotly_chart(style_fig(fig, 370), use_container_width=True)
        key_insight('The largest segment represents the gender with the highest enrollment participation in this view.')

    st.markdown('<div class="section-head">At a Glance</div>', unsafe_allow_html=True)
    cat = filtered["CourseCategory"].value_counts()
    lev = filtered["CourseLevel"].value_counts()
    age_top = filtered["Age Group"].value_counts().idxmax()
    gender_top = filtered["Gender"].value_counts().idxmax()
    st.markdown(
        f'<div class="insight">✨ <b>Most represented age group:</b> {age_top}. '
        f'<b>Highest gender participation:</b> {gender_top}. '
        f'<b>Most selected category:</b> {cat.idxmax()}. '
        f'<b>Most selected level:</b> {lev.idxmax()}.</div>',
        unsafe_allow_html=True,
    )

# Demographics page
elif page == "Demographics":
    st.markdown('<div class="section-head">Learner Demographics</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Age and gender patterns in the selected enrollment records.</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        age_df = filtered.groupby("Age Group", observed=False).size().reindex(age_options, fill_value=0).reset_index(name="Enrollments")
        fig = px.bar(age_df, x="Age Group", y="Enrollments", color="Age Group",
                     color_discrete_sequence=PALETTE, text_auto=True, title="Age-wise Enrollment Distribution")
        fig.update_layout(showlegend=False)
        st.plotly_chart(style_fig(fig), use_container_width=True)
        key_insight('The highest bar indicates the age group with the greatest enrollment activity.')
    with c2:
        gender_age = filtered.groupby(["Age Group", "Gender"], observed=False).size().reset_index(name="Enrollments")
        fig = px.bar(gender_age, x="Age Group", y="Enrollments", color="Gender",
                     barmode="group", color_discrete_sequence=["#ed83bd", "#36c5f0"],
                     title="Gender Participation Across Age Groups")
        st.plotly_chart(style_fig(fig), use_container_width=True)
        key_insight('Compare the paired bars to see how enrollment participation differs by gender across age groups.')

    gender_level = pd.crosstab(filtered["Gender"], filtered["CourseLevel"])
    fig = px.imshow(gender_level, text_auto=True, aspect="auto",
                    color_continuous_scale=["#12243b", "#087eae", "#36c5f0"],
                    title="Gender × Course Level")
    st.plotly_chart(style_fig(fig, 350), use_container_width=True)
    key_insight('The matrix compares course-level enrollment counts across gender groups; higher values indicate more enrollments.')

    st.markdown('<div class="insight">📌 Learner-level participation percentages can overlap across course levels because one learner may enroll in more than one level.</div>', unsafe_allow_html=True)

# Course preferences page
elif page == "Course Preferences":
    st.markdown('<div class="section-head">Course Preference Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Compare category popularity, course levels and free/paid course-type preferences.</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        cat_df = filtered["CourseCategory"].value_counts().sort_values().reset_index()
        cat_df.columns = ["Course Category", "Enrollments"]
        fig = px.bar(cat_df, x="Enrollments", y="Course Category", orientation="h",
                     text="Enrollments", color="Enrollments",
                     color_continuous_scale=["#244c78", "#36c5f0"],
                     title="Course Category Popularity")
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(style_fig(fig, 470), use_container_width=True)
        key_insight('The leading category is the most frequently enrolled course category in the current selection.')
    with c2:
        level_df = filtered["CourseLevel"].value_counts().reindex(["Beginner", "Intermediate", "Advanced"]).dropna().reset_index()
        level_df.columns = ["Course Level", "Enrollments"]
        fig = px.bar(level_df, x="Course Level", y="Enrollments", color="Course Level",
                     color_discrete_sequence=["#36c5f0", "#5687ff", "#8b7cff"],
                     text_auto=True, title="Course Level Preference")
        fig.update_layout(showlegend=False)
        st.plotly_chart(style_fig(fig, 470), use_container_width=True)
        key_insight('The tallest bar identifies the course level with the greatest enrollment volume.')

    c3, c4 = st.columns(2)
    with c3:
        type_df = filtered["CourseType"].value_counts().rename_axis("Course Type").reset_index(name="Enrollments")
        fig = px.pie(type_df, names="Course Type", values="Enrollments", hole=.62,
                     color_discrete_sequence=["#36c5f0", "#46d6b2"],
                     title="Free vs Paid Course Enrollments")
        fig.update_traces(textposition="inside", textinfo="label+percent")
        st.plotly_chart(style_fig(fig, 370), use_container_width=True)
        key_insight('The larger segment indicates which course type contributes more enrollments in the current selection.')
    with c4:
        type_level = pd.crosstab(filtered["CourseType"], filtered["CourseLevel"])
        fig = px.imshow(type_level, text_auto=True, aspect="auto",
                        color_continuous_scale=["#12243b", "#087eae", "#36c5f0"],
                        title="Course Type × Course Level")
        st.plotly_chart(style_fig(fig, 370), use_container_width=True)
        key_insight('Compare rows to see how course-level enrollment patterns vary between Free and Paid courses.')

    age_category = pd.crosstab(filtered["Age Group"], filtered["CourseCategory"])
    fig = px.imshow(age_category, aspect="auto",
                    color_continuous_scale=["#12243b", "#087eae", "#36c5f0"],
                    title="Age Group × Course Category")
    st.plotly_chart(style_fig(fig, 420), use_container_width=True)
    key_insight('This heatmap highlights the course categories with stronger enrollment activity within each age group.')

# Learner behaviour page
elif page == "Learner Behaviour":
    st.markdown('<div class="section-head">Learner Enrollment Behaviour</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Review enrollment frequency, engagement segments and enrollment concentration.</div>', unsafe_allow_html=True)

    learner_freq = filtered.groupby("UserID").size().rename("Enrollments")
    segment = pd.cut(learner_freq, bins=[0, 2, 4, np.inf],
                     labels=["Low (1–2)", "Moderate (3–4)", "High (5+)"])
    segment_df = segment.value_counts(sort=False).reindex(["Low (1–2)", "Moderate (3–4)", "High (5+)"], fill_value=0).rename_axis("Engagement Segment").reset_index(name="Learners")

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(segment_df, x="Engagement Segment", y="Learners",
                     color="Engagement Segment",
                     color_discrete_sequence=["#5687ff", "#36c5f0", "#46d6b2"],
                     text_auto=True, title="Learner Engagement Segmentation")
        fig.update_layout(showlegend=False)
        st.plotly_chart(style_fig(fig), use_container_width=True)
        key_insight('The largest bar identifies the most common learner engagement segment in the filtered data.')
    with c2:
        sorted_counts = learner_freq.sort_values(ascending=False).reset_index(drop=True)
        total = sorted_counts.sum()
        top10_n = max(1, int(np.ceil(len(sorted_counts) * .10)))
        top20_n = max(1, int(np.ceil(len(sorted_counts) * .20)))
        concentration = pd.DataFrame({
            "Learner Group": ["Top 10% learners", "Top 20% learners"],
            "Enrollment Share (%)": [
                sorted_counts.head(top10_n).sum() / total * 100,
                sorted_counts.head(top20_n).sum() / total * 100,
            ],
        })
        fig = px.bar(concentration, x="Learner Group", y="Enrollment Share (%)",
                     color="Learner Group", text=concentration["Enrollment Share (%)"].map(lambda x: f"{x:.2f}%"),
                     color_discrete_sequence=["#36c5f0", "#46d6b2"],
                     title="Enrollment Concentration")
        fig.update_layout(showlegend=False, yaxis_range=[0, 100])
        st.plotly_chart(style_fig(fig), use_container_width=True)
        key_insight('The chart shows how much of all selected enrollments are contributed by the top 10% and top 20% of learners.')

    level_counts = filtered.groupby("CourseLevel").size()
    level_learners = filtered.groupby("CourseLevel")["UserID"].nunique()
    level_summary = pd.DataFrame({
        "Course Level": level_counts.index,
        "Enrollments": level_counts.values,
        "Unique Learners": level_learners.reindex(level_counts.index).values,
    })
    level_summary["Avg. Enrollments per Learner"] = (
        level_summary["Enrollments"] / level_summary["Unique Learners"].replace(0, np.nan)
    ).round(2)
    st.markdown("#### Average Enrollment Activity by Course Level")
    st.dataframe(level_summary, use_container_width=True, hide_index=True)

    top10_share = concentration.loc[0, "Enrollment Share (%)"]
    top20_share = concentration.loc[1, "Enrollment Share (%)"]
    st.markdown(
        f'<div class="insight">📊 In the current filtered view, the top 10% of learners account for '
        f'<b>{top10_share:.2f}%</b> of enrollments, while the top 20% account for '
        f'<b>{top20_share:.2f}%</b>.</div>',
        unsafe_allow_html=True,
    )

# Data and export page
elif page == "Data & Export":
    st.markdown('<div class="section-head">Data Explorer & Export Centre</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Inspect the filtered integrated dataset and export the analysis data.</div>', unsafe_allow_html=True)
    st.markdown(
        f'<span class="pill">{len(filtered):,} filtered rows</span>'
        f'<span class="pill">{filtered["UserID"].nunique():,} unique learners</span>'
        f'<span class="pill">{filtered["CourseID"].nunique():,} courses</span>',
        unsafe_allow_html=True,
    )
    st.dataframe(filtered, use_container_width=True, height=430)

    csv_bytes = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download filtered data (CSV)",
        data=csv_bytes,
        file_name="EduPro_Filtered_Learner_Data.csv",
        mime="text/csv",
        use_container_width=True,
    )

    def make_excel_export():
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            filtered.to_excel(writer, sheet_name="Filtered_Integrated_Data", index=False)
            pd.DataFrame({
                "Metric": ["Learners in view", "Enrollments", "Courses represented",
                           "Average enrollments per learner"],
                "Value": [n_learners, n_enrolments, n_courses, round(avg_enrolments, 2)],
            }).to_excel(writer, sheet_name="Dashboard_KPIs", index=False)
            filtered["CourseCategory"].value_counts().rename_axis("CourseCategory").reset_index(name="Enrollments").to_excel(
                writer, sheet_name="Category_Summary", index=False
            )
            filtered["CourseLevel"].value_counts().rename_axis("CourseLevel").reset_index(name="Enrollments").to_excel(
                writer, sheet_name="Level_Summary", index=False
            )
        buffer.seek(0)
        return buffer.getvalue()

    st.download_button(
        "📘 Export dashboard data (Excel)",
        data=make_excel_export(),
        file_name="EduPro_Dashboard_Export.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

    with st.expander("Data quality note: TeacherID"):
        st.write(
            "TeacherID is retained from the source Transactions sheet. Repeated TeacherIDs can occur "
            "when a teacher is associated with multiple enrollment transactions. The current dashboard "
            "does not use TeacherID as a learner-demographic KPI. Any teacher-assignment imbalance "
            "should be documented separately rather than changing the source workbook."
        )

st.markdown(
    '<div class="footer">EDUPRO LEARNER ANALYTICS • Descriptive learner intelligence • Built with Streamlit & Plotly</div>',
    unsafe_allow_html=True,
)
