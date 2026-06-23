import streamlit as st
import requests
import os

st.set_page_config(page_title="DE Interview Prep Plan", page_icon="🚀", layout="centered")

# ── SUPABASE CONFIG ───────────────────────────────────────────────────────────
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates"
}

def load_progress() -> tuple[set, dict]:
    try:
        res = requests.get(
            f"{SUPABASE_URL}/rest/v1/progress?select=day_num,completed,notes",
            headers=HEADERS
        )
        if res.status_code == 200:
            data = res.json()
            completed = set(row["day_num"] for row in data if row.get("completed", True)) # default True for older rows
            notes = {row["day_num"]: row.get("notes", "") for row in data if row.get("notes")}
            return completed, notes
        else:
            # Fallback if notes column doesn't exist yet
            res2 = requests.get(f"{SUPABASE_URL}/rest/v1/progress?select=day_num", headers=HEADERS)
            if res2.status_code == 200:
                return set(row["day_num"] for row in res2.json()), {}
            st.session_state.db_error = f"GET Error {res.status_code}: {res.text}"
    except Exception as e:
        st.session_state.db_error = f"GET Request Failed: {e}"
    return set(), {}

def save_progress(day_num: int, completed: bool):
    try:
        payload = {"day_num": day_num, "completed": completed}
        if "notes" in st.session_state and day_num in st.session_state.notes:
            payload["notes"] = st.session_state.notes[day_num]
            
        res = requests.post(
            f"{SUPABASE_URL}/rest/v1/progress",
            headers=HEADERS,
            json=payload
        )
        if res.status_code not in (200, 201, 204):
            # Fallback: Try saving without notes if notes column is missing
            if "notes" in payload:
                del payload["notes"]
                res2 = requests.post(f"{SUPABASE_URL}/rest/v1/progress", headers=HEADERS, json=payload)
                if res2.status_code not in (200, 201, 204):
                    st.session_state.db_error = f"POST Error {res2.status_code}: {res2.text}"
            else:
                st.session_state.db_error = f"POST Error {res.status_code}: {res.text}"
    except Exception as e:
        st.session_state.db_error = f"Save Request Failed: {e}"



