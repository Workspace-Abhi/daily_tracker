import streamlit as st
import requests
import os
import pandas as pd
from datetime import datetime, timedelta
import time

try:
    from streamlit_calendar import calendar
    HAS_CALENDAR = True
except ImportError:
    HAS_CALENDAR = False

st.set_page_config(page_title="DE Interview Prep Plan", page_icon="🚀", layout="wide")

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
            completed = set(row["day_num"] for row in data if row.get("completed", True)) 
            notes = {row["day_num"]: row.get("notes", "") for row in data if row.get("notes")}
            return completed, notes
        else:
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
            if "notes" in payload:
                del payload["notes"]
                res2 = requests.post(f"{SUPABASE_URL}/rest/v1/progress", headers=HEADERS, json=payload)
                if res2.status_code not in (200, 201, 204):
                    st.session_state.db_error = f"POST Error {res2.status_code}: {res2.text}"
            else:
                st.session_state.db_error = f"POST Error {res.status_code}: {res.text}"
    except Exception as e:
        st.session_state.db_error = f"Save Request Failed: {e}"

def load_custom_events() -> list:
    try:
        res = requests.get(
            f"{SUPABASE_URL}/rest/v1/custom_events?select=id,title,start_time,end_time,color",
            headers=HEADERS
        )
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return []

def save_custom_event(title: str, start_time: str, end_time: str, color: str):
    try:
        payload = {
            "id": int(time.time() * 1000) % 2147483647,
            "title": title,
            "start_time": start_time,
            "end_time": end_time,
            "color": color
        }
        res = requests.post(f"{SUPABASE_URL}/rest/v1/custom_events", headers=HEADERS, json=payload)
        if res.status_code not in (200, 201, 204):
            st.session_state.db_error = f"Calendar Event Save Error {res.status_code}: {res.text}"
    except Exception as e:
        st.session_state.db_error = f"Calendar Event Request Failed: {e}"

def delete_custom_event(event_id: int):
    try:
        res = requests.delete(f"{SUPABASE_URL}/rest/v1/custom_events?id=eq.{event_id}", headers=HEADERS)
        if res.status_code not in (200, 204):
            st.session_state.db_error = f"Calendar Event Delete Error {res.status_code}: {res.text}"
    except Exception as e:
        st.session_state.db_error = f"Calendar Event Delete Request Failed: {e}"

