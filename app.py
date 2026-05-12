import json

import requests
import streamlit as st

st.set_page_config(
    page_title="Iceland Trip Planner",
    page_icon="IS",
    layout="wide",
)


# -----------------------------
# Data
# -----------------------------
TRIP_DAYS = [
    {
        "day": 1,
        "date": "May 21",
        "title": "Arrival in Reykjavik",
        "region": "Reykjavik",
        "pace": "Easy",
        "drive": "Local",
        "themes": ["City", "Food", "Views"],
        "description": "Ease into the trip with colorful streets, harbor air, and a mellow first evening.",
        "highlights": [
            "Hallgrimskirkja",
            "Harpa Concert Hall",
            "Sun Voyager",
            "Rainbow Street",
            "Icelandic hot dogs and pastries",
            "Harbor walk at sunset",
        ],
        "map_query": "Reykjavik Iceland",
        "tip": "Keep this day intentionally loose so delayed flights do not ripple through the trip.",
    },
    {
        "day": 2,
        "date": "May 22",
        "title": "Golden Circle",
        "region": "Golden Circle",
        "pace": "Moderate",
        "drive": "2-3 hr",
        "themes": ["Waterfalls", "Geothermal", "Classic Iceland"],
        "description": "A polished loop through tectonic rifts, erupting geothermal fields, and big waterfall drama.",
        "highlights": [
            "Thingvellir National Park",
            "Geysir Geothermal Area",
            "Gullfoss Waterfall",
            "Geothermal Bakery Tour",
            "Secret Lagoon Hot Spring",
        ],
        "links": {
            "Geothermal Bakery": "https://fontana.is/rye-bread-tour",
            "Secret Lagoon": "https://secretlagoon.is",
        },
        "map_query": "Golden Circle Iceland",
        "tip": "Start early and put Thingvellir first for quieter trails.",
    },
    {
        "day": 3,
        "date": "May 23",
        "title": "South Coast Adventure",
        "region": "South Coast",
        "pace": "Full",
        "drive": "2-3 hr",
        "themes": ["Waterfalls", "Black Sand", "Coast"],
        "description": "Waterfall spray, basalt cliffs, black sand beaches, and a night tucked near Vik.",
        "highlights": [
            "Seljalandsfoss",
            "Skogafoss",
            "Reynisfjara Black Sand Beach",
            "Vik Village",
            "Overnight at Paradise Cottage",
        ],
        "map_query": "Reynisfjara Black Sand Beach Iceland",
        "tip": "Bring a waterproof shell and keep a serious distance from Reynisfjara sneaker waves.",
    },
    {
        "day": 4,
        "date": "May 24",
        "title": "Glacier Adventure Day",
        "region": "South Coast",
        "pace": "Full",
        "drive": "1-2 hr",
        "themes": ["Adventure", "Glacier", "Views"],
        "description": "The high-adrenaline day: crampons, blue ice, and optional flight or zipline energy.",
        "highlights": [
            "Glacier hike at Solheimajokull",
            "Ziplining or paragliding",
        ],
        "links": {
            "Glacier Hike": "https://www.getyourguide.com/vik-l32622/solheimajokull-guided-glacier-hike-adventure-easy-t68907?ranking_uuid=3c523caf-c5ff-4dae-a36f-c6fa63114e5c&date_from=2026-05-24",
            "True Adventure Iceland": "https://trueadventure.is",
        },
        "map_query": "Solheimajokull Glacier Iceland",
        "tip": "Book the glacier slot first, then fit the optional activity around it.",
    },
    {
        "day": 5,
        "date": "May 25",
        "title": "Lagoon Recovery Day",
        "region": "Reykjanes",
        "pace": "Easy",
        "drive": "1 hr",
        "themes": ["Hot Springs", "Spa", "Recovery"],
        "description": "A soft reset in mineral-rich water after the South Coast push.",
        "highlights": [
            "Blue Lagoon",
            "Sky Lagoon",
            "Slow dinner back in Reykjavik",
        ],
        "links": {
            "Blue Lagoon": "https://www.bluelagoon.com/day-visit/the-blue-lagoon",
        },
        "map_query": "Blue Lagoon Iceland",
        "tip": "Choose one lagoon as the main event instead of trying to squeeze both into one perfect day.",
    },
    {
        "day": 6,
        "date": "May 26",
        "title": "Snaefellsnes Peninsula",
        "region": "Snaefellsnes",
        "pace": "Full",
        "drive": "3 hr",
        "themes": ["Mountains", "Coast", "Wildlife"],
        "description": "A mini-Iceland day with lava fields, sea cliffs, beaches, mountains, and puffin chances.",
        "highlights": [
            "Snaefellsjokull National Park",
            "Kirkjufell Mountain",
            "Djualonssandur Beach",
            "Budakirkja",
            "Ytri Tunga Beach",
            "Londrangar Basalt Cliffs",
            "Puffin spotting",
        ],
        "map_query": "Snaefellsnes Peninsula Iceland",
        "tip": "This is the biggest driving day, so pack snacks and keep the stop list flexible.",
    },
    {
        "day": 7,
        "date": "May 27",
        "title": "Flex / Relax Day",
        "region": "Reykjavik",
        "pace": "Flexible",
        "drive": "Local",
        "themes": ["City", "Wildlife", "Food"],
        "description": "A choose-your-own Reykjavik day for weather, energy, and whatever sounded good mid-trip.",
        "highlights": [
            "Whale watching",
            "Horseback riding",
            "Food tour",
            "Lava tunnel tour",
            "Museums and cafes",
            "Northern lights tour, season dependent",
        ],
        "map_query": "Reykjavik Harbor Iceland",
        "tip": "Use this as a weather buffer if an earlier outdoor day needs to move.",
    },
    {
        "day": 8,
        "date": "May 28",
        "title": "Reykjadalur Hot Spring Hike",
        "region": "Southwest",
        "pace": "Moderate",
        "drive": "1 hr",
        "themes": ["Hot Springs", "Hiking", "Geothermal"],
        "description": "A steam-valley hike ending in a warm river soak surrounded by mossy hills.",
        "highlights": [
            "Reykjadalur Thermal River",
            "Hot spring hike",
            "Bakery or cafe stop in Hveragerdi",
        ],
        "links": {
            "Reykjadalur": "https://share.google/ht54YMlXlbSVLNEzw",
        },
        "map_query": "Reykjadalur Hot Spring Thermal River",
        "tip": "Wear hiking shoes and pack the swimsuit where it is easy to grab.",
    },
]

