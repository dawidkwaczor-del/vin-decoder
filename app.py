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

/* Base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0d0f14;
    color: #e8eaf0;
}

/* Hide Streamlit defaults */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 780px;
}

/* Hero title */
.vin-hero {
    text-align: center;
    margin-bottom: 2.2rem;
}
.vin-hero h1 {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: -1px;
    color: #f0f2f8;
    margin-bottom: 0.3rem;
}
.vin-hero span.accent { color: #e8c547; }
.vin-hero p {
    color: #7a8099;
    font-size: 0.95rem;
    margin: 0;
}

/* Input area */
.stTextInput > div > div > input {
    background: #171a22 !important;
    border: 1.5px solid #2a2e3d !important;
    border-radius: 10px !important;
    color: #f0f2f8 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 1.1rem !important;
    letter-spacing: 2px !important;
    padding: 14px 18px !important;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: #e8c547 !important;
    box-shadow: 0 0 0 3px rgba(232,197,71,0.12) !important;
}
.stTextInput > label {
    font-size: 0.82rem !important;
    color: #7a8099 !important;
    letter-spacing: 0.05em !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
}

/* Button */
.stButton > button {
    background: #e8c547 !important;
    color: #0d0f14 !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 1px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 13px 30px !important;
    width: 100% !important;
    transition: background 0.2s, transform 0.1s !important;
    text-transform: uppercase !important;
}
.stButton > button:hover {
    background: #f5d55a !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0px) !important; }

/* Cards / metric tiles */
.result-card {
    background: #171a22;
    border: 1px solid #2a2e3d;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}
.result-card h3 {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    color: #7a8099;
    text-transform: uppercase;
    margin: 0 0 0.6rem 0;
}
.result-card p {
    font-size: 1.05rem;
    font-weight: 500;
    color: #f0f2f8;
    margin: 0;
}

/* Status badges */
.badge {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    margin-bottom: 1rem;
}
.badge-ok   { background: rgba(52,199,89,0.15);  color: #34c759; border: 1px solid rgba(52,199,89,0.3); }
.badge-warn { background: rgba(255,204,0,0.15);  color: #ffc400; border: 1px solid rgba(255,204,0,0.3); }
.badge-err  { background: rgba(255,69,58,0.15);  color: #ff453a; border: 1px solid rgba(255,69,58,0.3); }

/* Section label */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    color: #7a8099;
    text-transform: uppercase;
    margin: 1.8rem 0 0.8rem 0;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #2a2e3d;
}

/* History chips */
.history-chip {
    display: inline-block;
    background: #171a22;
    border: 1px solid #2a2e3d;
    border-radius: 8px;
    padding: 5px 13px;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    color: #b0b5c8;
    margin: 3px 4px 3px 0;
    cursor: default;
    letter-spacing: 1px;
}
.history-chip:hover { border-color: #e8c547; color: #e8c547; }

/* Divider */
hr.vin-divider {
    border: none;
    border-top: 1px solid #2a2e3d;
    margin: 1.5rem 0;
}

/* Alert box override */
.stAlert { border-radius: 10px !important; }

/* Spinner text */
.stSpinner > div { color: #e8c547 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="vin-hero">
    <h1>🔍 Dekoder <span class="accent">VIN</span></h1>
    <p>Walidacja · Suma kontrolna · Dekodowanie NHTSA API</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE – HISTORIA
# ─────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ─────────────────────────────────────────────
#  ETAP 1 – WALIDACJA REGEX
# ─────────────────────────────────────────────
def validate_vin(raw: str) -> tuple[bool, str, str]:
    """
    Zwraca (ok: bool, vin: str, error_msg: str).
    vin to znormalizowany VIN (wielkie litery, bez spacji).
    """
    vin = raw.strip().upper().replace(" ", "").replace("-", "")
    if len(vin) == 0:
        return False, vin, "Proszę wpisać numer VIN."
    if len(vin) != 17:
        return False, vin, f"VIN musi mieć dokładnie 17 znaków (podano: {len(vin)})."
    forbidden = set("IOQ")
    found = [c for c in vin if c in forbidden]
    if found:
        return False, vin, f"VIN zawiera niedozwolone znaki: {', '.join(sorted(set(found)))}  (litery I, O i Q są zabronione w standardzie VIN)."
    if not re.fullmatch(r"[A-HJ-NPR-Z0-9]{17}", vin):
        return False, vin, "VIN zawiera niedozwolone znaki. Dozwolone: cyfry 0–9 oraz litery A–Z (bez I, O, Q)."
    return True, vin, ""

# ─────────────────────────────────────────────
#  ETAP 2 – SUMA KONTROLNA ISO/USA
# ─────────────────────────────────────────────
TRANSLITERATION = {
    'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,
    'J':1,'K':2,'L':3,'M':4,'N':5,       'P':7,'R':9,
          'S':2,'T':3,'U':4,'V':5,'W':6,'X':7,'Y':8,'Z':9,
    '0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,
}

WEIGHTS = [8,7,6,5,4,3,2,10,0,9,8,7,6,5,4,3,2]

def checksum_verify(vin: str) -> tuple[bool, str, str]:
    """
    Zwraca (ok: bool, expected: str, actual: str).
    expected – jaki znak powinien stać na pozycji 9 wg algorytmu.
    actual   – jaki znak faktycznie stoi na pozycji 9 w VIN.
    """
    total = sum(TRANSLITERATION[ch] * WEIGHTS[i] for i, ch in enumerate(vin))
    remainder = total % 11
    expected = 'X' if remainder == 10 else str(remainder)
    actual = vin[8]
    return expected == actual, expected, actual

# ─────────────────────────────────────────────
#  ETAP 3 – DEKODOWANIE NHTSA API
# ─────────────────────────────────────────────
FIELDS_MAP = {
    "Make":                       "Marka",
    "Model":                      "Model",
    "Model Year":                 "Rok modelowy",
    "Plant Country":              "Kraj produkcji",
    "Vehicle Type":               "Typ pojazdu",
    "Body Class":                 "Typ nadwozia",
    "Displacement (L)":           "Pojemność silnika (L)",
    "Engine Number of Cylinders": "Liczba cylindrów",
    "Drive Type":                 "Rodzaj napędu",
}

def decode_vin_api(vin: str) -> tuple[bool, dict, str]:
    """
    Wywołuje NHTSA API i zwraca (ok, data_dict, error_msg).
    data_dict zawiera przefiltrowane i przetłumaczone pola.
    """
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
    except requests.exceptions.Timeout:
        return False, {}, "Przekroczono czas oczekiwania na odpowiedź z API (timeout 15 s)."
    except requests.exceptions.ConnectionError:
        return False, {}, "Brak połączenia z internetem lub serwer NHTSA jest niedostępny."
    except requests.exceptions.HTTPError as e:
        return False, {}, f"Błąd HTTP: {e}"
    except Exception as e:
        return False, {}, f"Nieznany błąd podczas połączenia: {e}"

    try:
        payload = resp.json()
        results = payload.get("Results", [])
    except Exception:
        return False, {}, "Nie udało się sparsować odpowiedzi JSON z serwera NHTSA."

    data = {}
    for item in results:
        var = item.get("Variable", "")
        val = item.get("Value", None)
        if var in FIELDS_MAP and val and val.strip() and val.strip().lower() != "not applicable":
            data[FIELDS_MAP[var]] = val.strip()

    if not data:
        return False, {}, "API zwróciło odpowiedź, ale nie znaleziono żadnych danych dla tego VIN. Może to być numer spoza bazy NHTSA (pojazdy europejskie są czasami nieznane)."

    return True, data, ""

# ─────────────────────────────────────────────
#  UI – INPUT
# ─────────────────────────────────────────────
vin_input = st.text_input(
    "Numer VIN pojazdu",
    placeholder="np. 1HGBH41JXMN109186",
    max_chars=20,
    help="17-znakowy numer identyfikacyjny pojazdu (bez liter I, O, Q)",
)

decode_btn = st.button("🔎 Dekoduj VIN", use_container_width=True)

# ─────────────────────────────────────────────
#  LOGIKA GŁÓWNA
# ─────────────────────────────────────────────
if decode_btn:
    if not vin_input.strip():
        st.markdown('<span class="badge badge-err">⛔ Błąd</span>', unsafe_allow_html=True)
        st.error("Pole VIN jest puste. Wpisz numer VIN, aby kontynuować.")
    else:
        # ── Etap 1: Walidacja ──────────────────────────────────────────
        st.markdown('<div class="section-label">Etap 1 — Walidacja formatu</div>', unsafe_allow_html=True)
        valid, vin_clean, err_msg = validate_vin(vin_input)

        if not valid:
            st.markdown('<span class="badge badge-err">⛔ Błąd formatu</span>', unsafe_allow_html=True)
            st.error(err_msg)
        else:
            st.markdown('<span class="badge badge-ok">✓ Format VIN poprawny</span>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="result-card">
                <h3>Znormalizowany VIN</h3>
                <p style="font-family:'Space Mono',monospace; letter-spacing:3px; font-size:1.25rem;">{vin_clean}</p>
            </div>""", unsafe_allow_html=True)

            # ── Etap 2: Suma kontrolna ─────────────────────────────────
            st.markdown('<div class="section-label">Etap 2 — Matematyczna suma kontrolna</div>', unsafe_allow_html=True)
            cs_ok, cs_expected, cs_actual = checksum_verify(vin_clean)

            if cs_ok:
                st.markdown('<span class="badge badge-ok">✓ Suma kontrolna się zgadza</span>', unsafe_allow_html=True)
                st.success(f"Znak kontrolny na pozycji 9: **{cs_actual}** — zgodny z algorytmem ISO/USA.")
            else:
                st.markdown('<span class="badge badge-warn">⚠ Ostrzeżenie — suma kontrolna</span>', unsafe_allow_html=True)
                st.warning(
                    f"Suma kontrolna się **nie zgadza** — algorytm oczekuje znaku **{cs_expected}**, "
                    f"a VIN zawiera **{cs_actual}** na pozycji 9.\n\n"
                    "ℹ️ W krajach UE weryfikacja sumy kontrolnej nie jest obowiązkowa, więc wiele europejskich "
                    "pojazdów nie przejdzie tego testu. Dekodowanie zostanie wykonane mimo to."
                )

            # ── Etap 3: API NHTSA ──────────────────────────────────────
            st.markdown('<div class="section-label">Etap 3 — Dekodowanie online (NHTSA API)</div>', unsafe_allow_html=True)

            with st.spinner("Pobieranie danych z serwera NHTSA…"):
                time.sleep(0.3)  # drobne opóźnienie dla lepszego UX spinnera
                api_ok, api_data, api_err = decode_vin_api(vin_clean)

            if not api_ok:
                st.markdown('<span class="badge badge-err">⛔ Błąd API</span>', unsafe_allow_html=True)
                st.error(api_err)
            else:
                st.markdown('<span class="badge badge-ok">✓ Dane pobrane pomyślnie</span>', unsafe_allow_html=True)

                # Wyświetl kafelki w układzie 3-kolumnowym
                cols_def = [
                    "Marka", "Model", "Rok modelowy",
                    "Kraj produkcji", "Typ pojazdu", "Typ nadwozia",
                    "Pojemność silnika (L)", "Liczba cylindrów", "Rodzaj napędu",
                ]

                # Filtruj do tych, które faktycznie mamy
                available = [f for f in cols_def if f in api_data]
                # Dopełnij do wielokrotności 3
                while len(available) % 3 != 0:
                    available.append(None)

                for row_start in range(0, len(available), 3):
                    cols = st.columns(3)
                    for ci, field in enumerate(available[row_start:row_start+3]):
                        with cols[ci]:
                            if field:
                                st.markdown(f"""
                                <div class="result-card" style="height:100px;">
                                    <h3>{field}</h3>
                                    <p>{api_data[field]}</p>
                                </div>""", unsafe_allow_html=True)

                # Dodaj do historii
                if vin_clean not in st.session_state.history:
                    st.session_state.history.insert(0, vin_clean)
                    if len(st.session_state.history) > 10:
                        st.session_state.history.pop()

# ─────────────────────────────────────────────
#  HISTORIA WYSZUKIWANIA
# ─────────────────────────────────────────────
if st.session_state.history:
    st.markdown('<hr class="vin-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Historia wyszukiwania (sesja)</div>', unsafe_allow_html=True)
    chips_html = "".join(
        f'<span class="history-chip">{v}</span>'
        for v in st.session_state.history
    )
    st.markdown(f'<div>{chips_html}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col_clear, _ = st.columns([1, 4])
    with col_clear:
        if st.button("🗑 Wyczyść historię", use_container_width=True):
            st.session_state.history = []
            st.rerun()

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<hr class="vin-divider">
<p style="text-align:center; color:#3d4255; font-size:0.78rem; margin-top:0.5rem;">
    Dane dostarczane przez <strong style="color:#5a607a;">NHTSA vPIC API</strong>
    &nbsp;·&nbsp; Weryfikacja sumy kontrolnej: standard <strong style="color:#5a607a;">ISO 3779 / FMVSS 115</strong>
</p>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  INSTRUKCJA URUCHOMIENIA
# ═══════════════════════════════════════════════════════════════
#
#  KROK 1 — Zainstaluj wymagane biblioteki (jednorazowo):
#     pip install streamlit requests
#
#  KROK 2 — Uruchom aplikację z terminala (będąc w folderze
#            z plikiem app.py):
#     streamlit run app.py
#
#  KROK 3 — Przeglądarka powinna otworzyć się automatycznie
#            pod adresem http://localhost:8501
#            Jeśli nie, wpisz ten adres ręcznie w przeglądarce.
#
# ═══════════════════════════════════════════════════════════════
