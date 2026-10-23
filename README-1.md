# 💧 SipWithVic — Your Daily Hydration Companion

**WaterBuddy** is a simple, private and motivating hydration tracker built with **Python + Streamlit**.
Meet **Vic**, the friendly water-drop mascot who cheers you on as you reach your daily goal.

> FA-1 | Python Programming | Planning & Designing

🔗 **Live app:** _paste your public Streamlit URL here_

---

## ✨ Features

| Feature | What it does |
|---|---|
| 🎂 **Age-based goals** | Pick Children (4–8), Teens (9–13), Adults (14–64) or Seniors (65+); a goal is suggested and can be adjusted |
| 🍼 **Digital 2-litre bottle** | The water level rises smoothly with a moving wave whenever you log water, with litre marks and a dashed goal line |
| 💦 **Drip animation** | A water drop falls into the bottle on every log |
| ➕ **Quick logger** | One-tap **+250 ml** button, plus a **custom amount** pop-up and **Undo** |
| 📊 **Real-time feedback** | Total, goal, remaining and a progress bar update instantly |
| 😊 **Mascot Vic** | Original drawn mascot whose mood changes at **50%, 75% and 100%** |
| 🎉 **Encouragement** | A friendly message ("Great job today!") after every log, and balloons when the goal is reached |
| 🌅 **Daily reset** | "Start a new day?" confirmation, plus automatic reset when the date changes |
| 💡 **Daily tips** | Short hydration tips in a sticky-note style card |

## 🆕 Improvements in this version

Based on the FA-1 storyboard and review feedback:

- Rebuilt the interface to match the storyboard flow: **Welcome → Age & Goal → Home Dashboard → Logging → Mascot Milestones → New Day / Reset**
- Added the **2-litre bottle** that fills as water is logged
- Made logging **interactive** with fill animation, drip effect and toast messages
- Added mascot **Vic** to every main screen, with milestone reactions
- Applied the storyboard **colour palette**: `#C8E6C9` `#F5EBE0` `#B3E5FC` `#37474F`
- Added **age-aware** goals with an adjustable slider
- Added a **reset confirmation** and automatic **daily reset**
- Replaced the deprecated `use_container_width` setting with `width="stretch"`
- Verified the code compiles and keeps all progress in `st.session_state`
- All graphics are **original inline SVG/CSS**: no copyrighted images, characters or external assets

## 🧰 Tech

- **Python** – calculations, conditions and data handling
- **Streamlit** – buttons, sliders, pop-up dialogs, layout and cloud deployment
- **SVG + CSS animation** – bottle, waves, drip and mascot (replaces the Tkinter/Turtle drawing from the storyboard, with the same logic)

## ▶️ Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## ☁️ Deploy on Streamlit Community Cloud

1. Push `app.py`, `requirements.txt` and `README.md` to GitHub.
2. On share.streamlit.io choose **New app**, select this repository, branch `main`, main file `app.py`.
3. Deploy and copy the public URL into this README.

## 📁 Files

- `app.py` – the whole application
- `requirements.txt` – dependencies
- `README.md` – this file

## ⚠️ Note

WaterBuddy is a habit-building tool, not medical advice. Hydration needs vary by person, climate and health, so talk to a doctor for personal guidance.

_Healthy Habits · Happy Users · A Brighter Tomorrow_
