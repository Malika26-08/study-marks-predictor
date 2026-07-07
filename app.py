import json
import os
from datetime import datetime, date, timedelta

import io
import base64
import numpy as np
import pandas as pd
import plotly.express as px
from PIL import Image, ImageDraw, ImageFont
import streamlit as st
from sklearn.linear_model import LinearRegression

SCHEDULE_FILE = "schedule.json"

MOTIVATIONAL_QUOTES = [
    "Consistency creates confidence. Stick to your schedule and results will follow.",
    "Small daily progress adds up to big outcomes. Every study session counts.",
    "A focused hour today is a stronger tomorrow. Keep your goals in sight.",
    "Study smart, not just hard. Use plans, pace, and rest for best results.",
]

STUDY_TIPS = [
    "Break study sessions into 25-45 minute focus blocks.",
    "Review your notes before bed to improve memory retention.",
    "Mix practice tests with revision for stronger preparation.",
    "Set one small learning goal before each study session.",
]


def normalize_task_list(tasks):
    normalized = []
    for task in tasks:
        if not isinstance(task, dict):
            continue
        task_id = task.get("task_id") or task.get("created_at") or datetime.now().strftime("%Y%m%d%H%M%S%f")
        task_id = str(task_id).replace(":", "-").replace(".", "-")
        task["task_id"] = task_id
        task.setdefault("done", False)
        normalized.append(task)
    return normalized


def load_schedule_data():
    if not os.path.exists(SCHEDULE_FILE):
        return {"schedule": [], "history": []}

    try:
        with open(SCHEDULE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        return {"schedule": [], "history": []}

    if isinstance(data, list):
        data = {"schedule": data, "history": []}
    if not isinstance(data, dict):
        return {"schedule": [], "history": []}

    return {
        "schedule": normalize_task_list(data.get("schedule", [])),
        "history": normalize_task_list(data.get("history", [])),
    }


def save_schedule_data(data):
    with open(SCHEDULE_FILE, "w", encoding="utf-8") as file:
        json.dump({"schedule": data.get("schedule", []), "history": data.get("history", [])}, file, indent=2, ensure_ascii=False)


def build_training_data():
    return pd.DataFrame(
        {
            "study_hours": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            "activity_score": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5, 5],
            "sleep_hours": [5, 6, 6, 7, 7, 8, 8, 8, 9, 9, 9, 10],
            "marks": [33, 40, 48, 55, 61, 70, 74, 80, 86, 91, 93, 95],
        }
    )


def train_model():
    data = build_training_data()
    features = data[["study_hours", "activity_score", "sleep_hours"]]
    target = data["marks"]
    model = LinearRegression()
    model.fit(features, target)
    return model


def make_prediction(model, study_hours, activity_score, sleep_hours):
    # Prediction depends only on study hours and intensity.
    return compute_marks_from_study_and_intensity(study_hours, activity_score)


def compute_marks_from_study_and_intensity(study_hours, activity_score):
    """Compute predicted marks using only study hours and study activity intensity."""
    h = float(study_hours or 0.0)
    intensity = float(activity_score or 3.0)
    intensity = max(1.0, min(5.0, intensity))

    if h <= 1.0:
        base = 10.0 + h * 15.0
    elif h <= 3.0:
        base = 25.0 + (h - 1.0) / 2.0 * 20.0
    elif h <= 6.0:
        base = 45.0 + (h - 3.0) / 3.0 * 25.0
    elif h <= 9.0:
        base = 70.0 + (h - 6.0) / 3.0 * 18.0
    else:
        base = 88.0 + min((h - 9.0) * 1.5, 10.0)

    intensity_factor = 1.0 + (intensity - 3.0) * 0.06
    marks = base * intensity_factor
    return round(float(max(0.0, min(100.0, marks))), 1)


def get_prediction_feedback(study_hours, activity_score):
    study = float(study_hours or 0.0)
    intensity = float(activity_score or 3.0)
    feedback = []
    if study >= 8 and intensity >= 4:
        feedback.extend(["Excellent study effort detected.", "Your study consistency is strong."])
    elif study >= 5 and intensity >= 3:
        feedback.extend(["Good study momentum - keep the intensity high.", "Increasing activity intensity may improve performance."])
    elif study < 4 and intensity >= 4:
        feedback.append("Strong intensity, but add more study hours for better results.")
    elif study < 4 and intensity < 4:
        feedback.append("Your predicted marks are low; increase study hours and intensity.")
    else:
        feedback.append("You are on the right track - focus on maintaining study hours.")
    return feedback