# ── DATA ──────────────────────────────────────────────────────────────────────
plan = [
    # MONTH 1
    {"week": 1, "month": 1, "theme": "SQL — Intermediate to Advanced", "days": [
        {"day": 1,  "topic": "SQL Recap — JOINs deep dive",        "tag": "SQL",      "tasks": ["INNER, LEFT, RIGHT, FULL OUTER joins", "Practice 10 JOIN problems on LeetCode"]},
        {"day": 2,  "topic": "Window Functions Part 1",             "tag": "SQL",      "tasks": ["ROW_NUMBER, RANK, DENSE_RANK", "PARTITION BY + ORDER BY logic", "Solve 5 problems"]},
        {"day": 3,  "topic": "Window Functions Part 2",             "tag": "SQL",      "tasks": ["LAG, LEAD, FIRST_VALUE, LAST_VALUE", "Running totals, moving averages", "Solve 5 problems"]},
        {"day": 4,  "topic": "Aggregations & Grouping",             "tag": "SQL",      "tasks": ["GROUP BY, HAVING, ROLLUP, CUBE", "Nested aggregations", "Solve 5 problems"]},
        {"day": 5,  "topic": "Subqueries & CTEs",                   "tag": "SQL",      "tasks": ["Correlated subqueries", "WITH clause (CTEs)", "Refactor subqueries into CTEs"]},
        {"day": 6,  "topic": "Practice Day",                        "tag": "Practice", "tasks": ["Solve 10 mixed SQL problems", "Focus on problems you got wrong this week"]},
        {"day": 7,  "topic": "Rest / Light Review",                 "tag": "Rest",     "tasks": ["Review notes from Week 1", "Watch 1 YouTube video on SQL optimization"]},
    ]},
    {"week": 2, "month": 1, "theme": "SQL — Optimization + Python Basics", "days": [
        {"day": 8,  "topic": "Query Optimization",                  "tag": "SQL",      "tasks": ["Indexes — what, why, when", "EXPLAIN / EXPLAIN ANALYZE", "Avoid SELECT *"]},
        {"day": 9,  "topic": "Advanced SQL Patterns",               "tag": "SQL",      "tasks": ["Pivot tables in SQL", "Gap and island problems", "Solve 5 tricky problems"]},
        {"day": 10, "topic": "Python — Data Structures",            "tag": "Python",   "tasks": ["Lists, dicts, sets, tuples", "List comprehensions", "Write 10 small functions"]},
        {"day": 11, "topic": "Python — Functions & OOP Basics",     "tag": "Python",   "tasks": ["*args, **kwargs", "Classes and objects basics", "Write a simple data class"]},
        {"day": 12, "topic": "Python — File I/O & Error Handling",  "tag": "Python",   "tasks": ["Read/write CSV, JSON", "Try/except patterns", "Practice with real datasets"]},
        {"day": 13, "topic": "Practice Day",                        "tag": "Practice", "tasks": ["5 SQL + 5 Python problems", "Mix of easy/medium difficulty"]},
        {"day": 14, "topic": "Rest / Light Review",                 "tag": "Rest",     "tasks": ["Review weak areas", "Plan next week"]},
    ]},
    {"week": 3, "month": 1, "theme": "Python — Pandas & Pipeline Thinking", "days": [
        {"day": 15, "topic": "Pandas Part 1",                       "tag": "Python",   "tasks": ["DataFrames, Series", "read_csv, head, describe, info", "Filtering and selecting"]},
        {"day": 16, "topic": "Pandas Part 2",                       "tag": "Python",   "tasks": ["groupby, merge, join", "apply, map, lambda", "Handle missing values"]},
        {"day": 17, "topic": "Pandas Part 3",                       "tag": "Python",   "tasks": ["Pivot tables in Pandas", "Time series basics", "Solve 5 Pandas exercises"]},
        {"day": 18, "topic": "Writing Clean Pipelines",             "tag": "Python",   "tasks": ["Modular functions for ETL", "Logging basics", "Write a mini ETL script"]},
        {"day": 19, "topic": "Python + SQL Together",               "tag": "Python",   "tasks": ["Connect Python to DB (sqlite3 / sqlalchemy)", "Run queries from Python", "Build a simple pipeline"]},
        {"day": 20, "topic": "Practice Day",                        "tag": "Practice", "tasks": ["Build end-to-end mini pipeline", "CSV → transform → output"]},
        {"day": 21, "topic": "Rest / Light Review",                 "tag": "Rest",     "tasks": ["Review Python notes", "Skim one DE blog post"]},
    ]},
    {"week": 4, "month": 1, "theme": "SQL Mock + Python Review", "days": [
        {"day": 22, "topic": "SQL Mock Interview",                  "tag": "Mock",     "tasks": ["Simulate 45-min SQL round", "Use StrataScratch or LeetCode"]},
        {"day": 23, "topic": "Review SQL Mistakes",                 "tag": "SQL",      "tasks": ["Fix every wrong answer from mock", "Re-solve with explanation"]},
        {"day": 24, "topic": "Python Mock Interview",               "tag": "Mock",     "tasks": ["Simulate coding round", "Focus on pandas + functions"]},
        {"day": 25, "topic": "Review Python Mistakes",              "tag": "Python",   "tasks": ["Fix every wrong answer", "Re-write clean versions"]},
        {"day": 26, "topic": "Month 1 Recap",                       "tag": "Review",   "tasks": ["List top 10 things you learned", "Note what still feels weak"]},
        {"day": 27, "topic": "Practice Day",                        "tag": "Practice", "tasks": ["10 mixed problems — SQL + Python", "Time yourself"]},
        {"day": 28, "topic": "Rest",                                "tag": "Rest",     "tasks": ["Full rest or light reading", "Don't study — recharge!"]},
    ]},

    # MONTH 2
    {"week": 5, "month": 2, "theme": "Data Modeling Fundamentals", "days": [
        {"day": 29, "topic": "Star Schema & Snowflake Schema",      "tag": "Modeling", "tasks": ["Fact vs Dimension tables", "When to use which", "Design a sample schema"]},
        {"day": 30, "topic": "Normalization",                       "tag": "Modeling", "tasks": ["1NF, 2NF, 3NF explained", "When to denormalize", "Practice normalization exercises"]},
        {"day": 31, "topic": "Slowly Changing Dimensions (SCD)",    "tag": "Modeling", "tasks": ["SCD Type 1, 2, 3", "When to use each", "Implement SCD Type 2 example"]},
        {"day": 32, "topic": "Data Vault Basics",                   "tag": "Modeling", "tasks": ["Hubs, Links, Satellites", "Compare vs Star Schema", "Read 1 article on Data Vault"]},
        {"day": 33, "topic": "Modeling Practice",                   "tag": "Practice", "tasks": ["Design schema for e-commerce", "Design schema for ride-sharing app"]},
        {"day": 34, "topic": "Practice Day",                        "tag": "Practice", "tasks": ["Review and refine your schemas", "Get feedback on design choices"]},
        {"day": 35, "topic": "Rest / Light Review",                 "tag": "Rest",     "tasks": ["Review week notes", "Sketch one more schema"]},
    ]},
    {"week": 6, "month": 2, "theme": "Pipeline System Design", "days": [
        {"day": 36, "topic": "Batch vs Streaming",                  "tag": "Design",   "tasks": ["When to use each", "Lambda architecture", "Kappa architecture"]},
        {"day": 37, "topic": "ETL vs ELT",                          "tag": "Design",   "tasks": ["Differences and trade-offs", "Modern data stack (dbt)", "Design an ELT pipeline"]},
        {"day": 38, "topic": "Data Warehouses",                     "tag": "Design",   "tasks": ["Redshift vs BigQuery vs Snowflake", "Partitioning and clustering", "Read comparison article"]},
        {"day": 39, "topic": "Data Lakes & Lakehouses",             "tag": "Design",   "tasks": ["S3 / GCS as data lake", "Delta Lake / Iceberg basics", "When lake vs warehouse"]},
        {"day": 40, "topic": "Orchestration Tools",                 "tag": "Design",   "tasks": ["Airflow — DAGs, operators, sensors", "Understand scheduling basics", "Draw a pipeline with Airflow"]},
        {"day": 41, "topic": "System Design Practice",              "tag": "Practice", "tasks": ["Design a ride-sharing data pipeline", "Think: ingestion → storage → serving"]},
        {"day": 42, "topic": "Rest / Light Review",                 "tag": "Rest",     "tasks": ["Review week notes", "Watch 1 system design video"]},
    ]},
    {"week": 7, "month": 2, "theme": "Spark + Cloud Basics", "days": [
        {"day": 43, "topic": "Spark Fundamentals",                  "tag": "Spark",    "tasks": ["RDD vs DataFrame vs Dataset", "Transformations vs Actions", "Read Spark architecture overview"]},
        {"day": 44, "topic": "PySpark Basics",                      "tag": "Spark",    "tasks": ["SparkSession, read/write", "select, filter, groupBy", "Write 3 PySpark scripts"]},
        {"day": 45, "topic": "Spark Optimization",                  "tag": "Spark",    "tasks": ["Partitioning, caching, broadcast", "Avoid data skew", "Review common bottlenecks"]},
        {"day": 46, "topic": "Cloud — Your Primary Cloud",          "tag": "Cloud",    "tasks": ["Focus on cloud you use at work", "Key services: storage, compute, orchestration"]},
        {"day": 47, "topic": "Cloud — Data Services Deep Dive",     "tag": "Cloud",    "tasks": ["Glue / Dataflow / Data Factory", "S3 / GCS / ADLS", "Redshift / BigQuery / Synapse"]},
        {"day": 48, "topic": "Practice Day",                        "tag": "Practice", "tasks": ["Design a cloud-native pipeline", "Combine Spark + Cloud services"]},
        {"day": 49, "topic": "Rest / Light Review",                 "tag": "Rest",     "tasks": ["Review all of Month 2", "Note gaps to fill in Month 3"]},
    ]},
    {"week": 8, "month": 2, "theme": "System Design Mock + Review", "days": [
        {"day": 50, "topic": "System Design Mock 1",                "tag": "Mock",     "tasks": ["Design: real-time analytics pipeline", "45-minute timed session", "Write down your design"]},
        {"day": 51, "topic": "Review System Design Mock 1",         "tag": "Review",   "tasks": ["Compare with best practices", "Fix gaps in your design"]},
        {"day": 52, "topic": "System Design Mock 2",                "tag": "Mock",     "tasks": ["Design: data platform for fintech", "Focus on reliability + scalability"]},
        {"day": 53, "topic": "Review System Design Mock 2",         "tag": "Review",   "tasks": ["Improve your design", "Practice explaining out loud"]},
        {"day": 54, "topic": "Month 2 Recap",                       "tag": "Review",   "tasks": ["List top 10 things learned", "Identify weak spots"]},
        {"day": 55, "topic": "Practice Day",                        "tag": "Practice", "tasks": ["Mixed practice: SQL + Design", "Timed, interview conditions"]},
        {"day": 56, "topic": "Rest",                                "tag": "Rest",     "tasks": ["Full rest", "You're halfway there!"]},
    ]},

    # MONTH 3
    {"week": 9, "month": 3, "theme": "DSA Basics for DE Interviews", "days": [
        {"day": 57, "topic": "Arrays & Strings",                    "tag": "DSA",      "tasks": ["Two pointers", "Sliding window", "Solve 5 easy/medium problems"]},
        {"day": 58, "topic": "HashMaps & Sets",                     "tag": "DSA",      "tasks": ["Frequency counters", "Two sum pattern", "Solve 5 problems"]},
        {"day": 59, "topic": "Sorting & Searching",                 "tag": "DSA",      "tasks": ["Binary search", "Merge sort concept", "Solve 5 problems"]},
        {"day": 60, "topic": "Stack & Queue",                       "tag": "DSA",      "tasks": ["Stack use cases", "Queue / deque", "Solve 5 problems"]},
        {"day": 61, "topic": "Recursion Basics",                    "tag": "DSA",      "tasks": ["Think recursively", "Factorial, fibonacci", "Solve 3 recursion problems"]},
        {"day": 62, "topic": "Practice Day",                        "tag": "Practice", "tasks": ["10 DSA problems — mixed topics", "Focus on patterns not memorization"]},
        {"day": 63, "topic": "Rest / Light Review",                 "tag": "Rest",     "tasks": ["Review DSA patterns", "Rest your brain"]},
    ]},
    {"week": 10, "month": 3, "theme": "Full Mock Interview Week", "days": [
        {"day": 64, "topic": "Mock Round 1 — SQL",                  "tag": "Mock",     "tasks": ["Full 45-min SQL interview", "Record yourself if possible", "Review after"]},
        {"day": 65, "topic": "Mock Round 2 — Python/DSA",           "tag": "Mock",     "tasks": ["Full 45-min coding round", "Explain your thinking out loud"]},
        {"day": 66, "topic": "Mock Round 3 — System Design",        "tag": "Mock",     "tasks": ["Full 45-min design round", "Draw diagrams, explain trade-offs"]},
        {"day": 67, "topic": "Review All 3 Mocks",                  "tag": "Review",   "tasks": ["List mistakes from each round", "Prioritize top 3 things to fix"]},
        {"day": 68, "topic": "Fix Weak Areas",                      "tag": "Review",   "tasks": ["Deep dive on biggest gaps", "Re-solve problems you got wrong"]},
        {"day": 69, "topic": "Practice Day",                        "tag": "Practice", "tasks": ["Re-do one mock from this week", "Aim to improve on previous score"]},
        {"day": 70, "topic": "Rest",                                "tag": "Rest",     "tasks": ["Full rest", "No screens if possible!"]},
    ]},
    {"week": 11, "month": 3, "theme": "Behavioral + Company Research", "days": [
        {"day": 71, "topic": "Behavioral Interview Prep",           "tag": "Behavioral","tasks": ["Write STAR answers for 10 questions", "Tell me about yourself — practice 3 versions"]},
        {"day": 72, "topic": "Behavioral Practice",                 "tag": "Behavioral","tasks": ["Practice out loud for 30 mins", "Record and review yourself"]},
        {"day": 73, "topic": "Research Target Companies",           "tag": "Research",  "tasks": ["List 10 companies you want to apply to", "Note their tech stack and team size"]},
        {"day": 74, "topic": "Resume Polish",                       "tag": "Resume",    "tasks": ["Quantify every bullet point", "Tailor resume for DE roles", "Get 1 person to review it"]},
        {"day": 75, "topic": "LinkedIn + Profile Optimization",     "tag": "Resume",    "tasks": ["Update LinkedIn headline and about", "Add projects and skills", "Connect with 5 DE professionals"]},
        {"day": 76, "topic": "Practice Day",                        "tag": "Practice",  "tasks": ["Full mock interview from scratch", "All 3 rounds back to back"]},
        {"day": 77, "topic": "Rest",                                "tag": "Rest",      "tasks": ["Rest and reflect on progress"]},
    ]},
    {"week": 12, "month": 3, "theme": "Final Prep + Start Applying", "days": [
        {"day": 78, "topic": "Final SQL Revision",                  "tag": "SQL",      "tasks": ["Top 20 SQL questions review", "Speed drill — solve fast"]},
        {"day": 79, "topic": "Final Python Revision",               "tag": "Python",   "tasks": ["Top 10 Python patterns", "Write clean pipeline from memory"]},
        {"day": 80, "topic": "Final System Design Revision",        "tag": "Design",   "tasks": ["Review all design patterns", "Practice explaining in 5 mins"]},
        {"day": 81, "topic": "Start Applying",                      "tag": "Action",   "tasks": ["Apply to first 5 companies", "Track in a spreadsheet"]},
        {"day": 82, "topic": "Apply + Practice",                    "tag": "Action",   "tasks": ["Apply to 5 more companies", "Do 1 hour of weak area review"]},
        {"day": 83, "topic": "Apply + Mock",                        "tag": "Action",   "tasks": ["Apply to 5 more companies", "Final full mock interview"]},
        {"day": 84, "topic": "Month 3 Complete 🎉",                 "tag": "Rest",     "tasks": ["Review your full journey", "Celebrate your progress!", "Keep applying and stay consistent"]},
    ]},

    # MONTH 4
    {"week": 13, "month": 4, "theme": "Active Applications + Interview Practice", "days": [
        {"day": 85, "topic": "Apply Daily Routine",                 "tag": "Action",      "tasks": ["Apply to 3-5 companies per day", "Customize cover letter lightly"]},
        {"day": 86, "topic": "Company-Specific Prep",              "tag": "Research",    "tasks": ["Research interview process of top 3 targets", "Check Glassdoor + Leetcode company tags"]},
        {"day": 87, "topic": "Mock + Apply",                       "tag": "Action",      "tasks": ["1 mock interview", "Apply to 5 companies"]},
        {"day": 88, "topic": "Referrals",                          "tag": "Networking",  "tasks": ["Reach out to 5 connections for referrals", "Message ex-colleagues or LinkedIn contacts"]},
        {"day": 89, "topic": "Weak Area Deep Dive",                "tag": "Review",      "tasks": ["Focus on your #1 weak topic", "Solve 10 targeted problems"]},
        {"day": 90, "topic": "Practice Day",                       "tag": "Practice",    "tasks": ["Full mock interview", "Review and improve"]},
        {"day": 91, "topic": "Rest",                               "tag": "Rest",        "tasks": ["Rest", "Trust your preparation"]},
    ]},
    {"week": 14, "month": 4, "theme": "Interviews Begin", "days": [
        {"day": 92, "topic": "Keep Applying",                      "tag": "Action",      "tasks": ["3-5 applications", "Follow up on pending ones"]},
        {"day": 93, "topic": "Interview Preparation",              "tag": "Research",    "tasks": ["For each interview: research company deeply", "Prep 3 questions to ask them"]},
        {"day": 94, "topic": "Post-Interview Review",              "tag": "Review",      "tasks": ["After each interview: write what went well", "Write what you'd do differently"]},
        {"day": 95, "topic": "Keep the Momentum",                  "tag": "Action",      "tasks": ["Don't stop applying even if interviews are going well", "Pipeline of 3-5 active processes is healthy"]},
        {"day": 96, "topic": "Negotiation Prep",                   "tag": "Negotiation", "tasks": ["Research market salaries on Levels.fyi / Glassdoor", "Prepare your number + justification"]},
        {"day": 97, "topic": "Practice Day",                       "tag": "Practice",    "tasks": ["Mock interview or apply", "Stay sharp"]},
        {"day": 98, "topic": "Done! 🎉",                           "tag": "Rest",        "tasks": ["Review your full journey", "You made it!", "Go get that offer!"]},
    ]},
]

