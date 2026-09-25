"""
Math 6 — Day 23: Equivalent Ratios with Mixed Numbers
Built to match the visual/interactive structure of the Day 6 and Day 22 apps
by Xavier Honablue, M.Ed.

Aligned to i-Ready Classroom Mathematics, Grade 6, Unit 3 (Ratio Reasoning):
Lesson 13, Session 4 — Develop: Using Equivalent Ratios (SB pp. 297-302)

Today's twist: the scale factor is no longer a whole number. 10 yd : 4 s scaled
to 25 yd needs a multiplier of 2 1/2, and the quantities themselves can be mixed
numbers (1 1/2 cups for every 2 batches).

Run locally with:  streamlit run app.py
"""

import json
import os
from datetime import datetime
from fractions import Fraction

import matplotlib.pyplot as plt
import streamlit as st

# ----------------------------------------------------------------------
# Page config & theme
# ----------------------------------------------------------------------
# Page config & theme
# ----------------------------------------------------------------------
st.set_page_config(page_title="Day 23 — Equivalent Ratios with Mixed Numbers", page_icon="🚲", layout="wide")

NAVY = "#1b3a5c"
NAVY_LIGHT = "#eef4fa"
NAVY_BORDER = "#2c4a6e"
GREEN = "#3f7d55"
GREEN_LIGHT = "#eef7f0"
GOLD = "#8a5a20"
GOLD_LIGHT = "#f6ecd9"
RED = "#b03a2e"
RED_LIGHT = "#fdf1ef"
PLUM = "#6b3fa0"
PLUM_LIGHT = "#f4effa"

