import { useState } from "react";

const plan = [
  // MONTH 1 — SQL + Python
  {
    week: 1, month: 1, theme: "SQL — Intermediate to Advanced",
    days: [
      { day: 1, topic: "SQL Recap — JOINs deep dive", tasks: ["INNER, LEFT, RIGHT, FULL OUTER joins", "Practice 10 JOIN problems on LeetCode"], tag: "SQL" },
      { day: 2, topic: "Window Functions Part 1", tasks: ["ROW_NUMBER, RANK, DENSE_RANK", "PARTITION BY + ORDER BY logic", "Solve 5 problems"], tag: "SQL" },
      { day: 3, topic: "Window Functions Part 2", tasks: ["LAG, LEAD, FIRST_VALUE, LAST_VALUE", "Running totals, moving averages", "Solve 5 problems"], tag: "SQL" },
      { day: 4, topic: "Aggregations & Grouping", tasks: ["GROUP BY, HAVING, ROLLUP, CUBE", "Nested aggregations", "Solve 5 problems"], tag: "SQL" },
      { day: 5, topic: "Subqueries & CTEs", tasks: ["Correlated subqueries", "WITH clause (CTEs)", "Refactor subqueries into CTEs"], tag: "SQL" },
      { day: 6, topic: "Practice Day", tasks: ["Solve 10 mixed SQL problems", "Focus on problems you got wrong this week"], tag: "Practice" },
      { day: 7, topic: "Rest / Light Review", tasks: ["Review notes from Week 1", "Watch 1 YouTube video on SQL optimization"], tag: "Rest" },
    ]
  },
  {
    week: 2, month: 1, theme: "SQL — Query Optimization + Python Basics",
    days: [
      { day: 8, topic: "Query Optimization", tasks: ["Indexes — what, why, when", "EXPLAIN / EXPLAIN ANALYZE", "Avoid SELECT *"], tag: "SQL" },
      { day: 9, topic: "Advanced SQL Patterns", tasks: ["Pivot tables in SQL", "Gap and island problems", "Solve 5 tricky problems"], tag: "SQL" },
      { day: 10, topic: "Python — Data Structures", tasks: ["Lists, dicts, sets, tuples", "List comprehensions", "Write 10 small functions"], tag: "Python" },
      { day: 11, topic: "Python — Functions & OOP Basics", tasks: ["*args, **kwargs", "Classes and objects basics", "Write a simple data class"], tag: "Python" },
      { day: 12, topic: "Python — File I/O & Error Handling", tasks: ["Read/write CSV, JSON", "Try/except patterns", "Practice with real datasets"], tag: "Python" },
      { day: 13, topic: "Practice Day", tasks: ["5 SQL + 5 Python problems", "Mix of easy/medium difficulty"], tag: "Practice" },
      { day: 14, topic: "Rest / Light Review", tasks: ["Review weak areas", "Plan next week"], tag: "Rest" },
    ]
  },
  {
    week: 3, month: 1, theme: "Python — Pandas & Pipeline Thinking",
    days: [
      { day: 15, topic: "Pandas Part 1", tasks: ["DataFrames, Series", "read_csv, head, describe, info", "Filtering and selecting"], tag: "Python" },
      { day: 16, topic: "Pandas Part 2", tasks: ["groupby, merge, join", "apply, map, lambda", "Handle missing values"], tag: "Python" },
      { day: 17, topic: "Pandas Part 3", tasks: ["Pivot tables in Pandas", "Time series basics", "Solve 5 Pandas exercises"], tag: "Python" },
      { day: 18, topic: "Writing Clean Pipelines", tasks: ["Modular functions for ETL", "Logging basics", "Write a mini ETL script"], tag: "Python" },
      { day: 19, topic: "Python + SQL Together", tasks: ["Connect Python to DB (sqlite3 / sqlalchemy)", "Run queries from Python", "Build a simple pipeline"], tag: "Python" },
      { day: 20, topic: "Practice Day", tasks: ["Build end-to-end mini pipeline", "CSV → transform → output"], tag: "Practice" },
      { day: 21, topic: "Rest / Light Review", tasks: ["Review Python notes", "Skim one DE blog post"], tag: "Rest" },
    ]
  },
  {
    week: 4, month: 1, theme: "SQL Mock + Python Review",
    days: [
      { day: 22, topic: "SQL Mock Interview", tasks: ["Simulate 45-min SQL round", "Use StrataScratch or LeetCode"], tag: "Mock" },
      { day: 23, topic: "Review SQL Mistakes", tasks: ["Fix every wrong answer from mock", "Re-solve with explanation"], tag: "SQL" },
      { day: 24, topic: "Python Mock Interview", tasks: ["Simulate coding round", "Focus on pandas + functions"], tag: "Mock" },
      { day: 25, topic: "Review Python Mistakes", tasks: ["Fix every wrong answer", "Re-write clean versions"], tag: "Python" },
      { day: 26, topic: "Month 1 Recap", tasks: ["List top 10 things you learned", "Note what still feels weak"], tag: "Review" },
      { day: 27, topic: "Practice Day", tasks: ["10 mixed problems — SQL + Python", "Time yourself"], tag: "Practice" },
      { day: 28, topic: "Rest", tasks: ["Full rest or light reading", "Don't study — recharge!"], tag: "Rest" },
    ]
  },

  // MONTH 2 — System Design + Data Modeling
  {
    week: 5, month: 2, theme: "Data Modeling Fundamentals",
    days: [
      { day: 29, topic: "Star Schema & Snowflake Schema", tasks: ["Fact vs Dimension tables", "When to use which", "Design a sample schema"], tag: "Modeling" },
      { day: 30, topic: "Normalization", tasks: ["1NF, 2NF, 3NF explained", "When to denormalize", "Practice normalization exercises"], tag: "Modeling" },
      { day: 31, topic: "Slowly Changing Dimensions (SCD)", tasks: ["SCD Type 1, 2, 3", "When to use each", "Implement SCD Type 2 example"], tag: "Modeling" },
      { day: 32, topic: "Data Vault Basics", tasks: ["Hubs, Links, Satellites", "Compare vs Star Schema", "Read 1 article on Data Vault"], tag: "Modeling" },
      { day: 33, topic: "Modeling Practice", tasks: ["Design schema for e-commerce", "Design schema for ride-sharing app"], tag: "Practice" },
      { day: 34, topic: "Practice Day", tasks: ["Review and refine your schemas", "Get feedback on design choices"], tag: "Practice" },
      { day: 35, topic: "Rest / Light Review", tasks: ["Review week notes", "Sketch one more schema"], tag: "Rest" },
    ]
  },
  {
    week: 6, month: 2, theme: "Pipeline System Design",
    days: [
      { day: 36, topic: "Batch vs Streaming", tasks: ["When to use each", "Lambda architecture", "Kappa architecture"], tag: "Design" },
      { day: 37, topic: "ETL vs ELT", tasks: ["Differences and trade-offs", "Modern data stack (dbt)", "Design an ELT pipeline"], tag: "Design" },
      { day: 38, topic: "Data Warehouses", tasks: ["Redshift vs BigQuery vs Snowflake", "Partitioning and clustering", "Read comparison article"], tag: "Design" },
      { day: 39, topic: "Data Lakes & Lakehouses", tasks: ["S3 / GCS as data lake", "Delta Lake / Iceberg basics", "When lake vs warehouse"], tag: "Design" },
      { day: 40, topic: "Orchestration Tools", tasks: ["Airflow — DAGs, operators, sensors", "Understand scheduling basics", "Draw a pipeline with Airflow"], tag: "Design" },
      { day: 41, topic: "System Design Practice", tasks: ["Design a ride-sharing data pipeline", "Think: ingestion → storage → serving"], tag: "Practice" },
      { day: 42, topic: "Rest / Light Review", tasks: ["Review week notes", "Watch 1 system design video"], tag: "Rest" },
    ]
  },
  {
    week: 7, month: 2, theme: "Spark + Cloud Basics",
    days: [
      { day: 43, topic: "Spark Fundamentals", tasks: ["RDD vs DataFrame vs Dataset", "Transformations vs Actions", "Read Spark architecture overview"], tag: "Spark" },
      { day: 44, topic: "PySpark Basics", tasks: ["SparkSession, read/write", "select, filter, groupBy", "Write 3 PySpark scripts"], tag: "Spark" },
      { day: 45, topic: "Spark Optimization", tasks: ["Partitioning, caching, broadcast", "Avoid data skew", "Review common bottlenecks"], tag: "Spark" },
      { day: 46, topic: "Cloud — Your Primary Cloud", tasks: ["Focus on cloud you use at work", "Key services: storage, compute, orchestration", "Review managed services"], tag: "Cloud" },
      { day: 47, topic: "Cloud — Data Services Deep Dive", tasks: ["Glue / Dataflow / Data Factory", "S3 / GCS / ADLS", "Redshift / BigQuery / Synapse"], tag: "Cloud" },
      { day: 48, topic: "Practice Day", tasks: ["Design a cloud-native pipeline", "Combine Spark + Cloud services"], tag: "Practice" },
      { day: 49, topic: "Rest / Light Review", tasks: ["Review all of Month 2", "Note gaps to fill in Month 3"], tag: "Rest" },
    ]
  },
  {
    week: 8, month: 2, theme: "System Design Mock + Review",
    days: [
      { day: 50, topic: "System Design Mock 1", tasks: ["Design: real-time analytics pipeline", "45-minute timed session", "Write down your design"], tag: "Mock" },
      { day: 51, topic: "Review System Design Mock 1", tasks: ["Compare with best practices", "Fix gaps in your design"], tag: "Review" },
      { day: 52, topic: "System Design Mock 2", tasks: ["Design: data platform for fintech", "Focus on reliability + scalability"], tag: "Mock" },
      { day: 53, topic: "Review System Design Mock 2", tasks: ["Improve your design", "Practice explaining out loud"], tag: "Review" },
      { day: 54, topic: "Month 2 Recap", tasks: ["List top 10 things learned", "Identify weak spots"], tag: "Review" },
      { day: 55, topic: "Practice Day", tasks: ["Mixed practice: SQL + Design", "Timed, interview conditions"], tag: "Practice" },
      { day: 56, topic: "Rest", tasks: ["Full rest", "You're halfway there!"], tag: "Rest" },
    ]
  },

  // MONTH 3 — Mock Interviews + DSA
  {
    week: 9, month: 3, theme: "DSA Basics for DE Interviews",
    days: [
      { day: 57, topic: "Arrays & Strings", tasks: ["Two pointers", "Sliding window", "Solve 5 easy/medium problems"], tag: "DSA" },
      { day: 58, topic: "HashMaps & Sets", tasks: ["Frequency counters", "Two sum pattern", "Solve 5 problems"], tag: "DSA" },
      { day: 59, topic: "Sorting & Searching", tasks: ["Binary search", "Merge sort concept", "Solve 5 problems"], tag: "DSA" },
      { day: 60, topic: "Stack & Queue", tasks: ["Stack use cases", "Queue / deque", "Solve 5 problems"], tag: "DSA" },
      { day: 61, topic: "Recursion Basics", tasks: ["Think recursively", "Factorial, fibonacci", "Solve 3 recursion problems"], tag: "DSA" },
      { day: 62, topic: "Practice Day", tasks: ["10 DSA problems — mixed topics", "Focus on patterns not memorization"], tag: "Practice" },
      { day: 63, topic: "Rest / Light Review", tasks: ["Review DSA patterns", "Rest your brain"], tag: "Rest" },
    ]
  },
  {
    week: 10, month: 3, theme: "Full Mock Interview Week",
    days: [
      { day: 64, topic: "Mock Round 1 — SQL", tasks: ["Full 45-min SQL interview", "Record yourself if possible", "Review after"], tag: "Mock" },
      { day: 65, topic: "Mock Round 2 — Python/DSA", tasks: ["Full 45-min coding round", "Explain your thinking out loud"], tag: "Mock" },
      { day: 66, topic: "Mock Round 3 — System Design", tasks: ["Full 45-min design round", "Draw diagrams, explain trade-offs"], tag: "Mock" },
      { day: 67, topic: "Review All 3 Mocks", tasks: ["List mistakes from each round", "Prioritize top 3 things to fix"], tag: "Review" },
      { day: 68, topic: "Fix Weak Areas", tasks: ["Deep dive on biggest gaps", "Re-solve problems you got wrong"], tag: "Review" },
      { day: 69, topic: "Practice Day", tasks: ["Re-do one mock from this week", "Aim to improve on previous score"], tag: "Practice" },
      { day: 70, topic: "Rest", tasks: ["Full rest", "No screens if possible!"], tag: "Rest" },
    ]
  },
  {
    week: 11, month: 3, theme: "Behavioral + Company Research",
    days: [
      { day: 71, topic: "Behavioral Interview Prep", tasks: ["Write STAR answers for 10 questions", "Tell me about yourself — practice 3 versions"], tag: "Behavioral" },
      { day: 72, topic: "Behavioral Practice", tasks: ["Practice out loud for 30 mins", "Record and review yourself"], tag: "Behavioral" },
      { day: 73, topic: "Research Target Companies", tasks: ["List 10 companies you want to apply to", "Note their tech stack and team size"], tag: "Research" },
      { day: 74, topic: "Resume Polish", tasks: ["Quantify every bullet point", "Tailor resume for DE roles", "Get 1 person to review it"], tag: "Resume" },
      { day: 75, topic: "LinkedIn + Profile Optimization", tasks: ["Update LinkedIn headline and about", "Add projects and skills", "Connect with 5 DE professionals"], tag: "Resume" },
      { day: 76, topic: "Practice Day", tasks: ["Full mock interview from scratch", "All 3 rounds back to back"], tag: "Practice" },
      { day: 77, topic: "Rest", tasks: ["Rest and reflect on progress"], tag: "Rest" },
    ]
  },
  {
    week: 12, month: 3, theme: "Final Prep + Start Applying",
    days: [
      { day: 78, topic: "Final SQL Revision", tasks: ["Top 20 SQL questions review", "Speed drill — solve fast"], tag: "SQL" },
      { day: 79, topic: "Final Python Revision", tasks: ["Top 10 Python patterns", "Write clean pipeline from memory"], tag: "Python" },
      { day: 80, topic: "Final System Design Revision", tasks: ["Review all design patterns", "Practice explaining in 5 mins"], tag: "Design" },
      { day: 81, topic: "Start Applying", tasks: ["Apply to first 5 companies", "Track in a spreadsheet"], tag: "Action" },
      { day: 82, topic: "Apply + Practice", tasks: ["Apply to 5 more companies", "Do 1 hour of weak area review"], tag: "Action" },
      { day: 83, topic: "Apply + Mock", tasks: ["Apply to 5 more companies", "Final full mock interview"], tag: "Action" },
      { day: 84, topic: "Month 3 Complete 🎉", tasks: ["Review your full journey", "Celebrate your progress!", "Keep applying and stay consistent"], tag: "Rest" },
    ]
  },

  // MONTH 4 — Applications + Company-Specific Prep
  {
    week: 13, month: 4, theme: "Active Applications + Interview Practice",
    days: [
      { day: 85, topic: "Apply Daily Routine", tasks: ["Apply to 3-5 companies per day", "Customize cover letter lightly"], tag: "Action" },
      { day: 86, topic: "Company-Specific Prep", tasks: ["Research interview process of top 3 targets", "Check Glassdoor + Leetcode company tags"], tag: "Research" },
      { day: 87, topic: "Mock + Apply", tasks: ["1 mock interview", "Apply to 5 companies"], tag: "Action" },
      { day: 88, topic: "Referrals", tasks: ["Reach out to 5 connections for referrals", "Message ex-colleagues or LinkedIn contacts"], tag: "Networking" },
      { day: 89, topic: "Weak Area Deep Dive", tasks: ["Focus on your #1 weak topic", "Solve 10 targeted problems"], tag: "Review" },
      { day: 90, topic: "Practice Day", tasks: ["Full mock interview", "Review and improve"], tag: "Practice" },
      { day: 91, topic: "Rest", tasks: ["Rest", "Trust your preparation"], tag: "Rest" },
    ]
  },
  {
    week: 14, month: 4, theme: "Interviews Begin",
    days: [
      { day: 92, topic: "Keep Applying", tasks: ["3-5 applications", "Follow up on pending ones"], tag: "Action" },
      { day: 93, topic: "Interview Preparation", tasks: ["For each interview: research company deeply", "Prep 3 questions to ask them"], tag: "Research" },
      { day: 94, topic: "Post-Interview Review", tasks: ["After each interview: write what went well", "Write what you'd do differently"], tag: "Review" },
      { day: 95, topic: "Keep the momentum", tasks: ["Don't stop applying even if interviews are going well", "Pipeline of 3-5 active processes is healthy"], tag: "Action" },
      { day: 96, topic: "Negotiation Prep", tasks: ["Research market salaries on Levels.fyi / Glassdoor", "Prepare your number + justification"], tag: "Negotiation" },
      { day: 97, topic: "Practice Day", tasks: ["Mock interview or apply", "Stay sharp"], tag: "Practice" },
      { day: 98, topic: "Rest", tasks: ["Rest", "You're in the final stretch!"], tag: "Rest" },
    ]
  },
];

