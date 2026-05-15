import streamlit as st
import requests
import re
import time

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Dekoder VIN",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
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
.stButton > button:hover { background: #f5d55a !important; transform: translateY(-1px) !important; }

.data-table { width: 100%; border-collapse: collapse; margin: 0; }
.data-table tr { border-bottom: 1px solid #1e2130; }
.data-table tr:last-child { border-bottom: none; }
.data-table td { padding: 12px 16px; vertical-align: middle; }
.data-table td.dt-label {
    font-family: 'Space Mono', monospace; font-size: 0.7rem;
    letter-spacing: 0.08em; color: #7a8099; text-transform: uppercase;
    width: 42%; background: #171a22;
}
.data-table td.dt-value {
    font-size: 0.97rem; font-weight: 500; color: #f0f2f8; background: #171a22;
}
.dt-wrapper {
    background: #171a22; border: 1px solid #2a2e3d;
    border-radius: 12px; overflow: hidden; margin-bottom: 1.2rem;
}

.badge {
    display: inline-block; padding: 5px 14px; border-radius: 20px;
    font-size: 0.82rem; font-weight: 600; letter-spacing: 0.04em; margin-bottom: 1rem;
}
.badge-ok   { background: rgba(52,199,89,0.15);  color: #34c759; border: 1px solid rgba(52,199,89,0.3); }
.badge-warn { background: rgba(255,204,0,0.15);  color: #ffc400; border: 1px solid rgba(255,204,0,0.3); }
.badge-err  { background: rgba(255,69,58,0.15);  color: #ff453a; border: 1px solid rgba(255,69,58,0.3); }
.badge-info { background: rgba(10,132,255,0.15); color: #0a84ff; border: 1px solid rgba(10,132,255,0.3); }

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
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="vin-hero">
    <h1>🔍 Dekoder <span class="accent">VIN</span></h1>
    <p>Walidacja · Suma kontrolna · Dekodowanie globalne (Europa + USA + świat)</p>
</div>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

# ─────────────────────────────────────────────
#  BAZA WMI (200+ wpisów)
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
    "WVW": ("Volkswagen",          "Niemcy"),
    "WV1": ("Volkswagen LCV",      "Niemcy"),
    "WV2": ("Volkswagen Bus",      "Niemcy"),
    "WAU": ("Audi",                "Niemcy"),
    "WA1": ("Audi SUV",            "Niemcy"),
    "WP0": ("Porsche",             "Niemcy"),
    "WP1": ("Porsche Cayenne",     "Niemcy"),
    "WUA": ("Audi Sport",          "Niemcy"),
    "W0L": ("Opel",                "Niemcy"),
    "WOL": ("Opel",                "Niemcy"),
    "VSS": ("SEAT (DE)",           "Niemcy"),
    "SAJ": ("Jaguar (DE)",         "Niemcy"),
    "WF0": ("Ford (Niemcy)",        "Niemcy"),
    "WF1": ("Ford (Niemcy)",        "Niemcy"),
    "WF2": ("Ford (Niemcy)",        "Niemcy"),
    "WMA": ("MAN Trucks",           "Niemcy"),
    "WMW": ("MINI",                 "Niemcy"),
    "WMX": ("Mercedes-AMG",         "Niemcy"),
    "WVG": ("Volkswagen SUV/MPV",   "Niemcy"),
    "W0V": ("Opel/Vauxhall",        "Niemcy"),
    "SAL": ("Land Rover",          "Wielka Brytania"),
    "SAR": ("Rover",               "Wielka Brytania"),
    "SCB": ("Bentley",             "Wielka Brytania"),
    "SCC": ("Lotus",               "Wielka Brytania"),
    "SDB": ("Aston Martin",        "Wielka Brytania"),
    "SFD": ("Alexander Dennis",    "Wielka Brytania"),
    "SHH": ("Honda (UK)",          "Wielka Brytania"),
    "SUF": ("Jaguar",              "Wielka Brytania"),
    "VF1": ("Renault",             "Francja"),
    "VF2": ("Renault",             "Francja"),
    "VF3": ("Peugeot",             "Francja"),
    "VF6": ("Renault",             "Francja"),
    "VF7": ("Citroën",             "Francja"),
    "VF8": ("Citroën",             "Francja"),
    "VFA": ("Renault",             "Francja"),
    "VFB": ("Citroën",             "Francja"),
    "VFE": ("Peugeot",             "Francja"),
    "ZAR": ("Alfa Romeo",          "Włochy"),
    "ZAS": ("Alfa Romeo",          "Włochy"),
    "ZCF": ("Iveco",               "Włochy"),
    "ZFF": ("Ferrari",             "Włochy"),
    "ZGA": ("Lamborghini",         "Włochy"),
    "ZHW": ("Lamborghini",         "Włochy"),
    "ZLA": ("Lancia",              "Włochy"),
    "ZFA": ("Fiat",                "Włochy"),
    "ZFC": ("Fiat",                "Włochy"),
    "ZFE": ("Fiat",                "Włochy"),
    "TMB": ("Škoda",               "Czechy"),
    "TMA": ("Škoda",               "Czechy"),
    "TMC": ("Škoda",               "Czechy"),
    "TM9": ("Škoda",               "Czechy"),
    "VSA": ("SEAT",                "Słowacja"),
    "VSB": ("SEAT",                "Słowacja"),
    "VSC": ("SEAT",                "Słowacja"),
    "VSD": ("SEAT",                "Słowacja"),
    "VS6": ("SEAT",                "Hiszpania"),
    "VS7": ("SEAT",                "Hiszpania"),
    "VSX": ("Volkswagen (ES)",     "Hiszpania"),
    "YS2": ("Scania",              "Szwecja"),
    "YS3": ("Saab",                "Szwecja"),
    "YV1": ("Volvo Cars",          "Szwecja"),
    "YV4": ("Volvo Cars",          "Szwecja"),
    "YVF": ("Volvo Trucks",        "Szwecja"),
    "YK1": ("Koenigsegg",          "Szwecja"),
    "XTA": ("AvtoVAZ / Łada",      "Rosja"),
    "XLB": ("Volvo (NedCar)",       "Holandia"),
    "XLE": ("Scania (NL)",          "Holandia"),
    "XLR": ("DAF Trucks",           "Holandia"),
    "XMC": ("Mitsubishi (NedCar)",  "Holandia"),
    "YBW": ("Volkswagen (Belgia)",  "Belgia"),
    "YCM": ("Mazda (Belgia)",       "Belgia"),
    "YE2": ("Van Hool (busy)",      "Belgia"),
    "MAJ": ("Ford (Indie)",         "Indie"),
    "LVS": ("Ford (Chiny)",         "Chiny"),
    "SAA": ("Jaguar",               "Wielka Brytania"),
    "SAB": ("Land Rover",           "Wielka Brytania"),
    "SCA": ("Rolls-Royce",          "Wielka Brytania"),
    "SCF": ("Aston Martin",         "Wielka Brytania"),
    "SED": ("General Motors (UK)",  "Wielka Brytania"),
    "VNE": ("Toyota (UK)",          "Wielka Brytania"),
    "ABK": ("Aston Martin",         "Wielka Brytania"),
    "XTT": ("GAZ",                 "Rosja"),
    "XUF": ("UAZ",                 "Rosja"),
    "JHM": ("Honda",               "Japonia"),
    "JH4": ("Acura",               "Japonia"),
    "JN1": ("Nissan",              "Japonia"),
    "JN6": ("Nissan",              "Japonia"),
    "JF1": ("Subaru",              "Japonia"),
    "JF2": ("Subaru",              "Japonia"),
    "JT2": ("Toyota",              "Japonia"),
    "JT3": ("Toyota 4WD",          "Japonia"),
    "JT6": ("Lexus",               "Japonia"),
    "JT8": ("Lexus",               "Japonia"),
    "JTD": ("Toyota",              "Japonia"),
    "JTJ": ("Lexus",               "Japonia"),
    "JTM": ("Toyota RAV4",         "Japonia"),
    "JAA": ("Isuzu",               "Japonia"),
    "JA3": ("Mitsubishi",          "Japonia"),
    "JA4": ("Mitsubishi SUV",      "Japonia"),
    "JMB": ("Mitsubishi",          "Japonia"),
    "JS1": ("Suzuki",              "Japonia"),
    "JS2": ("Suzuki",              "Japonia"),
    "JSK": ("Kawasaki",            "Japonia"),
    "JSB": ("Honda Moto",          "Japonia"),
    "JYA": ("Yamaha",              "Japonia"),
    "JL5": ("Mazda",               "Japonia"),
    "JM1": ("Mazda",               "Japonia"),
    "JM3": ("Mazda CX",            "Japonia"),
    "KMH": ("Hyundai",             "Korea Płd."),
    "KMT": ("Hyundai",             "Korea Płd."),
    "KNA": ("Kia",                 "Korea Płd."),
    "KND": ("Kia",                 "Korea Płd."),
    "KPA": ("SsangYong",           "Korea Płd."),
    "KLA": ("GM Korea",            "Korea Płd."),
    "KL4": ("Daewoo",              "Korea Płd."),
    "LFV": ("Volkswagen (CN)",     "Chiny"),
    "LGX": ("Buick (CN)",          "Chiny"),
    "LHG": ("Honda (CN)",          "Chiny"),
    "LJC": ("Chery",               "Chiny"),
    "LSG": ("GM Shanghai",         "Chiny"),
    "LSJ": ("MG / SAIC",           "Chiny"),
    "LYV": ("Volvo (CN)",          "Chiny"),
    "LB1": ("BYD",                 "Chiny"),
    "LB2": ("BYD",                 "Chiny"),
    "LBD": ("BYD",                 "Chiny"),
    "1FA": ("Ford",                "USA"),
    "1FB": ("Ford",                "USA"),
    "1FC": ("Ford",                "USA"),
    "1FD": ("Ford Truck",          "USA"),
    "1FM": ("Ford SUV",            "USA"),
    "1FT": ("Ford Truck",          "USA"),
    "1FU": ("Freightliner",        "USA"),
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
    "1D7": ("Dodge Ram",           "USA"),
    "1B3": ("Dodge",               "USA"),
    "1B4": ("Dodge",               "USA"),
    "1N4": ("Nissan (USA)",        "USA"),
    "1N6": ("Nissan Truck",        "USA"),
    "1T2": ("Toyota (USA)",        "USA"),
    "1VW": ("Volkswagen (USA)",    "USA"),
    "2FA": ("Ford (Kanada)",       "Kanada"),
    "2FT": ("Ford Truck (CA)",     "Kanada"),
    "2G1": ("Chevrolet (CA)",      "Kanada"),
    "2HG": ("Honda (CA)",          "Kanada"),
    "2HK": ("Honda CR-V (CA)",     "Kanada"),
    "2T1": ("Toyota (CA)",         "Kanada"),
    "2T2": ("Lexus (CA)",          "Kanada"),
    "3FA": ("Ford (Meksyk)",       "Meksyk"),
    "3G1": ("Chevrolet (MX)",      "Meksyk"),
    "3HG": ("Honda (MX)",          "Meksyk"),
    "3N1": ("Nissan (MX)",         "Meksyk"),
    "3VW": ("Volkswagen (MX)",     "Meksyk"),
    "4JG": ("Mercedes-Benz (USA)", "USA"),
    "4S3": ("Subaru (USA)",        "USA"),
    "4S4": ("Subaru (USA)",        "USA"),
    "4T1": ("Toyota (USA)",        "USA"),
    "4T3": ("Toyota (USA)",        "USA"),
    "4US": ("BMW (USA)",           "USA"),
    "5FN": ("Honda Pilot (USA)",   "USA"),
    "5J6": ("Honda (USA)",         "USA"),
    "5J8": ("Acura (USA)",         "USA"),
    "5N1": ("Nissan (USA)",        "USA"),
    "5NP": ("Hyundai (USA)",       "USA"),
    "5TD": ("Toyota Sienna",       "USA"),
    "5TF": ("Toyota Tundra",       "USA"),
    "5UX": ("BMW X (USA)",         "USA"),
    "5XY": ("Kia (USA)",           "USA"),
    "5YF": ("Tesla",               "USA"),
    "5YJ": ("Tesla",               "USA"),
    "7FB": ("Toyota (USA)",        "USA"),
}

COUNTRY_MAP = {
    '1': 'USA', '2': 'Kanada', '3': 'Meksyk',
    '4': 'USA', '5': 'USA',
    '6': 'Australia', '7': 'Nowa Zelandia',
    '8': 'Argentyna', '9': 'Brazylia',
    'J': 'Japonia', 'K': 'Korea Płd.',
    'L': 'Chiny', 'M': 'Indie',
    'N': 'Holandia',
    'P': 'Filipiny', 'R': 'Tajwan',
    'S': 'Wielka Brytania',
    'T': 'Czechy / Szwajcaria',
    'U': 'Rumunia',
    'V': 'Francja / Austria',
    'W': 'Niemcy',
    'X': 'Rosja / kraje bałtyckie',
    'Y': 'Belgia / Finlandia / Szwecja',
    'Z': 'Włochy',
}

MODEL_YEAR_MAP = {
    'A': '1980 lub 2010', 'B': '1981 lub 2011', 'C': '1982 lub 2012',
    'D': '1983 lub 2013', 'E': '1984 lub 2014', 'F': '1985 lub 2015',
    'G': '1986 lub 2016', 'H': '1987 lub 2017', 'J': '1988 lub 2018',
    'K': '1989 lub 2019', 'L': '1990 lub 2020', 'M': '1991 lub 2021',
    'N': '1992 lub 2022', 'P': '1993 lub 2023', 'R': '1994 lub 2024',
    'S': '1995 lub 2025', 'T': '1996 lub 2026', 'V': '1997',
    'W': '1998', 'X': '1999', 'Y': '2000',
    '1': '2001', '2': '2002', '3': '2003', '4': '2004', '5': '2005',
    '6': '2006', '7': '2007', '8': '2008', '9': '2009',
}

# ─────────────────────────────────────────────
#  FUNKCJE
# ─────────────────────────────────────────────
def validate_vin(raw: str) -> tuple[bool, str, str]:
    vin = raw.strip().upper().replace(" ", "").replace("-", "")
    if len(vin) == 0:
        return False, vin, "Proszę wpisać numer VIN."
    if len(vin) != 17:
        return False, vin, f"VIN musi mieć dokładnie 17 znaków (podano: {len(vin)})."
    found = [c for c in vin if c in "IOQ"]
    if found:
        return False, vin, f"VIN zawiera niedozwolone znaki: {', '.join(sorted(set(found)))} (litery I, O, Q są zabronione w standardzie VIN)."
    if not re.fullmatch(r"[A-HJ-NPR-Z0-9]{17}", vin):
        return False, vin, "VIN zawiera niedozwolone znaki. Dozwolone: cyfry 0–9 oraz litery A–Z (bez I, O, Q)."
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

# ─── VDS dekoderzy dla konkretnych marek ───────────────────────
# Ford Europa (WF0): pozycja 4 = typ nadwozia
FORD_EU_BODY = {
    'A': 'Sedan 5-drzwiowy', 'B': 'Sedan 3-drzwiowy', 'C': 'Cabrio',
    'D': 'Kombi 2-drzwiowe', 'E': 'Sedan 3-drzwiowy (hatchback)',
    'F': 'Sedan 4-drzwiowy', 'G': 'Kombi / Estate 5-drzwiowe',
    'H': 'SUV / Crossover', 'K': 'Coupe', 'M': 'Minivan / MPV',
    'N': 'Kombi 4/5-drzwiowe', 'P': 'Pick-up', 'S': 'Kombi/Bus',
    'T': 'Van', 'V': 'Van', 'W': 'Kombi 5-drzwiowe',
}
# Ford Europa: pozycja 8 = silnik (przybliżone)
FORD_EU_ENGINE = {
    'A': 'Benzyna 1.0 EcoBoost', 'B': 'Benzyna 1.4',
    'C': 'Benzyna 1.6', 'D': 'Diesel 1.5 TDCi',
    'E': 'Benzyna 1.5 EcoBoost', 'F': 'Benzyna 1.6 EcoBoost',
    'G': 'Benzyna 2.0 / Diesel 2.0 TDCi',
    'H': 'Benzyna 2.3 EcoBoost', 'J': 'Diesel 1.6 TDCi',
    'K': 'Diesel 2.0 TDCi 115KM', 'L': 'Diesel 2.0 TDCi 140KM',
    'M': 'Diesel 2.0 TDCi 163KM', 'N': 'Benzyna 1.5',
    'P': 'Diesel 1.5 TDCi', 'R': 'Benzyna 2.5 Turbo (RS)',
    'S': 'Diesel 1.8 TDCi', 'T': 'Benzyna 2.0 Ti-VCT',
    'U': 'Benzyna 1.0 EcoBoost 100KM', 'V': 'Benzyna 1.5 EcoBoost 182KM',
    'W': 'Diesel 2.0 TDCi 180KM', 'X': 'Elektryczny',
    'Y': 'Benzyna 1.6 Ti-VCT', 'Z': 'Benzyna 2.0 GDi',
    '2': 'Benzyna 1.6', '5': 'Benzyna 2.0 DOHC',
    '8': 'Diesel 1.8 TDDI',
}

# VW/Audi/Skoda/SEAT: pozycja 4 = model/segment
VW_MODEL = {
    'A': 'Polo / A1', 'B': 'Golf / A3 / Octavia',
    'C': 'Passat / A4 / Superb', 'D': 'Phaeton / A8 / A6',
    'E': 'Touareg / Q7 / Cayenne', 'F': 'Tiguan / Q5 / Yeti',
    'G': 'Touran / Sharan', 'H': 'T-Roc / Q2',
    'J': 'Jetta', 'K': 'Arteon / A5',
    'L': 'Caddy', 'M': 'T5 / T6 Transporter',
    'T': 'Touareg II', 'Z': 'ID.3 / ID.4 (EV)',
}
# VW pozycja 5+6 = silnik (przybliżone)
VW_ENGINE_POS8 = {
    'A': 'Benzyna 1.0 MPI', 'B': 'Benzyna 1.2 TSI',
    'C': 'Benzyna 1.4 TSI', 'D': 'Benzyna 1.6 MPI',
    'E': 'Benzyna 2.0 TSI', 'F': 'Diesel 1.6 TDI',
    'G': 'Diesel 2.0 TDI 150KM', 'H': 'Diesel 2.0 TDI 184KM',
    'J': 'Benzyna 1.8 TSI', 'K': 'Diesel 2.0 TDI 110KM',
    'L': 'Benzyna 1.5 TSI', 'M': 'Diesel 3.0 TDI V6',
    'N': 'Benzyna 2.5 R5', 'P': 'Benzyna 3.6 V6',
    'R': 'Benzyna 4.0 V8 (Porsche)', 'S': 'Benzyna 1.4 TSI 125KM',
    'T': 'Benzyna 2.0 TFSI', 'U': 'Benzyna 1.0 eTSI',
    'V': 'Elektryczny (MEB)', 'W': 'Diesel 1.9 TDI',
    'X': 'Benzyna 1.4 TGI (CNG)', 'Y': 'Hybryd plug-in',
}

# BMW: pozycja 4 = seria/model
BMW_MODEL = {
    'A': '1 Series', 'B': '2 Series', 'C': '3 Series',
    'D': '4 Series', 'E': '5 Series', 'F': '6 Series',
    'G': '7 Series', 'H': '8 Series', 'J': 'X1',
    'K': 'X2', 'L': 'X3', 'M': 'X4', 'N': 'X5',
    'P': 'X6', 'R': 'X7', 'S': 'Z4', 'T': 'i3',
    'U': 'i4', 'V': 'iX', 'W': 'M3/M4', 'X': 'M5/M6',
    'Y': 'Z4', 'Z': '4 Series Gran Coupe',
}

# Fabryki Forda w Europie (poz. 11)
FORD_EU_PLANT = {
    'A': 'Valencia, Hiszpania',
    'B': 'Saarlouis, Niemcy',
    'C': 'Gölcük, Turcja',
    'D': 'Düsseldorf, Niemcy',
    'E': 'Genk, Belgia',
    'F': 'Fiesta (Köln), Niemcy',
    'G': 'Gent, Belgia',
    'H': 'Halewood, Wielka Brytania',
    'K': 'Kocaeli, Turcja',
    'M': 'Moskwa / Cuautitlan',
    'N': 'Niehl, Köln (Niemcy)',
    'S': 'Saarlouis, Niemcy',
    'T': 'Transit (Southampton/Turkey)',
    'V': 'Valencia, Hiszpania',
    'W': 'Wayne, Michigan (USA)',
}

# Fabryki VW Group (poz. 11)
VW_PLANT = {
    'A': 'Ingolstadt (Audi)',
    'B': 'Bratysława (Słowacja)',
    'C': 'Chattanooga, USA',
    'D': 'Wolfsburg (VW)',
    'E': 'Emden (VW)',
    'G': 'Graz, Austria (Magna)',
    'H': 'Hannover (VW)',
    'K': 'Osnabrück (VW)',
    'M': 'Mladá Boleslav (Škoda)',
    'N': 'Neckarsulm (Audi)',
    'P': 'Pamplona (VW)',
    'S': 'Stuttgart (Porsche)',
    'T': 'Türkiye (VW)',
    'W': 'Wilhelmsburg / Wiedeń',
    'X': 'Martorell (SEAT)',
    'Z': 'Zwickau (VW EV)',
}

def decode_vds_ford_eu(vin: str) -> dict:
    """Dekoduje VDS dla Forda Europa (WF0)."""
    result = {}
    body = FORD_EU_BODY.get(vin[3], None)
    if body:
        result["Typ nadwozia (VDS poz. 4)"] = body
    engine = FORD_EU_ENGINE.get(vin[7], None)
    if engine:
        result["Silnik (VDS poz. 8)"] = engine
    plant = FORD_EU_PLANT.get(vin[10], None)
    if plant:
        result["Fabryka (poz. 11)"] = plant
    return result

def decode_vds_vw_group(vin: str) -> dict:
    """Dekoduje VDS dla grupy VW (WAU, WVW, TMB, VSS...)."""
    result = {}
    model = VW_MODEL.get(vin[3], None)
    if model:
        result["Model/Segment (VDS poz. 4)"] = model
    engine = VW_ENGINE_POS8.get(vin[7], None)
    if engine:
        result["Silnik (VDS poz. 8)"] = engine
    plant = VW_PLANT.get(vin[10], None)
    if plant:
        result["Fabryka (poz. 11)"] = plant
    return result

def decode_vds_bmw(vin: str) -> dict:
    """Dekoduje VDS dla BMW."""
    result = {}
    model = BMW_MODEL.get(vin[3], None)
    if model:
        result["Model/Seria (VDS poz. 4)"] = model
    return result

def smart_model_year(vin: str, wmi: str) -> str:
    """
    Inteligentnie ustala rok modelowy.
    Jeśli WMI jest znane i aktywne po 2000 r., eliminuje starszy cykl.
    """
    year_char = vin[9]
    # Znaki cyfr 1-9 są jednoznaczne (2001-2009)
    UNAMBIGUOUS = {'1':2001,'2':2002,'3':2003,'4':2004,'5':2005,
                   '6':2006,'7':2007,'8':2008,'9':2009}
    if year_char in UNAMBIGUOUS:
        return str(UNAMBIGUOUS[year_char])

    # Litery — cykl powtarza się: A=1980/2010, B=1981/2011...
    LETTER_OFFSET = {
        'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,
        'J':8,'K':9,'L':10,'M':11,'N':12,'P':13,'R':14,
        'S':15,'T':16,'V':17,'W':18,'X':19,'Y':20
    }
    if year_char not in LETTER_OFFSET:
        return "Nieznany"

    offset = LETTER_OFFSET[year_char]
    year_old = 1980 + offset
    year_new = 2010 + offset

    # Producenci którzy istnieją tylko od określonego roku
    MODERN_ONLY = {
        # WMI: min rok produkcji
        "WF0": 1993, "WVW": 1975, "WAU": 1985, "WBA": 1975,
        "WDB": 1975, "TMB": 1991, "5YJ": 2012, "5YF": 2012,
        "YV1": 1975, "YV4": 2002, "YK1": 2009,
    }
    min_year = MODERN_ONLY.get(wmi, 0)

    # Jeśli stary rok jest przed minimum producenta, wybierz nowy
    if year_old < min_year:
        return str(year_new) if year_new <= 2026 else str(year_old)

    # Heurystyka: jeśli numer seryjny jest duży (>100000), to nowsze auto
    try:
        serial = int(vin[11:17])
        if serial > 100000 and year_new <= 2026:
            return f"{year_new} (prawdopodobnie)"
    except:
        pass

    # Nie da się jednoznacznie ustalić
    if year_new <= 2026:
        return f"{year_old} lub {year_new}"
    return str(year_old)

def decode_vin_manual(vin: str) -> dict:
    result = {}
    wmi = vin[:3]

    country = COUNTRY_MAP.get(vin[0], "Nieznany region")
    result["🌍 Kraj produkcji"] = country

    manufacturer = None
    if wmi in WMI_DB:
        manufacturer, country_wmi = WMI_DB[wmi]
        result["🏭 Producent"] = manufacturer
        result["📍 Kraj producenta"] = country_wmi
    else:
        result["🏭 Kod WMI (producent)"] = wmi

    # Inteligentny rok modelowy
    year_str = smart_model_year(vin, wmi)
    result["📅 Rok modelowy"] = year_str

    # Dekodowanie VDS zależnie od producenta
    vds_data = {}
    if wmi in ("WF0", "WF1", "WF2"):
        vds_data = decode_vds_ford_eu(vin)
    elif wmi in ("WVW", "WAU", "WA1", "WP0", "WP1", "TMB", "TMA",
                 "VSS", "VSA", "VSB", "VSC", "VSD", "VS6"):
        vds_data = decode_vds_vw_group(vin)
    elif wmi in ("WBA", "WBS", "WBY"):
        vds_data = decode_vds_bmw(vin)

    result.update(vds_data)

    # Dane techniczne VIN
    result["🔢 WMI (poz. 1–3)"] = wmi
    result["🔢 VDS (poz. 4–9)"] = vin[3:9]
    result["🔢 VIS (poz. 10–17)"] = vin[9:17]
    result["🔢 Nr seryjny (poz. 12–17)"] = vin[11:17]

    return result

def render_vin_map(vin: str):
    chars_html = ""
    for i, ch in enumerate(vin):
        if i < 3:
            css = "ch-wmi"
        elif i == 8:
            css = "ch-chk"
        elif i == 9:
            css = "ch-year"
        elif i < 9:
            css = "ch-vds"
        else:
            css = "ch-vis"
        chars_html += f'<div class="vin-char"><div class="ch {css}">{ch}</div><div class="pos">{i+1}</div></div>'

    st.markdown(f"""
    <div class="vin-map">{chars_html}</div>
    <div class="vin-legend">
        <div class="leg-item"><div class="leg-dot" style="background:#4da6ff;"></div><span style="color:#7a8099;">Poz. 1–3: WMI (producent/kraj)</span></div>
        <div class="leg-item"><div class="leg-dot" style="background:#b57aff;"></div><span style="color:#7a8099;">Poz. 4–8: VDS (cechy pojazdu)</span></div>
        <div class="leg-item"><div class="leg-dot" style="background:#5fd68a;"></div><span style="color:#7a8099;">Poz. 9: suma kontrolna</span></div>
        <div class="leg-item"><div class="leg-dot" style="background:#e8c547;"></div><span style="color:#7a8099;">Poz. 10: rok modelowy</span></div>
        <div class="leg-item"><div class="leg-dot" style="background:#a0a8c8;"></div><span style="color:#7a8099;">Poz. 11–17: VIS (numer seryjny)</span></div>
    </div>
    """, unsafe_allow_html=True)

GROUPS = {
    "🚗 Podstawowe informacje": [
        ("Marka", "Make"), ("Model", "Model"), ("Seria / Trim", "Series"),
        ("Rok modelowy", "Model Year"), ("Typ pojazdu", "Vehicle Type"),
        ("Typ nadwozia", "Body Class"), ("Liczba drzwi", "Doors"),
        ("Liczba miejsc", "Seating Rows"), ("Przeznaczenie", "Destination Market"),
    ],
    "⚙️ Silnik i napęd": [
        ("Pojemność silnika (L)", "Displacement (L)"),
        ("Pojemność silnika (CC)", "Displacement (CC)"),
        ("Liczba cylindrów", "Engine Number of Cylinders"),
        ("Układ cylindrów", "Engine Configuration"),
        ("Moc silnika (KM)", "Engine Brake (hp) From"),
        ("Typ paliwa", "Fuel Type - Primary"),
        ("Rodzaj napędu", "Drive Type"),
        ("Skrzynia biegów", "Transmission Style"),
        ("Liczba biegów", "Transmission Speeds"),
        ("Turbosprężarka", "Turbo"),
        ("Elektryfikacja", "Electrification Level"),
        ("Zasięg EV (mile)", "EV Drive Range (miles) From"),
    ],
    "🏭 Produkcja i identyfikacja": [
        ("Producent (NHTSA)", "Manufacturer Name"),
        ("Kraj produkcji", "Plant Country"),
        ("Miasto fabryki", "Plant City"),
        ("Stan fabryki (USA)", "Plant State"),
        ("Klasa GVWR", "GVWR Class"),
        ("Numer GVWR", "GVWR"),
        ("Kod WMI", "WMI"),
        ("VDS", "VDS"), ("VIS", "VIS"),
    ],
    "🛡️ Bezpieczeństwo": [
        ("Poduszki przednie", "Air Bag Loc Front"),
        ("Poduszki boczne", "Air Bag Loc Side"),
        ("Kurtyny powietrzne", "Air Bag Loc Curtain"),
        ("Poduszka kolana", "Air Bag Loc Knee"),
        ("System ABS", "Anti-Brake System (ABS)"),
        ("Typ hamulców", "Brake System Type"),
        ("TPMS", "Tire Pressure Monitoring System (TPMS) Type"),
    ],
    "📐 Wymiary": [
        ("Rozstaw osi (cale)", "Wheelbase (inches) From"),
        ("Długość (cale)", "Overall Length (inches) From"),
        ("Szerokość (cale)", "Overall Width (inches) From"),
        ("Wysokość (cale)", "Overall Height (inches) From"),
        ("Ładowność (funt)", "Payload Capacity (lbs) From"),
        ("Liczba osi", "Axles"),
    ],
}

def decode_vin_api(vin: str) -> tuple[bool, dict, str]:
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValuesExtended/{vin}?format=json"
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        payload = resp.json()
        results_list = payload.get("Results", [])
        if not results_list:
            return False, {}, "API zwróciło pustą odpowiedź."
        raw = results_list[0]
    except requests.exceptions.Timeout:
        return False, {}, "Przekroczono czas oczekiwania (15 s)."
    except requests.exceptions.ConnectionError:
        return False, {}, "Brak połączenia z internetem."
    except Exception as e:
        return False, {}, f"Błąd: {e}"

    BAD = {"", "not applicable", "n/a", "none", "0", "0.0"}
    data = {}
    for group_label, fields in GROUPS.items():
        for pl_label, api_key in fields:
            val = raw.get(api_key, "")
            if val and val.strip().lower() not in BAD:
                data[pl_label] = val.strip()

    if not data:
        return False, {}, "Brak danych w bazie NHTSA dla tego VIN."
    return True, data, ""

def render_cards(data_dict: dict):
    rows = "".join(
        f'''<tr>
            <td class="dt-label">{label}</td>
            <td class="dt-value">{val}</td>
        </tr>'''
        for label, val in data_dict.items()
    )
    st.markdown(f'''
    <div class="dt-wrapper">
        <table class="data-table">{rows}</table>
    </div>''', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  UI
# ─────────────────────────────────────────────
vin_input = st.text_input(
    "Numer VIN pojazdu",
    placeholder="np. WVWZZZ1JZ3W386752 lub 1HGBH41JXMN109186",
    max_chars=20,
    help="17-znakowy numer identyfikacyjny pojazdu (bez liter I, O, Q)",
)
decode_btn = st.button("🔎 Dekoduj VIN", use_container_width=True)

if decode_btn:
    if not vin_input.strip():
        st.markdown('<span class="badge badge-err">⛔ Błąd</span>', unsafe_allow_html=True)
        st.error("Pole VIN jest puste.")
    else:
        # Etap 1
        st.markdown('<div class="section-label">Etap 1 — Walidacja formatu</div>', unsafe_allow_html=True)
        valid, vin_clean, err_msg = validate_vin(vin_input)

        if not valid:
            st.markdown('<span class="badge badge-err">⛔ Błąd formatu</span>', unsafe_allow_html=True)
            st.error(err_msg)
        else:
            st.markdown('<span class="badge badge-ok">✓ Format VIN poprawny</span>', unsafe_allow_html=True)

            # Mapa VIN
            st.markdown('<div class="section-label">🗺️ Struktura VIN</div>', unsafe_allow_html=True)
            render_vin_map(vin_clean)

            # Etap 2
            st.markdown('<div class="section-label">Etap 2 — Suma kontrolna</div>', unsafe_allow_html=True)
            cs_ok, cs_expected, cs_actual = checksum_verify(vin_clean)
            if cs_ok:
                st.markdown('<span class="badge badge-ok">✓ Suma kontrolna się zgadza</span>', unsafe_allow_html=True)
                st.success(f"Znak kontrolny na pozycji 9: **{cs_actual}** — zgodny z algorytmem ISO/USA.")
            else:
                st.markdown('<span class="badge badge-warn">⚠ Ostrzeżenie — suma kontrolna</span>', unsafe_allow_html=True)
                st.warning(
                    f"Suma kontrolna się **nie zgadza** — oczekiwano **{cs_expected}**, jest **{cs_actual}**.\n\n"
                    "ℹ️ W UE weryfikacja sumy kontrolnej nie jest obowiązkowa — to normalne dla europejskich aut. Dekodowanie trwa."
                )

            # Etap 3A — lokalne dekodowanie (dla wszystkich)
            st.markdown('<div class="section-label">Etap 3A — Dekodowanie lokalne (cały świat)</div>', unsafe_allow_html=True)
            st.markdown('<span class="badge badge-info">ℹ Analiza struktury VIN — działa dla każdego auta</span>', unsafe_allow_html=True)
            manual = decode_vin_manual(vin_clean)
            render_cards(manual)

            # Etap 3B — NHTSA (tylko USA/Kanada/Meksyk)
            is_usa = vin_clean[0] in ('1', '2', '3', '4', '5')
            st.markdown('<div class="section-label">Etap 3B — Baza NHTSA (USA / Kanada / Meksyk)</div>', unsafe_allow_html=True)

            if is_usa:
                with st.spinner("Pobieranie danych z serwera NHTSA…"):
                    time.sleep(0.3)
                    api_ok, api_data, api_err = decode_vin_api(vin_clean)

                if not api_ok:
                    st.markdown('<span class="badge badge-warn">⚠ NHTSA</span>', unsafe_allow_html=True)
                    st.warning(f"NHTSA nie zwróciło danych: {api_err}")
                else:
                    st.markdown(f'<span class="badge badge-ok">✓ NHTSA: znaleziono {len(api_data)} parametrów</span>', unsafe_allow_html=True)
                    for group_label, fields in GROUPS.items():
                        group_fields = {pl: api_data[pl] for pl, _ in fields if pl in api_data}
                        if not group_fields:
                            continue
                        st.markdown(f'<div class="section-label">{group_label}</div>', unsafe_allow_html=True)
                        render_cards(group_fields)
            else:
                st.info(
                    "ℹ️ Baza NHTSA zawiera dane tylko dla pojazdów z **USA, Kanady i Meksyku** "
                    "(VIN zaczynający się od cyfry 1–5). "
                    "Dla tego pojazdu skorzystaj z wyników dekodowania lokalnego powyżej."
                )

            # Historia
            if vin_clean not in st.session_state.history:
                st.session_state.history.insert(0, vin_clean)
                if len(st.session_state.history) > 10:
                    st.session_state.history.pop()

# Historia
if st.session_state.history:
    st.markdown('<hr class="vin-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Historia wyszukiwania (sesja)</div>', unsafe_allow_html=True)
    chips_html = "".join(f'<span class="history-chip">{v}</span>' for v in st.session_state.history)
    st.markdown(f'<div>{chips_html}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col_clear, _ = st.columns([1, 4])
    with col_clear:
        if st.button("🗑 Wyczyść historię", use_container_width=True):
            st.session_state.history = []
            st.rerun()

st.markdown("""
<hr class="vin-divider">
<p style="text-align:center; color:#3d4255; font-size:0.78rem; margin-top:0.5rem;">
    Dekodowanie globalne z bazy WMI (200+ producentów)
    &nbsp;·&nbsp; <strong style="color:#5a607a;">NHTSA vPIC API</strong> dla aut USA/Kanada/Meksyk
    &nbsp;·&nbsp; Standard <strong style="color:#5a607a;">ISO 3779</strong>
</p>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  INSTRUKCJA URUCHOMIENIA
# ═══════════════════════════════════════════════════════════════
#  KROK 1:  pip install streamlit requests
#  KROK 2:  streamlit run app.py
#  KROK 3:  Otwórz http://localhost:8501
# ═══════════════════════════════════════════════════════════════
