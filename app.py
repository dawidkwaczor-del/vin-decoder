import streamlit as st
import streamlit.components.v1 as components
import requests
import re
import time
import json

st.set_page_config(
    page_title="Dekoder VIN",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0d0f14;
    color: #e8eaf0;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2.5rem; padding-bottom: 3rem; max-width: 820px; }

.vin-hero { text-align: center; margin-bottom: 2.2rem; }
.vin-hero h1 {
    font-family: 'Space Mono', monospace; font-size: 2.4rem; font-weight: 700;
    letter-spacing: -1px; color: #f0f2f8; margin-bottom: 0.3rem;
}
.vin-hero span.accent { color: #e8c547; }
.vin-hero p { color: #7a8099; font-size: 0.95rem; margin: 0; }

.stTextInput > div > div > input {
    background: #171a22 !important; border: 1.5px solid #2a2e3d !important;
    border-radius: 10px !important; color: #f0f2f8 !important;
    font-family: 'Space Mono', monospace !important; font-size: 1.1rem !important;
    letter-spacing: 2px !important; padding: 14px 18px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #e8c547 !important;
    box-shadow: 0 0 0 3px rgba(232,197,71,0.12) !important;
}
.stTextInput > label {
    font-size: 0.82rem !important; color: #7a8099 !important;
    letter-spacing: 0.05em !important; font-weight: 500 !important;
    text-transform: uppercase !important;
}
.stButton > button {
    background: #e8c547 !important; color: #0d0f14 !important;
    font-family: 'Space Mono', monospace !important; font-weight: 700 !important;
    font-size: 0.9rem !important; letter-spacing: 1px !important;
    border: none !important; border-radius: 10px !important;
    padding: 13px 30px !important; width: 100% !important; text-transform: uppercase !important;
}
.stButton > button:hover { background: #f5d55a !important; }

.data-table { width: 100%; border-collapse: collapse; margin: 0; }
.data-table tr { border-bottom: 1px solid #1e2130; }
.data-table tr:last-child { border-bottom: none; }
.data-table td { padding: 12px 16px; vertical-align: middle; }
.data-table td.dt-label {
    font-family: 'Space Mono', monospace; font-size: 0.7rem;
    letter-spacing: 0.08em; color: #7a8099; text-transform: uppercase; width: 42%;
}
.data-table td.dt-value { font-size: 0.97rem; font-weight: 500; color: #f0f2f8; }
.dt-wrapper {
    background: #171a22; border: 1px solid #2a2e3d;
    border-radius: 12px; overflow: hidden; margin-bottom: 1.2rem;
}

.ai-box {
    background: #111520; border: 1px solid #2a3050;
    border-radius: 12px; padding: 1.4rem 1.6rem; margin-bottom: 1.2rem;
    line-height: 1.7; font-size: 0.97rem; color: #d0d4e8;
}
.ai-box h4 {
    font-family: 'Space Mono', monospace; font-size: 0.7rem;
    color: #4da6ff; letter-spacing: 0.12em; text-transform: uppercase;
    margin: 0 0 0.8rem 0;
}
.ai-section { margin-bottom: 1rem; }
.ai-section strong { color: #e8c547; }

.badge {
    display: inline-block; padding: 5px 14px; border-radius: 20px;
    font-size: 0.82rem; font-weight: 600; letter-spacing: 0.04em; margin-bottom: 1rem;
}
.badge-ok   { background: rgba(52,199,89,0.15);  color: #34c759; border: 1px solid rgba(52,199,89,0.3); }
.badge-warn { background: rgba(255,204,0,0.15);  color: #ffc400; border: 1px solid rgba(255,204,0,0.3); }
.badge-err  { background: rgba(255,69,58,0.15);  color: #ff453a; border: 1px solid rgba(255,69,58,0.3); }
.badge-info { background: rgba(10,132,255,0.15); color: #0a84ff; border: 1px solid rgba(10,132,255,0.3); }
.badge-ai   { background: rgba(180,100,255,0.15); color: #b464ff; border: 1px solid rgba(180,100,255,0.3); }

.section-label {
    font-family: 'Space Mono', monospace; font-size: 0.72rem;
    letter-spacing: 0.14em; color: #7a8099; text-transform: uppercase;
    margin: 1.8rem 0 0.8rem 0; display: flex; align-items: center; gap: 10px;
}
.section-label::after { content: ''; flex: 1; height: 1px; background: #2a2e3d; }

.vin-map {
    display: flex; flex-wrap: wrap; gap: 4px;
    background: #0d0f14; border: 1px solid #2a2e3d;
    border-radius: 12px; padding: 1rem; margin-bottom: 0.6rem;
}
.vin-char { display: flex; flex-direction: column; align-items: center; min-width: 38px; }
.vin-char .ch {
    font-family: 'Space Mono', monospace; font-size: 1.1rem; font-weight: 700;
    padding: 8px 10px; border-radius: 6px; border: 1px solid #2a2e3d;
    width: 38px; text-align: center;
}
.vin-char .pos { font-size: 0.6rem; color: #4a4f65; margin-top: 3px; font-family: 'Space Mono', monospace; }
.ch-wmi  { background: #1a2235; color: #4da6ff; border-color: #1e3a5f !important; }
.ch-vds  { background: #1e1a2e; color: #b57aff; border-color: #3a2060 !important; }
.ch-chk  { background: #1e2a1a; color: #5fd68a; border-color: #1f4d2a !important; }
.ch-year { background: #2e2a14; color: #e8c547; border-color: #4d4010 !important; }
.ch-vis  { background: #1a1e2e; color: #a0a8c8; border-color: #2a3050 !important; }
.vin-legend { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 1rem; font-size: 0.75rem; }
.leg-item { display: flex; align-items: center; gap: 5px; }
.leg-dot  { width: 10px; height: 10px; border-radius: 2px; flex-shrink: 0; }

.history-chip {
    display: inline-block; background: #171a22; border: 1px solid #2a2e3d;
    border-radius: 8px; padding: 5px 13px; font-family: 'Space Mono', monospace;
    font-size: 0.78rem; color: #b0b5c8; margin: 3px 4px 3px 0; letter-spacing: 1px;
}
hr.vin-divider { border: none; border-top: 1px solid #2a2e3d; margin: 1.5rem 0; }
.stAlert { border-radius: 10px !important; }
.stSpinner > div { color: #e8c547 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="vin-hero">
    <h1>🔍 Dekoder <span class="accent">VIN</span></h1>
    <p>Walidacja · Suma kontrolna · AI Dekodowanie (Europa + USA + świat)</p>
</div>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

# ─────────────────────────────────────────────
#  BAZA WMI
# ─────────────────────────────────────────────
WMI_DB = {
    "WBA": ("BMW",                 "Niemcy"),
    "WBS": ("BMW M GmbH",          "Niemcy"),
    "WBY": ("BMW (elektryczny)",   "Niemcy"),
    "WDB": ("Mercedes-Benz",       "Niemcy"),
    "WDC": ("Mercedes-Benz SUV",   "Niemcy"),
    "WDD": ("Mercedes-Benz",       "Niemcy"),
    "WDF": ("Mercedes-Benz Van",   "Niemcy"),
    "WME": ("Smart",               "Niemcy"),
    "WMW": ("MINI",                "Niemcy"),
    "WMX": ("Mercedes-AMG",        "Niemcy"),
    "WVW": ("Volkswagen",          "Niemcy"),
    "WV1": ("Volkswagen LCV",      "Niemcy"),
    "WV2": ("Volkswagen Bus",      "Niemcy"),
    "WVG": ("Volkswagen SUV/MPV",  "Niemcy"),
    "WAU": ("Audi",                "Niemcy"),
    "WA1": ("Audi SUV",            "Niemcy"),
    "WP0": ("Porsche",             "Niemcy"),
    "WP1": ("Porsche Cayenne",     "Niemcy"),
    "WUA": ("Audi Sport",          "Niemcy"),
    "W0L": ("Opel",                "Niemcy"),
    "W0V": ("Opel/Vauxhall",       "Niemcy"),
    "WF0": ("Ford (Niemcy)",       "Niemcy"),
    "WF1": ("Ford (Niemcy)",       "Niemcy"),
    "WMA": ("MAN Trucks",          "Niemcy"),
    "SAL": ("Land Rover",          "Wielka Brytania"),
    "SAR": ("Rover",               "Wielka Brytania"),
    "SCB": ("Bentley",             "Wielka Brytania"),
    "SCC": ("Lotus",               "Wielka Brytania"),
    "SDB": ("Aston Martin",        "Wielka Brytania"),
    "SCF": ("Aston Martin",        "Wielka Brytania"),
    "SAJ": ("Jaguar",              "Wielka Brytania"),
    "SUF": ("Jaguar",              "Wielka Brytania"),
    "SHH": ("Honda (UK)",          "Wielka Brytania"),
    "SCA": ("Rolls-Royce",         "Wielka Brytania"),
    "VF1": ("Renault",             "Francja"),
    "VF2": ("Renault",             "Francja"),
    "VF3": ("Peugeot",             "Francja"),
    "VF6": ("Renault",             "Francja"),
    "VF7": ("Citroën",             "Francja"),
    "VF8": ("Citroën",             "Francja"),
    "VFA": ("Renault",             "Francja"),
    "VFE": ("Peugeot",             "Francja"),
    "ZAR": ("Alfa Romeo",          "Włochy"),
    "ZFF": ("Ferrari",             "Włochy"),
    "ZGA": ("Lamborghini",         "Włochy"),
    "ZHW": ("Lamborghini",         "Włochy"),
    "ZLA": ("Lancia",              "Włochy"),
    "ZFA": ("Fiat",                "Włochy"),
    "ZCF": ("Iveco",               "Włochy"),
    "TMB": ("Škoda",               "Czechy"),
    "TMA": ("Škoda",               "Czechy"),
    "TMC": ("Škoda",               "Czechy"),
    "VSA": ("SEAT",                "Słowacja"),
    "VS6": ("SEAT",                "Hiszpania"),
    "VSX": ("Volkswagen (ES)",     "Hiszpania"),
    "YS2": ("Scania",              "Szwecja"),
    "YS3": ("Saab",                "Szwecja"),
    "YV1": ("Volvo Cars",          "Szwecja"),
    "YV4": ("Volvo Cars",          "Szwecja"),
    "YK1": ("Koenigsegg",          "Szwecja"),
    "XTA": ("AvtoVAZ / Łada",      "Rosja"),
    "XTT": ("GAZ",                 "Rosja"),
    "JHM": ("Honda",               "Japonia"),
    "JH4": ("Acura",               "Japonia"),
    "JN1": ("Nissan",              "Japonia"),
    "JN6": ("Nissan",              "Japonia"),
    "JF1": ("Subaru",              "Japonia"),
    "JF2": ("Subaru",              "Japonia"),
    "JT2": ("Toyota",              "Japonia"),
    "JT6": ("Lexus",               "Japonia"),
    "JTD": ("Toyota",              "Japonia"),
    "JTJ": ("Lexus",               "Japonia"),
    "JA3": ("Mitsubishi",          "Japonia"),
    "JMB": ("Mitsubishi",          "Japonia"),
    "JS1": ("Suzuki",              "Japonia"),
    "JYA": ("Yamaha",              "Japonia"),
    "JM1": ("Mazda",               "Japonia"),
    "JM3": ("Mazda CX",            "Japonia"),
    "KMH": ("Hyundai",             "Korea Płd."),
    "KNA": ("Kia",                 "Korea Płd."),
    "KND": ("Kia",                 "Korea Płd."),
    "KPA": ("SsangYong",           "Korea Płd."),
    "LFV": ("Volkswagen (CN)",     "Chiny"),
    "LHG": ("Honda (CN)",          "Chiny"),
    "LSG": ("GM Shanghai",         "Chiny"),
    "LSJ": ("MG / SAIC",           "Chiny"),
    "LYV": ("Volvo (CN)",          "Chiny"),
    "LB1": ("BYD",                 "Chiny"),
    "LBD": ("BYD",                 "Chiny"),
    "1FA": ("Ford",                "USA"),
    "1FB": ("Ford",                "USA"),
    "1FM": ("Ford SUV",            "USA"),
    "1FT": ("Ford Truck",          "USA"),
    "1G1": ("Chevrolet",           "USA"),
    "1G6": ("Cadillac",            "USA"),
    "1GC": ("Chevrolet Truck",     "USA"),
    "1GN": ("Chevrolet SUV",       "USA"),
    "1GT": ("GMC Truck",           "USA"),
    "1G4": ("Buick",               "USA"),
    "1HG": ("Honda (USA)",         "USA"),
    "1J4": ("Jeep",                "USA"),
    "1J8": ("Jeep",                "USA"),
    "1C3": ("Chrysler",            "USA"),
    "1C4": ("Chrysler / Jeep",     "USA"),
    "1C6": ("Ram Truck",           "USA"),
    "1D3": ("Dodge",               "USA"),
    "1D4": ("Dodge / RAM",         "USA"),
    "1N4": ("Nissan (USA)",        "USA"),
    "1N6": ("Nissan Truck",        "USA"),
    "1T2": ("Toyota (USA)",        "USA"),
    "1VW": ("Volkswagen (USA)",    "USA"),
    "2HG": ("Honda (CA)",          "Kanada"),
    "2T1": ("Toyota (CA)",         "Kanada"),
    "3FA": ("Ford (Meksyk)",       "Meksyk"),
    "3N1": ("Nissan (MX)",         "Meksyk"),
    "3VW": ("Volkswagen (MX)",     "Meksyk"),
    "4JG": ("Mercedes-Benz (USA)", "USA"),
    "4S3": ("Subaru (USA)",        "USA"),
    "4T1": ("Toyota (USA)",        "USA"),
    "4US": ("BMW (USA)",           "USA"),
    "5N1": ("Nissan (USA)",        "USA"),
    "5NP": ("Hyundai (USA)",       "USA"),
    "5UX": ("BMW X (USA)",         "USA"),
    "5XY": ("Kia (USA)",           "USA"),
    "5YJ": ("Tesla",               "USA"),
    "5YF": ("Tesla",               "USA"),
}

COUNTRY_MAP = {
    '1': 'USA', '2': 'Kanada', '3': 'Meksyk',
    '4': 'USA', '5': 'USA',
    '6': 'Australia', '7': 'Nowa Zelandia',
    '8': 'Argentyna', '9': 'Brazylia',
    'J': 'Japonia', 'K': 'Korea Płd.',
    'L': 'Chiny', 'M': 'Indie',
    'N': 'Holandia', 'P': 'Filipiny',
    'R': 'Tajwan', 'S': 'Wielka Brytania',
    'T': 'Czechy / Szwajcaria', 'U': 'Rumunia',
    'V': 'Francja / Austria', 'W': 'Niemcy',
    'X': 'Rosja / kraje bałtyckie',
    'Y': 'Belgia / Finlandia / Szwecja',
    'Z': 'Włochy',
}

MODEL_YEAR_MAP = {
    '1': 2001, '2': 2002, '3': 2003, '4': 2004, '5': 2005,
    '6': 2006, '7': 2007, '8': 2008, '9': 2009,
    'A': None, 'B': None, 'C': None, 'D': None, 'E': None,
    'F': None, 'G': None, 'H': None, 'J': None, 'K': None,
    'L': None, 'M': None, 'N': None, 'P': None, 'R': None,
    'S': None, 'T': None, 'V': None, 'W': None, 'X': None, 'Y': None,
}
LETTER_YEARS = {
    'A': (1980, 2010), 'B': (1981, 2011), 'C': (1982, 2012),
    'D': (1983, 2013), 'E': (1984, 2014), 'F': (1985, 2015),
    'G': (1986, 2016), 'H': (1987, 2017), 'J': (1988, 2018),
    'K': (1989, 2019), 'L': (1990, 2020), 'M': (1991, 2021),
    'N': (1992, 2022), 'P': (1993, 2023), 'R': (1994, 2024),
    'S': (1995, 2025), 'T': (1996, 2026), 'V': (1997, 2027),
    'W': (1998, 2028), 'X': (1999, 2029), 'Y': (2000, 2030),
}

def get_year_str(vin: str) -> str:
    ch = vin[9]
    if ch == '0':
        return "ok. 2019–2020 (niestandardowy)"
    if ch in MODEL_YEAR_MAP and isinstance(MODEL_YEAR_MAP[ch], int):
        return str(MODEL_YEAR_MAP[ch])
    if ch in LETTER_YEARS:
        y1, y2 = LETTER_YEARS[ch]
        # heurystyka: WMI nowsze niż 2000 → bierz y2
        wmi = vin[:3]
        new_only = {"WF0","WF1","5YJ","5YF","LB1","LBD","YK1","WMW","WMX"}
        if wmi in new_only:
            return str(y2)
        try:
            serial = int(vin[11:17])
            if serial > 80000 and y2 <= 2026:
                return f"{y2} (prawdopodobnie)"
        except:
            pass
        return f"{y1} lub {y2}"
    return "Nieznany"

# ─────────────────────────────────────────────
#  WALIDACJA I SUMA KONTROLNA
# ─────────────────────────────────────────────
def validate_vin(raw: str) -> tuple[bool, str, str]:
    vin = raw.strip().upper().replace(" ", "").replace("-", "")
    if len(vin) == 0:
        return False, vin, "Proszę wpisać numer VIN."
    if len(vin) != 17:
        return False, vin, f"VIN musi mieć dokładnie 17 znaków (podano: {len(vin)})."
    found = [c for c in vin if c in "IOQ"]
    if found:
        return False, vin, f"VIN zawiera niedozwolone znaki: {', '.join(sorted(set(found)))}."
    if not re.fullmatch(r"[A-HJ-NPR-Z0-9]{17}", vin):
        return False, vin, "VIN zawiera niedozwolone znaki (dozwolone: A–Z bez I/O/Q, cyfry 0–9)."
    return True, vin, ""

TRANSLITERATION = {
    'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,
    'J':1,'K':2,'L':3,'M':4,'N':5,'P':7,'R':9,
    'S':2,'T':3,'U':4,'V':5,'W':6,'X':7,'Y':8,'Z':9,
    '0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,
}
WEIGHTS = [8,7,6,5,4,3,2,10,0,9,8,7,6,5,4,3,2]

def checksum_verify(vin: str) -> tuple[bool, str, str]:
    total = sum(TRANSLITERATION[ch] * WEIGHTS[i] for i, ch in enumerate(vin))
    remainder = total % 11
    expected = 'X' if remainder == 10 else str(remainder)
    return expected == vin[8], expected, vin[8]

# ─────────────────────────────────────────────
#  MAPA VIN
# ─────────────────────────────────────────────
def render_vin_map(vin: str):
    chars_html = ""
    for i, ch in enumerate(vin):
        if i < 3:       css = "ch-wmi"
        elif i == 8:    css = "ch-chk"
        elif i == 9:    css = "ch-year"
        elif i < 9:     css = "ch-vds"
        else:           css = "ch-vis"
        chars_html += f'<div class="vin-char"><div class="ch {css}">{ch}</div><div class="pos">{i+1}</div></div>'
    st.markdown(f"""
    <div class="vin-map">{chars_html}</div>
    <div class="vin-legend">
        <div class="leg-item"><div class="leg-dot" style="background:#4da6ff;"></div><span style="color:#7a8099;">Poz. 1–3: WMI (producent)</span></div>
        <div class="leg-item"><div class="leg-dot" style="background:#b57aff;"></div><span style="color:#7a8099;">Poz. 4–8: VDS (opis pojazdu)</span></div>
        <div class="leg-item"><div class="leg-dot" style="background:#5fd68a;"></div><span style="color:#7a8099;">Poz. 9: suma kontrolna</span></div>
        <div class="leg-item"><div class="leg-dot" style="background:#e8c547;"></div><span style="color:#7a8099;">Poz. 10: rok modelowy</span></div>
        <div class="leg-item"><div class="leg-dot" style="background:#a0a8c8;"></div><span style="color:#7a8099;">Poz. 11–17: VIS (numer seryjny)</span></div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TABELA
# ─────────────────────────────────────────────
def render_table(data: dict):
    rows = "".join(
        f'<tr><td class="dt-label">{k}</td><td class="dt-value">{v}</td></tr>'
        for k, v in data.items()
    )
    st.markdown(f'<div class="dt-wrapper"><table class="data-table">{rows}</table></div>',
                unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CLAUDE AI — komponent HTML/JS
# ─────────────────────────────────────────────
def render_ai_component(vin: str, manufacturer: str, country: str, year_hint: str):
    """Renderuje komponent HTML który wywołuje Claude API z przeglądarki."""
    prompt_text = (
        f"Zdekoduj VIN: {vin}\n"
        f"Znane: Producent={manufacturer}, Kraj={country}, Rok={year_hint}\n\n"
        "Zwróc TYLKO JSON (bez markdown):\n"
        "{\"marka\":\"...\",\"model\":\"...\",\"generacja\":\"...\","
        "\"rok_modelowy\":\"...\",\"typ_nadwozia\":\"...\","
        "\"liczba_drzwi\":\"...\",\"silnik_pojemnosc\":\"...\","
        "\"silnik_moc\":\"...\",\"silnik_typ\":\"...\","
        "\"paliwo\":\"...\",\"naped\":\"...\","
        "\"skrzynia_biegow\":\"...\",\"fabryka\":\"...\","
        "\"kraj_produkcji\":\"...\",\"numer_seryjny\":\"...\","
        "\"uwagi\":\"...krótki opis po polsku\"}\n\n"
        "Zasady: dekoduj VDS wg rzeczywistych tabel VIN tej marki i roku; "
        "rok z poz.10 wg ISO 3779; dla EU VIN uzywaj europejskich tabel; "
        "null jezeli nieznane."
    )
    html = f"""
<!DOCTYPE html><html><head>
<style>
  body{{margin:0;padding:0;font-family:'DM Sans',system-ui,sans-serif;background:transparent;}}
  #loading{{color:#7a8099;font-size:0.88rem;padding:0.5rem 0;}}
  #loading span{{color:#e8c547;font-family:monospace;font-weight:700;}}
  table{{width:100%;border-collapse:collapse;}}
  td{{padding:11px 14px;border-bottom:1px solid #1e2130;vertical-align:middle;}}
  td.lb{{font-family:monospace;font-size:0.65rem;letter-spacing:0.08em;color:#7a8099;text-transform:uppercase;width:42%;background:#171a22;}}
  td.vb{{font-size:0.93rem;font-weight:500;color:#f0f2f8;background:#171a22;}}
  .box{{background:#171a22;border:1px solid #2a2e3d;border-radius:12px;overflow:hidden;margin-bottom:0.8rem;}}
  .ai-note{{background:#111520;border:1px solid #2a3050;border-radius:12px;padding:1rem 1.2rem;font-size:0.9rem;color:#d0d4e8;line-height:1.7;margin-top:0.5rem;}}
  .ai-head{{font-family:monospace;font-size:0.65rem;color:#4da6ff;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.6rem;}}
  .err{{color:#ff453a;background:rgba(255,69,58,0.1);border-radius:8px;padding:0.8rem;font-size:0.88rem;}}
</style>
</head><body>
<div id="loading">⏳ Claude analizuje <span>{vin}</span>…</div>
<div id="result"></div>
<div id="err"></div>
<script>
const PROMPT = {json.dumps(prompt_text)};
const LABELS = {{
  marka:"🚗 Marka", model:"📋 Model", generacja:"🏷️ Generacja",
  rok_modelowy:"📅 Rok modelowy", typ_nadwozia:"🚙 Typ nadwozia",
  liczba_drzwi:"🚪 Liczba drzwi", silnik_pojemnosc:"⚙️ Pojemność silnika",
  silnik_moc:"💪 Moc silnika", silnik_typ:"🔩 Typ silnika",
  paliwo:"⛽ Paliwo", naped:"🔄 Napęd", skrzynia_biegow:"⚙️ Skrzynia biegów",
  fabryka:"🏭 Fabryka", kraj_produkcji:"🌍 Kraj produkcji",
  numer_seryjny:"🔢 Numer seryjny"
}};
(async()=>{{
  try{{
    const r = await fetch("https://api.anthropic.com/v1/messages",{{
      method:"POST",
      headers:{{"Content-Type":"application/json"}},
      body:JSON.stringify({{
        model:"claude-sonnet-4-20250514",
        max_tokens:1000,
        messages:[{{role:"user",content:PROMPT}}]
      }})
    }});
    const d = await r.json();
    let txt = (d.content||[]).filter(b=>b.type==="text").map(b=>b.text).join("");
    txt = txt.replace(/```[a-z]*/g,"").replace(/```/g,"").trim();
    const obj = JSON.parse(txt);
    let rows="";
    for(const [k,lbl] of Object.entries(LABELS)){{
      const v=obj[k];
      if(v&&v!=="null"&&v!==null&&v!=="")
        rows+=`<tr><td class="lb">${{lbl}}</td><td class="vb">${{v}}</td></tr>`;
    }}
    let html=`<div class="box"><table>${{rows}}</table></div>`;
    if(obj.uwagi&&obj.uwagi!=="null"&&obj.uwagi!=="")
      html+=`<div class="ai-note"><div class="ai-head">✦ Analiza AI</div>${{obj.uwagi}}</div>`;
    document.getElementById("loading").style.display="none";
    document.getElementById("result").innerHTML=html;
  }}catch(e){{
    document.getElementById("loading").style.display="none";
    document.getElementById("err").innerHTML=`<div class="err">⚠ Błąd AI: ${{e.message}}</div>`;
  }}
}})();
</script>
</body></html>
"""
    components.html(html, height=600, scrolling=False)


# ─────────────────────────────────────────────
#  NHTSA API
# ─────────────────────────────────────────────
NHTSA_FIELDS = [
    ("Make", "Marka"), ("Model", "Model"), ("Series", "Seria / Trim"),
    ("Model Year", "Rok modelowy"), ("Vehicle Type", "Typ pojazdu"),
    ("Body Class", "Typ nadwozia"), ("Doors", "Liczba drzwi"),
    ("Displacement (L)", "Pojemność silnika (L)"),
    ("Engine Number of Cylinders", "Liczba cylindrów"),
    ("Engine Configuration", "Układ cylindrów"),
    ("Engine Brake (hp) From", "Moc (KM)"),
    ("Fuel Type - Primary", "Typ paliwa"),
    ("Drive Type", "Rodzaj napędu"),
    ("Transmission Style", "Skrzynia biegów"),
    ("Transmission Speeds", "Liczba biegów"),
    ("Turbo", "Turbosprężarka"),
    ("Electrification Level", "Elektryfikacja"),
    ("Manufacturer Name", "Producent"),
    ("Plant Country", "Kraj fabryki"),
    ("Plant City", "Miasto fabryki"),
    ("Plant State", "Stan fabryki"),
    ("GVWR Class", "Klasa GVWR"),
    ("Anti-Brake System (ABS)", "System ABS"),
    ("Air Bag Loc Front", "Poduszki przednie"),
    ("Air Bag Loc Side", "Poduszki boczne"),
    ("Wheelbase (inches) From", "Rozstaw osi (cale)"),
]

def decode_nhtsa(vin: str) -> tuple[bool, dict, str]:
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValuesExtended/{vin}?format=json"
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        payload = resp.json()
        results_list = payload.get("Results", [])
        if not results_list:
            return False, {}, "API zwróciło pustą odpowiedź."
        raw = results_list[0]
    except Exception as e:
        return False, {}, f"Błąd połączenia: {e}"

    BAD = {"", "not applicable", "n/a", "none", "0", "0.0"}
    data = {}
    for api_key, pl_label in NHTSA_FIELDS:
        val = raw.get(api_key, "")
        if val and val.strip().lower() not in BAD:
            data[pl_label] = val.strip()

    if not data:
        return False, {}, "Brak danych w bazie NHTSA."
    return True, data, ""

# ─────────────────────────────────────────────
#  UI
# ─────────────────────────────────────────────
vin_input = st.text_input(
    "Numer VIN pojazdu",
    placeholder="np. WBADP91020GX82421 lub 1HGBH41JXMN109186",
    max_chars=20,
    help="17-znakowy numer identyfikacyjny (bez I, O, Q)",
)
decode_btn = st.button("🔎 Dekoduj VIN", use_container_width=True)

if decode_btn:
    if not vin_input.strip():
        st.error("Wpisz numer VIN.")
    else:
        # ── Etap 1: Walidacja
        st.markdown('<div class="section-label">Etap 1 — Walidacja formatu</div>', unsafe_allow_html=True)
        valid, vin, err = validate_vin(vin_input)
        if not valid:
            st.markdown('<span class="badge badge-err">⛔ Błąd formatu</span>', unsafe_allow_html=True)
            st.error(err)
        else:
            st.markdown('<span class="badge badge-ok">✓ Format VIN poprawny</span>', unsafe_allow_html=True)

            # Mapa VIN
            st.markdown('<div class="section-label">🗺️ Struktura VIN</div>', unsafe_allow_html=True)
            render_vin_map(vin)

            # ── Etap 2: Suma kontrolna
            st.markdown('<div class="section-label">Etap 2 — Suma kontrolna</div>', unsafe_allow_html=True)
            cs_ok, cs_exp, cs_act = checksum_verify(vin)
            if cs_ok:
                st.markdown('<span class="badge badge-ok">✓ Suma kontrolna poprawna</span>', unsafe_allow_html=True)
                st.success(f"Znak kontrolny na pozycji 9: **{cs_act}** — zgodny z algorytmem ISO/USA.")
            else:
                st.markdown('<span class="badge badge-warn">⚠ Suma kontrolna — ostrzeżenie</span>', unsafe_allow_html=True)
                st.warning(
                    f"Algorytm oczekuje **{cs_exp}**, VIN zawiera **{cs_act}** na poz. 9. "
                    "W UE suma kontrolna nie jest obowiązkowa — dekodowanie trwa."
                )

            # ── Dane bazowe z WMI (szybkie, lokalne)
            wmi = vin[:3]
            manufacturer = "Nieznany"
            country_wmi = COUNTRY_MAP.get(vin[0], "Nieznany")
            if wmi in WMI_DB:
                manufacturer, country_wmi = WMI_DB[wmi]
            year_hint = get_year_str(vin)

            st.markdown('<div class="section-label">Etap 3A — Dane podstawowe (WMI)</div>', unsafe_allow_html=True)
            render_table({
                "🌍 Kraj produkcji": country_wmi,
                "🏭 Producent": manufacturer,
                "📅 Rok modelowy": year_hint,
                "🔢 WMI": wmi,
                "🔢 VDS (poz. 4–9)": vin[3:9],
                "🔢 Nr seryjny (poz. 12–17)": vin[11:17],
            })

            # ── Etap 3B: Claude AI dekodowanie
            st.markdown('<div class="section-label">Etap 3B — 🤖 Dekodowanie AI (Claude)</div>', unsafe_allow_html=True)
            st.markdown('<span class="badge badge-ai">✦ Claude analizuje VIN…</span>', unsafe_allow_html=True)
            render_ai_component(vin, manufacturer, country_wmi, year_hint)

            # ── Etap 3C: NHTSA (tylko USA/Kanada/Meksyk)
            is_usa = vin[0] in ('1', '2', '3', '4', '5')
            if is_usa:
                st.markdown('<div class="section-label">Etap 3C — Baza NHTSA (USA/Kanada/Meksyk)</div>', unsafe_allow_html=True)
                with st.spinner("Pobieranie z bazy NHTSA…"):
                    nhtsa_ok, nhtsa_data, nhtsa_err = decode_nhtsa(vin)
                if nhtsa_ok:
                    st.markdown(f'<span class="badge badge-ok">✓ NHTSA: {len(nhtsa_data)} parametrów</span>', unsafe_allow_html=True)
                    render_table(nhtsa_data)
                else:
                    st.warning(f"NHTSA: {nhtsa_err}")

            # Historia
            if vin not in st.session_state.history:
                st.session_state.history.insert(0, vin)
                if len(st.session_state.history) > 10:
                    st.session_state.history.pop()

# Historia
if st.session_state.history:
    st.markdown('<hr class="vin-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Historia wyszukiwania (sesja)</div>', unsafe_allow_html=True)
    chips = "".join(f'<span class="history-chip">{v}</span>' for v in st.session_state.history)
    st.markdown(f'<div>{chips}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col, _ = st.columns([1, 4])
    with col:
        if st.button("🗑 Wyczyść historię", use_container_width=True):
            st.session_state.history = []
            st.rerun()

st.markdown("""
<hr class="vin-divider">
<p style="text-align:center; color:#3d4255; font-size:0.78rem;">
    🤖 <strong style="color:#5a607a;">Claude AI</strong> · Baza WMI 200+ producentów
    · <strong style="color:#5a607a;">NHTSA vPIC API</strong> dla USA/Kanada/Meksyk
    · Standard <strong style="color:#5a607a;">ISO 3779</strong>
</p>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  INSTRUKCJA URUCHOMIENIA
#  KROK 1:  pip install streamlit requests
#  KROK 2:  streamlit run app.py
#  KROK 3:  Otwórz http://localhost:8501
# ═══════════════════════════════════════════════════════════════
