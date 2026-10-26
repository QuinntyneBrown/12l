"""Marketing page at /welcome and its 30-second pitch video dialog (L1-020, L2-078 to L2-083).

Copy rules (ADR general/0005): headlines of 3 to 6 words, one supporting line, scannable
points, and size wording that fits the size lock: "built for size 12 and L", "big sizes,
finally in one place", never "only".
"""
from mk import *

MEDIA = f"{A}media/"
STATIC_NA = {"loading": "Static content ships with the app; the page calls no 12L API endpoint.",
             "empty": "The page always has content.",
             "error": "Static content cannot fail to load once the app is served; the video has its own error state."}

SHOPPER_POINTS = [("Every pair is a men’s US 12", "Sneakers, boots and dress shoes, all in your size."),
                  ("Every top, jacket and pant is a men’s L", "Browse without a size filter."),
                  ("Honest condition", "Five grades, and flaws named up front.")]
SELLER_POINTS = [("List in minutes", "Photos, a price and the condition. The size is set for you."),
                 ("Buyers already wear your size", "Sell to people your size, not the whole internet."),
                 ("10% fee, only when it sells", "Taken when the order completes. Listing is free.")]
STEPS = [("List it", "Add photos, a price and the condition."),
         ("Sell it", "A buyer pays. You ship within 5 business days."),
         ("Get paid", "The order completes and your payout is on its way.")]


def shapes(quiet: bool = False) -> str:
    q = " shapes--quiet" if quiet else ""
    return (f'<div class="shapes{q}" aria-hidden="true"><span class="shapes__shape shapes__shape--brand"></span>'
            '<span class="shapes__shape shapes__shape--tone"></span><span class="shapes__shape shapes__shape--light"></span>'
            '<span class="shapes__stripes"></span></div>')


def seller_href(member: bool) -> str:
    return P("sell") if member else P("register")


def poster() -> str:
    return (f'<a class="video-poster" href="{D("pitch-video")}"><img src="{MEDIA}12l-pitch-poster.png" alt="" width="1920" height="1080">'
            f'<span class="video-poster__play">{ic("play")}Watch the 30-second pitch</span>'
            '<span class="video-poster__meta" aria-hidden="true">0:30</span></a>')


def hero(member: bool) -> str:
    actions = btn("Shop the catalog", "primary lg", P("catalog")) + btn("Start selling", "lg", seller_href(member))
    return (f'<section class="marketing-hero" aria-labelledby="welcome-title">{shapes()}<div class="marketing-hero__inner">'
            '<div><p class="marketing-hero__eyebrow">Men’s US 12 shoes · Men’s L clothing</p>'
            '<h1 class="marketing-hero__title" id="welcome-title">Built for size <em>12 and L.</em></h1>'
            '<p class="marketing-hero__lede">Big sizes, finally in one place. Shop pieces that already fit, or sell yours to people your size.</p>'
            f'<div class="marketing-hero__actions">{actions}</div></div>'
            f'<div class="marketing-hero__media">{poster()}</div></div></section>')


def points(items) -> str:
    return '<ul class="feature-band__points" role="list">' + "".join(
        f'<li class="feature-band__point"><strong>{t}</strong><span>{d}</span></li>' for t, d in items) + "</ul>"


def band(bid: str, eyebrow: str, title: str, body: str, action: str = "", mod: str = "") -> str:
    a = f'<div class="feature-band__actions">{action}</div>' if action else ""
    return (f'<section class="feature-band {mod}" aria-labelledby="{bid}"><div class="feature-band__inner">'
            f'<div><p class="feature-band__eyebrow">{eyebrow}</p><h2 class="feature-band__title" id="{bid}">{title}</h2>{a}</div>'
            f'<div>{body}</div></div></section>')


def steps() -> str:
    return '<ol class="steps">' + "".join(
        f'<li class="steps__item"><h3 class="steps__title">{t}</h3><p class="steps__text">{d}</p></li>' for t, d in STEPS) + "</ol>"


def closing(member: bool) -> str:
    actions = btn("Shop the catalog", "primary lg", P("catalog")) + btn("Start selling", "lg", seller_href(member))
    return (f'<section class="marketing-hero marketing-hero--closing" aria-labelledby="closing-title">{shapes(quiet=True)}'
            '<div class="marketing-hero__inner"><div><h2 class="marketing-hero__title" id="closing-title">Your size is <em>waiting.</em></h2>'
            f'<p class="marketing-hero__lede">New listings every day, every one in men’s US 12 or men’s L.</p>'
            f'<div class="marketing-hero__actions">{actions}</div></div></div></section>')