const tagColors = {
  SQL: { bg: "#EFF6FF", text: "#1D4ED8", border: "#BFDBFE" },
  Python: { bg: "#F0FDF4", text: "#15803D", border: "#BBF7D0" },
  Practice: { bg: "#FFF7ED", text: "#C2410C", border: "#FED7AA" },
  Rest: { bg: "#F9FAFB", text: "#6B7280", border: "#E5E7EB" },
  Mock: { bg: "#FDF4FF", text: "#7E22CE", border: "#E9D5FF" },
  Review: { bg: "#FFFBEB", text: "#92400E", border: "#FDE68A" },
  Modeling: { bg: "#F0F9FF", text: "#0369A1", border: "#BAE6FD" },
  Design: { bg: "#FFF1F2", text: "#BE123C", border: "#FECDD3" },
  Spark: { bg: "#FFF7ED", text: "#9A3412", border: "#FDBA74" },
  Cloud: { bg: "#F0FDFA", text: "#0F766E", border: "#99F6E4" },
  DSA: { bg: "#EEF2FF", text: "#3730A3", border: "#C7D2FE" },
  Behavioral: { bg: "#FDF2F8", text: "#86198F", border: "#F5D0FE" },
  Research: { bg: "#F0FDF4", text: "#166534", border: "#86EFAC" },
  Resume: { bg: "#FFFBEB", text: "#78350F", border: "#FCD34D" },
  Action: { bg: "#FFF1F2", text: "#9F1239", border: "#FECACA" },
  Networking: { bg: "#F5F3FF", text: "#5B21B6", border: "#DDD6FE" },
  Negotiation: { bg: "#F0FDF4", text: "#14532D", border: "#86EFAC" },
};

