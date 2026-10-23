"""
WaterBuddy - Your Daily Hydration Companion
FA-1 | Python Programming | Planning & Designing

Streamlit implementation of the FA-1 storyboard:
Welcome -> Age Select & Goal -> Home Dashboard -> Logging -> Mascot Milestones -> New Day / Reset

All graphics (bottle + mascot) are original inline SVG/CSS drawn for this project,
so there are no copyrighted images, characters or external assets.
"""

import random
from datetime import date

import streamlit as st

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------
MASCOT_NAME = "Wick"           # mascot name used across the app
BOTTLE_ML = 2000               # the digital bottle holds 2 litres
QUICK_ML = 250                 # the compulsory quick-log button

# Palette from the storyboard
GREEN = "#C8E6C9"
CREAM = "#F5EBE0"
BLUE = "#B3E5FC"
DARK = "#37474F"
WATER = "#4FC3F7"

# Age-specific hydration goals (ml) - recommended, user can adjust
AGE_GROUPS = {
    "Children (4–8 yrs)": 1200,
    "Teens (9–13 yrs)": 1700,
    "Adults (14–64 yrs)": 2400,
    "Seniors (65+ yrs)": 1800,
}

CHEERS = [
    "Great job today! 💧",
    "Nice sip! Keep it up! 🌟",
    "Your body says thank you! 💙",
    "Hydration hero in action! 🦸",
    "Splash! One step closer to your goal! 🎯",
]

TIPS = [
    "Keep your water bottle on your desk so it's always in sight.",
    "Drink a glass of water first thing in the morning.",
    "Sip a little after every break or meeting.",
    "Add a slice of lemon or mint if plain water feels boring.",
    "Drink a glass before each meal.",
]

st.set_page_config(page_title="WaterBuddy", page_icon="💧", layout="centered")


def html(markup: str) -> str:
    """Collapse indentation so Streamlit's markdown never treats HTML as code."""
    return "".join(line.strip() for line in markup.splitlines())


# --------------------------------------------------------------------------
# Session state
# --------------------------------------------------------------------------
def init_state():
    s = st.session_state
    defaults = {
        "screen": "welcome",
        "age": None,
        "goal": 2400,
        "total": 0,
        "prev": 0,          # previous total, used to animate the bottle
        "log": [],
        "fills": 0,
        "just_logged": False,
        "celebrate": False,
        "day": date.today(),
    }
    for k, v in defaults.items():
        s.setdefault(k, v)
    # Daily reset when a new calendar day starts
    if s.day != date.today():
        s.day = date.today()
        reset_day()


def reset_day():
    s = st.session_state
    s.total = 0
    s.prev = 0
    s.log = []
    s.just_logged = False
    s.celebrate = False


def add_water(ml: int):
    s = st.session_state
    before = s.total
    s.prev = before
    s.total = before + ml
    s.log.append(ml)
    s.fills += 1
    s.just_logged = True
    goal = s.goal
    # milestone messages
    crossed = [m for m in (50, 75, 100)
               if before * 100 < goal * m <= s.total * 100]
    if crossed:
        top = max(crossed)
        msg = {50: "Halfway there! Keep sipping! 💧",
               75: "You're doing great! Almost there! 🌟",
               100: "Goal achieved! Great job! 🎉"}[top]
        st.toast(msg, icon="🎯")
        if top == 100:
            s.celebrate = True
    else:
        st.toast(random.choice(CHEERS))


def undo_last():
    s = st.session_state
    if s.log:
        ml = s.log.pop()
        s.prev = s.total
        s.total = max(0, s.total - ml)
        s.just_logged = False


def go(screen: str):
    st.session_state.screen = screen