TAG_COLORS = {
    "SQL":        "#1D4ED8",
    "Python":     "#15803D",
    "Practice":   "#C2410C",
    "Rest":       "#6B7280",
    "Mock":       "#7E22CE",
    "Review":     "#92400E",
    "Modeling":   "#0369A1",
    "Design":     "#BE123C",
    "Spark":      "#9A3412",
    "Cloud":      "#0F766E",
    "DSA":        "#3730A3",
    "Behavioral": "#86198F",
    "Research":   "#166534",
    "Resume":     "#78350F",
    "Action":     "#9F1239",
    "Networking": "#5B21B6",
    "Negotiation":"#14532D",
}

MONTH_TITLES = {
    1: "📘 Month 1 — SQL & Python",
    2: "📙 Month 2 — System Design & Modeling",
    3: "📗 Month 3 — Mock Interviews & DSA",
    4: "📕 Month 4 — Applications & Interviews",
}

# ── SESSION STATE ─────────────────────────────────────────────────────────────

if "completed" not in st.session_state or "notes" not in st.session_state:
    completed_data, notes_data = load_progress()
    st.session_state.completed = completed_data
    st.session_state.notes = notes_data

def toggle(day_num):
    if day_num in st.session_state.completed:
        st.session_state.completed.remove(day_num)
        save_progress(day_num, completed=False)
    else:
        st.session_state.completed.add(day_num)
        save_progress(day_num, completed=True)