PACKING_ITEMS = [
    "Waterproof jacket",
    "Warm layers / thermals",
    "Hiking shoes",
    "Swimsuit",
    "Portable charger",
    "Gloves and beanie",
    "Camera",
    "Reusable water bottle",
    "Snacks for road trips",
    "Sleep mask for bright late-May nights",
]

PUFFIN_FACTS = [
    "Puffins flap their wings incredibly fast, but they are much more graceful underwater than in the air.",
    "In Iceland, puffins are most commonly seen from late April through August.",
    "A puffin's colorful beak gets brightest during breeding season.",
    "Young puffins are called pufflings, which is almost unfairly charming.",
    "Puffins often return to the same nesting burrow year after year.",
]

WEATHER_CITIES = {
    "Reykjavik": "Reykjavik",
    "Vik": "Vik",
    "Hveragerdi": "Hveragerdi",
}

GOLDEN_CIRCLE_LANDMARKS = [
    {
        "name": "Reykjavik",
        "description": "Start / return base",
        "lat": 64.1466,
        "lon": -21.9426,
    },
    {
        "name": "Thingvellir National Park",
        "description": "Rift valley and historic parliament site",
        "lat": 64.2559,
        "lon": -21.1295,
    },
    {
        "name": "Laugarvatn Fontana",
        "description": "Geothermal bakery tour",
        "lat": 64.2142,
        "lon": -20.7335,
    },
    {
        "name": "Geysir Geothermal Area",
        "description": "Strokkur geyser eruptions",
        "lat": 64.3137,
        "lon": -20.3009,
    },
    {
        "name": "Gullfoss Waterfall",
        "description": "Two-tier glacial waterfall",
        "lat": 64.3271,
        "lon": -20.1199,
    },
    {
        "name": "Secret Lagoon",
        "description": "Hot spring soak in Fludir",
        "lat": 64.1374,
        "lon": -20.3094,
    },
]

