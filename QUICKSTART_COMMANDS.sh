#!/bin/bash
# QUICK DEPLOYMENT COMMANDS — Copy and paste these into your terminal

# ============================================================================
# STEP 1: PREPARE YOUR WORKSPACE
# ============================================================================

cd c:\ml_miniproj
git init
git config user.email "your-email@example.com"
git config user.name "Your Name"


# ============================================================================
# STEP 2: CREATE INITIAL COMMIT
# ============================================================================

git add .
git commit -m "Initial commit: AI Study Planner Dashboard with marks prediction, schedule management, and analytics"


# ============================================================================
# STEP 3: CONNECT TO GITHUB (after creating repo on GitHub)
# Replace 'yourusername' with your GitHub username
# ============================================================================

git remote add origin https://github.com/yourusername/study-marks-predictor.git
git branch -M main
git push -u origin main


# ============================================================================
# STEP 4: VERIFY DEPLOYMENT READINESS
# ============================================================================

# Check syntax
python -m py_compile app.py

# Run locally to verify
streamlit run app.py

# This will start the app at http://localhost:8501


# ============================================================================
# STEP 5: AFTER MAKING CHANGES, PUSH UPDATES
# ============================================================================

# Edit app.py or other files, then:
git add .
git commit -m "Feature/fix: describe your change here"
git push origin main

# Streamlit Cloud will auto-deploy!


# ============================================================================
# USEFUL ADDITIONAL COMMANDS
# ============================================================================

# View commit history
git log --oneline

# Check git status
git status

# View all branches
git branch -a

# Create a new feature branch (optional)
git checkout -b feature/my-feature
# ... make changes ...
git commit -am "Add my feature"
git push origin feature/my-feature
# Then create a Pull Request on GitHub


# ============================================================================
# STREAMLIT-SPECIFIC COMMANDS
# ============================================================================

# Run on different port
streamlit run app.py --server.port 8502

# Run with specific logger level
streamlit run app.py --logger.level=debug

# View config
streamlit config show

# Clear cache
streamlit cache clear


# ============================================================================
# LOCAL TESTING BEFORE PUSH
# ============================================================================

# Verify all dependencies installed
pip install -r requirements.txt

# Run syntax check
python -m py_compile app.py

# Import test
python -c "import streamlit, sklearn, pandas, numpy, plotly, PIL; print('All imports OK')"

# Run the app
streamlit run app.py