def toggle_theme():
    os.makedirs(".streamlit", exist_ok=True)
    config_path = ".streamlit/config.toml"
    current_theme = "dark"
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            if 'base="light"' in f.read().replace(" ", ""):
                current_theme = "light"
    
    new_theme = "dark" if current_theme == "light" else "light"
    with open(config_path, "w") as f:
        f.write(f'[theme]\nbase="{new_theme}"\n')

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚀 DE Interview Prep")
    
    current_theme = "dark"
    config_path = ".streamlit/config.toml"
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            if 'base="light"' in f.read().replace(" ", ""):
                current_theme = "light"
                
    theme_label = "🌞 Switch to Day Mode" if current_theme == "dark" else "🌙 Switch to Night Mode"
    if st.button(theme_label):
        toggle_theme()
        st.rerun()
        

    total = 98
    done  = len(st.session_state.completed)
    pct   = int(done / total * 100)
    st.progress(pct / 100)
    st.caption(f"**{done}/{total} days complete ({pct}%)**")

    st.divider()
    selected_month = st.radio("Jump to month", [1, 2, 3, 4],
                               format_func=lambda m: MONTH_TITLES[m])

    st.divider()
    st.info("💡 **Daily Rule**\nStudy 1–1.5 hrs *before* picking up your phone. Consistency beats intensity.")