# --------------------------------------------------------------------------
# Graphics
# --------------------------------------------------------------------------
def mascot_svg(mood: str = "happy", size: int = 170, bounce: bool = True) -> str:
    """Original water-drop mascot. mood: calm | happy | cheer | party"""
    mouths = {
        "calm": f'<path d="M50 98 Q60 105 70 98" stroke="{DARK}" stroke-width="3" fill="none" stroke-linecap="round"/>',
        "happy": f'<path d="M47 95 Q60 112 73 95" stroke="{DARK}" stroke-width="3" fill="none" stroke-linecap="round"/>',
        "cheer": f'<path d="M47 94 Q60 120 73 94 Z" fill="{DARK}"/><path d="M53 105 Q60 111 67 105 Q60 101 53 105Z" fill="#F48FB1"/>',
        "party": f'<path d="M45 93 Q60 124 75 93 Z" fill="{DARK}"/><path d="M52 106 Q60 114 68 106 Q60 101 52 106Z" fill="#F48FB1"/>',
    }
    if mood == "party":
        eyes = (f'<path d="M39 84 Q46 76 53 84" stroke="{DARK}" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
                f'<path d="M67 84 Q74 76 81 84" stroke="{DARK}" stroke-width="3.5" fill="none" stroke-linecap="round"/>')
        extras = ('<text x="6" y="30" font-size="18" fill="#FFD54F">★</text>'
                  '<text x="96" y="22" font-size="22" fill="#FFB74D">★</text>'
                  '<text x="100" y="70" font-size="14" fill="#FFD54F">✦</text>'
                  '<text x="4" y="70" font-size="14" fill="#F48FB1">✦</text>')
    else:
        eyes = (f'<circle cx="46" cy="84" r="5.5" fill="{DARK}"/><circle cx="74" cy="84" r="5.5" fill="{DARK}"/>'
                '<circle cx="48" cy="82" r="1.8" fill="#fff"/><circle cx="76" cy="82" r="1.8" fill="#fff"/>')
        extras = ""
    cls = "wb-bob" if bounce else ""
    return html(f"""
    <svg class="{cls}" width="{size}" height="{int(size*1.08)}" viewBox="0 0 120 130" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{MASCOT_NAME} the water drop mascot">
    <defs><linearGradient id="dropg{mood}" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#81D4FA"/><stop offset="1" stop-color="{WATER}"/></linearGradient></defs>
    <ellipse cx="60" cy="125" rx="30" ry="4" fill="{DARK}" opacity="0.12"/>
    <path d="M60 6 C60 6 16 58 16 88 A44 44 0 0 0 104 88 C104 58 60 6 60 6 Z" fill="url(#dropg{mood})" stroke="{DARK}" stroke-width="3" stroke-linejoin="round"/>
    <ellipse cx="38" cy="78" rx="6" ry="12" fill="#fff" opacity="0.45" transform="rotate(18 38 78)"/>
    {eyes}
    <ellipse cx="35" cy="98" rx="6" ry="3.5" fill="#F48FB1" opacity="0.55"/>
    <ellipse cx="85" cy="98" rx="6" ry="3.5" fill="#F48FB1" opacity="0.55"/>
    {mouths[mood]}
    {extras}
    </svg>""")