SOUTH_COAST_LANDMARKS = [
    {
        "name": "Reykjavik",
        "description": "Start / return base",
        "lat": 64.1466,
        "lon": -21.9426,
    },
    {
        "name": "Seljalandsfoss",
        "description": "Walk-behind waterfall",
        "lat": 63.6156,
        "lon": -19.9886,
    },
    {
        "name": "Skogafoss",
        "description": "Powerful waterfall with viewpoint stairs",
        "lat": 63.5321,
        "lon": -19.5114,
    },
    {
        "name": "Reynisfjara Black Sand Beach",
        "description": "Basalt columns and black sand beach",
        "lat": 63.4043,
        "lon": -19.0449,
    },
    {
        "name": "Vik",
        "description": "South Coast village stop",
        "lat": 63.4186,
        "lon": -19.0060,
    },
]

SNAEFELLSNES_LANDMARKS = [
    {
        "name": "Reykjavik",
        "description": "Start / return base",
        "lat": 64.1466,
        "lon": -21.9426,
    },
    {
        "name": "Ytri Tunga Beach",
        "description": "Seal spotting beach",
        "lat": 64.8034,
        "lon": -23.0806,
    },
    {
        "name": "Budakirkja",
        "description": "Black church near Budir",
        "lat": 64.8217,
        "lon": -23.3840,
    },
    {
        "name": "Djualonssandur Beach",
        "description": "Lava beach and shipwreck remains",
        "lat": 64.7538,
        "lon": -23.9034,
    },
    {
        "name": "Londrangar Basalt Cliffs",
        "description": "Sea stacks and coastal viewpoints",
        "lat": 64.7355,
        "lon": -23.7753,
    },
    {
        "name": "Snaefellsjokull National Park",
        "description": "Glacier-capped volcano and lava coast",
        "lat": 64.8057,
        "lon": -23.7731,
    },
    {
        "name": "Kirkjufell Mountain",
        "description": "Iconic mountain and waterfall viewpoint",
        "lat": 64.9417,
        "lon": -23.3069,
    },
]

TRIP_DAYS[1]["map_landmarks"] = GOLDEN_CIRCLE_LANDMARKS
TRIP_DAYS[2]["map_landmarks"] = SOUTH_COAST_LANDMARKS
TRIP_DAYS[5]["map_landmarks"] = SNAEFELLSNES_LANDMARKS


# -----------------------------
# Helpers
# -----------------------------
def embed_map(query, height=330):
    url = f"https://www.google.com/maps?q={query}&output=embed"
    st.components.v1.iframe(url, height=height)