def calculate_streak(history):
    if not history:
        return 0

    dates = sorted({task["task_date"] for task in history}, reverse=True)
    streak = 0
    today = date.today()
    for offset in range(len(dates)):
        expected = today - timedelta(days=offset)
        if expected.strftime("%Y-%m-%d") in dates:
            streak += 1
        else:
            break
    return streak


def build_daily_progress(schedule_data):
    today = date.today().strftime("%Y-%m-%d")
    todays_tasks = [task for task in schedule_data["schedule"] if task["task_date"] == today]
    completed_today = [task for task in schedule_data["history"] if task["task_date"] == today]
    total = len(todays_tasks) + len(completed_today)
    return int(min(100, (len(completed_today) / total) * 100)) if total else 0


def get_ai_suggestions(predicted_marks):
    if predicted_marks >= 90:
        return [
            "You're on a high-performance track - keep reviewing the hardest topics.",
            "Stay consistent and maintain your rest schedule for peak recall.",
        ]
    if predicted_marks >= 75:
        return [
            "Your structure is strong. Add a few practice tests to improve confidence.",
            "Use active recall and spaced repetition for best retention.",
        ]
    return [
        "Focus on the top 2 weak topics before your next study session.",
        "Increase study intensity a little and take short breaks every 30 minutes.",
    ]