def bottle_svg(total: int, prev: int, goal: int, fills: int, drip: bool) -> str:
    """2-litre bottle whose water level animates from prev -> total."""
    body_h = 290.0
    top_y = 50.0

    def offset(ml):
        frac = min(ml, BOTTLE_ML) / BOTTLE_ML
        return body_h * (1 - frac) + (22 if frac == 0 else 0)

    a, b = offset(prev), offset(total)
    name = f"wbfill{fills}"

    ticks = ""
    for ml in (500, 1000, 1500, 2000):
        y = top_y + body_h * (1 - ml / BOTTLE_ML)
        label = f"{ml/1000:g}L"
        ticks += (f'<line x1="120" y1="{y}" x2="130" y2="{y}" stroke="{DARK}" stroke-width="2"/>'
                  f'<text x="134" y="{y+4}" font-size="11" fill="{DARK}" font-weight="600">{label}</text>')

    gy = top_y + body_h * (1 - min(goal, BOTTLE_ML) / BOTTLE_ML)
    goal_line = (f'<line x1="20" y1="{gy}" x2="120" y2="{gy}" stroke="#2E7D32" stroke-width="2" stroke-dasharray="5 4"/>'
                 f'<text x="26" y="{gy-4}" font-size="9" fill="#2E7D32" font-weight="700">GOAL</text>')

    drip_el = ('<circle class="wb-drip" cx="70" cy="-14" r="6" fill="#4FC3F7"/>' if drip else "")

    st.markdown(f"<style>@keyframes {name}{{from{{transform:translateY({a}px)}}to{{transform:translateY({b}px)}}}}</style>",
                unsafe_allow_html=True)
    return html(f"""
    <svg class="wb-bottle" viewBox="0 -40 180 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="2 litre water bottle, {total} ml filled">
    <defs>
    <clipPath id="wbclip"><rect x="20" y="50" width="100" height="290" rx="30"/></clipPath>
    <linearGradient id="wbwater" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#81D4FA"/><stop offset="1" stop-color="#29B6F6"/></linearGradient>
    </defs>
    <rect x="44" y="6" width="52" height="16" rx="5" fill="{DARK}"/>
    <rect x="48" y="20" width="44" height="36" rx="6" fill="#fff" stroke="{DARK}" stroke-width="3"/>
    <rect x="20" y="50" width="100" height="290" rx="30" fill="#ffffff" opacity="0.85"/>
    <g clip-path="url(#wbclip)">
    <g style="transform:translateY({b}px);animation:{name} 1.4s ease-out;">
    <g class="wb-wave"><path d="M0 50 Q25 40 50 50 T100 50 T150 50 T200 50 T250 50 T300 50 V70 H0 Z" fill="url(#wbwater)"/></g>
    <rect x="0" y="60" width="200" height="320" fill="url(#wbwater)"/>
    <circle cx="45" cy="120" r="3" fill="#fff" opacity="0.5"/><circle cx="90" cy="150" r="2" fill="#fff" opacity="0.5"/>
    <circle cx="60" cy="190" r="4" fill="#fff" opacity="0.4"/><circle cx="95" cy="230" r="3" fill="#fff" opacity="0.4"/>
    </g></g>
    {goal_line}
    <rect x="20" y="50" width="100" height="290" rx="30" fill="none" stroke="{DARK}" stroke-width="4"/>
    <path d="M32 90 Q30 150 34 210" stroke="#fff" stroke-width="5" fill="none" opacity="0.55" stroke-linecap="round"/>
    {ticks}
    {drip_el}
    </svg>""")


def mood_for(pct: float) -> str:
    if pct >= 100:
        return "party"
    if pct >= 75:
        return "cheer"
    if pct >= 50:
        return "happy"
    return "calm"


def message_for(pct: float) -> str:
    if pct >= 100:
        return "Goal achieved! Great job! 🎉"
    if pct >= 75:
        return "You're doing great! Almost there!"
    if pct >= 50:
        return "Halfway there! Keep sipping!"
    if pct > 0:
        return "Nice start! Let's keep going!"
    return f"Hi, I'm {MASCOT_NAME}! Let's drink some water together."