CUSTOM_CSS = f"""
<style>
.box {{
    border: 2px solid {NAVY};
    border-radius: 8px;
    padding: 14px 18px;
    margin: 10px 0;
    background: white;
}}
.pill {{
    display: inline-block;
    color: white;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.4px;
    padding: 4px 12px;
    border-radius: 12px;
    margin-bottom: 8px;
}}
.box-readaloud {{ border-color: {NAVY}; }}
.box-readaloud .pill {{ background: {NAVY}; }}
.box-readaloud p {{ font-style: italic; margin: 4px 0 0 0; }}

.box-literacy {{ border-color: {NAVY_BORDER}; background: {NAVY_LIGHT}; }}
.box-literacy .pill {{ background: {NAVY_BORDER}; }}

.box-existing {{ border-color: {GREEN}; background: {GREEN_LIGHT}; }}
.box-existing .pill {{ background: {GREEN}; }}

.box-tools {{ border-color: {GOLD}; background: {GOLD_LIGHT}; }}
.box-tools .pill {{ background: {GOLD}; }}

.box-observer {{ border: 2px dashed {RED}; background: {RED_LIGHT}; }}
.box-observer .pill {{ background: {RED}; }}

.box-slides {{ border-color: {PLUM}; background: {PLUM_LIGHT}; }}
.box-slides .pill {{ background: {PLUM}; }}

.ask {{ color: {RED}; font-weight: 700; margin-top: 8px; }}

.roadmap-title {{ color: {NAVY}; font-weight: 700; font-size: 15px; margin-bottom: 0; }}
.roadmap-sub {{ color: #5a6672; font-size: 11.5px; margin-top: -4px; }}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def box(kind, pill, body_html):
    st.markdown(
        f'<div class="box box-{kind}"><span class="pill">{pill}</span>{body_html}</div>',
        unsafe_allow_html=True,
    )


def read_aloud(text):
    box("readaloud", "🔊 READ ALOUD", f"<p>&ldquo;{text}&rdquo;</p>")


def ask_the_class(text):
    st.markdown(f'<p class="ask">❓ Ask the class: {text}</p>', unsafe_allow_html=True)


def slides_ref(text):
    box("slides", "📊 TEACHER TOOLBOX SLIDES", text)


# ----------------------------------------------------------------------
# Observer notes — a running teacher log, persisted to a local JSON file
# ----------------------------------------------------------------------
NOTES_FILE = os.path.join(os.path.dirname(__file__), "observer_notes.json")
DEFAULT_NOTES = [
    {
        "date": "Day 22",
        "note": "Tables clicked as long as the multiplier was a whole number. The Heartbeat Lab exposed the gap: when the target beats were not a multiple of the measured beats, most teams stopped. Today is about that exact moment — the scale factor that is a fraction or a mixed number.",
    }
]


def load_notes():
    if os.path.exists(NOTES_FILE):
        try:
            with open(NOTES_FILE) as f:
                return json.load(f)
        except Exception:
            return list(DEFAULT_NOTES)
    return list(DEFAULT_NOTES)


def save_notes(notes):
    try:
        with open(NOTES_FILE, "w") as f:
            json.dump(notes, f, indent=2)
    except Exception:
        pass  # read-only filesystem — notes still live for this session


if "observer_notes" not in st.session_state:
    st.session_state.observer_notes = load_notes()




# ----------------------------------------------------------------------
# Fraction / mixed-number helpers
# ----------------------------------------------------------------------
def mixed(x):
    """Plain-text mixed number: Fraction(5, 2) -> '2 1/2'."""
    x = Fraction(x)
    if x.denominator == 1:
        return str(x.numerator)
    sign = "-" if x < 0 else ""
    x = abs(x)
    whole, rem = divmod(x.numerator, x.denominator)
    if whole == 0:
        return f"{sign}{rem}/{x.denominator}"
    return f"{sign}{whole} {rem}/{x.denominator}"


def tex(x):
    """LaTeX mixed number for st.markdown: Fraction(5, 2) -> '2\\tfrac{1}{2}'."""
    x = Fraction(x)
    if x.denominator == 1:
        return str(x.numerator)
    whole, rem = divmod(abs(x.numerator), x.denominator)
    sign = "-" if x < 0 else ""
    frac = rf"\tfrac{{{rem}}}{{{x.denominator}}}"
    return f"{sign}{whole}{frac}" if whole else f"{sign}{frac}"


def m(x):
    """Inline math wrapper for a mixed number."""
    return f"${tex(x)}$"


def parse_mixed(text):
    """Parse '2 1/4', '9/4', '2.25', or '3' into a Fraction. Returns None if unreadable."""
    t = (text or "").strip().replace("½", " 1/2").replace("¼", " 1/4").replace("¾", " 3/4")
    if not t:
        return None
    try:
        parts = t.split()
        if len(parts) == 2:
            whole = Fraction(parts[0])
            frac = Fraction(parts[1])
            return whole + frac if whole >= 0 else whole - frac
        return Fraction(parts[0])
    except (ValueError, ZeroDivisionError):
        return None


def equivalent(r1, r2):
    """True when ratio r1 = (a, b) is equivalent to r2 = (c, d)."""
    return Fraction(r1[0]) * Fraction(r2[1]) == Fraction(r1[1]) * Fraction(r2[0])


def draw_double_number_line(pairs, label_a, label_b, highlight=None, figsize=(8.6, 2.4)):
    """Double number line through (0, 0) and each (a, b) pair, placed by the value of a.
    Labels print as mixed numbers so 12 1/2 sits exactly halfway between 10 and 15."""
    pairs = sorted({(Fraction(a), Fraction(b)) for a, b in pairs})
    top = max(a for a, _ in pairs)
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot([0, 1], [1.35, 1.35], color=NAVY, linewidth=2)
    ax.plot([0, 1], [0.45, 0.45], color=GOLD, linewidth=2)
    for a, b in [(Fraction(0), Fraction(0))] + pairs:
        x = float(a / top)
        hot = highlight is not None and a == Fraction(highlight)
        col_a = RED if hot else NAVY
        col_b = RED if hot else GOLD
        ax.plot([x, x], [1.25, 1.45], color=col_a, linewidth=2.6 if hot else 2)
        ax.plot([x, x], [0.35, 0.55], color=col_b, linewidth=2.6 if hot else 2)
        ax.text(x, 1.62, mixed(a), ha="center", va="bottom", fontsize=10, color=col_a,
                fontweight="bold" if hot else "normal")
        ax.text(x, 0.22, mixed(b), ha="center", va="top", fontsize=10, color=col_b,
                fontweight="bold" if hot else "normal")
    ax.text(-0.03, 1.35, label_a, ha="right", va="center", fontsize=10,
            color=NAVY, fontweight="bold")
    ax.text(-0.03, 0.45, label_b, ha="right", va="center", fontsize=10,
            color=GOLD, fontweight="bold")
    ax.set_xlim(-0.32, 1.04)
    ax.set_ylim(-0.1, 1.95)
    ax.axis("off")
    return fig


def draw_scale_bar(factor, figsize=(7.6, 1.5)):
    """Show a multiplier like 2 1/2 as whole copies plus a partial copy of one group."""
    factor = Fraction(factor)
    whole = factor.numerator // factor.denominator
    part = factor - whole
    fig, ax = plt.subplots(figsize=figsize)
    for i in range(whole):
        ax.add_patch(plt.Rectangle((i, 0.2), 0.94, 0.6, facecolor="#dbe8f6",
                                   edgecolor=NAVY, linewidth=1.8))
        ax.text(i + 0.47, 0.5, "1 group", ha="center", va="center", fontsize=9, color=NAVY)
    if part:
        ax.add_patch(plt.Rectangle((whole, 0.2), 0.94, 0.6, facecolor="white",
                                   edgecolor=NAVY, linewidth=1.2, linestyle="--"))
        ax.add_patch(plt.Rectangle((whole, 0.2), 0.94 * float(part), 0.6, facecolor="#f6ecd9",
                                   edgecolor=GOLD, linewidth=1.8))
        ax.text(whole + 0.47, 0.5, f"{mixed(part)} group", ha="center", va="center",
                fontsize=9, color=GOLD)
    ax.set_xlim(-0.1, max(whole + (1 if part else 0), 1) + 0.1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig


# ----------------------------------------------------------------------
# Sidebar — Sign In + Roadmap
# ----------------------------------------------------------------------
STEPS = [
    "1. Welcome Back",
    "2. Warm-Up: Same and Different",
    "3. Ian's Unicycle",
    "4. Model It: Go Through a Smaller Ratio",
    "5. Model It: A Mixed-Number Multiplier",
    "6. Discuss It & Devon's Error",
    "7. Real Life: Part-to-Part ↔ Part-to-Whole",
    "8. Project: Mixed-Number Recipe Lab",
    "9. Practice, Stations & Exit Ticket",
]

with st.sidebar:
    st.subheader("Sign In")
    st.text_input("Your name:", key="student_name")
    st.selectbox("Choose your shape avatar:",
                 ["Rectangle", "Square", "Triangle", "Circle", "Hexagon"], key="avatar")
    st.selectbox(
        "Pick your learning mode:",
        ["Focus Champ", "Growth Mode", "Problem Solver", "Data Boss", "Brain Builder"],
        key="learning_mode",
    )
    st.markdown("---")
    st.markdown('<p class="roadmap-title">Day 23 Roadmap</p>', unsafe_allow_html=True)
    st.markdown('<p class="roadmap-sub">55-minute period — Find Equivalent Ratios, '
                'Session 4 (Develop: Using Equivalent Ratios)</p>', unsafe_allow_html=True)

    if "step" not in st.session_state:
        st.session_state.step = 0
    for i, label in enumerate(STEPS):
        marker = "▶ " if i == st.session_state.step else ""
        if st.button(marker + label, key=f"nav_{i}", width="stretch"):
            st.session_state.step = i
            st.rerun()

# ----------------------------------------------------------------------
# Roadmap step content
# ----------------------------------------------------------------------
step = st.session_state.step
name = st.session_state.get("student_name", "") or "class"

st.markdown(f"## {STEPS[step]}")
st.progress((step + 1) / len(STEPS))


if step == 0:
    box(
        "observer",
        "🔎 OBSERVER NOTE — carried from Day 22",
        f"<p style='margin:0'>{st.session_state.observer_notes[0]['note']}</p>",
    )
    read_aloud(
        "Last class every multiplier was a whole number: times 5, times 10, times 15. Real life "
        "does not cooperate like that. Today a unicycle covers 10 yards every 4 seconds and I want "
        "to know about 25 yards. Ten does not go into twenty-five a whole number of times. It goes "
        "in two and a half times. By the end of today, multiplying a ratio by two and a half — or "
        "by any fraction or mixed number — will feel exactly like multiplying by two."
    )
    box("tools", "Today's tools",
        "Fraction strips &middot; double-number-line strips &middot; grid paper &middot; "
        "measuring cups (&frac14;, &frac12;, &frac34;, 1 cup) for the Recipe Lab &middot; "
        "journal &middot; exit ticket.")
    box("literacy", "LEARNING TARGETS",
        "I can identify and find equivalent ratios.<br>"
        "I can represent equivalent ratios in tables or as points in the coordinate plane.<br>"
        "I can use equivalent ratios to solve problems — even when the multiplier is a "
        "<b>fraction</b> or a <b>mixed number</b>.")
    ask_the_class("If 10 yards takes 4 seconds, is 25 yards more or less than twice as far? "
                  "So will the time be more or less than 8 seconds?")

elif step == 1:
    st.write("**Purpose:** Warm up equivalence and slip in the first non-whole multiplier "
             "before anyone is told it is coming.")
    st.markdown("##### Same and Different")
    cards = {"A": ("2 to 3", (2, 3)), "B": ("12 : 6", (12, 6)),
             "C": ("6 : 9", (6, 9)), "D": ("18 to 9", (18, 9))}
    cols = st.columns(4)
    for col, (k, (txt, _)) in zip(cols, cards.items()):
        col.info(f"**{k}**\n\n### {txt}")

    box("tools", "What to draw out",
        "<b>Written the same way:</b> A and D use the word <i>to</i>; B and C use a colon.<br>"
        "<b>Equivalent:</b> A and C (both reduce to 2 : 3); B and D (both reduce to 2 : 1).<br>"
        "<b>Order matters:</b> A is 2 : 3 but D is 18 : 9 — the bigger number is in a different "
        "place.<br>"
        "<b>The hidden surprise:</b> B → D multiplies both by <b>1&frac12;</b>. "
        "12 × 1&frac12; = 18 and 6 × 1&frac12; = 9.")

    st.markdown("##### Test any pair")
    c1, c2 = st.columns(2)
    p = c1.selectbox("First card", list(cards), index=1, key="d23_p")
    q = c2.selectbox("Second card", list(cards), index=3, key="d23_q")
    if st.button("Are they equivalent?", key="d23_pair"):
        r1, r2 = cards[p][1], cards[q][1]
        if p == q:
            st.warning("Pick two different cards.")
        elif equivalent(r1, r2):
            k = Fraction(r2[0], r1[0])
            st.success(f"Yes. Multiply both quantities in {p} by {m(k)}: "
                       f"{r1[0]} × {m(k)} = {r2[0]} and {r1[1]} × {m(k)} = {r2[1]}.")
        else:
            st.error(f"No. {r1[0]} × {r2[1]} = {r1[0] * r2[1]} but {r1[1]} × {r2[0]} = "
                     f"{r1[1] * r2[0]}. Different cross products, different comparison.")
    ask_the_class("B and D are equivalent. What single number takes 12 to 18 and 6 to 9? "
                  "Is it a whole number?")

elif step == 2:
    box("literacy", "CONNECT TO CULTURE",
        "A <b>unicycle</b> is like a bicycle with only one wheel. With no handlebars, the rider "
        "steers and balances by pedaling and shifting their weight. <i>What is your experience "
        "with bicycles, scooters, or skateboards?</i>")
    read_aloud(
        "Ian travels 10 yards on his unicycle every 4 seconds. Based on this ratio, how many "
        "seconds does it take Ian to travel 25 yards? Three reads before anybody picks up a pencil."
    )
    box("tools", "THREE READS",
        "<b>Read 1 — say it in your own words.</b> Ian rides a one-wheeled bike at a steady "
        "speed.<br>"
        "<b>Read 2 — what are you trying to find?</b> The number of seconds for 25 yards.<br>"
        "<b>Read 3 — what information is important?</b> The ratio 10 yd : 4 s, and the new "
        "distance, 25 yd.")
    box("existing", "WHY YESTERDAY'S MOVE STALLS",
        "Yesterday you asked <i>what do I multiply by?</i> 10 × 2 = 20 is too short. "
        "10 × 3 = 30 is too far. There is no <b>whole</b> number that takes 10 to 25. "
        "Let students sit in that for a minute — then let them choose a tool.")

    st.markdown("##### Solve and support your thinking")
    guess = st.number_input("Seconds for Ian to travel 25 yd:", min_value=0.0, step=0.5,
                            key="d23_uni")
    if st.button("Check", key="d23_uni_chk"):
        if abs(guess - 10) < 1e-9:
            st.success("Correct — **10 seconds**. Next we will look at two ways to prove it.")
        elif abs(guess - 8.5) < 1e-9:
            st.error("8½ is a classic slip. Hold on to that answer — we will study it in step 6.")
        else:
            st.error("Not yet. Try a smaller, friendlier ratio first: what is half of 10 yd : 4 s?")
    ask_the_class("Is there a number you could divide 10 and 4 by that gets you to a ratio that "
                  "*does* scale nicely to 25?")

elif step == 3:
    box("literacy", "MATH LITERACY: GO THROUGH A SMALLER RATIO",
        "When the multiplier is not a whole number, <b>divide both quantities first</b> to reach "
        "a smaller equivalent ratio, then <b>multiply</b> up to the target. Dividing and "
        "multiplying by the same nonzero number both keep the ratio equivalent.")
    read_aloud(
        "Ten yards in four seconds. Cut both in half: five yards in two seconds. Now twenty-five "
        "is easy — five times five. So the seconds are two times five. Ten seconds."
    )
    st.markdown(r"$$10 : 4 \;\xrightarrow{\;\div 2\;}\; 5 : 2 \;\xrightarrow{\;\times 5\;}\; "
                r"25 : 10$$")

    st.markdown("##### The double number line")
    target = st.select_slider("Yards Ian rides",
                              options=[Fraction(5, 2) * k for k in range(1, 21)],
                              value=Fraction(25), format_func=mixed, key="d23_dnl")
    pts = [(5 * k, 2 * k) for k in range(1, 7)] + [(target, target * Fraction(2, 5))]
    st.pyplot(draw_double_number_line(pts, "yards", "seconds", highlight=target))
    st.markdown(f"**{m(target)} yd lines up with {m(target * Fraction(2, 5))} s.** "
                "Drag to a point between the ticks — like 12½ yd — and the line still works.")

    st.markdown("##### The ratio table")
    st.table([{"Distance (yd)": "10", "Time (s)": "4", "Move": "given"},
              {"Distance (yd)": "5", "Time (s)": "2", "Move": "÷ 2 on both"},
              {"Distance (yd)": "25", "Time (s)": "10", "Move": "× 5 on both"}])
    box("existing", "ANOTHER PATH — GO THROUGH 1 SECOND",
        "Divide both by 4: 10 : 4 → <b>2&frac12; : 1</b>. Ian rides 2&frac12; yards every "
        "second. Then 25 ÷ 2&frac12; = 10 seconds. Same answer, and the first appearance of a "
        "mixed number <i>inside</i> a ratio.")
    ask_the_class("Why did we divide by 2 and not by 3? What makes a smaller ratio 'friendly'?")

elif step == 4:
    box("literacy", "MATH LITERACY: SCALE FACTOR",
        "The <b>scale factor</b> (multiplier) is the number both quantities are multiplied by. "
        "Find it by dividing the new amount by the original amount of the <b>same</b> quantity. "
        "It can be a whole number, a <b>fraction</b> (smaller), or a <b>mixed number</b>.")
    read_aloud(
        "One step instead of two. Twenty-five divided by ten is two and a half. So Ian rides two "
        "and a half groups of ten yards. Two and a half groups of four seconds is eight plus two. "
        "Ten seconds. The mixed number is the multiplier."
    )
    st.markdown(r"$$\frac{25}{10} = 2\tfrac{1}{2} \qquad 4 \times 2\tfrac{1}{2} = "
                r"(4 \times 2) + \left(4 \times \tfrac{1}{2}\right) = 8 + 2 = 10$$")

    st.markdown("##### Scale Ian's ratio to any distance")
    txt = st.text_input("Distance in yards (try 25, 15, 12 1/2, 32 1/2, 5):", "25", key="d23_any")
    d = parse_mixed(txt)
    if d is None or d <= 0:
        st.warning("Type a positive number, a fraction like 5/2, or a mixed number like 12 1/2.")
    else:
        k = d / 10
        secs = 4 * k
        st.markdown(f"Scale factor = {m(d)} ÷ 10 = **{m(k)}**")
        st.pyplot(draw_scale_bar(k) if k <= 6 else draw_scale_bar(Fraction(6)))
        if k > 6:
            st.caption("(Bar shows the first 6 groups.)")
        st.markdown(f"Time = 4 × {m(k)} = **{m(secs)} seconds**")

    st.markdown("##### When the quantities are mixed numbers")
    box("tools", "TRAIL MIX",
        "A trail mix recipe uses <b>2&frac14; cups of peanuts for every 1&frac12; cups of "
        "raisins</b>. How many cups of raisins go with <b>9 cups</b> of peanuts?")
    ans = st.text_input("Cups of raisins (you can type 6, or 5 1/2, etc.):", key="d23_trail")
    if st.button("Check", key="d23_trail_chk"):
        v = parse_mixed(ans)
        if v == 6:
            st.success("Correct. 9 ÷ 2¼ = 4, so the scale factor is 4: 1½ × 4 = **6 cups**.")
            st.table([{"Peanuts (c)": "2 1/4", "Raisins (c)": "1 1/2", "Move": "given"},
                      {"Peanuts (c)": "4 1/2", "Raisins (c)": "3", "Move": "× 2"},
                      {"Peanuts (c)": "9", "Raisins (c)": "6", "Move": "× 4"}])
        else:
            st.error("Find the scale factor on the peanut side first: 9 ÷ 2¼. "
                     "(Hint: how many 2¼'s make 4½? Make 9?)")

    st.markdown("##### A scale factor less than 1")
    box("existing", "SHAMPOO",
        "A large bottle holds <b>32 fl oz and costs $8</b>. A small bottle holds <b>12 fl oz</b> "
        "and has the same capacity-to-cost ratio. What does the small bottle cost?")
    if st.button("Reveal", key="d23_sham"):
        st.markdown("Scale factor = 12 ÷ 32 = $\\tfrac{3}{8}$. "
                    "Cost = 8 × $\\tfrac{3}{8}$ = **$3**.")
        st.table([{"Capacity (fl oz)": 32, "Cost ($)": 8, "Move": "given"},
                  {"Capacity (fl oz)": 4, "Cost ($)": 1, "Move": "÷ 8"},
                  {"Capacity (fl oz)": 12, "Cost ($)": 3, "Move": "× 3"}])
    ask_the_class("A scale factor of 2½ made Ian's numbers bigger. A scale factor of ⅜ made the "
                  "shampoo numbers smaller. How can you tell before you multiply?")

elif step == 5:
    st.markdown("#### Discuss It")
    box("tools", "Talk moves",
        "<b>Ask:</b> Why can you divide both quantities by the same number and still have an "
        "equivalent ratio?<br>"
        "<b>Ask:</b> When is going through a smaller ratio easier than finding one mixed-number "
        "multiplier?<br>"
        "<b>Share:</b> &ldquo;I found the scale factor by . . .&rdquo;<br>"
        "<b>Reflect:</b> which strategy will you try first on the exit ticket?")

    st.markdown("#### Devon's error")
    box("existing", "THE CLAIM",
        "Devon solves Ian's problem: <i>&ldquo;25 ÷ 10 = 2&frac12;. So the time is "
        "4 × 2&frac12; = 8&frac12; seconds.&rdquo;</i> Is Devon correct? Explain.")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**What Devon did**")
        st.markdown(r"$$4 \times 2\tfrac{1}{2} \;\to\; (4 \times 2) + \tfrac{1}{2} = 8\tfrac{1}{2}$$")
        st.error("Devon multiplied the whole-number part and just tacked on the ½.")
    with c2:
        st.markdown("**What the mixed number means**")
        st.markdown(r"$$4 \times 2\tfrac{1}{2} = (4 \times 2) + \left(4 \times \tfrac{1}{2}\right)"
                    r" = 8 + 2 = 10$$")
        st.success("Both parts of the mixed number multiply 4. Half a group of 4 s is 2 s.")
    st.pyplot(draw_scale_bar(Fraction(5, 2)))
    st.caption("2½ groups of 4 seconds: 4 + 4 + 2 = 10.")
    box("literacy", "CHECK IT WITH A RATIO",
        "Is 25 : 8&frac12; equivalent to 10 : 4? Cross products: 25 × 4 = 100, but "
        "10 × 8&frac12; = 85. Not equal — Devon's answer breaks the ratio. "
        "25 × 4 = 100 and 10 × 10 = 100 — 10 seconds keeps it.")

    st.markdown("#### Apply It — the baker")
    box("tools", "THE PROBLEM",
        "Each day a baker makes the same ratio of blueberry muffins to banana muffins. On Tuesday "
        "they make <b>96 blueberry and 72 banana</b>. On Wednesday they make <b>36 blueberry</b>. "
        "How many banana muffins on Wednesday?")
    pick = st.radio("Choose:", ["A — 12 banana", "B — 27 banana", "C — 48 banana",
                                "D — 132 banana"], key="d23_muf", index=None)
    if st.button("Check", key="d23_muf_chk"):
        if pick and pick.startswith("B"):
            st.success("Correct — **27**. Two ways:")
            st.table([{"Blueberry": 96, "Banana": 72, "Move": "given"},
                      {"Blueberry": 12, "Banana": 9, "Move": "÷ 8"},
                      {"Blueberry": 36, "Banana": 27, "Move": "× 3"}])
            st.markdown("Or one step: scale factor = 36 ÷ 96 = $\\tfrac{3}{8}$, and "
                        "72 × $\\tfrac{3}{8}$ = 27.")
        elif pick and pick.startswith("D"):
            st.error("132 = 96 + 36 — that is adding, not scaling. Ratios are multiplicative.")
        elif pick and pick.startswith("C"):
            st.error("48 = 72 − 24? Subtracting a constant keeps the difference, not the ratio.")
        else:
            st.error("Find what takes 96 down to 36, then do the same to 72.")
    ask_the_class("Answer D came from adding. Where have we seen that error before this week?")

elif step == 6:
    box("literacy", "MATH LITERACY: PART-TO-PART, PART-TO-WHOLE, AND CROSSING BETWEEN",
        "A <b>part-to-part</b> ratio compares one part of a mixture to another part "
        "(concentrate : water). A <b>part-to-whole</b> ratio compares one part to the "
        "<b>total</b> (concentrate : whole pitcher). To <b>cross</b> from one to the other:<br>"
        "&nbsp;&nbsp;part : part &nbsp;<b>a : b</b> &nbsp;→&nbsp; part : whole &nbsp;"
        "<b>a : (a + b)</b> &nbsp;&nbsp;(add the parts)<br>"
        "&nbsp;&nbsp;part : whole &nbsp;<b>a : w</b> &nbsp;→&nbsp; part : part &nbsp;"
        "<b>a : (w − a)</b> &nbsp;&nbsp;(subtract to find the other part)<br>"
        "Then scale either one with the same multiplier — whole number, fraction, or mixed number.")
    read_aloud(
        "Every recipe, every paint color, every bag of concrete on a job site is a ratio of parts. "
        "But the store sells the whole thing — the pitcher, the gallon, the wheelbarrow. So real "
        "people constantly cross between part-to-part and part-to-whole. Today you will too, and "
        "the numbers will not always be whole."
    )

    CONTEXTS = {
        "🍋 Lemonade stand": dict(
            a_name="concentrate", b_name="water", unit="cups", whole_name="pitcher",
            a=Fraction(3, 2), b=Fraction(9, 2), target=Fraction(10),
            story="The lemonade recipe uses <b>1&frac12; cups of concentrate for every "
                  "4&frac12; cups of water</b>. You have a <b>10-cup</b> pitcher to fill.",
            career="Food service & small business: scaling a recipe to the container you own."),
        "🧱 Mixing concrete": dict(
            a_name="cement", b_name="sand", unit="shovels", whole_name="batch",
            a=Fraction(1), b=Fraction(5, 2), target=Fraction(14),
            story="A mason mixes <b>1 shovel of cement for every 2&frac12; shovels of sand</b>. "
                  "The wheelbarrow holds <b>14 shovels</b> total.",
            career="Construction trades: too little cement and the sidewalk crumbles."),
        "🎨 Mixing paint": dict(
            a_name="blue", b_name="yellow", unit="quarts", whole_name="can of green",
            a=Fraction(9, 4), b=Fraction(3, 4), target=Fraction(5),
            story="A painter mixes <b>2&frac14; quarts of blue for every &frac34; quart of "
                  "yellow</b> to get the right green. The client needs <b>5 quarts</b> of green.",
            career="Art, design & auto body: every repaint has to match the original color."),
        "💵 Save & spend": dict(
            a_name="save", b_name="spend", unit="dollars", whole_name="paycheck",
            a=Fraction(5, 2), b=Fraction(10), target=Fraction(175, 2),
            story="Jaylen saves <b>$2&frac12; for every $10 he spends</b>. His paycheck is "
                  "<b>$87&frac12;</b>.",
            career="Personal finance: a savings ratio is a part-to-whole of every paycheck."),
        "🏀 Free throws": dict(
            a_name="made", b_name="missed", unit="shots", whole_name="attempts",
            a=Fraction(3), b=Fraction(2), target=Fraction(40),
            story="A guard makes <b>3 free throws for every 2 she misses</b>. At that rate, how "
                  "many does she make in <b>40 attempts</b>?",
            career="Sports analytics: a shooting percentage is a part-to-whole ratio."),
    }
    pick = st.selectbox("Choose a real-life situation:", list(CONTEXTS), key="d23_rl")
    c = CONTEXTS[pick]
    a, b = c["a"], c["b"]
    whole = a + b
    box("tools", "THE SITUATION", f"<p style='margin:0'>{c['story']}</p>"
        f"<p style='margin:6px 0 0 0;font-size:13px'><i>Career connection:</i> {c['career']}</p>")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Part-to-part**")
        st.markdown(f"{c['a_name']} : {c['b_name']} = {m(a)} : {m(b)}")
    with col2:
        st.markdown("**Part-to-whole** (add the parts)")
        st.markdown(f"{c['a_name']} : {c['whole_name']} = {m(a)} : {m(a)} + {m(b)} = "
                    f"{m(a)} : **{m(whole)}**")

    k = c["target"] / whole
    st.markdown(f"##### Scale to the {c['whole_name']}: {m(c['target'])} {c['unit']}")
    st.markdown(f"Scale factor = {m(c['target'])} ÷ {m(whole)} = **{m(k)}**")
    st.table([
        {"": "recipe", c["a_name"]: mixed(a), c["b_name"]: mixed(b), c["whole_name"]: mixed(whole)},
        {"": f"× {mixed(k)}", c["a_name"]: mixed(a * k), c["b_name"]: mixed(b * k),
         c["whole_name"]: mixed(c["target"])},
    ])
    st.caption(f"Check: {mixed(a * k)} + {mixed(b * k)} = {mixed(a * k + b * k)} — the parts "
               f"still add up to the whole.")

    st.markdown("##### Your turn")
    guess = st.text_input(f"{c['a_name'].capitalize()} for the {c['whole_name']} — how many {c['unit']}? (e.g. 2 1/2)",
                          key=f"d23_rl_{pick}")
    if guess:
        v = parse_mixed(guess)
        if v == a * k:
            st.success(f"Correct — {c['a_name']}: {m(a * k)} {c['unit']}.")
        elif v == c["target"] * a / b:
            st.error("That used the part-to-part ratio against the whole. Cross to part-to-whole "
                     "first: add the parts.")
        else:
            st.error("Find the whole of one recipe (add the parts), then the scale factor.")

    st.markdown("---")
    st.markdown("#### Cross products — is it the same mix?")
    box("existing", "THE CHECK",
        "Two ratios <b>a : b</b> and <b>c : d</b> are equivalent exactly when "
        "<b>a × d = b × c</b>. Use it to decide whether two mixes, written as part-to-part "
        "<i>or</i> part-to-whole, are really the same.")
    c1, c2, c3, c4 = st.columns(4)
    r1a = c1.text_input("Mix 1: part A", "1 1/2", key="d23_x1")
    r1b = c2.text_input("Mix 1: part B", "4 1/2", key="d23_x2")
    r2a = c3.text_input("Mix 2: part A", "2", key="d23_x3")
    r2b = c4.text_input("Mix 2: part B", "6", key="d23_x4")
    vals = [parse_mixed(x) for x in (r1a, r1b, r2a, r2b)]
    if all(v is not None and v > 0 for v in vals):
        p, q, r, s = vals
        left, right = p * s, q * r
        st.markdown(f"{m(p)} × {m(s)} = **{m(left)}** &nbsp;&nbsp;&nbsp; "
                    f"{m(q)} × {m(r)} = **{m(right)}**")
        if left == right:
            st.success(f"Equal cross products — same mix. Part-to-whole for both: "
                       f"{mixed(p)} : {mixed(p + q)} and {mixed(r)} : {mixed(r + s)}.")
        else:
            st.error("Different cross products — the mixes taste (or look) different.")
    else:
        st.caption("Type positive numbers, fractions, or mixed numbers in all four boxes.")

    st.markdown("##### Which statement is true?")
    box("tools", "CLASS DATA",
        "A class has <b>12 girls and 15 boys</b>. Another class has <b>8 girls out of 18 "
        "students</b>.")
    ch = st.radio("Pick one:", [
        "A — In the first class, 12 : 15 is a part-to-whole ratio.",
        "B — The first class's girls-to-whole ratio is 4 : 5.",
        "C — The second class's girls-to-boys ratio is 4 : 9.",
        "D — Both classes have a girls-to-whole ratio of 4 : 9.",
    ], index=None, key="d23_cls")
    if st.button("Check", key="d23_cls_chk"):
        if ch and ch.startswith("D"):
            st.success("Correct. First class: 12 : (12 + 15) = 12 : 27 = 4 : 9. Second class: "
                       "8 : 18 = 4 : 9. Cross products agree: 12 × 18 = 216 = 27 × 8. "
                       "Bonus: cross back to part-to-part — 12 : 15 and 8 : 10 are both 4 : 5.")
        elif ch and ch.startswith("A"):
            st.error("12 : 15 is girls to boys — part-to-part. The whole is 12 + 15 = 27.")
        elif ch and ch.startswith("B"):
            st.error("4 : 5 is girls to boys (12 : 15 simplified). Girls to whole is 12 : 27.")
        elif ch and ch.startswith("C"):
            st.error("8 : 18 is girls to the whole class. Girls to boys is 8 : (18 − 8) = 8 : 10.")
        else:
            st.warning("Pick an answer first.")
    ask_the_class("Where in your own life do you see a ratio of parts, but pay for or use the "
                  "whole? Name the parts and the whole.")

elif step == 7:
    read_aloud(
        "Recipe Lab. Your team runs a smoothie stand. The house recipe is one and a half cups of "
        "mango for every three quarters of a cup of yogurt. Customers order in different sizes, "
        "so every order needs a new, equivalent recipe. Your team draws an order, finds the scale "
        "factor, and measures it out. An answer without the scale factor scores zero."
    )
    box("tools", "The rules",
        "1) One student reads the order, one computes, one measures, one checks. "
        "2) Write the scale factor as a <b>mixed number or fraction</b>. "
        "3) Build a three-row ratio table: given → smaller ratio → order. "
        "4) Check with cross products before you measure.")

    BASE_MANGO, BASE_YOG = Fraction(3, 2), Fraction(3, 4)
    st.markdown(f"##### House recipe: {m(BASE_MANGO)} cups mango : {m(BASE_YOG)} cup yogurt")
    orders = {
        "Order 1 — 4½ cups mango": ("mango", Fraction(9, 2)),
        "Order 2 — 2¼ cups yogurt": ("yogurt", Fraction(9, 4)),
        "Order 3 — 3¾ cups mango": ("mango", Fraction(15, 4)),
        "Order 4 — 1⅛ cups yogurt": ("yogurt", Fraction(9, 8)),
        "Order 5 — ¾ cup mango": ("mango", Fraction(3, 4)),
    }
    pick = st.selectbox("Draw an order:", list(orders), key="d23_order")
    which, amt = orders[pick]
    k = amt / (BASE_MANGO if which == "mango" else BASE_YOG)
    other = BASE_YOG * k if which == "mango" else BASE_MANGO * k
    other_name = "yogurt" if which == "mango" else "mango"
    if st.checkbox("Show the teacher key for this order", key="d23_key"):
        st.markdown(f"Scale factor = {m(amt)} ÷ {m(BASE_MANGO if which == 'mango' else BASE_YOG)}"
                    f" = **{m(k)}** → {other_name} = **{m(other)} cups**")

    st.markdown("##### 🏆 Team submissions")
    if "d23_lab" not in st.session_state:
        st.session_state.d23_lab = []
    with st.form("d23_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        team = c1.text_input("Team")
        order = c2.selectbox("Order", list(orders))
        sf = c3.text_input("Scale factor (e.g. 2 1/2)")
        c4, c5 = st.columns(2)
        mango_in = c4.text_input("Cups of mango")
        yog_in = c5.text_input("Cups of yogurt")
        if st.form_submit_button("Submit"):
            sfv, mv, yv = parse_mixed(sf), parse_mixed(mango_in), parse_mixed(yog_in)
            if not team.strip() or sfv is None or mv is None or yv is None:
                st.warning("Team, scale factor, mango, and yogurt are all required "
                           "(numbers like 3, 1/2, or 2 1/4).")
            else:
                w, a = orders[order]
                true_k = a / (BASE_MANGO if w == "mango" else BASE_YOG)
                ok = sfv == true_k and mv == BASE_MANGO * true_k and yv == BASE_YOG * true_k
                st.session_state.d23_lab.append({
                    "Team": team.strip(), "Order": order.split(" — ")[0],
                    "Scale factor": mixed(sfv), "Mango": mixed(mv), "Yogurt": mixed(yv),
                    "Should be": f"× {mixed(true_k)} → {mixed(BASE_MANGO * true_k)} : "
                                 f"{mixed(BASE_YOG * true_k)}",
                    "Result": "✅" if ok else "❌",
                })
    if st.session_state.d23_lab:
        st.table(st.session_state.d23_lab)
    else:
        st.caption("No orders submitted yet.")
    ask_the_class("Order 5 used a scale factor less than 1. Did anyone's recipe get smaller? "
                  "How did your team know before measuring?")

elif step == 8:
    st.markdown("#### Engage / Explore / Enrich stations")
    tabs = st.tabs(["Engage (all)", "Explore (on-level)", "Enrich (extend)"])
    with tabs[0]:
        st.write("Independent practice, **Lesson 13 Session 4 practice (SB pp. 301-302)**:")
        box("existing", "WORKED EXAMPLE — SHAMPOO",
            "32 fl oz : $8 → ÷ 8 → 4 fl oz : $1 → × 3 → <b>12 fl oz : $3</b>.")
        practice = [
            ("A car goes 45 mi on 1½ gal of gas. How far on 4 gal?", Fraction(120)),
            ("A recipe uses 2⅔ cups flour for 2 loaves. How much flour for 5 loaves?",
             Fraction(20, 3)),
            ("Paint: 3½ qt covers 140 sq ft. How much paint for 60 sq ft?", Fraction(3, 2)),
        ]
        for i, (q, a) in enumerate(practice):
            st.markdown(f"**{i + 1}.** {q}")
            r = st.text_input("Answer:", key=f"d23_pr{i}", label_visibility="collapsed",
                              placeholder="Type a whole number, fraction, or mixed number")
            if r:
                v = parse_mixed(r)
                if v == a:
                    st.success(f"Correct — {m(a)}.")
                else:
                    st.error("Not yet. Find the scale factor first, then multiply the other "
                             "quantity by it.")
    with tabs[1]:
        st.write("Partner check: one partner solves Ian's problem for **32½ yd** by going through "
                 "a smaller ratio; the other uses a single mixed-number scale factor. Compare. "
                 "Then graph Ian's equivalent ratios as ordered pairs (yards, seconds) — "
                 "(5, 2), (10, 4), (12½, 5), (25, 10) — and describe the pattern of the points.")
    with tabs[2]:
        st.write("**Mixed numbers on both sides.** Is 2⅔ : 1⅓ equivalent to 2 : 1? To 8 : 4? "
                 "Multiply both by 3 to clear the fractions and decide. Then invent a ratio "
                 "with two mixed numbers that is equivalent to 3 : 5 and trade with a partner.")
        if st.button("Reveal", key="d23_enrich"):
            st.success("2⅔ : 1⅓ × 3 = 8 : 4 = 2 : 1. Yes to both. "
                       "One example for 3 : 5: 1½ : 2½ (scale factor ½).")

    box("existing", "EXIT TICKET",
        "An architect designs a skyscraper with <b>56 floors</b>. The height must be <b>45 m for "
        "every 10 floors</b>. Based on this ratio, what is the planned height of the skyscraper? "
        "Show your work.")
    et = st.text_input("Height in meters:", key="d23_exit")
    if et:
        v = parse_mixed(et)
        if v == 252:
            st.success("Correct — **252 m**.")
        else:
            st.error("Not yet. Scale factor = 56 ÷ 10. Write it as a mixed number, then "
                     "multiply 45 by it.")
    st.caption("Answer: 56 ÷ 10 = 5⅗; 45 × 5⅗ = 225 + 27 = 252 m. Or go through a smaller ratio: "
               "10 : 45 → ÷ 5 → 2 : 9 → × 28 → 56 : 252. Look for the scale factor in the work.")

    st.markdown("---")
    st.markdown("#### 🔎 Observer Notes (running log)")
    st.caption("A running teacher log carried day to day. Add what you noticed in class today, "
               "then Save — copy it into tomorrow's app to keep the thread going.")
    for n in st.session_state.observer_notes:
        st.markdown(f"**{n['date']}:** {n['note']}")
    new_note = st.text_area("Add a new observation:", key="new_observer_note")
    if st.button("Save observation"):
        if new_note.strip():
            st.session_state.observer_notes.append(
                {"date": f"Day 23 — {datetime.now().strftime('%Y-%m-%d')}",
                 "note": new_note.strip()}
            )
            save_notes(st.session_state.observer_notes)
            st.success("Saved to the observer log.")
            st.rerun()
        else:
            st.warning("Write a note first.")


st.markdown("---")
c_back, c_next = st.columns([1, 1])
if c_back.button("⬅ Back", disabled=(step == 0)):
    st.session_state.step = max(0, step - 1)
    st.rerun()
if c_next.button("Next ➡", disabled=(step == len(STEPS) - 1)):
    st.session_state.step = min(len(STEPS) - 1, step + 1)
    st.rerun()

st.caption("Standards in play: 6.RP.A.1 (part-to-part & part-to-whole) · 6.RP.A.3 (use ratio and rate reasoning to solve problems) · "
           "6.RP.A.3a (make tables of equivalent ratios; find missing values) · "
           "6.NS.A.1 / 5.NF.B.4 (multiplying by fractions and mixed numbers).")
st.markdown(
    "<div style='text-align:center;color:#8a939c;font-size:11px;margin-top:18px;'>"
    "www.cognitivecloud.ai &middot; Developed by Xavier Honablue, M.Ed"
    "</div>",
    unsafe_allow_html=True,
)