# ── DATA (2 YOE PREMIUM CURRICULUM) ───────────────────────────────────────────
plan = [
    # MONTH 1
    {"week": 1, "month": 1, "theme": "Advanced SQL & Query Optimization", "days": [
        {"day": 1,  "topic": "Query Execution Plans",               "tag": "SQL",      "tasks": ["Understand EXPLAIN / EXPLAIN ANALYZE", "Scan types (Index, Seq, Bitmap)", "Identify bottlenecks"]},
        {"day": 2,  "topic": "Advanced Indexing",                   "tag": "SQL",      "tasks": ["B-Tree vs Hash vs GiST", "Composite & Covering Indexes", "Solve 3 hard LeetCode problems"]},
        {"day": 3,  "topic": "Window Functions Deep Dive",          "tag": "SQL",      "tasks": ["Advanced framing (ROWS BETWEEN)", "Gaps and Islands problem", "Solve 5 problems"]},
        {"day": 4,  "topic": "Concurrency & Locking",               "tag": "SQL",      "tasks": ["Row-level vs Table-level locks", "Deadlocks", "Transaction Isolation Levels (ACID)"]},
        {"day": 5,  "topic": "Query Tuning Scenarios",              "tag": "SQL",      "tasks": ["Rewrite correlated subqueries to JOINs", "Optimize GROUP BY memory", "Review material"]},
        {"day": 6,  "topic": "Practice Day",                        "tag": "Practice", "tasks": ["Solve 5 hard StrataScratch SQL problems"]},
        {"day": 7,  "topic": "Rest / Review",                       "tag": "Rest",     "tasks": ["Review weak spots", "Prepare for Python week"]},
    ]},
    {"week": 2, "month": 1, "theme": "Python for Data Pipelines", "days": [
        {"day": 8,  "topic": "OOP in Data Engineering",             "tag": "Python",   "tasks": ["Design a modular ETL class", "Inheritance & Polymorphism", "Mixins"]},
        {"day": 9,  "topic": "Generators & Memory Profiling",       "tag": "Python",   "tasks": ["yield keyword", "Handling 10GB files in 1GB RAM", "Use memory_profiler"]},
        {"day": 10, "topic": "Concurrency in Python",               "tag": "Python",   "tasks": ["Multiprocessing vs Multithreading", "asyncio basics", "When to use which"]},
        {"day": 11, "topic": "Advanced Pandas & Vectorization",     "tag": "Python",   "tasks": ["Avoid apply(), use vectorization", "Pandas memory optimization (categoricals)", "Chunking"]},
        {"day": 12, "topic": "Testing Data Pipelines",              "tag": "Python",   "tasks": ["pytest basics", "Mocking database connections", "Write tests for your ETL class"]},
        {"day": 13, "topic": "Practice Day",                        "tag": "Practice", "tasks": ["Build a multi-threaded web scraper/ingestor", "Write unit tests for it"]},
        {"day": 14, "topic": "Rest / Review",                       "tag": "Rest",     "tasks": ["Review Python notes"]},
    ]},
    {"week": 3, "month": 1, "theme": "Data Modeling for Scale", "days": [
        {"day": 15, "topic": "Kimball Deep Dive",                   "tag": "Modeling", "tasks": ["Factless Fact tables", "Accumulating Snapshot tables", "Conformed Dimensions"]},
        {"day": 16, "topic": "Advanced SCDs",                       "tag": "Modeling", "tasks": ["SCD Type 4 & 6", "Handling late-arriving dimensions", "Implement SCD logic in SQL"]},
        {"day": 17, "topic": "Modern Data Stack Modeling",          "tag": "Modeling", "tasks": ["dbt modeling conventions (staging, intermediate, mart)", "Wide tables vs Star Schema"]},
        {"day": 18, "topic": "Data Vault 2.0",                      "tag": "Modeling", "tasks": ["Hubs, Links, Satellites design", "When to choose Data Vault over Kimball"]},
        {"day": 19, "topic": "NoSQL Modeling",                      "tag": "Modeling", "tasks": ["Cassandra/DynamoDB modeling patterns", "Partition/Sort keys", "Wide-column vs Document"]},
        {"day": 20, "topic": "Practice Day",                        "tag": "Practice", "tasks": ["Design schema for an Uber-like app", "Design schema for a social network feed"]},
        {"day": 21, "topic": "Rest / Review",                       "tag": "Rest",     "tasks": ["Review Month 1 concepts"]},
    ]},
    {"week": 4, "month": 1, "theme": "Month 1 Mocks", "days": [
        {"day": 22, "topic": "Advanced SQL Mock",                   "tag": "Mock",     "tasks": ["45-min timed session", "Focus on window functions and performance"]},
        {"day": 23, "topic": "Review SQL Mock",                     "tag": "Review",   "tasks": ["Identify syntax issues or logic gaps", "Re-solve with optimal execution plan"]},
        {"day": 24, "topic": "Python / ETL Mock",                   "tag": "Mock",     "tasks": ["45-min timed session: Write an ETL parser in Python", "Focus on modularity and memory"]},
        {"day": 25, "topic": "Review Python Mock",                  "tag": "Review",   "tasks": ["Refactor code for PEP8", "Add docstrings and type hints"]},
        {"day": 26, "topic": "Data Modeling Mock",                  "tag": "Mock",     "tasks": ["45-min timed session: Schema design", "Draw on whiteboard/excalidraw"]},
        {"day": 27, "topic": "Month 1 Recap",                       "tag": "Review",   "tasks": ["List 5 key takeaways", "Identify weak areas to review on weekends"]},
        {"day": 28, "topic": "Rest",                                "tag": "Rest",     "tasks": ["Full rest!"]},
    ]},

    # MONTH 2
    {"week": 5, "month": 2, "theme": "Big Data & Spark Architecture", "days": [
        {"day": 29, "topic": "Spark Internals",                     "tag": "Spark",    "tasks": ["Driver, Executors, Tasks, Stages", "DAG visualization", "Lazy Evaluation mechanics"]},
        {"day": 30, "topic": "Shuffling & Partitioning",            "tag": "Spark",    "tasks": ["Hash vs Range partitioning", "repartition vs coalesce", "Managing data skew"]},
        {"day": 31, "topic": "Advanced Spark Optimization",         "tag": "Spark",    "tasks": ["Broadcast joins", "AQE (Adaptive Query Execution)", "Salting for skewed joins"]},
        {"day": 32, "topic": "Spark Memory Management",             "tag": "Spark",    "tasks": ["Execution vs Storage memory", "Spilling to disk", "Garbage collection tuning basics"]},
        {"day": 33, "topic": "PySpark Practice",                    "tag": "Practice", "tasks": ["Write a script to aggregate 10M rows", "Apply broadcast joins", "Optimize execution"]},
        {"day": 34, "topic": "Practice Day",                        "tag": "Practice", "tasks": ["Solve 3 complex PySpark transformations", "Use Window functions in PySpark"]},
        {"day": 35, "topic": "Rest / Review",                       "tag": "Rest",     "tasks": ["Review Spark concepts"]},
    ]},
    {"week": 6, "month": 2, "theme": "Data Lakes & Open Table Formats", "days": [
        {"day": 36, "topic": "Data Lake Architecture",              "tag": "Cloud",    "tasks": ["S3/GCS partition strategies", "Parquet vs ORC vs Avro internals", "Columnar advantages"]},
        {"day": 37, "topic": "Delta Lake / Iceberg",                "tag": "Cloud",    "tasks": ["ACID in Data Lakes", "Time travel & Z-Ordering", "Read architecture comparison"]},
        {"day": 38, "topic": "Cloud Data Warehouses",               "tag": "Cloud",    "tasks": ["Snowflake vs BigQuery architecture", "Compute vs Storage separation", "Clustering keys"]},
        {"day": 39, "topic": "dbt (Data Build Tool)",               "tag": "Cloud",    "tasks": ["dbt macros & jinja", "Materialization strategies", "dbt tests and documentation"]},
        {"day": 40, "topic": "Lakehouse Design",                    "tag": "Design",   "tasks": ["Design a medallion architecture (Bronze, Silver, Gold)", "Trade-offs vs pure DWH"]},
        {"day": 41, "topic": "Practice Day",                        "tag": "Practice", "tasks": ["Set up a dummy dbt project locally", "Write 2 models and 1 macro"]},
        {"day": 42, "topic": "Rest / Review",                       "tag": "Rest",     "tasks": ["Review Lakehouse architecture"]},
    ]},
    {"week": 7, "month": 2, "theme": "Streaming & Real-Time Data", "days": [
        {"day": 43, "topic": "Kafka Internals",                     "tag": "Kafka",    "tasks": ["Topics, Partitions, Brokers", "Consumer Groups & Offsets", "Exactly-once semantics"]},
        {"day": 44, "topic": "Stream Processing Frameworks",        "tag": "Kafka",    "tasks": ["Spark Structured Streaming vs Flink", "Micro-batch vs Continuous processing"]},
        {"day": 45, "topic": "Windows & Watermarks",                "tag": "Kafka",    "tasks": ["Tumbling, Hopping, Session windows", "Handling late data with watermarks"]},
        {"day": 46, "topic": "CDC (Change Data Capture)",           "tag": "Kafka",    "tasks": ["Debezium architecture", "Log-based vs Query-based CDC", "Design a CDC pipeline"]},
        {"day": 47, "topic": "Real-Time Databases",                 "tag": "Design",   "tasks": ["Druid / ClickHouse / Pinot basics", "When to use OLAP databases for real-time"]},
        {"day": 48, "topic": "Practice Day",                        "tag": "Practice", "tasks": ["Design a real-time fraud detection pipeline", "Map out components and latencies"]},
        {"day": 49, "topic": "Rest / Review",                       "tag": "Rest",     "tasks": ["Review Streaming concepts"]},
    ]},
    {"week": 8, "month": 2, "theme": "System Design Mock + Review", "days": [
        {"day": 50, "topic": "System Design Mock 1",                "tag": "Mock",     "tasks": ["Design an event tracking system for a global app", "45-minute timed session"]},
        {"day": 51, "topic": "Review System Design Mock 1",         "tag": "Review",   "tasks": ["Evaluate scalability, fault tolerance, cost", "Identify single points of failure"]},
        {"day": 52, "topic": "System Design Mock 2",                "tag": "Mock",     "tasks": ["Design a real-time leaderboards system", "Focus on streaming and state management"]},
        {"day": 53, "topic": "Review System Design Mock 2",         "tag": "Review",   "tasks": ["Refine your diagram", "Practice explaining trade-offs aloud"]},
        {"day": 54, "topic": "Month 2 Recap",                       "tag": "Review",   "tasks": ["List top 5 Big Data takeaways", "Identify weak spots in Streaming/Spark"]},
        {"day": 55, "topic": "Practice Day",                        "tag": "Practice", "tasks": ["Mixed practice: SQL + Spark Optimization", "Timed conditions"]},
        {"day": 56, "topic": "Rest",                                "tag": "Rest",     "tasks": ["Full rest", "You are halfway there!"]},
    ]},

    # MONTH 3
    {"week": 9, "month": 3, "theme": "Orchestration & DevOps", "days": [
        {"day": 57, "topic": "Advanced Airflow",                    "tag": "DevOps",   "tasks": ["Custom Operators & Hooks", "XComs vs external storage", "Dynamic DAG generation"]},
        {"day": 58, "topic": "Airflow Architecture",                "tag": "DevOps",   "tasks": ["Scheduler, Webserver, Workers", "Celery vs Kubernetes executor"]},
        {"day": 59, "topic": "Data Quality & Governance",           "tag": "DevOps",   "tasks": ["Great Expectations / Soda basics", "Data lineage (DataHub)", "Handling PII"]},
        {"day": 60, "topic": "Docker & Containers",                 "tag": "DevOps",   "tasks": ["Write a Dockerfile for an ETL app", "Docker Compose for local testing"]},
        {"day": 61, "topic": "CI/CD & Infrastructure as Code",      "tag": "DevOps",   "tasks": ["GitHub Actions for data pipelines", "Terraform basics (S3 bucket, IAM roles)"]},
        {"day": 62, "topic": "Practice Day",                        "tag": "Practice", "tasks": ["Write a CI/CD yaml to run dbt/pytest", "Deploy dummy Airflow DAG"]},
        {"day": 63, "topic": "Rest / Review",                       "tag": "Rest",     "tasks": ["Review DevOps concepts"]},
    ]},
    {"week": 10, "month": 3, "theme": "Senior System Design Concepts", "days": [
        {"day": 64, "topic": "Scalability Patterns",                "tag": "Design",   "tasks": ["Vertical vs Horizontal scaling", "Load balancing", "Caching strategies (Redis/Memcached)"]},
        {"day": 65, "topic": "Distributed Systems",                 "tag": "Design",   "tasks": ["CAP Theorem", "PACELC Theorem", "Consistency models (Eventual vs Strong)"]},
        {"day": 66, "topic": "Fault Tolerance",                     "tag": "Design",   "tasks": ["Retries with Exponential Backoff", "Dead Letter Queues (DLQ)", "Circuit Breakers"]},
        {"day": 67, "topic": "Cost Optimization",                   "tag": "Design",   "tasks": ["Spot instances", "Lifecycle rules (S3)", "Serverless vs Provisioned compute"]},
        {"day": 68, "topic": "Security & Networking",               "tag": "Design",   "tasks": ["VPCs, Subnets, Security Groups", "Encryption at rest vs in transit", "IAM best practices"]},
        {"day": 69, "topic": "Practice Day",                        "tag": "Practice", "tasks": ["Redesign an existing pipeline at work for 10x scale", "Document trade-offs"]},
        {"day": 70, "topic": "Rest",                                "tag": "Rest",     "tasks": ["Rest your brain!"]},
    ]},
    {"week": 11, "month": 3, "theme": "Mid-Level Behavioral Prep", "days": [
        {"day": 71, "topic": "Impact & Leadership",                 "tag": "Behavioral","tasks": ["Write 3 STAR stories showing technical leadership", "Focus on 'I' not 'We'"]},
        {"day": 72, "topic": "Conflict & Failure",                  "tag": "Behavioral","tasks": ["Write a story about a pipeline failure", "How did you fix it? What was the post-mortem?"]},
        {"day": 73, "topic": "System Architecture deep dive",       "tag": "Behavioral","tasks": ["Prepare to whiteboard your current company's architecture", "Know every component's purpose"]},
        {"day": 74, "topic": "Resume Polish (2 YOE)",               "tag": "Resume",    "tasks": ["Remove beginner projects", "Focus on scale, cost-savings, and business impact"]},
        {"day": 75, "topic": "LinkedIn Strategy",                   "tag": "Resume",    "tasks": ["Update headline", "Turn on 'Open to Work' for recruiters", "Connect with Senior DEs"]},
        {"day": 76, "topic": "Practice Day",                        "tag": "Practice",  "tasks": ["Record yourself answering behavioral questions", "Review pacing and clarity"]},
        {"day": 77, "topic": "Rest",                                "tag": "Rest",      "tasks": ["Rest and reflect"]},
    ]},
    {"week": 12, "month": 3, "theme": "Full Mocks & Apply", "days": [
        {"day": 78, "topic": "Full System Design Mock",             "tag": "Mock",      "tasks": ["Design a Data Platform from scratch", "Cover ingestion, storage, processing, serving"]},
        {"day": 79, "topic": "Full SQL/Python Mock",                "tag": "Mock",      "tasks": ["45-min hard problems", "Focus on edge cases and clean code"]},
        {"day": 80, "topic": "Full Behavioral Mock",                "tag": "Mock",      "tasks": ["Practice with a peer if possible", "Focus on confidence and impact"]},
        {"day": 81, "topic": "Start Applying (Targeted)",           "tag": "Action",    "tasks": ["Apply to 5 high-priority roles", "Tailor resume for each"]},
        {"day": 82, "topic": "Apply + Reach Out",                   "tag": "Action",    "tasks": ["Message 3 recruiters directly on LinkedIn", "Apply to 5 more roles"]},
        {"day": 83, "topic": "Review Weaknesses",                   "tag": "Review",    "tasks": ["Review notes from mocks", "Read 1 engineering blog (Uber/Netflix/Airbnb)"]},
        {"day": 84, "topic": "Month 3 Complete 🎉",                 "tag": "Rest",      "tasks": ["Celebrate! You are ready for interviews."]},
    ]},

    # MONTH 4
    {"week": 13, "month": 4, "theme": "Interviewing & Iterating", "days": [
        {"day": 85, "topic": "Daily Applications",                  "tag": "Action",    "tasks": ["Apply to 5 roles", "Follow up on previous week's apps"]},
        {"day": 86, "topic": "Company-Specific Prep",               "tag": "Research",  "tasks": ["Research engineering blogs of companies you're interviewing with"]},
        {"day": 87, "topic": "Mock Interview",                      "tag": "Mock",      "tasks": ["Do 1 technical mock", "Focus on speed and communication"]},
        {"day": 88, "topic": "Referrals & Networking",              "tag": "Networking","tasks": ["Ask former colleagues/managers for referrals", "Attend virtual DE meetup"]},
        {"day": 89, "topic": "Deep Work on Weakness",               "tag": "Review",    "tasks": ["Spend 2 hours on your weakest topic", "Build a tiny PoC if needed"]},
        {"day": 90, "topic": "Practice Day",                        "tag": "Practice",  "tasks": ["Solve 5 medium/hard SQL problems to stay sharp"]},
        {"day": 91, "topic": "Rest",                                "tag": "Rest",      "tasks": ["Rest to avoid burnout"]},
    ]},
    {"week": 14, "month": 4, "theme": "The Final Stretch", "days": [
        {"day": 92, "topic": "Pipeline Management",                 "tag": "Action",    "tasks": ["Track application statuses", "Send thank-you notes post-interview"]},
        {"day": 93, "topic": "System Design Refresh",               "tag": "Review",    "tasks": ["Review your own architecture diagrams", "Practice explaining them in 2 minutes"]},
        {"day": 94, "topic": "Post-Interview Reviews",              "tag": "Review",    "tasks": ["Write down questions you were asked", "Research the ones you missed"]},
        {"day": 95, "topic": "Keep Applying",                       "tag": "Action",    "tasks": ["Maintain momentum until you sign an offer"]},
        {"day": 96, "topic": "Offer Negotiation",                   "tag": "Negotiation","tasks": ["Review Levels.fyi for current market rate", "Prepare your script for HR calls"]},
        {"day": 97, "topic": "Final Mock",                          "tag": "Mock",      "tasks": ["One last behavioral/technical review", "Stay confident"]},
        {"day": 98, "topic": "Done! 🎉",                            "tag": "Rest",      "tasks": ["You've put in the work.", "Go secure that mid/senior DE offer!"]},
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
    "Kafka":      "#0284C7",
    "DevOps":     "#4338CA",
    "Behavioral": "#86198F",
    "Research":   "#166534",
    "Resume":     "#78350F",
    "Action":     "#9F1239",
    "Networking": "#5B21B6",
    "Negotiation":"#14532D",
}

MONTH_TITLES = {
    1: "📘 Month 1 — Advanced SQL & Python Pipelines",
    2: "📙 Month 2 — Big Data, Streaming & Lakes",
    3: "📗 Month 3 — Orchestration, CI/CD & Design",
    4: "📕 Month 4 — Interviews & Negotiation",
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
    st.markdown("## 🚀 DE Interview Prep (2 YOE)")
    
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

    st.divider()

    total = 98
    done  = len(st.session_state.completed)
    pct   = int(done / total * 100) if total else 0
    st.progress(pct / 100)
    st.caption(f"**{done}/{total} days complete ({pct}%)**")

    st.divider()
    page = st.radio("Navigation", ["📚 98-Day Tracker", "📅 My Schedule & Calendar"])

    st.divider()
    if page == "📚 98-Day Tracker":
        selected_month = st.radio("Jump to month", [1, 2, 3, 4], format_func=lambda m: MONTH_TITLES[m])

# ── MAIN TABS ─────────────────────────────────────────────────────────────────
if "just_completed" in st.session_state:
    dn_completed = st.session_state.just_completed
    st.toast(f"🎉 Awesome work! Day {dn_completed} is in the books.")
    if dn_completed % 7 == 0:
        st.balloons()
    del st.session_state.just_completed

if "db_error" in st.session_state:
    st.error(f"Supabase Database Error: {st.session_state.db_error}")
    st.info("Tip: If you're getting a 401/403 or empty results, make sure your Supabase table 'progress' exists and has Row Level Security (RLS) disabled, or has appropriate policies set up!")
    del st.session_state.db_error

if "just_added_event" in st.session_state:
    st.toast("🎉 Custom Event added to Calendar!")
    del st.session_state.just_added_event

if "just_deleted_event" in st.session_state:
    st.toast("🗑️ Custom Event deleted!")
    del st.session_state.just_deleted_event

# ── PAGE 1: 98-DAY TRACKER ──
if page == "📚 98-Day Tracker":
    st.title(MONTH_TITLES[selected_month])

    # ANALYTICS DASHBOARD
    st.header("📊 Your Progress Dashboard")

    total_days = 98
    completed_count = len(st.session_state.completed)
    completion_pct = int((completed_count / total_days) * 100) if total_days else 0

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
                current_note = st.session_state.notes.get(dn, "")
                new_note = st.text_area("📝 Personal Notes / Links", value=current_note, key=f"note_{dn}", placeholder="Paste LeetCode links or personal notes here...")
                if st.button("Save Note 💾", key=f"save_note_{dn}"):
                    st.session_state.notes[dn] = new_note
                    save_progress(dn, is_done)
                    st.toast(f"Notes saved for Day {dn}!")

        st.divider()

# ── PAGE 2: SCHEDULE & CALENDAR ──
if page == "📅 My Schedule & Calendar":
    st.title("📅 My Study Schedule")
    st.markdown("Structure your week for maximum consistency. Edit the routines below to fit your real life!")
    
    if "routine_weekday_v2" not in st.session_state:
        st.session_state.routine_weekday_v2 = pd.DataFrame([
            {"Time": "07:00 - 09:00", "Activity": "Morning Study 🧠"},
            {"Time": "09:30 - 19:30", "Activity": "Office 🏢"},
            {"Time": "19:30 - 21:00", "Activity": "Cooking & Resting 🍳"},
            {"Time": "21:00 - 22:30", "Activity": "Evening Review 📚"}
        ])
    if "routine_weekend" not in st.session_state:
        st.session_state.routine_weekend = pd.DataFrame([
            {"Time": "08:00 - 12:00", "Activity": "Deep Study Block 1 🧠"},
            {"Time": "12:00 - 14:00", "Activity": "Lunch / Break 🥪"},
            {"Time": "14:00 - 16:00", "Activity": "Mock Interview / Review 🗣️"},
            {"Time": "16:00 - 22:00", "Activity": "Free Time & Rest 🎉"}
        ])
        
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💼 Weekday Routine")
        st.session_state.routine_weekday_v2 = st.data_editor(st.session_state.routine_weekday_v2, num_rows="dynamic", hide_index=True, key="wd_editor_v2")
    with col2:
        st.subheader("🏖️ Weekend Routine")
        st.session_state.routine_weekend = st.data_editor(st.session_state.routine_weekend, num_rows="dynamic", hide_index=True, key="we_editor")
        
    st.divider()
    st.subheader("🗓️ Calendar View")
    
    if not HAS_CALENDAR:
        st.warning("⚠️ The interactive calendar plugin is not installed. To see the beautiful full calendar view, please run this command in your terminal:\n\n`pip install streamlit-calendar`\n\nThen refresh this page!")
    else:
        # Load custom events from Supabase early so we can delete them
        db_events = load_custom_events()

        c1, c2 = st.columns(2)
        with c1:
            with st.expander("➕ Add Custom Calendar Block"):
                with st.form("add_event_form"):
                    e_title = st.text_input("Event Title", placeholder="e.g. Mock Interview with friend")
                    ec1, ec2, ec3 = st.columns(3)
                    e_date = ec1.date_input("Date")
                    e_start = ec2.time_input("Start Time", value=datetime.strptime("14:00", "%H:%M").time())
                    e_end = ec3.time_input("End Time", value=datetime.strptime("15:00", "%H:%M").time())
                    e_color = st.color_picker("Event Color", "#7E22CE")
                    submitted = st.form_submit_button("Add to Calendar")
                    
                    if submitted and e_title:
                        # Combine date and time to ISO strings
                        start_iso = datetime.combine(e_date, e_start).isoformat()
                        end_iso = datetime.combine(e_date, e_end).isoformat()
                        save_custom_event(e_title, start_iso, end_iso, e_color)
                        st.session_state.just_added_event = True
                        st.rerun()

        with c2:
            with st.expander("🗑️ Delete Calendar Block"):
                with st.form("delete_event_form"):
                    if not db_events:
                        st.info("No custom events to delete.")
                        st.form_submit_button("Delete Event", disabled=True)
                    else:
                        ev_options = {ev["id"]: f"{ev['title']} ({str(ev['start_time'])[:10]})" for ev in db_events}
                        selected_id = st.selectbox("Select Event to Delete", options=list(ev_options.keys()), format_func=lambda x: ev_options[x])
                        del_submitted = st.form_submit_button("Delete Event")
                        
                        if del_submitted and selected_id:
                            delete_custom_event(selected_id)
                            st.session_state.just_deleted_event = True
                            st.rerun()

        # Generate dummy events based on routines
        calendar_events = []
        today = datetime.now().date()
        for i in range(-3, 10):
            target_date = today + timedelta(days=i)
            is_weekend = target_date.weekday() >= 5
            if is_weekend:
                calendar_events.append({
                    "title": "Deep Study Block 1",
                    "start": f"{target_date}T08:00:00",
                    "end": f"{target_date}T12:00:00",
                    "color": "#1D4ED8"
                })
                calendar_events.append({
                    "title": "Mock / Review",
                    "start": f"{target_date}T14:00:00",
                    "end": f"{target_date}T16:00:00",
                    "color": "#7E22CE"
                })
            else:
                calendar_events.append({
                    "title": "Morning Study",
                    "start": f"{target_date}T07:00:00",
                    "end": f"{target_date}T09:00:00",
                    "color": "#15803D"
                })
                calendar_events.append({
                    "title": "Office",
                    "start": f"{target_date}T09:30:00",
                    "end": f"{target_date}T19:30:00",
                    "color": "#4B5563"
                })
                calendar_events.append({
                    "title": "Cooking & Resting",
                    "start": f"{target_date}T19:30:00",
                    "end": f"{target_date}T21:00:00",
                    "color": "#D97706"
                })
                calendar_events.append({
                    "title": "Evening Review",
                    "start": f"{target_date}T21:00:00",
                    "end": f"{target_date}T22:30:00",
                    "color": "#15803D"
                })

        # Add custom events from Supabase
        for ev in db_events:
            calendar_events.append({
                "title": ev.get("title"),
                "start": ev.get("start_time"),
                "end": ev.get("end_time"),
                "color": ev.get("color", "#7E22CE")
            })
        
        calendar_options = {
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "timeGridWeek,timeGridDay,dayGridMonth",
            },
            "initialView": "timeGridWeek",
            "height": 650,
        }
        
        st.caption(f"Loaded {len(calendar_events)} events into the calendar engine...")
        try:
            cal_result = calendar(events=calendar_events, options=calendar_options, key="main_calendar")
        except Exception as e:
            st.error(f"Calendar component crashed: {e}")