def embed_landmark_map(landmarks, height=430):
    marker_data = json.dumps(landmarks)
    html = f"""
    <div id="map" style="height:{height}px; width:100%; border-radius:8px; overflow:hidden;"></div>
    <link
        rel="stylesheet"
        href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        const landmarks = {marker_data};
        const map = L.map("map", {{
            scrollWheelZoom: false,
        }});

        L.tileLayer("https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png", {{
            attribution: "&copy; OpenStreetMap contributors",
        }}).addTo(map);

        const points = landmarks.map((place) => [place.lat, place.lon]);
        const route = L.polyline(points, {{
            color: "#cc6b49",
            weight: 4,
            opacity: 0.9,
        }}).addTo(map);

        landmarks.forEach((place, index) => {{
            const marker = L.marker([place.lat, place.lon]).addTo(map);
            const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${{place.lat}},${{place.lon}}`;
            marker.bindPopup(`
                <strong>${{index + 1}}. ${{place.name}}</strong><br />
                ${{place.description}}<br />
                <a href="${{mapsUrl}}" target="_blank" rel="noopener noreferrer">Open in Google Maps</a>
            `);
        }});

        map.fitBounds(route.getBounds(), {{
            padding: [28, 28],
        }});
    </script>
    """
    st.components.v1.html(html, height=height)


@st.cache_data(ttl=900)
def get_weather(city):
    api_key = st.secrets.get("WEATHER_API_KEY")
    if not api_key:
        return None

    url = (
        "https://api.openweathermap.org/data/2.5/weather?"
        f"q={city},IS&appid={api_key}&units=metric"
    )

    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        return None

    return {
        "temp": round(data["main"]["temp"]),
        "condition": data["weather"][0]["description"].title(),
        "humidity": data["main"]["humidity"],
        "wind": round(data["wind"]["speed"]),
    }


def pill(text):
    return f'<span class="pill">{text}</span>'


