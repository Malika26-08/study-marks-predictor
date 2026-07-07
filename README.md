# Study Time vs Marks Prediction Dashboard

> **AI-powered study planner and marks prediction dashboard** — Predict your exam marks, manage study schedules, track daily progress, and get personalized study recommendations using machine learning.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://malika26-08-study-marks-predictor.streamlit.app)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Features

- **AI Marks Prediction** — Get real-time predicted exam marks based on study hours and activity intensity
- **Smart Schedule Management** — Create, track, and complete daily study tasks with priority levels
- **Progress Analytics** — Visualize study patterns, completion rates, and learning streaks with interactive charts
- **Daily Goal Tracking** — Monitor today's tasks, study streak, and daily progress percentage
- **Personalized Insights** — Receive AI-generated study recommendations and performance feedback
- **Export Reports** — Download study progress as CSV or visual PNG reports
- **Responsive Design** — Modern dark-mode UI with smooth animations and intuitive controls
- **Data Persistence** — All tasks and history saved locally in JSON format

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | [Streamlit](https://streamlit.io) 1.28+ |
| **ML/Prediction** | scikit-learn (LinearRegression) |
| **Data Processing** | pandas, numpy |
| **Visualization** | Plotly |
| **Image Generation** | Pillow |
| **Language** | Python 3.8+ |

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip or conda package manager

### Quick Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/study-marks-predictor.git
cd study-marks-predictor

# 2. Create a virtual environment (recommended)
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app locally
streamlit run app.py
```

The app will open at `http://localhost:8501` in your default browser.

---

## 🚀 Usage

### Dashboard Tab
1. **Enter Study Details:**
   - Study hours per day (0–24)
   - Study activity intensity (1–5, where 5 = maximum focus)
   - Sleep hours per day
   - Rest/other activity hours

2. **Run Prediction:**
   - Click "Run Prediction" to calculate expected marks (0–100)
   - View confidence score and personalized feedback
   - Read AI-generated study recommendations

### Schedule Tab
1. **Create Tasks:**
   - Task name
   - Date and time
   - Priority level (High/Medium/Low)

2. **Track Progress:**
   - Check off completed tasks
   - View task history
   - See daily goal progress

### Insights Tab
- Study streaks and consistency metrics
- Interactive charts showing study patterns
- Performance analytics based on logged tasks
- Export reports as CSV or PNG

---

## 📊 How Predictions Work

The prediction model uses **study hours** and **activity intensity** to estimate exam marks:

```
Base Score = Piecewise function based on study hours
- ≤1 hour → 10–25 marks
- 1–3 hours → 25–45 marks
- 3–6 hours → 45–70 marks
- 6–9 hours → 70–88 marks
- >9 hours → 88–100 marks

Intensity Multiplier = 1.0 + (intensity - 3.0) × 0.06
(Higher intensity increases marks by up to 12%)

Final Mark = Base × Multiplier (clamped to 0–100)
```

**Note:** Sleep hours and other activities are tracked for wellness insights but do not directly affect mark predictions.

---

## 📂 Project Structure

```
study-marks-predictor/
├── app.py                 # Main Streamlit application
├── schedule.json          # Local data store (auto-created)
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── LICENSE                # MIT License
└── .gitignore             # Git ignore rules
```

---

## 🌐 Deployment

### Deploy to Streamlit Cloud (Recommended)

**🎉 Your app is now LIVE!**

**Live App:** https://malika26-08-study-marks-predictor.streamlit.app

**GitHub Repository:** https://github.com/Malika26-08/study-marks-predictor

**See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide**, including:
- Setting up a GitHub repository
- Pushing code to GitHub
- Deploying to Streamlit Cloud
- Troubleshooting common issues
- Portfolio integration

### Deploy to Other Platforms

- **Docker:** See `DEPLOYMENT.md` for Dockerfile setup
- **Cloud Run / Heroku:** See deployment docs for setup instructions
- **Self-hosted:** Run locally on any server with Python 3.8+

---

## 🔧 Configuration

### Environment Variables
No API keys or secrets required. The app runs entirely offline with local JSON storage.

### Customizing Predictions
Edit the `compute_marks_from_study_and_intensity()` function in `app.py` to adjust the prediction algorithm.

### Modifying Themes
CSS styling is defined in `apply_theme_css()` — adjust colors, fonts, and animations there.

---

## 📈 Screenshots

| Feature | Preview |
|---------|---------|
| **Dashboard** | Main prediction and tracking interface |
| **Schedule** | Daily task management view |
| **Insights** | Performance charts and analytics |

*Screenshots will be added to this section.*

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "Add your feature"`
4. Push to branch: `git push origin feature/your-feature`
5. Submit a Pull Request

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Port 8501 already in use** | `streamlit run app.py --server.port 8502` |
| **Module not found errors** | Run `pip install -r requirements.txt` again |
| **Data not persisting** | Ensure `schedule.json` is writable in the app directory |
| **Slow performance** | Close other browser tabs; increase Streamlit cache timeout |

---

## 📝 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) file for details.

You are free to use, modify, and distribute this project with proper attribution.

---

## ✅ Deployed & Live!

**Live Application:** https://malika26-08-study-marks-predictor.streamlit.app

**GitHub Repository:** https://github.com/Malika26-08/study-marks-predictor

**For deployment details:** See [DEPLOYMENT.md](DEPLOYMENT.md) and [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md)

---

## 💡 Future Enhancements

- [ ] User authentication and cloud data sync
- [ ] Support for multiple subjects/exams
- [ ] Advanced ML model with cross-validation
- [ ] Mobile app (React Native)
- [ ] Integration with calendar apps (Google Calendar, Notion)
- [ ] Email notifications for study reminders
- [ ] Dark/light theme toggle
- [ ] Collaborative study groups

---

## 📞 Support & Contact

- **Issues:** Open a GitHub issue for bugs or feature requests
- **Email:** your-email@example.com
- **Twitter:** [@yourhandle](https://twitter.com)

---

## 🏆 Made with ❤️

Built for students, by students. Optimize your study time and ace your exams! 🚀

**Star ⭐ this repo if you find it helpful!**
