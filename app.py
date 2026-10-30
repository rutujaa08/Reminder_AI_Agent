import streamlit as st
from datetime import datetime, date, time, timedelta
import json, os, uuid

st.set_page_config(page_title="RemindMe AI | Smart Reminder Agent", page_icon="🔔", layout="wide")

DATA_FILE = "reminders.json"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.stApp {background:linear-gradient(135deg,#f5f7ff 0%,#fbfcff 55%,#f0fdfa 100%);}
.block-container {max-width:1250px;padding-top:1.5rem;padding-bottom:2.5rem;}
[data-testid="stSidebar"] {background:#172554;}
[data-testid="stSidebar"] * {color:#f8fafc;}
.hero {background:linear-gradient(120deg,#172554,#4338ca 58%,#0f766e);color:white;padding:2rem 2.2rem;border-radius:24px;margin-bottom:1.2rem;box-shadow:0 14px 35px rgba(30,41,99,.16);}
.hero h1 {font-family:Manrope,sans-serif;color:white;font-size:2.3rem;margin:0 0 .45rem;}
.hero p {font-size:1.02rem;opacity:.93;margin:0;max-width:800px;}
.pill {display:inline-block;background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.25);border-radius:999px;padding:.35rem .75rem;font-size:.8rem;margin-bottom:.85rem;}
.card {background:white;border:1px solid #e5eaf4;border-radius:18px;padding:1.1rem 1.2rem;box-shadow:0 5px 18px rgba(20,35,90,.04);margin:.3rem 0 .8rem;}
.metric {background:white;border:1px solid #e5eaf4;border-radius:18px;padding:1rem 1.1rem;min-height:115px;}
.label {color:#64748b;font-size:.84rem;font-weight:600;}
.value {font-family:Manrope,sans-serif;color:#172554;font-size:1.7rem;font-weight:800;margin:.2rem 0;}
.note {color:#64748b;font-size:.8rem;}
.section {font-family:Manrope,sans-serif;color:#172554;font-size:1.35rem;font-weight:800;margin:.7rem 0 .25rem;}
div.stButton>button {border-radius:12px;font-weight:700;min-height:2.65rem;}
div[data-testid="stFormSubmitButton"] button {border-radius:12px;font-weight:700;min-height:2.65rem;}
</style>
""", unsafe_allow_html=True)

def load_reminders():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_reminders(items):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

if "reminders" not in st.session_state:
    st.session_state.reminders = load_reminders()
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "notice" not in st.session_state:
    st.session_state.notice = ""

def hero(title, subtitle, tag="YOUR PERSONAL REMINDER AGENT"):
    st.markdown(f'<div class="hero"><div class="pill">{tag}</div><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)

def metric(label, value, note):
    st.markdown(f'<div class="metric"><div class="label">{label}</div><div class="value">{value}</div><div class="note">{note}</div></div>', unsafe_allow_html=True)

def parse_quick(text):
    """Simple natural-language helper for common reminder phrases."""
    t = text.lower().strip()
    title = text.strip()
    due_date = date.today()
    due_time = time(18, 0)
    if "tomorrow" in t:
        due_date = date.today() + timedelta(days=1)
        title = title.replace("tomorrow", "").replace("Tomorrow", "").strip()
    elif "today" in t:
        title = title.replace("today", "").replace("Today", "").strip()
    if "morning" in t:
        due_time = time(9, 0)
        title = title.replace("morning", "").replace("Morning", "").strip()
    elif "afternoon" in t:
        due_time = time(14, 0)
        title = title.replace("afternoon", "").replace("Afternoon", "").strip()
    elif "evening" in t:
        due_time = time(18, 0)
        title = title.replace("evening", "").replace("Evening", "").strip()
    elif "night" in t:
        due_time = time(21, 0)
        title = title.replace("night", "").replace("Night", "").strip()
    return (title or text.strip()), due_date, due_time

with st.sidebar:
    st.markdown("## 🔔 RemindMe AI")
    st.caption("One agent to organize your day.")
    st.markdown("---")
    nav = ["Dashboard", "Add Reminder", "My Reminders", "Smart Quick Add", "Insights", "About"]
    current_index = nav.index(st.session_state.page) if st.session_state.page in nav else 0
    selected = st.radio("NAVIGATION", nav, index=current_index)
    st.session_state.page = selected
    st.markdown("---")
    if st.button("＋ Create reminder", use_container_width=True):
        st.session_state.page = "Add Reminder"
        st.rerun()
    if st.button("↻ Refresh dashboard", use_container_width=True):
        st.rerun()
    st.markdown("---")
    st.caption("Local demo · No account required")

items = st.session_state.reminders
today = date.today()
now = datetime.now()
active = [r for r in items if not r.get("done", False)]
completed = [r for r in items if r.get("done", False)]
due_today = [r for r in active if r.get("date") == today.isoformat()]
overdue = []
for r in active:
    try:
        if datetime.fromisoformat(r["date"] + "T" + r["time"]) < now:
            overdue.append(r)
    except Exception:
        pass

if st.session_state.notice:
    st.success(st.session_state.notice)
    st.session_state.notice = ""

if st.session_state.page == "Dashboard":
    hero("Your day, under control.", "A friendly single-agent reminder system to capture tasks, organize deadlines, and keep your next steps visible.")
    a,b,c,d = st.columns(4)
    with a: metric("ACTIVE REMINDERS", len(active), "Tasks still to do")
    with b: metric("DUE TODAY", len(due_today), "Scheduled for today")
    with c: metric("OVERDUE", len(overdue), "Past due time")
    with d: metric("COMPLETED", len(completed), "Tasks checked off")
    st.markdown('<div class="section">✨ Quick actions</div>', unsafe_allow_html=True)
    x,y,z = st.columns(3)
    with x:
        st.markdown('<div class="card"><h3>➕ Add a reminder</h3><p>Create a reminder with date, time, category and priority.</p></div>', unsafe_allow_html=True)
        if st.button("Add new →", key="dash_add", use_container_width=True):
            st.session_state.page="Add Reminder"; st.rerun()
    with y:
        st.markdown('<div class="card"><h3>⚡ Quick add</h3><p>Type something like “Submit assignment tomorrow morning”.</p></div>', unsafe_allow_html=True)
        if st.button("Quick add →", key="dash_quick", use_container_width=True):
            st.session_state.page="Smart Quick Add"; st.rerun()
    with z:
        st.markdown('<div class="card"><h3>📋 View tasks</h3><p>Mark completed tasks, filter by category, or remove old reminders.</p></div>', unsafe_allow_html=True)
        if st.button("View reminders →", key="dash_view", use_container_width=True):
            st.session_state.page="My Reminders"; st.rerun()
    st.markdown('<div class="section">📌 Upcoming reminders</div>', unsafe_allow_html=True)
    upcoming = sorted(active, key=lambda r:(r.get("date",""),r.get("time","")))[:5]
    if upcoming:
        for r in upcoming:
            status = "⚠️ Overdue" if r in overdue else ("📅 Today" if r.get("date")==today.isoformat() else "🗓️ Upcoming")
            st.markdown(f'<div class="card"><b>{status} · {r["title"]}</b><br><span style="color:#64748b">{r.get("date","")} at {r.get("time","")} · {r.get("category","Personal")} · {r.get("priority","Medium")} priority</span></div>', unsafe_allow_html=True)
    else:
        st.info("No reminders yet. Create your first one to get started.")
    st.caption("Note: this demo saves reminders locally. It does not send push notifications or SMS while the app is closed.")

elif st.session_state.page == "Add Reminder":
    hero("Create a reminder", "Capture what matters and choose when it should be done.", "PLAN AHEAD")
    with st.form("add_reminder_form", clear_on_submit=True):
        title = st.text_input("Reminder title *", placeholder="e.g., Submit AI assignment")
        details = st.text_area("Notes (optional)", placeholder="Add a little detail…", height=90)
        col1,col2 = st.columns(2)
        with col1:
            due = st.date_input("Date", value=date.today())
            category = st.selectbox("Category", ["Personal","College","Work","Health","Shopping","Other"])
        with col2:
            due_t = st.time_input("Time", value=time(18,0), step=300)
            priority = st.select_slider("Priority", options=["Low","Medium","High"], value="Medium")
        submitted = st.form_submit_button("🔔 Save reminder", type="primary", use_container_width=True)
    if submitted:
        if not title.strip():
            st.error("Please enter a reminder title.")
        else:
            new = {"id":uuid.uuid4().hex[:8],"title":title.strip(),"details":details.strip(),
                   "date":due.isoformat(),"time":due_t.strftime("%H:%M"),"category":category,
                   "priority":priority,"done":False,"created":datetime.now().isoformat(timespec="seconds")}
            st.session_state.reminders.append(new)
            save_reminders(st.session_state.reminders)
            st.session_state.notice = "Reminder saved successfully!"
            st.rerun()

elif st.session_state.page == "My Reminders":
    hero("My reminders", "Search, filter, complete, and manage all your tasks in one place.")
    search = st.text_input("🔎 Search reminders", placeholder="Search by title or notes…")
    f1,f2 = st.columns(2)
    with f1: status_filter = st.selectbox("Status", ["All","Active","Completed"])
    with f2: cat_filter = st.selectbox("Category", ["All","Personal","College","Work","Health","Shopping","Other"])
    filtered = items[:]
    if search:
        filtered = [r for r in filtered if search.lower() in (r.get("title","")+" "+r.get("details","")).lower()]
    if status_filter == "Active": filtered = [r for r in filtered if not r.get("done")]
    if status_filter == "Completed": filtered = [r for r in filtered if r.get("done")]
    if cat_filter != "All": filtered = [r for r in filtered if r.get("category")==cat_filter]
    filtered.sort(key=lambda r:(r.get("date",""),r.get("time","")))
    if not filtered:
        st.info("No reminders match those filters.")
    for r in filtered:
        with st.container(border=True):
            left,right = st.columns([5,1])
            with left:
                st.markdown(f"### {'✅ ' if r.get('done') else '🔔 '}{r['title']}")
                st.caption(f"{r.get('date','')} · {r.get('time','')} · {r.get('category','Personal')} · {r.get('priority','Medium')} priority")
                if r.get("details"): st.write(r["details"])
                if r.get("done"): st.success("Completed")
            with right:
                if not r.get("done"):
                    if st.button("Mark done", key=f"done_{r['id']}", use_container_width=True):
                        r["done"] = True; save_reminders(items); st.rerun()
                else:
                    if st.button("Reopen", key=f"reopen_{r['id']}", use_container_width=True):
                        r["done"] = False; save_reminders(items); st.rerun()
                if st.button("Delete", key=f"del_{r['id']}", use_container_width=True):
                    st.session_state.reminders = [q for q in items if q["id"] != r["id"]]
                    save_reminders(st.session_state.reminders); st.rerun()
    if items:
        st.download_button("⬇️ Export all reminders (JSON)", data=json.dumps(items, indent=2, ensure_ascii=False),
                           file_name="my_reminders.json", mime="application/json")

elif st.session_state.page == "Smart Quick Add":
    hero("Smart Quick Add", "Write a reminder naturally. The helper suggests a title, date and time that you can review before saving.", "QUICK CAPTURE")
    st.info('Example: "Submit assignment tomorrow morning" or "Call the dentist this evening". This demo understands a few common time words; it is not full natural-language AI.')
    phrase = st.text_input("What do you need to remember?", placeholder="e.g., Finish project tomorrow evening")
    if st.button("✨ Understand my reminder", type="primary"):
        if not phrase.strip():
            st.error("Type a reminder first.")
        else:
            suggested_title, suggested_date, suggested_time = parse_quick(phrase)
            st.session_state.quick_suggestion = {"title":suggested_title,"date":suggested_date,"time":suggested_time}
    if st.session_state.get("quick_suggestion"):
        q = st.session_state.quick_suggestion
        st.markdown('<div class="section">Review suggestion</div>', unsafe_allow_html=True)
        with st.form("quick_save"):
            qtitle = st.text_input("Reminder title", value=q["title"])
            qdate = st.date_input("Suggested date", value=q["date"])
            qtime = st.time_input("Suggested time", value=q["time"], step=300)
            qcat = st.selectbox("Category", ["Personal","College","Work","Health","Shopping","Other"])
            qpriority = st.select_slider("Priority", options=["Low","Medium","High"], value="Medium")
            qsave = st.form_submit_button("Save this reminder", type="primary", use_container_width=True)
        if qsave:
            if qtitle.strip():
                st.session_state.reminders.append({"id":uuid.uuid4().hex[:8],"title":qtitle.strip(),"details":f"Created from: {phrase}",
                    "date":qdate.isoformat(),"time":qtime.strftime("%H:%M"),"category":qcat,"priority":qpriority,
                    "done":False,"created":datetime.now().isoformat(timespec="seconds")})
                save_reminders(st.session_state.reminders)
                st.session_state.quick_suggestion = None
                st.session_state.notice = "Quick reminder saved!"
                st.rerun()
            else: st.error("Please add a title.")

elif st.session_state.page == "Insights":
    hero("Your productivity insights", "A simple overview of how your reminders are organized.")
    total = len(items)
    c1,c2,c3 = st.columns(3)
    with c1: metric("TOTAL TASKS", total, "All saved reminders")
    with c2: metric("COMPLETION RATE", f"{round(len(completed)/total*100) if total else 0}%", "Completed reminders")
    with c3: metric("HIGH PRIORITY", sum(1 for r in active if r.get("priority")=="High"), "Still active")
    st.markdown('<div class="section">Tasks by category</div>', unsafe_allow_html=True)
    if items:
        cats = ["Personal","College","Work","Health","Shopping","Other"]
        counts = {c:sum(1 for r in items if r.get("category")==c) for c in cats}
        st.bar_chart(counts)
        st.markdown('<div class="section">A small suggestion</div>', unsafe_allow_html=True)
        if overdue:
            st.warning(f"You have {len(overdue)} overdue reminder(s). Review them and update their date if needed.")
        elif active:
            st.success("You are all caught up on overdue tasks. Keep adding one clear next step at a time.")
        else:
            st.info("Add a reminder to start tracking your progress.")
    else:
        st.info("Insights will appear after you add reminders.")

else:
    hero("About RemindMe AI", "Reminder System — a single-agent productivity assistant with a clear, accessible interface.", "PROJECT OVERVIEW")
    st.markdown("""
    <div class="card"><h3>🎯 Project aim</h3>Help users record tasks, manage deadlines, and keep a clear view of what needs attention.</div>
    <div class="card"><h3>🤖 Single-agent design</h3>The same agent supports quick reminder interpretation, scheduling suggestions, task organization, and simple productivity insights.</div>
    <div class="card"><h3>🧰 Technology</h3>Python · Streamlit · JSON local storage · Date/time utilities</div>
    <div class="card"><h3>🔔 Important limitation</h3>This version saves reminders locally and shows them when you open the app. It does not send real push notifications, SMS, or email and it does not run while the app is closed.</div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align:center;color:#64748b;font-size:.82rem'>RemindMe AI · Smart Reminder Agent · Demo project</p>", unsafe_allow_html=True)