def welcome(member: bool) -> Page:
    main = (hero(member)
            + band("shoppers-title", "For shoppers", "Everything already fits you.", points(SHOPPER_POINTS),
                   btn("Browse the catalog", "primary", P("catalog")))
            + band("sellers-title", "For sellers", "Sell to people your size.", points(SELLER_POINTS),
                   btn("Start selling", "primary", seller_href(member)), "feature-band--surface")
            + band("how-title", "How it works", "Three steps. That’s it.", steps(), mod="feature-band--stacked")
            + closing(member))
    return Page(main=main, user="member" if member else "guest", main_class="marketing")


wl = screen("welcome", "page", "Marketing page", route="/welcome",
            reqs=["L2-078", "L2-079", "L2-080", "L2-081", "L2-082", "L2-083"], na=STATIC_NA)


@wl.state("default", "Signed out: hero with the video poster, shoppers, sellers, three steps and a closing CTA; Start selling goes to /join.")
def _():
    pg = welcome(False)
    pg.notes = note("Shapes drift slowly; prefers-reduced-motion stops them. The poster opens the video dialog; nothing autoplays.",
                    "top: 6rem; right: 1rem;")
    return pg


@wl.state("signed-in", "Signed in: the same page; Start selling goes to /sell.")
def _():
    return welcome(True)


# ---------------------------------------------------------------------------
# Pitch video dialog
# ---------------------------------------------------------------------------
TRANSCRIPT = f"{MEDIA}12l-pitch.txt"


def player(state: str) -> str:
    track_default = " default" if state == "captions" else ""
    video = (f'<video controls playsinline preload="metadata" poster="{MEDIA}12l-pitch-poster.png" aria-label="12L in 30 seconds">'
             f'<source src="{MEDIA}12l-pitch.mp4" type="video/mp4"><source src="{MEDIA}12l-pitch.webm" type="video/webm">'
             f'<track kind="captions" src="{MEDIA}12l-pitch.vtt" srclang="en" label="English"{track_default}></video>')
    overlay = ""
    if state == "loading":
        overlay = ('<div class="video-player__state" role="status"><span class="spinner spinner--lg" aria-hidden="true"></span>'
                   '<p>Loading video…</p></div>')
    elif state == "error":
        overlay = (f'<div class="video-player__state" role="alert">{ic("alert", "icon icon--lg")}<strong>The video didn’t load</strong>'
                   f'<p>Check your connection and try again, or read the transcript.</p>{btn("Try again", "primary", icon="refresh")}</div>')
    playing = state in ("default", "captions")
    play = btn("Pause", "primary", icon="pause") if playing else btn("Play", "primary", icon="play", attrs="disabled")
    cc_on = state == "captions"
    cc = btn("Captions", "", icon="captions", attrs=f'aria-pressed="{"true" if cc_on else "false"}"' + ("" if state != "error" else " disabled"))
    controls = "" if state == "error" else play + cc
    link = f'<a class="btn btn--link video-player__transcript" href="{TRANSCRIPT}">Read the transcript</a>'
    return (f'<div class="video-player"><div class="video-player__frame">{video}{overlay}</div>'
            f'<div class="video-player__controls">{controls}{link}</div></div>')


pv = screen("pitch-video", "dialog", "Pitch video", opens_from="welcome", reqs=["L2-080", "L2-081", "L2-082"],
            na={"busy": "Playing a video sends nothing to 12L API.", "invalid": "Nothing to fill in."})


@pv.state("default", "Playing after the visitor pressed Watch: native controls plus Pause, Captions and the transcript link.")
def _():
    d = Dialog(bg=("welcome", "default"), html=dialog("12L in 30 seconds", player("default"), size="lg"))
    d.notes = note("Opens only from the poster button and plays with sound because the visitor asked. Space or K pauses; Esc closes and returns focus to the poster.",
                   "top: 1rem; left: 1rem;")
    return d


@pv.state("loading", "The video is buffering: spinner over the poster; Play waits.")
def _():
    return Dialog(bg=("welcome", "default"), html=dialog("12L in 30 seconds", player("loading"), size="lg"))


@pv.state("error", "The video failed to load: plain message, Try again and the transcript; the page behind still works once closed.")
def _():
    return Dialog(bg=("welcome", "default"), html=dialog("12L in 30 seconds", player("error"), size="lg"))


@pv.state("captions", "Captions on: the English track shows; the Captions button is pressed.")
def _():
    d = Dialog(bg=("welcome", "default"), html=dialog("12L in 30 seconds", player("captions"), size="lg"))
    d.notes = note("Captions come from 12l-pitch.vtt and stay on for the rest of the visit.", "top: 1rem; left: 1rem;")
    return d