const monthNames = { 1: "Month 1 — SQL & Python", 2: "Month 2 — System Design & Modeling", 3: "Month 3 — Mock Interviews & DSA", 4: "Month 4 — Applications & Interviews" };
const monthColors = { 1: "#1D4ED8", 2: "#7E22CE", 3: "#0F766E", 4: "#9A3412" };

export default function StudyPlan() {
  const [selectedMonth, setSelectedMonth] = useState(1);
  const [expandedDay, setExpandedDay] = useState(null);
  const [completedDays, setCompletedDays] = useState({});

  const months = [1, 2, 3, 4];
  const currentMonthWeeks = plan.filter(w => w.month === selectedMonth);
  const totalDays = plan.reduce((acc, w) => acc + w.days.length, 0);
  const completedCount = Object.values(completedDays).filter(Boolean).length;
  const progress = Math.round((completedCount / totalDays) * 100);

  const toggleDay = (dayNum) => {
    setExpandedDay(expandedDay === dayNum ? null : dayNum);
  };

  const toggleComplete = (e, dayNum) => {
    e.stopPropagation();
    setCompletedDays(prev => ({ ...prev, [dayNum]: !prev[dayNum] }));
  };

  return (
    <div style={{ fontFamily: "'Inter', -apple-system, sans-serif", background: "#F8FAFC", minHeight: "100vh", padding: "24px 16px" }}>
      {/* Header */}
      <div style={{ maxWidth: 720, margin: "0 auto" }}>
        <div style={{ background: "linear-gradient(135deg, #1E3A5F 0%, #0F4C81 100%)", borderRadius: 16, padding: "28px 28px", marginBottom: 24, color: "white" }}>
          <div style={{ fontSize: 12, letterSpacing: 2, textTransform: "uppercase", opacity: 0.7, marginBottom: 8 }}>Data Engineering</div>
          <h1 style={{ margin: "0 0 4px", fontSize: 24, fontWeight: 700 }}>Your 4-Month Interview Plan</h1>
          <p style={{ margin: "0 0 20px", opacity: 0.8, fontSize: 14 }}>98 days · SQL → Python → System Design → Mock Interviews → Offer</p>
          
          {/* Progress */}
          <div style={{ background: "rgba(255,255,255,0.15)", borderRadius: 8, padding: "14px 16px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8, fontSize: 13 }}>
              <span>Overall Progress</span>
              <span style={{ fontWeight: 600 }}>{completedCount}/{totalDays} days ({progress}%)</span>
            </div>
            <div style={{ background: "rgba(255,255,255,0.2)", borderRadius: 99, height: 8 }}>
              <div style={{ background: "#34D399", borderRadius: 99, height: 8, width: `${progress}%`, transition: "width 0.4s ease" }} />
            </div>
          </div>
        </div>

        {/* Month Tabs */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", gap: 8, marginBottom: 24 }}>
          {months.map(m => (
            <button key={m}
              onClick={() => setSelectedMonth(m)}
              style={{
                padding: "10px 8px", borderRadius: 10, border: "2px solid",
                borderColor: selectedMonth === m ? monthColors[m] : "#E2E8F0",
                background: selectedMonth === m ? monthColors[m] : "white",
                color: selectedMonth === m ? "white" : "#64748B",
                fontWeight: 600, fontSize: 12, cursor: "pointer", transition: "all 0.2s",
                textAlign: "center", lineHeight: 1.3
              }}>
              Month {m}
            </button>
          ))}
        </div>

        {/* Month Title */}
        <div style={{ marginBottom: 16, paddingBottom: 12, borderBottom: `3px solid ${monthColors[selectedMonth]}` }}>
          <h2 style={{ margin: 0, fontSize: 18, fontWeight: 700, color: monthColors[selectedMonth] }}>
            {monthNames[selectedMonth]}
          </h2>
        </div>

        {/* Weeks */}
        {currentMonthWeeks.map(week => {
          const weekCompleted = week.days.filter(d => completedDays[d.day]).length;
          return (
            <div key={week.week} style={{ marginBottom: 20 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 10 }}>
                <div>
                  <span style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", color: "#94A3B8", letterSpacing: 1 }}>Week {week.week} · </span>
                  <span style={{ fontSize: 13, fontWeight: 600, color: "#334155" }}>{week.theme}</span>
                </div>
                <span style={{ fontSize: 12, color: "#94A3B8" }}>{weekCompleted}/{week.days.length}</span>
              </div>

              <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                {week.days.map(day => {
                  const tag = tagColors[day.tag] || tagColors.Rest;
                  const isExpanded = expandedDay === day.day;
                  const isDone = completedDays[day.day];

                  return (
                    <div key={day.day}
                      onClick={() => toggleDay(day.day)}
                      style={{
                        background: isDone ? "#F0FDF4" : "white",
                        border: `1px solid ${isDone ? "#86EFAC" : "#E2E8F0"}`,
                        borderRadius: 10, padding: "12px 14px",
                        cursor: "pointer", transition: "all 0.2s",
                        boxShadow: isExpanded ? "0 4px 12px rgba(0,0,0,0.08)" : "none"
                      }}>
                      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                        {/* Checkbox */}
                        <div onClick={(e) => toggleComplete(e, day.day)}
                          style={{
                            width: 22, height: 22, borderRadius: 6, border: `2px solid ${isDone ? "#16A34A" : "#CBD5E1"}`,
                            background: isDone ? "#16A34A" : "white", display: "flex", alignItems: "center", justifyContent: "center",
                            flexShrink: 0, cursor: "pointer", transition: "all 0.2s"
                          }}>
                          {isDone && <span style={{ color: "white", fontSize: 13, lineHeight: 1 }}>✓</span>}
                        </div>

                        {/* Day number */}
                        <span style={{ fontSize: 11, fontWeight: 700, color: "#94A3B8", minWidth: 36 }}>Day {day.day}</span>

                        {/* Topic */}
                        <span style={{ fontSize: 13, fontWeight: 600, color: isDone ? "#15803D" : "#1E293B", flex: 1, textDecoration: isDone ? "line-through" : "none", opacity: isDone ? 0.7 : 1 }}>
                          {day.topic}
                        </span>

                        {/* Tag */}
                        <span style={{
                          fontSize: 10, fontWeight: 700, padding: "2px 8px", borderRadius: 99,
                          background: tag.bg, color: tag.text, border: `1px solid ${tag.border}`,
                          flexShrink: 0, letterSpacing: 0.5
                        }}>{day.tag}</span>

                        <span style={{ color: "#94A3B8", fontSize: 12, flexShrink: 0 }}>{isExpanded ? "▲" : "▼"}</span>
                      </div>

                      {/* Expanded Tasks */}
                      {isExpanded && (
                        <div style={{ marginTop: 12, paddingTop: 12, borderTop: "1px solid #F1F5F9" }}>
                          <div style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", color: "#94A3B8", letterSpacing: 1, marginBottom: 8 }}>Today's Tasks</div>
                          {day.tasks.map((task, i) => (
                            <div key={i} style={{ display: "flex", alignItems: "flex-start", gap: 8, marginBottom: 6 }}>
                              <span style={{ color: tag.text, fontSize: 14, marginTop: 1 }}>→</span>
                              <span style={{ fontSize: 13, color: "#475569", lineHeight: 1.5 }}>{task}</span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}

        {/* Footer tip */}
        <div style={{ background: "#FFFBEB", border: "1px solid #FDE68A", borderRadius: 10, padding: "14px 16px", marginTop: 8 }}>
          <div style={{ fontSize: 12, fontWeight: 700, color: "#92400E", marginBottom: 4 }}>💡 Daily Rule</div>
          <div style={{ fontSize: 13, color: "#78350F" }}>Study 1-1.5 hours BEFORE picking up your phone in the evening. Consistency over intensity — 1 hour daily beats 7 hours on Sunday.</div>
        </div>
      </div>
    </div>
  );
}
