#!/usr/bin/env python3
"""Builds preview/: the site rewritten to the Aurora Care messaging guide, for review before it replaces the live pages.

Run from the repository root: python3 tools/build_preview.py
It reads the live pages, applies the guide's changes and writes preview/<page>.html. The live pages are not touched.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "preview"
PAGES = ["index.html", "overview.html", "star-features.html", "angel-features.html", "care-intelligence.html",
         "personas.html", "team.html", "contact.html", "privacy.html", "pricing.html", "aurora-private-preview.html"]

NO_REPLACE = "Aurora Care does not replace clinicians, emergency services, or medical diagnosis."

# The guide: no internal persona terms in menus; plain names instead.
MENU = [("index.html", "Home"), ("overview.html", "How it works"), ("star-features.html", "For your parent"),
        ("angel-features.html", "For family"), ("team.html", "Team")]


def nav(page):
    links = "".join(
        f'<a{" aria-current=\"page\"" if href == page else ""} href="{href}">{label}</a>' for href, label in MENU)
    contact = f'<a{" aria-current=\"page\"" if page == "contact.html" else ""} class="nav-cta" href="contact.html">Contact</a>'
    return (f'<nav class="site-nav" aria-label="Main navigation">{links}{contact}'
            '<a class="nav-signin" href="https://aurora.ragaven.com/">Sign in</a></nav>')


# Exact text changes from the guide: headings without persona terms, no timing promises, "see" not "watch".
TEXT = [
    ("Know what is changing before it becomes urgent.", "Know how they’re really doing."),
    ("shared, watched, and acted on", "shared and acted on"),
    ("The Star stays independent. Angels stay informed.", "Your parent stays independent. Family stays informed."),
    ("<h3>Trusted Angels</h3>", "<h3>Trusted family</h3>"),
    (">For Stars<", ">For your parent<"),
    (">For Angels<", ">For family<"),
    ("Star control", "They stay in control"),
    ("Watch what changes from the Star’s normal pattern.", "See what changes from their own usual."),
    ("Catch drift before it becomes urgent.", "See change while there’s still time to talk it through."),
    ("watch drift early and alert quickly when the moment needs action",
     "see change early and alert quickly when they need help right away"),
    ("fall detected", "falls"),
    ("Analyze risk before incidents happen.", "Compared with their own usual."),
    ("What Aurora Care Intelligence watches", "What Aurora Care Intelligence looks at"),
    ("Risks assessed from multiple signals and trends, and personalized to the Star's personal profile and history.",
     "Each reading is compared with your parent’s own history and profile, so meaningful change is easier to see."),
    ("<title>Star Features | Aurora Care</title>", "<title>For your parent | Aurora Care</title>"),
    ("<title>Angel Features | Aurora Care</title>", "<title>For family | Aurora Care</title>"),
    ("<title>Aurora Care Overview | Aurora Care by Ragaven</title>", "<title>How it works | Aurora Care by Ragaven</title>"),
]

# The guide: define Star and Angel before using them.
DEFINE = {
    "star-features.html": ("Aurora Care helps senior adults keep routine, dignity, and control while making care changes easier to see.",
                           "Aurora Care helps your parent keep their routine, dignity, and control while making changes in their health easier to see. In the app, your parent is called the Star."),
    "angel-features.html": ("Angels can observe changes, receive alerts, and help the Star take the right next step.",
                            "In the app, the family members and caregivers your parent chooses are called Angels. They see changes, receive alerts, and help your parent take the right next step."),
}

HOME_MAIN = """<main>
      <section class="problem-hero home-hero-simple">
        <div class="wrap home-hero-grid">
          <div class="problem-hero-copy">
            <p class="eyebrow">Aurora Care by Ragaven</p>
            <h1>Know how they’re really doing. Get help when it counts.</h1>
            <p class="lead">A 30-second check on your aging parent’s own phone gives you a daily picture of their vitals, medicines, and appointments, compared with their own usual.</p>
            <div class="button-row">
              <a class="button primary" href="contact.html">Join the waitlist</a>
            </div>
            <p class="pv-for">For families caring for a parent who lives at home, and for the parent who wants to stay independent.</p>
          </div>
          <figure class="pv-hero-figure"><img src="../assets/messaging/thirty-second-tall.jpg" alt="An older woman takes a 30-second check on her phone; her daughter sees heart rate and breathing rate within her usual."></figure>
        </div>
      </section>

      <section class="section pv-benefit">
        <div class="wrap pv-benefit-grid">
          <figure><img src="../assets/messaging/thirty-second-wide.jpg" alt="Mom checks in for 30 seconds in her kitchen; on her daughter's phone, heart rate and breathing rate are within her usual and blood pressure has been higher than usual for four days."></figure>
          <div>
            <p class="eyebrow">Daily picture</p>
            <h2>See the trends calls and texts miss.</h2>
            <p class="lead">A 30-second check on their phone shows how blood pressure, heart rate, and other vitals compare with their usual, and whether they are taking their medicines on schedule.</p>
            <ul class="pv-points">
              <li>Vitals come from the phone, watch, or band they already own. No extra hardware to buy.</li>
              <li>Each reading is compared with their own history and profile.</li>
              <li>Missed medicines show up as a pattern the family can see.</li>
            </ul>
          </div>
        </div>
      </section>

      <section class="section pv-benefit pv-benefit-alt">
        <div class="wrap pv-benefit-grid">
          <figure><img src="../assets/messaging/voice-help-wide.jpg" alt="An older woman sitting on the floor says &quot;Hey Siri, Aurora help&quot;; her phone on a table across the room hears her and her care circle is alerted."></figure>
          <div>
            <p class="eyebrow">Help right away</p>
            <h2>Help arrives even when the phone is out of reach.</h2>
            <p class="lead">If they fall, leave a familiar area, or show vitals far outside their usual range, the people they chose get an alert. They can also call for help by voice from across the room by saying “Hey Siri, Aurora help,” as long as the phone is within earshot.</p>
            <ul class="pv-points">
              <li>No wearable or button needed for voice help.</li>
              <li>Alerts repeat every 5 minutes until someone responds.</li>
              <li>Safe-area alerts work when they have their phone with them.</li>
            </ul>
            <p class="pv-note">{no_replace}</p>
          </div>
        </div>
      </section>

      <section class="section pv-benefit">
        <div class="wrap pv-benefit-grid">
          <figure><img src="../assets/messaging/safe-area-wide.jpg" alt="An older man walks past the edge of his safe area; his family gets an alert asking whether they want to check in."></figure>
          <div>
            <p class="eyebrow">One place</p>
            <h2>Everything to support their care, in one place.</h2>
            <p class="lead">Book the doctor or lab visit together and bring one report of vitals, medicines, and recent labs. Your loved one decides who sees what.</p>
            <ul class="pv-points">
              <li>A health summary for 7, 30, or 90 days, with a report to share with their doctor.</li>
              <li>Lab results read from a photo of the paper copy.</li>
              <li>Safe-area alerts sit alongside their vitals, labs, and medicines.</li>
            </ul>
          </div>
        </div>
      </section>

      <section class="section home-video-section">
        <div class="wrap split home-video-wrap">
          <div>
            <p class="eyebrow">One-minute overview</p>
            <h2>See Aurora Care in a minute.</h2>
            <p class="lead">A daily 30-second check, a clear update for the family, and help when it’s needed.</p>
          </div>
          <div class="video-shell">
            <video controls poster="../assets/aurora-one-minute-poster.jpg">
              <source src="../assets/aurora-one-minute.mp4" type="video/mp4">
            </video>
          </div>
        </div>
      </section>

    </main>"""

# The family page carries the voice-help and safe-area pictures next to those features.
FAMILY_FIGURES = """<section class="section pv-figures"><div class="wrap pv-figure-row">
<figure><img src="../assets/messaging/voice-help-tall.jpg" alt="She says &quot;Hey Siri, Aurora help&quot;; her phone hears her from across the room and her care circle is alerted."></figure>
<figure><img src="../assets/messaging/safe-area-square.jpg" alt="An alert when he goes beyond his safe area, alongside his vitals, labs, and medicines."></figure>
</div></section>"""

PREVIEW_CSS = '<link rel="stylesheet" href="preview.css">'


def build(page):
    s = (ROOT / page).read_text()
    s = re.sub(r'(src|href|poster)="assets/', r'\1="../assets/', s)
    s = s.replace('href="styles.css"', 'href="../styles.css"')
    s = s.replace('src="script.js"', 'src="../script.js"')
    s = s.replace("<head>", '<head>\n    <meta name="robots" content="noindex, nofollow">', 1)
    s = s.replace('href="../styles.css">', 'href="../styles.css">' + PREVIEW_CSS, 1)
    s, n = re.subn(r'<nav class="site-nav"[^>]*>.*?</nav>', nav(page), s, count=1, flags=re.S)
    assert n == 1, page
    for old, new in TEXT:
        s = s.replace(old, new)
    if page in DEFINE:
        old, new = DEFINE[page]
        assert old in s, page
        s = s.replace(old, new)
    if page == "index.html":
        s, n = re.subn(r"<main>.*?</main>", HOME_MAIN.replace("{no_replace}", NO_REPLACE), s, count=1, flags=re.S)
        assert n == 1
    if page == "angel-features.html":
        s = s.replace("</main>", FAMILY_FIGURES + "</main>", 1)
    if NO_REPLACE not in s and "does not replace clinicians" not in s:
        s, n = re.subn(r"(<footer[^>]*>)", r'\1<p class="pv-footnote">' + NO_REPLACE + "</p>", s, count=1)
        assert n == 1, page
    (OUT / page).write_text(s)


OUT.mkdir(exist_ok=True)
for p in PAGES:
    build(p)
print(f"built {len(PAGES)} preview pages in {OUT}")