def day_card(trip_day):
    theme_pills = " ".join(pill(theme) for theme in trip_day["themes"])
    puffin_badge = ""
    if "Wildlife" in trip_day["themes"] or any("puffin" in item.lower() for item in trip_day["highlights"]):
        puffin_badge = '<div class="puffin-badge">(o)> puffin watch</div>'

    st.markdown(
        f"""
        <section class="day-card">
            <div class="day-topline">
                <span>Day {trip_day["day"]} · {trip_day["date"]}</span>
                <span>{trip_day["region"]}</span>
            </div>
            <h3>{trip_day["title"]}</h3>
            <p class="day-description">{trip_day["description"]}</p>
            <div class="pill-row">
                {pill(trip_day["pace"])}
                {pill(trip_day["drive"])}
                {theme_pills}
            </div>
            {puffin_badge}
        </section>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label, value, detail):
    st.markdown(
        f"""
        <div class="metric-card">
            <span>{label}</span>
            <strong>{value}</strong>
            <small>{detail}</small>
        </div>
        """,
        unsafe_allow_html=True,
    )


def puffin_easter_egg(day):
    if "Wildlife" not in day["themes"] and not any("puffin" in item.lower() for item in day["highlights"]):
        return

    fact = PUFFIN_FACTS[(day["day"] - 1) % len(PUFFIN_FACTS)]
    if st.button("Puffin peek", key=f"puffin_{day['day']}"):
        st.markdown(
            f"""
            <div class="puffin-note">
                <strong>Little puffin note:</strong> {fact}
            </div>
            """,
            unsafe_allow_html=True,
        )


# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
    :root {
        --ink: #102126;
        --muted: #5b6b70;
        --mist: #f4f8f7;
        --ice: #d9eef0;
        --aqua: #4b9ca7;
        --moss: #6f8b62;
        --lava: #cc6b49;
        --charcoal: #1d2c30;
        --line: rgba(16, 33, 38, .12);
    }

    .stApp {
        color: var(--ink);
        background:
            radial-gradient(circle at 12% 0%, rgba(143, 198, 198, .34), transparent 28rem),
            linear-gradient(180deg, #eef8f7 0%, #f7fbf9 42%, #eef3ee 100%);
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3 {
        letter-spacing: 0;
    }

    .hero {
        min-height: 360px;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        padding: clamp(2rem, 5vw, 4.5rem);
        border-radius: 0;
        color: white;
        background:
            linear-gradient(180deg, rgba(16, 33, 38, .16), rgba(16, 33, 38, .78)),
            url("https://images.unsplash.com/photo-1504829857797-ddff29c27927?auto=format&fit=crop&w=1800&q=80");
        background-position: center;
        background-size: cover;
        margin-bottom: 1.25rem;
    }

    .hero h1 {
        font-size: clamp(2.4rem, 6vw, 5.4rem);
        line-height: .95;
        margin: 0 0 .8rem;
        color: white;
        max-width: 900px;
    }

    .hero p {
        color: rgba(255,255,255,.9);
        font-size: 1.05rem;
        max-width: 690px;
        margin: 0;
    }

    .metric-card {
        min-height: 116px;
        padding: 1.1rem 1.2rem;
        border: 1px solid var(--line);
        background: rgba(255,255,255,.72);
        border-radius: 8px;
    }

    .metric-card span,
    .metric-card small {
        display: block;
        color: var(--muted);
    }

    .metric-card strong {
        display: block;
        color: var(--charcoal);
        font-size: 1.9rem;
        line-height: 1.1;
        margin: .35rem 0;
    }

    .day-card {
        padding: 1.15rem 1.2rem 1.25rem;
        border: 1px solid var(--line);
        border-left: 6px solid var(--aqua);
        border-radius: 8px;
        background: rgba(255,255,255,.82);
        margin-bottom: .85rem;
    }

    .day-topline {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        color: var(--muted);
        font-size: .82rem;
        text-transform: uppercase;
        letter-spacing: .06em;
        margin-bottom: .45rem;
    }

    .day-card h3 {
        margin: 0 0 .45rem;
        color: var(--charcoal);
        font-size: 1.35rem;
    }

    .day-description {
        margin: 0 0 .8rem;
        color: var(--muted);
    }

    .pill-row {
        display: flex;
        flex-wrap: wrap;
        gap: .45rem;
    }

    .pill {
        display: inline-flex;
        align-items: center;
        min-height: 28px;
        padding: .2rem .62rem;
        border-radius: 999px;
        color: #173136;
        background: #dcefed;
        border: 1px solid rgba(75, 156, 167, .28);
        font-size: .82rem;
        font-weight: 650;
    }

    .puffin-badge {
        display: inline-flex;
        margin-top: .8rem;
        padding: .28rem .62rem;
        border-radius: 999px;
        background: rgba(111, 139, 98, .16);
        border: 1px dashed rgba(111, 139, 98, .55);
        color: #405a36;
        font-size: .82rem;
        font-weight: 700;
    }

    .detail-panel {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: rgba(255,255,255,.75);
        padding: 1.2rem;
    }

    .quiet-note {
        padding: .85rem 1rem;
        border-left: 4px solid var(--lava);
        background: rgba(204, 107, 73, .1);
        color: #663220;
        margin: .8rem 0 1rem;
    }

    .puffin-note {
        margin-top: .75rem;
        padding: .85rem 1rem;
        border: 1px dashed rgba(75, 156, 167, .5);
        border-radius: 8px;
        background: rgba(217, 238, 240, .5);
        color: #173136;
    }

    .weather-strip {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: .8rem;
        margin: 1rem 0;
    }

    .weather-card {
        padding: 1rem;
        border-radius: 8px;
        background: #102126;
        color: white;
    }

    .weather-card strong {
        display: block;
        font-size: 1.6rem;
        margin: .2rem 0;
    }

    .weather-card span,
    .weather-card small {
        display: block;
        color: rgba(255,255,255,.72);
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 8px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: .35rem;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: .7rem 1rem;
    }

    a {
        color: #247987;
        text-decoration: none;
        font-weight: 650;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Header
# -----------------------------
st.markdown(
    """
    <div class="hero">
        <h1>Iceland 9-Day Adventure</h1>
        <p>Reykjavik-based planning for waterfalls, geothermal soaks, black sand coastlines, glacier ice, puffins, and a little breathing room.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_cols = st.columns(4)
with metric_cols[0]:
    metric_card("Base", "Reykjavik", "Easy day trips and city nights")
with metric_cols[1]:
    metric_card("Travel Style", "Scenic", "Nature-first, with recovery time")
with metric_cols[2]:
    metric_card("Longest Drive", "3 hr", "One way target from base")
with metric_cols[3]:
    metric_card("Best Fit", "Late May", "Long daylight, spring wildlife")


# -----------------------------
# Tabs
# -----------------------------
overview_tab, details_tab, map_tab, packing_tab = st.tabs(
    ["Overview", "Day Details", "Map + Weather", "Packing"]
)

with overview_tab:
    st.subheader("Itinerary Overview")
    st.caption(f"{len(TRIP_DAYS)} planned days, Reykjavik-based with scenic day trips.")

    for day in TRIP_DAYS:
        day_card(day)

with details_tab:
    st.subheader("Daily Plan")

    for day in TRIP_DAYS:
        with st.expander(f"Day {day['day']} - {day['title']}", expanded=day["day"] == 1):
            left, right = st.columns([1.15, .85])
            with left:
                st.markdown(f"**{day['description']}**")
                st.markdown("**Highlights**")
                for item in day["highlights"]:
                    st.markdown(f"- {item}")

                if day.get("links"):
                    st.markdown("**Useful links**")
                    for label, url in day["links"].items():
                        st.markdown(f"- [{label}]({url})")

                puffin_easter_egg(day)

            with right:
                st.markdown('<div class="detail-panel">', unsafe_allow_html=True)
                st.markdown(f"**Region:** {day['region']}")
                st.markdown(f"**Pace:** {day['pace']}")
                st.markdown(f"**Drive:** {day['drive']}")
                st.markdown(" ".join(pill(theme) for theme in day["themes"]), unsafe_allow_html=True)
                st.markdown(f'<div class="quiet-note">{day["tip"]}</div>', unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

with map_tab:
    st.subheader("Map + Weather")
    map_day_title = st.selectbox(
        "Map focus",
        [day["title"] for day in TRIP_DAYS],
    )
    selected_map_day = next(day for day in TRIP_DAYS if day["title"] == map_day_title)
    st.markdown(f"**Map focus:** Day {selected_map_day['day']} - {selected_map_day['title']}")
    if selected_map_day.get("map_landmarks"):
        embed_landmark_map(selected_map_day["map_landmarks"])
    else:
        embed_map(selected_map_day["map_query"], height=380)

    st.markdown("#### Current Conditions")
    weather_html = ['<div class="weather-strip">']
    for label, city in WEATHER_CITIES.items():
        weather = get_weather(city)
        if weather:
            weather_html.append(
                f"""
                <div class="weather-card">
                    <span>{label}</span>
                    <strong>{weather["temp"]} C</strong>
                    <small>{weather["condition"]} · wind {weather["wind"]} m/s · humidity {weather["humidity"]}%</small>
                </div>
                """
            )
        else:
            weather_html.append(
                f"""
                <div class="weather-card">
                    <span>{label}</span>
                    <strong>--</strong>
                    <small>Add WEATHER_API_KEY in Streamlit secrets for live weather.</small>
                </div>
                """
            )
    weather_html.append("</div>")
    st.markdown("".join(weather_html), unsafe_allow_html=True)

with packing_tab:
    st.subheader("Packing Checklist")
    st.caption("Built around late-May weather: layers, waterproofing, and hot spring readiness.")

    cols = st.columns(2)
    for idx, item in enumerate(PACKING_ITEMS):
        cols[idx % 2].checkbox(item, key=f"pack_{idx}")

    st.markdown("#### Quick Booking List")
    for task in [
        "Reserve glacier hike",
        "Book lagoon entry window",
        "Choose one flex-day anchor activity",
        "Confirm Paradise Cottage check-in details",
        "Download offline Google Maps areas",
    ]:
        st.checkbox(task, key=f"booking_{task}")

st.caption("Built with Streamlit · Iceland 2026")