def apply_theme_css():
    st.markdown(
        """
        <style>
        :root { --accent: rgb(158,235,71); --bg:#0b0d12; --card: rgba(10,12,18,0.6); --text: #ffffff; }
        body, .stApp, .block-container { background: var(--bg); color: var(--text); }
        .stSidebar { background: rgba(6,8,12,0.95) !important; color: var(--text); }
        .sidebar .sidebar-content { color: var(--text); }
        .block-container { padding: 1.5rem 2rem 2rem 2rem; }
        .glass-card { background: var(--card); border: 1px solid rgba(158,235,71,0.14); border-radius: 18px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); padding: 1.25rem; margin-bottom: 1rem; }
        .hero-card { background: linear-gradient(180deg, rgba(20,22,26,0.8), rgba(8,9,10,0.95)); border: 1px solid rgba(158,235,71,0.12); border-radius: 18px; padding: 1.5rem; margin-bottom: 1rem; }
        .hero-title { font-size: 2.25rem; font-weight: 800; color: var(--text); }
        .hero-subtitle { color: rgba(255,255,255,0.85); font-size: 0.98rem; }
        .card-heading { color: var(--accent); font-size: 1.05rem; margin-bottom: 0.5rem; font-weight:700; }
        .progress-shell { background: rgba(255,255,255,0.04); border-radius: 999px; overflow: hidden; height: 14px; margin: 0.6rem 0; }
        .progress-fill { background: linear-gradient(90deg, rgba(158,235,71,0.95) 0%, rgba(100,200,50,0.9) 100%); height: 100%; border-radius: 999px; }
        .result-card { padding: 1rem; background: rgba(8,10,12,0.6); border: 1px solid rgba(158,235,71,0.12); border-radius: 14px; animation: pulseGlow 5s ease-in-out infinite alternate; }
        .result-score { font-size: 2rem; font-weight: 800; color: var(--text); margin: 0.4rem 0; }
        .badge { display: inline-block; padding: 0.25rem 0.6rem; border-radius: 999px; background: rgba(158,235,71,0.12); color: var(--text); font-size: 0.85rem; }
        @keyframes pulseGlow { from { box-shadow: 0 0 12px rgba(158,235,71,0.08); } to { box-shadow: 0 0 28px rgba(158,235,71,0.2); } }
        .stButton>button { transition: transform 0.12s ease, box-shadow 0.12s ease; background: linear-gradient(90deg, rgba(158,235,71,0.95), rgba(120,200,40,0.9)); color: #000; }
        .stButton>button:hover { transform: translateY(-1px); box-shadow: 0 6px 18px rgba(158,235,71,0.12); }
        .dashboard-metric { background: rgba(6,8,12,0.6); border: 1px solid rgba(158,235,71,0.08); border-radius: 12px; padding: 0.9rem; color: var(--text); }
        .task-card { background: rgba(6,8,12,0.5); border: 1px solid rgba(158,235,71,0.06); border-radius: 12px; padding: 0.9rem; margin-bottom: 0.8rem; }
        .task-label { font-weight: 700; color: var(--text); margin-bottom: 0.25rem; }
        .task-meta { color: rgba(255,255,255,0.8); font-size: 0.92rem; }
        .quote { font-style: normal; color: var(--text); font-weight: 700; }
        .value-chip { color: var(--text); font-weight: 700; }
        .stDownloadButton>button { background: linear-gradient(90deg, rgba(158,235,71,0.95), rgba(100,200,40,0.9)); color: #000; border: none; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def complete_task(task_id):
    schedule_data = st.session_state["schedule_data"]
    for index, task in enumerate(schedule_data["schedule"]):
        if task["task_id"] == task_id:
            finished = schedule_data["schedule"].pop(index)
            finished["done"] = True
            finished["completed_at"] = datetime.now().isoformat(timespec="minutes")
            schedule_data["history"].append(finished)
            save_schedule_data(schedule_data)
            state_key = f"done_{task_id}"
            if state_key in st.session_state:
                del st.session_state[state_key]
            st.session_state["message"] = f"Completed and archived: {finished['task_name']}"
            return


def delete_history_task(task_id):
    schedule_data = st.session_state["schedule_data"]
    schedule_data["history"] = [task for task in schedule_data["history"] if task["task_id"] != task_id]
    save_schedule_data(schedule_data)
    st.session_state["message"] = "Completed task deleted from history."
    return


def delete_schedule_task(task_id):
    schedule_data = st.session_state["schedule_data"]
    schedule_data["schedule"] = [task for task in schedule_data["schedule"] if task["task_id"] != task_id]
    save_schedule_data(schedule_data)
    st.session_state["message"] = "Task removed from your schedule."
    return


def add_schedule_task(task_name, task_date, task_time, priority):
    new_task = {
        "task_id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "task_name": task_name.strip(),
        "task_date": task_date.strftime("%Y-%m-%d"),
        "task_time": task_time.strftime("%H:%M"),
        "priority": priority,
        "done": False,
        "created_at": datetime.now().isoformat(timespec="minutes"),
    }
    st.session_state["schedule_data"]["schedule"].append(new_task)
    save_schedule_data(st.session_state["schedule_data"])
    st.session_state["message"] = f"Added task: {task_name}."


def render_prediction_result(predicted_marks, confidence):
    sentiment = (
        "Excellent performance ahead!"
        if predicted_marks >= 85
        else "Good progress - keep refining your study plan."
        if predicted_marks >= 70
        else "You can improve with sharper focus and practice."
    )
    st.markdown(
        f"""
        <div class='result-card'>
            <div class='badge'>AI Prediction</div>
            <div class='result-score'>{predicted_marks} / 100</div>
            <div>{sentiment}</div>
            <div class='progress-shell'><div class='progress-fill' style='width: {confidence}%;'></div></div>
            <div style='display:flex; justify-content: space-between; color:#b9c4ff; margin-top:0.4rem;'>
                <span>Confidence</span>
                <span>{confidence}%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_report(schedule_data, predicted_marks, confidence, study_hours, activity_score, sleep_hours):
    rows = []
    for task in schedule_data["history"]:
        rows.append(
            {
                "Task": task["task_name"],
                "Date": task["task_date"],
                "Time": task["task_time"],
                "Priority": task["priority"],
                "Completed At": task.get("completed_at", ""),
                "Predicted Marks": predicted_marks,
                "Confidence": confidence,
                "Study Hours": study_hours,
                "Activity Score": activity_score,
                "Sleep Hours": sleep_hours,
            }
        )
    report_df = pd.DataFrame(rows)
    return report_df.to_csv(index=False).encode("utf-8")


def build_image_report(schedule_data, predicted_marks, confidence, study_hours, activity_score, sleep_hours, theme="dark"):
    width, height = 1200, 800
    # Theme-aware color selection
    if theme == "light":
        bg_hex = "#ffffff"
        panel_fill = (245, 245, 245)
        text_color = (20, 20, 20)
        accent = (30, 120, 20)
        grey = (100, 100, 100)
    else:
        bg_hex = "#0b0d12"
        panel_fill = (18, 26, 34)
        text_color = (255, 255, 255)
        accent = (158, 235, 71)
        grey = (190, 190, 190)

    background = Image.new("RGB", (width, height), bg_hex)
    draw = ImageDraw.Draw(background)

    try:
        title_font = ImageFont.truetype("arial.ttf", 52)
        subtitle_font = ImageFont.truetype("arial.ttf", 28)
        body_font = ImageFont.truetype("arial.ttf", 24)
        small_font = ImageFont.truetype("arial.ttf", 20)
    except OSError:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Header
    draw.rectangle([(40, 40), (width - 40, 180)], fill=panel_fill)
    draw.text((60, 60), "Study Progress Summary", font=title_font, fill=accent)
    draw.text((60, 130), "AI-powered result snapshot with clear insights.", font=subtitle_font, fill=grey)

    # Core metrics
    draw.rectangle([(40, 200), (width - 40, 380)], fill=panel_fill)
    draw.text((60, 220), f"Predicted Marks: {predicted_marks} / 100", font=title_font, fill=text_color)
    draw.text((60, 290), f"Confidence: {confidence}%", font=subtitle_font, fill=accent)
    draw.text((60, 335), f"Study Hours: {study_hours}  |  Activity: {activity_score}  |  Sleep: {sleep_hours}", font=body_font, fill=grey)

    # Takeaway
    draw.rectangle([(40, 410), (width - 40, 520)], fill=panel_fill)
    draw.text((60, 430), "Key takeaway:", font=subtitle_font, fill=accent)
    takeaway = "Stay consistent and refine your study plan for stronger marks."
    draw.text((60, 470), takeaway, font=body_font, fill=text_color)

    # History
    draw.rectangle([(40, 540), (width - 40, height - 40)], fill=panel_fill)
    draw.text((60, 560), "Latest completed tasks:", font=subtitle_font, fill=accent)

    history_items = schedule_data.get("history", [])[-6:]
    y = 600
    if not history_items:
        draw.text((60, y), "No completed tasks yet.", font=body_font, fill=grey)
    else:
        for task in history_items:
            line = f"- {task.get('task_date','')} {task.get('task_time','')} - {task.get('task_name','')} ({task.get('priority','')})"
            draw.text((60, y), line, font=small_font, fill=text_color)
            y += 32

    image_bytes = io.BytesIO()
    background.save(image_bytes, format="PNG")
    image_bytes.seek(0)
    return image_bytes.getvalue()


def detect_streamlit_theme_base():
    # Attempt to detect Streamlit's configured theme base (light/dark).
    try:
        base = st.get_option("theme.base")
        if base:
            return base
    except Exception:
        pass
    try:
        theme = st.get_option("theme")
        if isinstance(theme, dict):
            return theme.get("base", "dark")
        if isinstance(theme, str):
            return theme
    except Exception:
        pass
    return "dark"


def parse_and_validate_day_hours(study_input, sleep_input, rest_input):
    """Parse and validate study, sleep and rest inputs.

    Returns a dict with keys:
      study, sleep, rest (floats or None),
      errors (dict of field->message),
      total (float or None), remaining (float or None), valid (bool)
    """
    result = {
        "study": None,
        "sleep": None,
        "rest": None,
        "errors": {},
        "total": None,
        "remaining": None,
        "valid": True,
    }

    # helper to parse a float field
    def _parse_field(val, name, max_value=24.0, allow_empty=False):
        if val is None or str(val).strip() == "":
            return None, f"Please enter {name} hours." if not allow_empty else (None, None)
        try:
            v = float(val)
            if v < 0:
                return None, f"{name.capitalize()} cannot be negative."
            if v > max_value:
                return None, f"{name.capitalize()} seems unrealistic (>{max_value})."
            return v, None
        except Exception:
            return None, f"Enter a valid number for {name} hours."

    study_v, study_err = _parse_field(study_input, "study")
    sleep_v, sleep_err = _parse_field(sleep_input, "sleep")
    rest_v, rest_err = _parse_field(rest_input, "rest/other")

    if study_err:
        result["errors"]["study"] = study_err
    if sleep_err:
        result["errors"]["sleep"] = sleep_err
    if rest_err:
        result["errors"]["rest"] = rest_err

    result["study"] = study_v
    result["sleep"] = sleep_v
    result["rest"] = rest_v

    # If any individual parsing error, mark invalid
    if study_err or sleep_err or rest_err:
        result["valid"] = False
        return result

    # compute total and remaining
    total = (study_v or 0.0) + (sleep_v or 0.0) + (rest_v or 0.0)
    result["total"] = total
    remaining = 24.0 - total
    result["remaining"] = remaining

    if total > 24.0:
        result["errors"]["total"] = "Total daily hours cannot exceed 24 hours."
        result["valid"] = False

    return result


def initialize_schedule_state():
    if "schedule_data" not in st.session_state:
        st.session_state["schedule_data"] = load_schedule_data()
    if "message" not in st.session_state:
        st.session_state["message"] = ""
    if "prediction" not in st.session_state:
        st.session_state["prediction"] = {"marks": None, "confidence": 0, "study_hours": 0, "activity_score": 3, "sleep_hours": 7}


def main():
    st.set_page_config(page_title="AI Study Planner Dashboard", page_icon="?", layout="wide", initial_sidebar_state="expanded")
    apply_theme_css()
    initialize_schedule_state()
    model = train_model()

    page = st.sidebar.radio("Navigation", ["Dashboard", "Schedule", "Insights"])
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Startup AI Study Assistant")
    st.sidebar.markdown("Use this dashboard to predict your marks, manage study tasks, track streaks, and visualize performance.")
    st.sidebar.markdown("---")
    st.sidebar.markdown("#### Quick tips")
    for tip in STUDY_TIPS:
        st.sidebar.markdown(f"- {tip}")

    st.markdown(
        "<div class='hero-card'><div class='hero-title'>Study Time vs Marks</div>"
        "<div class='hero-subtitle'>Modern study planner with predictions, task tracking, charts, and goal tracking.</div></div>",
        unsafe_allow_html=True,
    )

    schedule_data = st.session_state["schedule_data"]
    streak = calculate_streak(schedule_data["history"])
    daily_progress = build_daily_progress(schedule_data)

    top_col1, top_col2, top_col3 = st.columns(3)
    top_col1.markdown(
        f"<div class='dashboard-metric'><div class='card-heading'>Study Streak</div><div class='value-chip'>{streak} days</div></div>",
        unsafe_allow_html=True,
    )
    top_col2.markdown(
        f"<div class='dashboard-metric'><div class='card-heading'>Daily Goal</div><div class='value-chip'>{daily_progress}%</div></div>",
        unsafe_allow_html=True,
    )
    tasks_today = [
        task for task in schedule_data["schedule"] if task["task_date"] == date.today().strftime("%Y-%m-%d")
    ]
    completed_today = [
        task for task in schedule_data["history"] if task["task_date"] == date.today().strftime("%Y-%m-%d")
    ]
    top_col3.markdown(
        f"<div class='dashboard-metric'><div class='card-heading'>Today's Tasks</div><div class='value-chip'>{len(tasks_today) + len(completed_today)}</div></div>",
        unsafe_allow_html=True,
    )

    if page == "Dashboard":
        pred_col, stat_col = st.columns([2, 1])
        with pred_col:
            st.markdown("<div class='glass-card'><div class='card-heading'>Predict Your Marks</div></div>", unsafe_allow_html=True)
            study_hours_input = st.text_input("Study hours per day", placeholder="e.g. 3.5", value="3.0")
            activity_score_input = st.text_input("Study activity intensity (1-5)", placeholder="e.g. 3", value="3")
            sleep_hours_input = st.text_input("Sleep hours per day", placeholder="e.g. 7", value="7.0")
            rest_hours_input = st.text_input("Rest/Other activity hours per day", placeholder="e.g. 3", value="2.0")

            # Validate all three hour inputs using the reusable helper
            validation = parse_and_validate_day_hours(study_hours_input, sleep_hours_input, rest_hours_input)
            input_error = not validation.get("valid", False)

            # Assign parsed values to local vars for later use
            study_hours = validation.get("study")
            sleep_hours = validation.get("sleep")
            rest_hours = validation.get("rest")

            # Parse activity score input into a safe numeric value (1-5)
            try:
                activity_score = int(float(activity_score_input))
                if activity_score < 1:
                    activity_score = 1
                if activity_score > 5:
                    activity_score = 5
            except Exception:
                activity_score = 3

            # Display total and remaining hours helper UI
            total_disp = validation.get("total")
            remaining_disp = validation.get("remaining")
            if total_disp is not None:
                used = round(total_disp, 2)
                rem = round(remaining_disp, 2) if remaining_disp is not None else None
                st.markdown(f"**Total Hours Used:** {used} / 24")
                st.markdown(f"**Remaining Hours:** {rem}")

            # Show errors if present
            if "total" in validation.get("errors", {}):
                st.markdown(
                    """
                    <style>
                    input[placeholder="e.g. 3.5"], input[placeholder="e.g. 7"], input[placeholder="e.g. 3"] { border-color: #ff4d4f !important; box-shadow: 0 0 0 6px rgba(255,77,79,0.06) !important; transition: box-shadow .18s ease, border-color .18s ease; }
                    .validation-fade { animation: fadeIn .28s ease both; }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )
                st.error(validation["errors"]["total"], icon="??")
            else:
                # show per-field parse errors
                errs = validation.get("errors", {})
                if errs.get("study"):
                    st.error(errs.get("study"))
                if errs.get("sleep"):
                    st.error(errs.get("sleep"))
                if errs.get("rest"):
                    st.error(errs.get("rest"))

            extra_focus = st.checkbox("Include extra practice and revision boost", value=True)
            if extra_focus:
                st.caption("Extra focus applied: +0.5 hour effective study time")

            # Disable the predict button when validation fails
            if input_error:
                st.button("Run Prediction", key="run_prediction_disabled", disabled=True)
            else:
                if st.button("Run Prediction", key="run_prediction"):
                    effective_hours = study_hours + (0.5 if extra_focus else 0)
                    predicted_marks = make_prediction(model, effective_hours, activity_score, None)
                    # Confidence depends on study hours and intensity.
                    conf_calc = 30 + min(65, (effective_hours / 12.0) * 45 + (activity_score - 1) / 4.0 * 35)
                    confidence = int(max(20, min(95, round(conf_calc))))
                    st.session_state["prediction"] = {
                        "marks": predicted_marks,
                        "confidence": confidence,
                        "study_hours": effective_hours,
                        "activity_score": activity_score,
                        "sleep_hours": sleep_hours,
                    }

            if st.session_state["prediction"]["marks"] is not None:
                render_prediction_result(
                    st.session_state["prediction"]["marks"],
                    st.session_state["prediction"]["confidence"],
                )
                feedback_messages = get_prediction_feedback(
                    st.session_state["prediction"]["study_hours"],
                    st.session_state["prediction"]["activity_score"],
                )
                for message in feedback_messages:
                    st.write(f"- {message}")
                suggestions = get_ai_suggestions(st.session_state["prediction"]["marks"])
                st.markdown("<div class='glass-card'><div class='card-heading'>Study Advice</div></div>", unsafe_allow_html=True)
                for suggestion in suggestions:
                    st.write(f"- {suggestion}")
                st.markdown("**Download your study result image**")
                theme_base = detect_streamlit_theme_base()
                report_image_bytes = build_image_report(
                    schedule_data,
                    st.session_state["prediction"]["marks"],
                    st.session_state["prediction"]["confidence"],
                    study_hours,
                    activity_score,
                    sleep_hours,
                    theme=theme_base,
                )
                # Render responsive preview using a data URI to avoid use_column_width deprecation
                b64 = base64.b64encode(report_image_bytes).decode()
                img_html = f'<img src="data:image/png;base64,{b64}" style="max-width:100%;height:auto;border-radius:8px;box-shadow:0 8px 24px rgba(0,0,0,0.35);"/>'
                st.markdown(img_html, unsafe_allow_html=True)
                st.download_button(
                    "Download result image",
                    data=report_image_bytes,
                    file_name="study_progress_report.png",
                    mime="image/png",
                )

        with stat_col:
            st.markdown("<div class='glass-card'><div class='card-heading'>Performance Summary</div></div>", unsafe_allow_html=True)
            st.metric("Current streak", f"{streak} days")
            st.metric("Task progress", f"{daily_progress}%")
            st.write("---")
            st.markdown("**study tip**")
            st.write(np.random.choice(STUDY_TIPS))

        if st.session_state["prediction"]["marks"] is not None:
            chart_data = pd.DataFrame(
                {
                    "Study Hours": np.linspace(0, 12, 13),
                    "Predicted Marks": [
                        compute_marks_from_study_and_intensity(hours, st.session_state["prediction"]["activity_score"])
                        for hours in np.linspace(0, 12, 13)
                    ],
                }
            )
            intensity_data = pd.DataFrame(
                {
                    "Activity Intensity": np.arange(1, 6),
                    "Predicted Marks": [
                        compute_marks_from_study_and_intensity(st.session_state["prediction"]["study_hours"], intensity)
                        for intensity in np.arange(1, 6)
                    ],
                }
            )
            chart_left, chart_right = st.columns(2)
            fig_hours = px.line(
                chart_data,
                x="Study Hours",
                y="Predicted Marks",
                markers=True,
                title="Study Hours vs Predicted Marks",
                template="plotly_dark",
                color_discrete_sequence=["#8f8dff"],
            )
            fig_intensity = px.line(
                intensity_data,
                x="Activity Intensity",
                y="Predicted Marks",
                markers=True,
                title="Intensity vs Predicted Marks",
                template="plotly_dark",
                color_discrete_sequence=["#63d2ff"],
            )
            chart_left.plotly_chart(fig_hours, use_container_width=True)
            chart_right.plotly_chart(fig_intensity, use_container_width=True)

            # Plain bold motivational quote (no boxed card)
            st.markdown(f"**{np.random.choice(MOTIVATIONAL_QUOTES)}**")

    if page in ["Schedule", "Dashboard"]:
        st.markdown("<div class='glass-card'><div class='card-heading'>Study Timetable</div></div>", unsafe_allow_html=True)
        task_col, list_col = st.columns([2, 1])
        with task_col:
            with st.form("schedule_form", clear_on_submit=True):
                st.subheader("Add New Study Task")
                task_name = st.text_input("Task name", placeholder="e.g. Physics revision")
                task_date = st.date_input("Date", value=date.today())
                task_time = st.time_input("Time")
                priority = st.selectbox("Priority", ["High", "Medium", "Low"])
                add_task = st.form_submit_button("Add task")
                if add_task:
                    if task_name.strip() == "":
                        st.error("Please enter a task name.")
                    else:
                        add_schedule_task(task_name, task_date, task_time, priority)
                        st.success("Task added to your schedule.")

            st.markdown("### Active Tasks")
            if not schedule_data["schedule"]:
                st.info("No active tasks yet. Add one to begin your timetable.")
            for task in schedule_data["schedule"]:
                with st.container():
                    st.markdown(
                        f"<div class='task-card'><div class='task-label'>{task['task_name']}</div>"
                        f"<div class='task-meta'>Date: {task['task_date']} - Time: {task['task_time']} - Priority: {task['priority']}</div></div>",
                        unsafe_allow_html=True,
                    )
                    complete_col, delete_col = st.columns([3, 1])
                    if complete_col.checkbox("Mark as completed", key=f"done_{task['task_id']}"):
                        complete_task(task["task_id"])
                    if delete_col.button("Remove", key=f"remove_{task['task_id']}"):
                        delete_schedule_task(task["task_id"])

        with list_col:
            st.markdown("### Completed History")
            if not schedule_data["history"]:
                st.info("No completed tasks yet. Complete a task to move it here.")
            for task in schedule_data["history"]:
                st.markdown(
                    f"<div class='task-card'><div class='task-label'>{task['task_name']}</div>"
                    f"<div class='task-meta'>Completed: {task.get('completed_at', task['task_date'])} - Priority: {task['priority']}</div></div>",
                    unsafe_allow_html=True,
                )
                if st.button("Delete", key=f"delete_{task['task_id']}"):
                    delete_history_task(task["task_id"])

    if page == "Insights":
        st.markdown("<div class='glass-card'><div class='card-heading'>Insight Charts</div></div>", unsafe_allow_html=True)
        if st.session_state["prediction"]["marks"] is not None:
            fig_trend = px.bar(
                pd.DataFrame(
                    {
                        "Metric": ["Predicted Marks", "Confidence", "Goal Progress"],
                        "Value": [
                            st.session_state["prediction"]["marks"],
                            st.session_state["prediction"]["confidence"],
                            daily_progress,
                        ],
                    }
                ),
                x="Metric",
                y="Value",
                color="Metric",
                template="plotly_dark",
                color_discrete_map={
                    "Predicted Marks": "#7c5cff",
                    "Confidence": "#3bc5ff",
                    "Goal Progress": "#8cd4ff",
                },
            )
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("Run a prediction from the Dashboard first to unlock insight charts.")

    if st.session_state["message"]:
        st.sidebar.success(st.session_state["message"])


if __name__ == "__main__":
    main()
