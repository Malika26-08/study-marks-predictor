# 📚 Study Time vs Marks Prediction Dashboard

> **Machine Learning–powered study planner and marks prediction dashboard** built with Streamlit. Predict exam marks, manage study schedules, track daily progress, and receive personalized study recommendations through an interactive dashboard.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://malika26-08-study-marks-predictor.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

---

## 🌐 Live Demo

🚀 **Live Application**  
https://malika26-08-study-marks-predictor.streamlit.app

💻 **GitHub Repository**  
https://github.com/Malika26-08/study-marks-predictor

---

## ✨ Project Highlights

- 📈 Predict exam marks based on study habits
- 📅 Manage daily study schedules
- 📊 Visualize study progress with interactive analytics
- 🎯 Track goals and maintain study streaks
- 🤖 Receive personalized study recommendations
- 📁 Export reports in CSV and PNG formats
- 💾 Local JSON-based data storage
- 🌙 Modern responsive Streamlit interface

---

## 🎯 Features

- **Marks Prediction** – Estimate expected exam marks using study hours and activity intensity
- **Smart Schedule Management** – Create, organize, and complete daily study tasks
- **Progress Analytics** – Interactive charts showing study consistency and completion rates
- **Daily Goal Tracking** – Monitor study streaks, completed tasks, and daily progress
- **Personalized Recommendations** – Receive intelligent study suggestions based on your activity
- **Export Reports** – Download progress reports in CSV or PNG format
- **Responsive UI** – Modern dark-themed dashboard built with Streamlit
- **Local Data Storage** – Automatically saves tasks and study history using JSON

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Prediction Engine | Python |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly |
| Image Processing | Pillow |
| Data Storage | JSON |
| Language | Python 3.8+ |

---

## 📦 Installation

### Prerequisites

- Python 3.8+
- pip

### Clone the Repository

```bash
git clone https://github.com/Malika26-08/study-marks-predictor.git
cd study-marks-predictor
```

### Create Virtual Environment (Optional)

```bash
python -m venv venv
```

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app.py
```

The application will open at:

```
http://localhost:8501
```

---

## 🚀 Usage

### Dashboard

- Enter study hours
- Select study intensity
- Enter sleep hours
- Enter rest/activity hours
- Click **Run Prediction**
- View predicted marks and personalized recommendations

### Schedule

- Add study tasks
- Set priorities
- Mark tasks as completed
- Track daily goals

### Insights

- Study streak analysis
- Progress charts
- Completion statistics
- Export reports

---

## 📊 Prediction Logic

The application estimates marks using a custom rule-based prediction algorithm based on:

- Study hours
- Study intensity

Prediction flow:

```
Study Hours
      │
      ▼
 Base Score
      │
      ▼
Intensity Adjustment
      │
      ▼
 Final Predicted Marks
```

Sleep and rest hours are recorded for wellness tracking but are not directly included in the prediction calculation.

> **Note:** This project is intended for educational purposes and demonstrates how study-related inputs can be used to estimate academic performance.

---

## 📂 Project Structure

```
study-marks-predictor/
│
├── app.py
├── requirements.txt
├── schedule.json
├── README.md
├── LICENSE
└── .gitignore
```

---

## 🌐 Deployment

The project is deployed using **Streamlit Community Cloud**.

### Live Application

https://malika26-08-study-marks-predictor.streamlit.app

Deployment steps:

1. Push the project to GitHub
2. Connect the repository to Streamlit Community Cloud
3. Select `app.py`
4. Deploy

---

## 🔧 Customization

### Modify Prediction Logic

Update the following function inside `app.py`:

```
compute_marks_from_study_and_intensity()
```

### Customize Theme

Modify the CSS inside:

```
apply_theme_css()
```

---

## 📸 Screenshots

Add screenshots here after deployment.

| Feature | Screenshot |
|----------|------------|
| Dashboard | *(Add Image)* |
| Schedule | *(Add Image)* |
| Insights | *(Add Image)* |

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/new-feature
```

3. Commit changes

```bash
git commit -m "Added new feature"
```

4. Push

```bash
git push origin feature/new-feature
```

5. Open a Pull Request

---

## 🐞 Troubleshooting

| Problem | Solution |
|----------|----------|
| Port already in use | `streamlit run app.py --server.port 8502` |
| Missing packages | `pip install -r requirements.txt` |
| Data not saving | Ensure `schedule.json` has write permission |

---

## 📝 License

This project is licensed under the **MIT License**.

Feel free to use, modify, and distribute it with proper attribution.

---

## 💡 Future Enhancements

- User authentication
- Cloud data synchronization
- Multi-subject support
- Advanced Machine Learning models
- Google Calendar integration
- Email reminders
- Dark/Light theme toggle
- Mobile application
- Collaborative study groups

---

## 👩‍💻 Author

**Malika Harmaien**

📧 Email: **harmaienmalika@gmail.com**

🐙 GitHub: https://github.com/Malika26-08

🌐 Live App: https://malika26-08-study-marks-predictor.streamlit.app

---

## ⭐ Support

If you found this project useful, consider giving it a **Star ⭐** on GitHub.

---

## ❤️ Built With

Python • Streamlit • Pandas • NumPy • Plotly • Pillow

Made with ❤️ for students to study smarter and achieve better academic performance.