# ── MAIN ──────────────────────────────────────────────────────────────────────
st.title(MONTH_TITLES[selected_month])

if "just_completed" in st.session_state:
    dn_completed = st.session_state.just_completed
    st.toast(f"🎉 Awesome work! Day {dn_completed} is in the books.")
    # Show balloons every 7 days (end of a week)
    if dn_completed % 7 == 0:
        st.balloons()
    del st.session_state.just_completed

if "db_error" in st.session_state:
    st.error(f"Supabase Database Error: {st.session_state.db_error}")
    st.info("Tip: If you're getting a 401/403 or empty results, make sure your Supabase table 'progress' exists and has Row Level Security (RLS) disabled, or has appropriate policies set up!")
    del st.session_state.db_error

# ── ANALYTICS DASHBOARD ───────────────────────────────────────────────────────
st.header("📊 Your Progress Dashboard")

total_days = 98
completed_count = len(st.session_state.completed)
completion_pct = int((completed_count / total_days) * 100) if total_days else 0

# Calculate Streak
streak = 0
if st.session_state.completed:
    max_day = max(st.session_state.completed)
    for d in range(max_day, 0, -1):
        if d in st.session_state.completed:
            streak += 1
        else:
            break

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Completed", f"{completed_count} / {total_days}")
col2.metric("Remaining", total_days - completed_count)
col3.metric("Completion %", f"{completion_pct}%")
col4.metric("Current Streak", f"🔥 {streak} Days")