# --------------------------------------------------------------------------
# Styling
# --------------------------------------------------------------------------
def inject_css():
    st.markdown(html(f"""
    <style>
    .stApp{{background:{CREAM};}}
    header[data-testid="stHeader"]{{background:transparent;}}
    #MainMenu, footer{{visibility:hidden;}}
    .block-container{{max-width:760px;padding-top:1.5rem;padding-bottom:3rem;}}
    h1,h2,h3,p,label,span,div{{color:{DARK};}}
    .wb-title{{text-align:center;font-weight:800;font-size:2.4rem;letter-spacing:.5px;margin:.2rem 0 0;color:{DARK};}}
    .wb-sub{{text-align:center;font-size:1.05rem;opacity:.8;margin-bottom:.6rem;}}
    .wb-center{{display:flex;justify-content:center;}}
    .wb-card{{background:#fff;border-radius:20px;padding:14px 16px;box-shadow:0 4px 14px rgba(55,71,79,.10);border:2px solid {GREEN};}}
    .wb-stats{{display:flex;gap:10px;margin:10px 0;}}
    .wb-stat{{flex:1;background:{BLUE};border-radius:16px;padding:10px 6px;text-align:center;}}
    .wb-stat b{{display:block;font-size:1.35rem;color:{DARK};}}
    .wb-stat span{{font-size:.78rem;opacity:.8;}}
    .wb-bar{{height:22px;background:#fff;border:2px solid {DARK};border-radius:14px;overflow:hidden;}}
    .wb-bar>div{{height:100%;background:linear-gradient(90deg,#81D4FA,{WATER});border-radius:12px;transition:width .8s ease;}}
    .wb-bubble{{background:#fff;border:2px solid {DARK};border-radius:18px;padding:10px 14px;text-align:center;font-weight:700;position:relative;margin-bottom:8px;}}
    .wb-bubble:after{{content:"";position:absolute;bottom:-11px;left:50%;margin-left:-10px;border:10px solid transparent;border-top-color:{DARK};border-bottom:0;}}
    .wb-bob{{animation:wbbob 2.2s ease-in-out infinite;}}
    @keyframes wbbob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-8px)}}}}
    .wb-wave{{animation:wbwave 2.4s linear infinite;}}
    @keyframes wbwave{{from{{transform:translateX(0)}}to{{transform:translateX(-100px)}}}}
    .wb-drip{{animation:wbdrip .9s ease-in;opacity:0;}}
    @keyframes wbdrip{{0%{{transform:translateY(0);opacity:1}}85%{{transform:translateY(76px);opacity:1}}100%{{transform:translateY(80px);opacity:0}}}}
    .wb-bottle{{width:100%;max-width:230px;height:auto;display:block;margin:0 auto;}}
    .wb-mile{{background:#fff;border-radius:16px;padding:8px 4px;text-align:center;border:2px solid {GREEN};font-size:.8rem;font-weight:700;}}
    .wb-mile.off{{opacity:.38;filter:grayscale(.7);}}
    .wb-tip{{background:#FFF59D;border-radius:6px;padding:10px 14px;transform:rotate(-1.2deg);box-shadow:2px 3px 8px rgba(0,0,0,.15);font-style:italic;text-align:center;}}
    .stButton>button{{border-radius:16px;font-weight:700;border:2px solid {DARK};background:#fff;color:{DARK};padding:.55rem 1rem;transition:transform .12s ease, box-shadow .12s ease;}}
    .stButton>button:hover{{transform:translateY(-2px);box-shadow:0 4px 10px rgba(55,71,79,.25);border-color:{DARK};color:{DARK};}}
    .stButton>button:active{{transform:scale(.96);}}
    .stButton>button[kind="primary"]{{background:{WATER};color:{DARK};}}
    </style>"""), unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Screens
# --------------------------------------------------------------------------
def screen_welcome():
    st.markdown("<div class='wb-title'>Water Buddy</div>", unsafe_allow_html=True)
    st.markdown("<div class='wb-sub'>Your Daily Hydration Companion<br>Simple · Private · Personalized · Motivating</div>",
                unsafe_allow_html=True)
    st.markdown(f"<div class='wb-center'>{mascot_svg('happy', 230)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='wb-bubble' style='max-width:340px;margin:12px auto;'>Hi, I'm {MASCOT_NAME}! Let's stay hydrated together 💧</div>",
                unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.button("Get Started", type="primary", key="start", on_click=go, args=("age",), width="stretch")


def screen_age():
    st.markdown("<div class='wb-title' style='font-size:1.8rem'>Select your age group</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='wb-center'>{mascot_svg('calm', 110)}</div>", unsafe_allow_html=True)
    age = st.radio("Age group", list(AGE_GROUPS.keys()), index=2, label_visibility="collapsed")
    rec = AGE_GROUPS[age]
    st.markdown(f"<div class='wb-card' style='text-align:center'>Recommended goal: <b>{rec} ml</b> (about {rec/250:.0f} cups)</div>",
                unsafe_allow_html=True)
    goal = st.slider("Adjust your daily goal (ml) if you want", 500, 4000, rec, 50, key=f"goal_{age}")
    if st.button("Let's Go!", type="primary", width="stretch"):
        st.session_state.age = age
        st.session_state.goal = goal
        reset_day()
        go("home")
        st.rerun()


@st.dialog("Add a custom amount")
def custom_dialog():
    ml = st.number_input("Amount (ml)", min_value=10, max_value=1000, value=150, step=10)
    if st.button("Add water 💧", type="primary", width="stretch"):
        add_water(int(ml))
        st.rerun()


@st.dialog("Start a new day?")
def reset_dialog():
    st.write("Your current progress will be reset.")
    c1, c2 = st.columns(2)
    if c1.button("Cancel", width="stretch"):
        st.rerun()
    if c2.button("Yes, reset", type="primary", width="stretch"):
        reset_day()
        st.rerun()


def screen_home():
    s = st.session_state
    pct = min(100.0, s.total / s.goal * 100) if s.goal else 0
    remaining = max(0, s.goal - s.total)

    st.markdown("<div class='wb-title' style='font-size:1.9rem'>Water Buddy 💧</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='wb-sub'>{s.age} · daily goal {s.goal} ml</div>", unsafe_allow_html=True)

    left, right = st.columns([1, 1.15], gap="medium")

    with left:
        st.markdown(bottle_svg(s.total, s.prev, s.goal, s.fills, s.just_logged), unsafe_allow_html=True)
        st.caption("2-litre bottle · dashed line = your daily goal")

    with right:
        st.markdown(f"<div class='wb-bubble'>{message_for(pct)}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='wb-center'>{mascot_svg(mood_for(pct), 150)}</div>", unsafe_allow_html=True)
        st.markdown(html(f"""
        <div class='wb-stats'>
        <div class='wb-stat'><b>{s.total}</b><span>Total ml</span></div>
        <div class='wb-stat'><b>{s.goal}</b><span>Goal ml</span></div>
        <div class='wb-stat'><b>{remaining}</b><span>Remaining</span></div>
        </div>
        <div class='wb-bar'><div style='width:{pct:.0f}%'></div></div>
        <div style='text-align:center;font-weight:700;margin-top:4px'>{pct:.0f}% of today's goal</div>"""),
            unsafe_allow_html=True)

    st.write("")
    b1, b2 = st.columns(2)
    b1.button(f"＋ {QUICK_ML} ml", type="primary", key="quick", on_click=add_water, args=(QUICK_ML,), width="stretch")
    if b2.button("✏️ Custom amount", key="custom", width="stretch"):
        custom_dialog()

    b3, b4, b5 = st.columns(3)
    b3.button("↩️ Undo", key="undo", on_click=undo_last, disabled=not s.log, width="stretch")
    if b4.button("🌅 New Day", key="newday", width="stretch"):
        reset_dialog()
    b5.button("🎂 Age group", key="agechg", on_click=go, args=("age",), width="stretch")

    # Mascot milestones
    st.markdown("<h4 style='text-align:center;margin-top:1.2rem'>Mascot Milestones</h4>", unsafe_allow_html=True)
    cols = st.columns(3)
    for col, (mark, mood, text) in zip(cols, [(50, "happy", "Halfway there!<br>Keep sipping!"),
                                              (75, "cheer", "You're doing great!"),
                                              (100, "party", "Goal achieved!<br>Great job!")]):
        cls = "wb-mile" if pct >= mark else "wb-mile off"
        col.markdown(f"<div class='{cls}'><div>{mark}%</div><div class='wb-center'>{mascot_svg(mood, 78, bounce=False)}</div>{text}</div>",
                     unsafe_allow_html=True)

    if s.log:
        st.caption(f"Today: {len(s.log)} sip(s) logged · " + " + ".join(str(x) for x in s.log[-6:]) + " ml")

    st.write("")
    st.markdown(f"<div class='wb-tip'>💡 Tip: {TIPS[s.fills % len(TIPS)]}</div>", unsafe_allow_html=True)

    # animation flags are one-shot
    s.prev = s.total
    s.just_logged = False
    if s.celebrate:
        st.balloons()
        s.celebrate = False


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
init_state()
inject_css()

screen = st.session_state.screen
if screen == "welcome":
    screen_welcome()
elif screen == "age":
    screen_age()
else:
    screen_home()

st.markdown(f"<p style='text-align:center;opacity:.6;font-size:.8rem;margin-top:2rem'>WaterBuddy · Healthy Habits · Happy Users · A Brighter Tomorrow</p>",
            unsafe_allow_html=True)
