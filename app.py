import streamlit as st
import requests
import re
import time

st.set_page_config(
    page_title="Dekoder VIN",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background-color: #0d0f14; color: #e8eaf0; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2.5rem; padding-bottom: 3rem; max-width: 820px; }
.vin-hero { text-align: center; margin-bottom: 2.2rem; }
.vin-hero h1 { font-family: 'Space Mono', monospace; font-size: 2.4rem; font-weight: 700; letter-spacing: -1px; color: #f0f2f8; margin-bottom: 0.3rem; }
.vin-hero span.accent { color: #e8c547; }
.vin-hero p { color: #7a8099; font-size: 0.95rem; margin: 0; }
.stTextInput > div > div > input { background: #171a22 !important; border: 1.5px solid #2a2e3d !important; border-radius: 10px !important; color: #f0f2f8 !important; font-family: 'Space Mono', monospace !important; font-size: 1.1rem !important; letter-spacing: 2px !important; padding: 14px 18px !important; }
.stTextInput > div > div > input:focus { border-color: #e8c547 !important; box-shadow: 0 0 0 3px rgba(232,197,71,0.12) !important; }
.stTextInput > label { font-size: 0.82rem !important; color: #7a8099 !important; letter-spacing: 0.05em !important; font-weight: 500 !important; text-transform: uppercase !important; }
.stButton > button { background: #e8c547 !important; color: #0d0f14 !important; font-family: 'Space Mono', monospace !important; font-weight: 700 !important; font-size: 0.9rem !important; letter-spacing: 1px !important; border: none !important; border-radius: 10px !important; padding: 13px 30px !important; width: 100% !important; text-transform: uppercase !important; }
.stButton > button:hover { background: #f5d55a !important; }
.data-table { width: 100%; border-collapse: collapse; margin: 0; }
.data-table tr { border-bottom: 1px solid #1e2130; }
.data-table tr:last-child { border-bottom: none; }
.data-table td { padding: 12px 16px; vertical-align: middle; }
.data-table td.dt-label { font-family: 'Space Mono', monospace; font-size: 0.7rem; letter-spacing: 0.08em; color: #7a8099; text-transform: uppercase; width: 42%; }
.data-table td.dt-value { font-size: 0.97rem; font-weight: 500; color: #f0f2f8; }
.dt-wrapper { background: #171a22; border: 1px solid #2a2e3d; border-radius: 12px; overflow: hidden; margin-bottom: 1.2rem; }
.badge { display: inline-block; padding: 5px 14px; border-radius: 20px; font-size: 0.82rem; font-weight: 600; letter-spacing: 0.04em; margin-bottom: 1rem; }
.badge-ok   { background: rgba(52,199,89,0.15);  color: #34c759; border: 1px solid rgba(52,199,89,0.3); }
.badge-warn { background: rgba(255,204,0,0.15);  color: #ffc400; border: 1px solid rgba(255,204,0,0.3); }
.badge-err  { background: rgba(255,69,58,0.15);  color: #ff453a; border: 1px solid rgba(255,69,58,0.3); }
.badge-info { background: rgba(10,132,255,0.15); color: #0a84ff; border: 1px solid rgba(10,132,255,0.3); }
.badge-ai   { background: rgba(180,100,255,0.15); color: #b464ff; border: 1px solid rgba(180,100,255,0.3); }
.section-label { font-family: 'Space Mono', monospace; font-size: 0.72rem; letter-spacing: 0.14em; color: #7a8099; text-transform: uppercase; margin: 1.8rem 0 0.8rem 0; display: flex; align-items: center; gap: 10px; }
.section-label::after { content: ''; flex: 1; height: 1px; background: #2a2e3d; }
.vin-map { display: flex; flex-wrap: wrap; gap: 4px; background: #0d0f14; border: 1px solid #2a2e3d; border-radius: 12px; padding: 1rem; margin-bottom: 0.6rem; }
.vin-char { display: flex; flex-direction: column; align-items: center; min-width: 38px; }
.vin-char .ch { font-family: 'Space Mono', monospace; font-size: 1.1rem; font-weight: 700; padding: 8px 10px; border-radius: 6px; border: 1px solid #2a2e3d; width: 38px; text-align: center; }
.vin-char .pos { font-size: 0.6rem; color: #4a4f65; margin-top: 3px; font-family: 'Space Mono', monospace; }
.ch-wmi  { background: #1a2235; color: #4da6ff; border-color: #1e3a5f !important; }
.ch-vds  { background: #1e1a2e; color: #b57aff; border-color: #3a2060 !important; }
.ch-chk  { background: #1e2a1a; color: #5fd68a; border-color: #1f4d2a !important; }
.ch-year { background: #2e2a14; color: #e8c547; border-color: #4d4010 !important; }
.ch-vis  { background: #1a1e2e; color: #a0a8c8; border-color: #2a3050 !important; }
.vin-legend { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 1rem; font-size: 0.75rem; }
.leg-item { display: flex; align-items: center; gap: 5px; }
.leg-dot  { width: 10px; height: 10px; border-radius: 2px; flex-shrink: 0; }
.history-chip { display: inline-block; background: #171a22; border: 1px solid #2a2e3d; border-radius: 8px; padding: 5px 13px; font-family: 'Space Mono', monospace; font-size: 0.78rem; color: #b0b5c8; margin: 3px 4px 3px 0; letter-spacing: 1px; }
hr.vin-divider { border: none; border-top: 1px solid #2a2e3d; margin: 1.5rem 0; }
.stAlert { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="vin-hero">
    <h1>🔍 Dekoder <span class="accent">VIN</span></h1>
    <p>Walidacja · Suma kontrolna · Dekodowanie globalne (Europa + USA + świat)</p>
</div>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

# ═══════════════════════════════════════════════════════════════
#  BAZA WMI
# ═══════════════════════════════════════════════════════════════
WMI_DB = {
    "WBA": ("BMW",                 "Niemcy"),
    "WBS": ("BMW M GmbH",          "Niemcy"),
    "WBY": ("BMW (EV)",            "Niemcy"),
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
    "SAJ": ("Jaguar",              "Wielka Brytania"),
    "SCB": ("Bentley",             "Wielka Brytania"),
    "SCC": ("Lotus",               "Wielka Brytania"),
    "SDB": ("Aston Martin",        "Wielka Brytania"),
    "SCF": ("Aston Martin",        "Wielka Brytania"),
    "SCA": ("Rolls-Royce",         "Wielka Brytania"),
    "SUF": ("Jaguar",              "Wielka Brytania"),
    "VF1": ("Renault",             "Francja"),
    "VF3": ("Peugeot",             "Francja"),
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
    "KMT": ("Hyundai",             "Korea Płd."),
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
    '1':'USA','2':'Kanada','3':'Meksyk','4':'USA','5':'USA',
    '6':'Australia','7':'Nowa Zelandia','8':'Argentyna','9':'Brazylia',
    'J':'Japonia','K':'Korea Płd.','L':'Chiny','M':'Indie',
    'N':'Holandia','P':'Filipiny','R':'Tajwan','S':'Wielka Brytania',
    'T':'Czechy / Szwajcaria','U':'Rumunia','V':'Francja / Austria',
    'W':'Niemcy','X':'Rosja','Y':'Belgia / Finlandia / Szwecja','Z':'Włochy',
}

LETTER_YEARS = {
    'A':(1980,2010),'B':(1981,2011),'C':(1982,2012),'D':(1983,2013),
    'E':(1984,2014),'F':(1985,2015),'G':(1986,2016),'H':(1987,2017),
    'J':(1988,2018),'K':(1989,2019),'L':(1990,2020),'M':(1991,2021),
    'N':(1992,2022),'P':(1993,2023),'R':(1994,2024),'S':(1995,2025),
    'T':(1996,2026),'V':(1997,2027),'W':(1998,2028),'X':(1999,2029),'Y':(2000,2030),
}
DIGIT_YEARS = {'1':2001,'2':2002,'3':2003,'4':2004,'5':2005,'6':2006,'7':2007,'8':2008,'9':2009}

# ═══════════════════════════════════════════════════════════════
#  BAZA WIEDZY VDS — każda marka osobno
# ═══════════════════════════════════════════════════════════════

# ── BMW ────────────────────────────────────────────────────────
# Pozycja 4: linia modelu
BMW_P4 = {
    'A':'Seria 3 (E46/E90/F30/G20)',
    'B':'Seria 4 (F32/F36/G22)',
    'C':'Seria 5 (E39/E60/F10/G30)',
    'D':'Seria 3 Touring/Compact (E46, do 2006) lub Seria 6/GT (F12/G32, po 2010)',
    'E':'Seria 1 (E87/E81/F20/F40)',
    'F':'Seria 2 / Active Tourer (F22/F45)',
    'G':'Seria 7 (E65/F01/G11)',
    'H':'Seria 8 (G14/G15)',
    'J':'X1 (E84/F48/U11)',
    'K':'X3 (E83/F25/G01)',
    'L':'X4 (F26/G02)',
    'M':'X5 (E53/E70/F15/G05)',
    'N':'X6 (E71/F16/G06)',
    'P':'X7 (G07)',
    'R':'X2 (F39)',
    'S':'Z4 (E85/E89/G29)',
    'T':'Z3',
    'U':'i3 / iX3',
    'V':'i4 / iX',
    'W':'M3 / M4 / M5',
    'X':'M6 / M8',
    'Y':'X2 (F39) / X1 (U11)',
    'Z':'Seria 4 Gran Coupe / i8',
}
# Pozycja 5: typ nadwozia / wariant
BMW_P5 = {
    'A':'Sedan','B':'Coupe','C':'Cabrio / Convertible',
    'D':'Gran Coupe (4-dr)','E':'Touring / Kombi',
    'F':'Gran Turismo','G':'xDrive (AWD)','H':'sDrive (FWD/RWD)',
    'J':'Active Tourer','K':'Gran Tourer','L':'Limuzyna długa (L)',
    'M':'M Performance','N':'SUV xDrive','P':'SAV / SUV',
    'R':'Roadster','S':'Sport','T':'Sport Line',
    'U':'M Sport','V':'Advantage','W':'Luxury Line',
    'X':'xDrive','Y':'sDrive','Z':'Elektryczny (BEV)',
}
# Pozycja 8: silnik
BMW_P8 = {
    'A':'Benzyna 1.5 3-cyl (B38) 136–140 KM',
    'B':'Benzyna 2.0 4-cyl (B48) 184–252 KM',
    'C':'Benzyna 3.0 6-cyl (B58) 258–374 KM',
    'D':'Benzyna 4.4 V8 (N63/S63) 450–625 KM',
    'E':'Diesel 2.0 4-cyl (B47) 150–190 KM',
    'F':'Diesel 3.0 6-cyl (B57) 249–400 KM',
    'G':'Diesel 4.4 V8',
    'H':'Benzyna 1.5 Hybrid (B38e)',
    'J':'Benzyna 2.0 Hybrid (B48e)',
    'K':'Benzyna 3.0 M (S55/S58) 431–530 KM',
    'L':'Benzyna 4.4 M (S63) 560–625 KM',
    'M':'Elektryczny (BMW i)',
    'N':'Benzyna 1.6 (N13)',
    'P':'Benzyna 2.0 (N20/N26) 184 KM',
    'R':'Diesel 2.0 (N47) 143–177 KM',
    'S':'Diesel 3.0 (N57) 258 KM',
    'T':'Benzyna 4.4 (N63) 407 KM',
    'U':'Benzyna 3.0 (N55) 306–340 KM',
    'V':'Benzyna 2.0 (N46) 150–170 KM',
    'W':'Diesel 2.5 (M57) 163–197 KM',
    'X':'Benzyna 2.0 (N43) 143–170 KM',
    'Y':'Benzyna 1.5 (B38) 102 KM',
    'Z':'Plug-in Hybrid',
    '0':'Diesel 2.5 M57D25 163 KM (E46/E39, ~2003) lub Benzyna B38 (nowsze)',
    '1':'Benzyna 1.5 3-cyl turbo',
    '3':'Benzyna 2.0 turbo',
    '5':'Diesel 2.0 (N47)',
    '6':'Diesel 3.0 (M57D30) 218–231 KM',
    '7':'Diesel 2.5 (M57D25) 163 KM',
    '8':'Benzyna 2.5 (M54) 192 KM',
    '9':'Benzyna 3.0 (M54) 231 KM',
}
# Pozycja 11: fabryka
BMW_P11 = {
    'A':'Dingolfing, Niemcy (S5/S6/S7/S8)',
    'B':'Monachium, Niemcy (S3)',
    'C':'Regensburg, Niemcy (S1/S3/S4)',
    'D':'Leipzig, Niemcy (S1/S2/i3)',
    'G':'Regensburg, Niemcy (Seria 3, E46) lub Graz, Austria — Magna Steyr (Z4/Supra, nowsze)',
    'J':'Spartanburg, USA (X3/X4/X5/X6/X7)',
    'K':'Oxford, UK (MINI)',
    'M':'Monachium, Niemcy',
    'N':'Nedcar, Holandia (X1/X2)',
    'R':'Regensburg, Niemcy',
    'S':'Spartanburg, USA',
    'T':'Shenyang, Chiny (BMW Brilliance)',
    'U':'San Luis Potosí, Meksyk (S3)',
    '0':'Nedcar, Holandia (X2 F39)',
    '5':'Nedcar, Holandia (X2 F39)',
    '6':'Shenyang 2, Chiny',
}

# ── VW GROUP (VW, Audi, Škoda, SEAT, Porsche) ─────────────────
VW_P4_MODEL = {
    'WVW':{'A':'Polo','B':'Golf','C':'Passat','D':'Phaeton','E':'Touareg',
           'F':'Tiguan','G':'Touran / Sharan','H':'T-Roc','J':'Jetta',
           'K':'Arteon','L':'Caddy','M':'Transporter T5/T6','T':'Touareg II',
           'Z':'ID.3 / ID.4'},
    'WAU':{'A':'A1','B':'A3 / S3','C':'A4 / S4','D':'A6 / S6','E':'A8 / S8',
           'F':'Q5','G':'Q7','H':'Q2','J':'TT','K':'A5 / S5',
           'L':'A7','M':'Q3','N':'Q8','P':'R8','T':'e-tron'},
    'TMB':{'A':'Fabia','B':'Octavia','C':'Superb','D':'Yeti','E':'Karoq',
           'F':'Kodiaq','G':'Scala','H':'Kamiq','J':'Enyaq'},
    'VSA':{'A':'Ibiza','B':'Leon','C':'Ateca','D':'Arona','E':'Tarraco'},
    'WP0':{'A':'911','B':'Boxster / Cayman','C':'Cayenne','D':'Panamera',
           'E':'Macan','F':'Taycan'},
}
# Pozycja 8 VW Group: silnik
VW_P8 = {
    'A':'Benzyna 1.0 MPI 60–75 KM',
    'B':'Benzyna 1.2 TSI 86–105 KM',
    'C':'Benzyna 1.4 TSI 122–150 KM',
    'D':'Benzyna 1.6 MPI 102–110 KM',
    'E':'Benzyna 2.0 TSI 180–310 KM',
    'F':'Diesel 1.6 TDI 90–115 KM',
    'G':'Diesel 2.0 TDI 136–150 KM',
    'H':'Diesel 2.0 TDI 177–184 KM',
    'J':'Benzyna 1.8 TSI 152–180 KM',
    'K':'Diesel 2.0 TDI 102–115 KM',
    'L':'Benzyna 1.5 TSI 130–150 KM',
    'M':'Diesel 3.0 TDI V6 204–272 KM',
    'N':'Benzyna 2.5 R5 220 KM',
    'P':'Benzyna 3.6 V6 280 KM',
    'R':'Benzyna 5.0 V10 FSI (R8)',
    'S':'Benzyna 1.4 TSI 125 KM',
    'T':'Benzyna 2.0 TFSI 211–280 KM',
    'U':'Benzyna 1.0 eTSI 110 KM (mHEV)',
    'V':'Elektryczny / e-tron',
    'W':'Diesel 1.9 TDI 90–130 KM',
    'X':'Benzyna 1.4 TGI CNG',
    'Y':'Plug-in Hybrid PHEV',
    'Z':'Benzyna 1.6 FSI / 1.4 FSI',
    '5':'Benzyna 2.0 TFSI 265–320 KM (S/RS)',
    '6':'Diesel 2.5 TDI 150–163 KM',
    '7':'Diesel 3.0 TDI 225 KM',
    '8':'Benzyna 4.0 V8 TFSI (RS7/RS6)',
    '9':'Benzyna 3.0 TFSI V6 272–333 KM',
}
# Pozycja 11 VW Group: fabryka
VW_P11 = {
    'A':'Ingolstadt, Niemcy (Audi)',
    'B':'Bratysława, Słowacja (VW/Audi/Porsche)',
    'C':'Chattanooga, USA (VW)',
    'D':'Wolfsburg, Niemcy (VW Golf/Tiguan)',
    'E':'Emden, Niemcy (VW Passat)',
    'G':'Graz, Austria — Magna Steyr',
    'H':'Hannover, Niemcy (VW Transporter)',
    'K':'Osnabrück, Niemcy',
    'M':'Mladá Boleslav, Czechy (Škoda)',
    'N':'Neckarsulm, Niemcy (Audi A6/A8)',
    'P':'Pamplona, Hiszpania (VW Polo)',
    'S':'Stuttgart, Niemcy (Porsche)',
    'T':'Türkiye (VW)',
    'X':'Martorell, Hiszpania (SEAT)',
    'Z':'Zwickau, Niemcy (VW ID.3/ID.4)',
    '5':'Kvasiny, Czechy (Škoda Kodiaq/Superb)',
    '7':'Vrchlabí, Czechy (DSG)',
}

# ── FORD EUROPA (WF0) ──────────────────────────────────────────
FORD_EU_P4 = {
    'A':'Mondeo / Focus Sedan 5-dr','B':'Fiesta 3-dr / Focus 3-dr',
    'C':'Cabrio','D':'Kombi 2-dr',
    'E':'Fiesta 5-dr / Focus 5-dr hatchback',
    'F':'Sedan 4-dr','G':'Kombi / Estate (Focus Kombi, Mondeo Kombi)',
    'H':'SUV / Kuga / EcoSport / Explorer','K':'Coupe',
    'M':'S-MAX / C-MAX / B-MAX (MPV)','N':'Kombi 4/5-dr',
    'P':'Pick-up / Ranger','S':'Transit / Tourneo',
    'T':'Transit Van','V':'Transit Custom','W':'Kombi 5-dr',
}
FORD_EU_P8 = {
    'A':'Benzyna 1.0 EcoBoost 100 KM',
    'B':'Diesel 2.0 TDCi 115–140 KM (GXXGBB → 140 KM)',
    'C':'Benzyna 1.6 Ti-VCT 105–125 KM',
    'D':'Diesel 1.5 TDCi 95–120 KM',
    'E':'Benzyna 1.5 EcoBoost 150–182 KM',
    'F':'Benzyna 1.6 EcoBoost 150–182 KM',
    'G':'Benzyna 2.0 / Diesel 2.0 TDCi 140–180 KM',
    'H':'Benzyna 2.3 EcoBoost 280 KM (Focus RS)',
    'J':'Diesel 1.6 TDCi 95–115 KM',
    'K':'Diesel 2.0 TDCi 115 KM',
    'L':'Diesel 2.0 TDCi 140 KM',
    'M':'Diesel 2.0 TDCi 163–180 KM',
    'N':'Benzyna 1.5 EcoBoost 120 KM',
    'P':'Diesel 1.5 TDCi 85–120 KM',
    'R':'Benzyna 2.5 Turbo 305 KM (Focus RS Mk2)',
    'S':'Diesel 1.8 TDCi 100–116 KM',
    'T':'Benzyna 2.0 Ti-VCT 145 KM',
    'U':'Benzyna 1.0 EcoBoost 100 KM (mHEV)',
    'V':'Benzyna 1.5 EcoBoost 182 KM',
    'W':'Diesel 2.0 TDCi 180 KM',
    'X':'Elektryczny',
    'Y':'Benzyna 1.6 Ti-VCT 85–105 KM',
    '2':'Benzyna 1.6 85 KM',
    '5':'Benzyna 2.0 DOHC 145 KM',
    '8':'Diesel 1.8 TDDI 75–90 KM',
}
FORD_EU_P11 = {
    'A':'Valencia, Hiszpania (Mondeo/Kuga)',
    'B':'Saarlouis, Niemcy (Focus)',
    'C':'Gölcük, Turcja (Transit)',
    'D':'Düsseldorf, Niemcy (Transit)',
    'E':'Genk, Belgia',
    'H':'Halewood, Wielka Brytania (Kuga/Edge)',
    'K':'Kocaeli, Turcja (Transit)',
    'N':'Köln-Niehl, Niemcy (Fiesta)',
    'S':'Saarlouis, Niemcy (Focus)',
    'V':'Valencia, Hiszpania',
}

# ── MERCEDES-BENZ ──────────────────────────────────────────────
MERC_P4 = {
    'A':'Klasa A (W168/W169/W176/W177)',
    'B':'Klasa B (W245/W246/W247)',
    'C':'Klasa C (W202/W203/W204/W205/W206)',
    'D':'Klasa CLA (C117/C118)',
    'E':'Klasa E (W210/W211/W212/W213)',
    'F':'Klasa CLS (C219/C257)',
    'G':'Klasa G / G-Wagen (W463)',
    'H':'Klasa S (W220/W221/W222/W223)',
    'J':'GLA (X156/H247)',
    'K':'GLC (X253/C253)',
    'L':'GLE (W166/V167)',
    'M':'GLB (X247)',
    'N':'GLS (X166/X167)',
    'P':'Klasa V / Vito (W638/W639/W447)',
    'R':'SL (R129/R230/R231/R232)',
    'S':'SLC / SLK (R170/R171/R172)',
    'T':'AMG GT (C190/R190)',
    'U':'EQC / EQA / EQB (elektryczny)',
    'V':'EQS / EQE (elektryczny)',
    'W':'Sprinter',
    'X':'Klasa X (pick-up)',
}
MERC_P8 = {
    'A':'Benzyna 1.3 (M282) 102–163 KM',
    'B':'Benzyna 1.5 EQ Boost (M264) 163 KM',
    'C':'Benzyna 2.0 (M264) 184–258 KM',
    'D':'Benzyna 3.0 6-cyl (M256) 367–429 KM',
    'E':'Diesel 1.5 (OM608) 95–116 KM',
    'F':'Diesel 2.0 (OM654) 150–194 KM',
    'G':'Diesel 3.0 6-cyl (OM656) 286–340 KM',
    'H':'Benzyna 4.0 V8 AMG (M177) 476–639 KM',
    'J':'Benzyna 5.5 / 6.2 V8 AMG',
    'K':'Benzyna 6.0 V12 (M279)',
    'L':'Elektryczny EQ',
    'M':'Benzyna 1.6 (M270) 122–156 KM',
    'N':'Diesel 1.6 (OM626) 90 KM',
    'P':'Diesel 2.2 (OM651) 136–204 KM',
    'R':'Benzyna 2.5 / 3.5 V6 (M272)',
    'S':'Diesel 3.0 V6 (OM642) 190–265 KM',
    'T':'Benzyna 3.5 V6 (M276) 258–333 KM',
    'U':'Benzyna 4.7 V8 (M278)',
    'V':'Plug-in Hybrid',
    'W':'Diesel 2.7 / 3.0 (OM612/613) 163–204 KM',
    'X':'Benzyna 2.0 kompressor (M271) 163–193 KM',
    'Y':'Benzyna 2.3 / 2.6 (M111)',
    'Z':'Diesel 2.0 CDI (OM646) 122–136 KM',
    '0':'Diesel 2.2 CDI (OM651) 136 KM',
    '6':'Diesel 2.5 CDI (OM605/607)',
    '7':'Diesel 3.0 CDI V6 (OM642) 224 KM',
    '8':'Diesel 3.2 CDI (OM613)',
    '9':'Benzyna 3.2 / 3.7 V6 (M112)',
}

# ── VOLVO ──────────────────────────────────────────────────────
VOLVO_P4 = {
    'B':'S60 / V60','C':'S70 / V70 (old)',
    'D':'S80 / V90','E':'XC60',
    'F':'XC40 / XC90','G':'S90 / V90',
    'H':'XC90 (2. gen)','J':'V40',
    'K':'S40 / V40 (old)','L':'V70 / XC70',
    'M':'C30 / C70','N':'XC60 (2. gen)',
    'P':'XC40 Recharge','S':'EX40 / EC40 (EV)',
}

# ── TOYOTA / LEXUS ─────────────────────────────────────────────
TOYOTA_P4 = {
    'A':'Aygo / Yaris (Japonia)','B':'Corolla',
    'C':'Camry','D':'Avalon / Lexus ES',
    'E':'Land Cruiser','F':'RAV4',
    'G':'Highlander','H':'Prius (Hybrid)',
    'J':'C-HR / bZ4X','K':'4Runner',
    'L':'Tacoma','M':'Tundra',
    'N':'Sequoia','P':'GR Yaris / GR86',
    'R':'Lexus RX','S':'Lexus NX',
    'T':'Lexus IS / GS','U':'Lexus LS',
    'V':'Lexus LC / LX','W':'Lexus UX',
}

def get_vds_info(vin: str, wmi: str, manufacturer: str) -> dict:
    """Dekoduje VDS na podstawie producenta — używa szczegółowych tabel."""
    result = {}
    p4, p5, p8, p11 = vin[3], vin[4], vin[7], vin[10]

    if wmi in ("WBA", "WBS", "WBY", "4US", "5UX"):
        # BMW
        if p4 in BMW_P4:
            result["Model / seria"] = BMW_P4[p4]
        if p5 in BMW_P5:
            result["Typ nadwozia / wariant"] = BMW_P5[p5]
        if p8 in BMW_P8:
            result["Silnik"] = BMW_P8[p8]
        if p11 in BMW_P11:
            result["Fabryka"] = BMW_P11[p11]

    elif wmi in ("WDB", "WDC", "WDD", "WDF", "WMX"):
        # Mercedes-Benz
        if p4 in MERC_P4:
            result["Model / klasa"] = MERC_P4[p4]
        if p8 in MERC_P8:
            result["Silnik"] = MERC_P8[p8]

    elif wmi in ("WVW", "WV1", "WV2", "WVG"):
        # Volkswagen
        models = VW_P4_MODEL.get("WVW", {})
        if p4 in models:
            result["Model VW"] = models[p4]
        if p8 in VW_P8:
            result["Silnik"] = VW_P8[p8]
        if p11 in VW_P11:
            result["Fabryka"] = VW_P11[p11]

    elif wmi in ("WAU", "WUA", "WA1"):
        # Audi
        models = VW_P4_MODEL.get("WAU", {})
        if p4 in models:
            result["Model Audi"] = models[p4]
        if p8 in VW_P8:
            result["Silnik"] = VW_P8[p8]
        if p11 in VW_P11:
            result["Fabryka"] = VW_P11[p11]

    elif wmi in ("TMB", "TMA", "TMC"):
        # Škoda
        models = VW_P4_MODEL.get("TMB", {})
        if p4 in models:
            result["Model Škoda"] = models[p4]
        if p8 in VW_P8:
            result["Silnik"] = VW_P8[p8]
        if p11 in VW_P11:
            result["Fabryka"] = VW_P11[p11]

    elif wmi in ("WP0", "WP1"):
        # Porsche
        models = VW_P4_MODEL.get("WP0", {})
        if p4 in models:
            result["Model Porsche"] = models[p4]
        if p8 in VW_P8:
            result["Silnik"] = VW_P8[p8]

    elif wmi in ("WF0", "WF1", "WF2"):
        # Ford Europa
        if p4 in FORD_EU_P4:
            result["Model Ford (EU)"] = FORD_EU_P4[p4]
        if p8 in FORD_EU_P8:
            result["Silnik"] = FORD_EU_P8[p8]
        if p11 in FORD_EU_P11:
            result["Fabryka"] = FORD_EU_P11[p11]

    elif wmi in ("YV1", "YV4"):
        # Volvo
        if p4 in VOLVO_P4:
            result["Model Volvo"] = VOLVO_P4[p4]

    elif wmi in ("JT2", "JTD", "JTJ", "JT6", "1T2", "4T1"):
        # Toyota / Lexus
        if p4 in TOYOTA_P4:
            result["Model Toyota/Lexus"] = TOYOTA_P4[p4]

    elif wmi in ("VSA", "VS6"):
        # SEAT
        models = VW_P4_MODEL.get("VSA", {})
        if p4 in models:
            result["Model SEAT"] = models[p4]
        if p8 in VW_P8:
            result["Silnik"] = VW_P8[p8]

    return result


def get_year_str(vin: str) -> str:
    """Inteligentnie ustala rok modelowy."""
    ch = vin[9]
    if ch == '0':
        return "ok. 2019–2020 (kod niestandardowy)"
    if ch in DIGIT_YEARS:
        return str(DIGIT_YEARS[ch])
    if ch in LETTER_YEARS:
        y1, y2 = LETTER_YEARS[ch]
        wmi = vin[:3]
        # Producenci aktywni tylko w nowym cyklu
        new_only = {"WF0","WF1","5YJ","5YF","LB1","LBD","YK1","WMW","WMX","5UX"}
        if wmi in new_only:
            return str(y2)
        try:
            serial = int(vin[11:17])
            if serial > 80000 and y2 <= 2026:
                return f"{y2} (prawdopodobnie; lub {y1})"
            if serial < 5000 and y1 >= 1990:
                return f"{y1} lub {y2}"
        except:
            pass
        if y2 <= 2026:
            return f"{y1} lub {y2}"
        return str(y1)
    return "Nieznany"


# ═══════════════════════════════════════════════════════════════
#  WALIDACJA I SUMA KONTROLNA
# ═══════════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════════
#  NHTSA API
# ═══════════════════════════════════════════════════════════════
NHTSA_FIELDS = [
    ("Make","Marka"),("Model","Model"),("Series","Seria / Trim"),
    ("Model Year","Rok modelowy"),("Vehicle Type","Typ pojazdu"),
    ("Body Class","Typ nadwozia"),("Doors","Liczba drzwi"),
    ("Displacement (L)","Pojemność silnika (L)"),
    ("Engine Number of Cylinders","Liczba cylindrów"),
    ("Engine Configuration","Układ cylindrów"),
    ("Engine Brake (hp) From","Moc (KM)"),
    ("Fuel Type - Primary","Typ paliwa"),
    ("Drive Type","Rodzaj napędu"),
    ("Transmission Style","Skrzynia biegów"),
    ("Transmission Speeds","Liczba biegów"),
    ("Turbo","Turbosprężarka"),
    ("Electrification Level","Elektryfikacja"),
    ("Manufacturer Name","Producent"),
    ("Plant Country","Kraj fabryki"),
    ("Plant City","Miasto fabryki"),
    ("GVWR Class","Klasa GVWR"),
    ("Anti-Brake System (ABS)","System ABS"),
    ("Air Bag Loc Front","Poduszki przednie"),
    ("Wheelbase (inches) From","Rozstaw osi (cale)"),
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

# ═══════════════════════════════════════════════════════════════
#  UI HELPERS
# ═══════════════════════════════════════════════════════════════
def render_table(data: dict):
    rows = "".join(
        f'<tr><td class="dt-label">{k}</td><td class="dt-value">{v}</td></tr>'
        for k, v in data.items()
    )
    st.markdown(f'<div class="dt-wrapper"><table class="data-table">{rows}</table></div>',
                unsafe_allow_html=True)

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

# ═══════════════════════════════════════════════════════════════
#  UI
# ═══════════════════════════════════════════════════════════════
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
        st.markdown('<div class="section-label">Etap 1 — Walidacja formatu</div>', unsafe_allow_html=True)
        valid, vin, err = validate_vin(vin_input)
        if not valid:
            st.markdown('<span class="badge badge-err">⛔ Błąd formatu</span>', unsafe_allow_html=True)
            st.error(err)
        else:
            st.markdown('<span class="badge badge-ok">✓ Format VIN poprawny</span>', unsafe_allow_html=True)

            st.markdown('<div class="section-label">🗺️ Struktura VIN</div>', unsafe_allow_html=True)
            render_vin_map(vin)

            st.markdown('<div class="section-label">Etap 2 — Suma kontrolna</div>', unsafe_allow_html=True)
            cs_ok, cs_exp, cs_act = checksum_verify(vin)
            if cs_ok:
                st.markdown('<span class="badge badge-ok">✓ Suma kontrolna poprawna</span>', unsafe_allow_html=True)
                st.success(f"Znak kontrolny na pozycji 9: **{cs_act}** — zgodny z ISO/USA.")
            else:
                st.markdown('<span class="badge badge-warn">⚠ Suma kontrolna — ostrzeżenie</span>', unsafe_allow_html=True)
                st.warning(f"Oczekiwano **{cs_exp}**, jest **{cs_act}** na poz. 9. W UE suma kontrolna nie jest obowiązkowa — dekodowanie trwa.")

            # Dane bazowe
            wmi = vin[:3]
            manufacturer = "Nieznany"
            country_wmi = COUNTRY_MAP.get(vin[0], "Nieznany")
            if wmi in WMI_DB:
                manufacturer, country_wmi = WMI_DB[wmi]
            year_str = get_year_str(vin)

            st.markdown('<div class="section-label">Etap 3A — Dane podstawowe (WMI)</div>', unsafe_allow_html=True)
            render_table({
                "🌍 Kraj produkcji": country_wmi,
                "🏭 Producent": manufacturer,
                "📅 Rok modelowy": year_str,
                "🔢 WMI (poz. 1–3)": wmi,
                "🔢 VDS (poz. 4–9)": vin[3:9],
                "🔢 Nr seryjny (poz. 12–17)": vin[11:17],
            })

            # Szczegółowe dekodowanie VDS
            st.markdown('<div class="section-label">Etap 3B — Szczegółowe dekodowanie VDS</div>', unsafe_allow_html=True)
            vds_data = get_vds_info(vin, wmi, manufacturer)
            if vds_data:
                st.markdown('<span class="badge badge-ai">✦ Dekodowanie szczegółowe</span>', unsafe_allow_html=True)
                render_table(vds_data)
            else:
                st.markdown('<span class="badge badge-warn">⚠ Brak szczegółowych danych VDS</span>', unsafe_allow_html=True)
                st.info(
                    f"Dla producenta **{manufacturer}** nie mam jeszcze szczegółowych tabel kodów VDS. "
                    "Dane podstawowe z WMI są dostępne powyżej."
                )

            # NHTSA dla USA/Kanada/Meksyk
            is_usa = vin[0] in ('1', '2', '3', '4', '5')
            if is_usa:
                st.markdown('<div class="section-label">Etap 3C — Baza NHTSA (USA/Kanada/Meksyk)</div>', unsafe_allow_html=True)
                with st.spinner("Pobieranie z bazy NHTSA…"):
                    time.sleep(0.2)
                    nhtsa_ok, nhtsa_data, nhtsa_err = decode_nhtsa(vin)
                if nhtsa_ok:
                    st.markdown(f'<span class="badge badge-ok">✓ NHTSA: {len(nhtsa_data)} parametrów</span>', unsafe_allow_html=True)
                    render_table(nhtsa_data)
                else:
                    st.warning(f"NHTSA: {nhtsa_err}")

            if vin not in st.session_state.history:
                st.session_state.history.insert(0, vin)
                if len(st.session_state.history) > 10:
                    st.session_state.history.pop()

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
    Baza WMI 200+ producentów · Tabele VDS: BMW / Mercedes / VW Group / Ford EU / Volvo / Toyota
    · <strong style="color:#5a607a;">NHTSA vPIC API</strong> dla USA · Standard ISO 3779
</p>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  INSTRUKCJA: pip install streamlit requests → streamlit run app.py
# ═══════════════════════════════════════════════════════════════