with st.expander("Show Topic Breakdown Chart 📈"):
    import pandas as pd
    topic_counts = {}
    topic_completed = {}
    for w in plan:
        for d in w["days"]:
            t = d["tag"]
            topic_counts[t] = topic_counts.get(t, 0) + 1
            if d["day"] in st.session_state.completed:
                topic_completed[t] = topic_completed.get(t, 0) + 1
                
    df = pd.DataFrame({
        "Topic": list(topic_counts.keys()),
        "Completed": [topic_completed.get(t, 0) for t in topic_counts.keys()],
        "Total": [topic_counts.get(t, 0) for t in topic_counts.keys()]
    })
    st.bar_chart(df.set_index("Topic")["Completed"])

st.divider()

weeks_in_month = [w for w in plan if w["month"] == selected_month]

for week in weeks_in_month:
    week_done = sum(1 for d in week["days"] if d["day"] in st.session_state.completed)
    st.subheader(f"Week {week['week']} · {week['theme']}  ({week_done}/{len(week['days'])})")

    for day in week["days"]:
        dn      = day["day"]
        is_done = dn in st.session_state.completed
        color   = TAG_COLORS.get(day["tag"], "#6B7280")
        badge   = f'<span style="background:{color};color:white;padding:2px 10px;border-radius:99px;font-size:11px;font-weight:700;">{day["tag"]}</span>'

        label   = f"~~Day {dn} — {day['topic']}~~" if is_done else f"Day {dn} — {day['topic']}"

        with st.expander(f"{'✅' if is_done else '⬜'} Day {dn} — {day['topic']}"):
            st.markdown(badge, unsafe_allow_html=True)
            st.markdown("**Tasks for today:**")
            for task in day["tasks"]:
                st.markdown(f"→ {task}")
            btn_label = "Mark as done ✅" if not is_done else "Mark as incomplete ↩️"
            if st.button(btn_label, key=f"btn_{dn}"):
                if not is_done:
                    st.session_state.just_completed = dn
                toggle(dn)
                st.rerun()
                
            st.markdown("---")
            # Interactive Notes
            current_note = st.session_state.notes.get(dn, "")
            new_note = st.text_area("📝 Personal Notes / Links", value=current_note, key=f"note_{dn}", placeholder="Paste LeetCode links or personal notes here...")
            if st.button("Save Note 💾", key=f"save_note_{dn}"):
                st.session_state.notes[dn] = new_note
                save_progress(dn, is_done) # Upserts the progress and new note
                st.toast(f"Notes saved for Day {dn}!")

    st.divider()
