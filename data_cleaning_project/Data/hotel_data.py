"""
Generador de dataset ficticio de reservas hoteleras (nivel de RESERVA, no diario)
-----------------------------------------------------------------------------
Hotel: "Hotel Playa Serena" — hotel vacacional de playa (4*) en Mallorca, 200 hab.


"""

import numpy as np
import pandas as pd
from datetime import date, timedelta
import random

# ------------------------------------------------------------------
# CONFIGURACIÓN GENERAL
# ------------------------------------------------------------------
SEED = 42
np.random.seed(SEED)
random.seed(SEED)

HOTEL_NAME = "Hotel Playa Serena"
TOTAL_ROOMS = 200
YEAR = 2025
START_DATE = date(YEAR, 1, 1)
N_DAYS = 365

# ------------------------------------------------------------------
# EVENTOS: festivos fijos + eventos culturales/deportivos/conciertos
# ------------------------------------------------------------------
FIXED_EVENTS = {
    date(YEAR, 1, 1): ("Festivo", "Año Nuevo"),
    date(YEAR, 1, 6): ("Festivo", "Reyes"),
    date(YEAR, 4, 18): ("Festivo", "Semana Santa"),
    date(YEAR, 4, 19): ("Festivo", "Semana Santa"),
    date(YEAR, 4, 20): ("Festivo", "Semana Santa (Pascua)"),
    date(YEAR, 4, 25): ("Feria", "Fira del Ram (Palma)"),
    date(YEAR, 5, 3): ("Feria", "Palma International Boat Show"),
    date(YEAR, 5, 16): ("Concierto", "Mallorca Live Festival"),
    date(YEAR, 5, 17): ("Concierto", "Mallorca Live Festival"),
    date(YEAR, 6, 23): ("Festivo", "Sant Joan (Nit de Foc)"),
    date(YEAR, 6, 24): ("Festivo", "Sant Joan"),
    date(YEAR, 7, 30): ("Deporte", "Copa del Rey MAPFRE (Vela)"),
    date(YEAR, 7, 31): ("Deporte", "Copa del Rey MAPFRE (Vela)"),
    date(YEAR, 8, 1): ("Deporte", "Copa del Rey MAPFRE (Vela)"),
    date(YEAR, 8, 15): ("Festivo", "Asunción / Festes de Palma"),
    date(YEAR, 9, 12): ("Concierto", "Rock the Coast Festival"),
    date(YEAR, 9, 13): ("Concierto", "Rock the Coast Festival"),
    date(YEAR, 9, 19): ("Cultural", "Nit de l'Art (Palma)"),
    date(YEAR, 10, 19): ("Deporte", "Mallorca Marathon"),
    date(YEAR, 12, 24): ("Festivo", "Nochebuena"),
    date(YEAR, 12, 25): ("Festivo", "Navidad"),
    date(YEAR, 12, 31): ("Festivo", "Nochevieja"),
}

# Eventos "aleatorios" tipo concierto/partido/congreso: no siempre caen en la
# misma fecha cada año, así que se generan al azar dentro de rangos plausibles.
def generar_eventos_aleatorios():
    eventos = {}
    posibles_dias = list(pd.date_range(f"{YEAR}-04-01", f"{YEAR}-10-31"))
    idx_concierto = np.random.choice(len(posibles_dias), size=10, replace=False)
    for i in idx_concierto:
        d = pd.Timestamp(posibles_dias[i]).date()
        eventos[d] = ("Concierto", random.choice(
            ["Concierto Internacional Palma Arena", "Festival de Música Local",
             "Concierto Playa de Palma", "DJ Set / Festival Electrónico"]))

    posibles_partidos = list(pd.date_range(f"{YEAR}-01-01", f"{YEAR}-05-31")) + \
                        list(pd.date_range(f"{YEAR}-08-15", f"{YEAR}-12-31"))
    idx_futbol = np.random.choice(len(posibles_partidos), size=8, replace=False)
    for i in idx_futbol:
        d = pd.Timestamp(posibles_partidos[i]).date()
        eventos[d] = ("Deporte", "Partido Real Mallorca (Son Moix)")

    posibles_congresos = list(pd.date_range(f"{YEAR}-02-01", f"{YEAR}-03-31")) + \
                         list(pd.date_range(f"{YEAR}-11-01", f"{YEAR}-11-30"))
    idx_congreso = np.random.choice(len(posibles_congresos), size=6, replace=False)
    for i in idx_congreso:
        d = pd.Timestamp(posibles_congresos[i]).date()
        eventos[d] = ("Congreso", "Congreso / Convención Corporativa")
    return eventos


ALL_EVENTS = {**FIXED_EVENTS, **generar_eventos_aleatorios()}

DISTRIBUTION_CHANNELS = ["Directo (Web/Teléfono)", "Booking.com", "Expedia",
                         "Turoperador", "Agencia de Viajes", "GDS"]
MARKET_SEGMENTS = ["Ocio/Vacacional", "Turoperador/Contratado", "Corporativo",
                   "Grupos", "Bodas/Eventos"]
ROOM_TYPES = ["Estándar", "Superior", "Deluxe Vista Mar", "Suite Familiar", "Swim-up"]
RATE_PLANS = ["BAR (Tarifa Flexible)", "No Reembolsable", "Todo Incluido",
              "Media Pensión", "Oferta Anticipada (Early Booking)", "Última Hora"]
NATIONALITIES = ["Alemania", "Reino Unido", "España", "Francia", "Países Bajos",
                 "Bélgica", "Países Nórdicos", "Italia", "Otros"]


def pesos_por_temporada(temporada):
    if temporada == "Alta":
        canal = [0.20, 0.32, 0.18, 0.20, 0.07, 0.03]
        segmento = [0.55, 0.25, 0.05, 0.10, 0.05]
        nacionalidad = [0.27, 0.25, 0.10, 0.10, 0.08, 0.07, 0.06, 0.04, 0.03]
    elif temporada == "Media":
        canal = [0.25, 0.28, 0.15, 0.15, 0.12, 0.05]
        segmento = [0.45, 0.15, 0.15, 0.15, 0.10]
        nacionalidad = [0.20, 0.18, 0.20, 0.10, 0.09, 0.06, 0.05, 0.06, 0.06]
    else:
        canal = [0.30, 0.20, 0.10, 0.05, 0.15, 0.20]
        segmento = [0.25, 0.05, 0.35, 0.20, 0.15]
        nacionalidad = [0.12, 0.10, 0.40, 0.08, 0.06, 0.04, 0.04, 0.06, 0.10]
    return canal, segmento, nacionalidad


def get_season(d: date) -> str:
    m, day = d.month, d.day
    if m in (6, 7, 8) or (m == 9 and day <= 15):
        return "Alta"
    elif m in (4, 5, 10) or (m == 9 and day > 15):
        return "Media"
    else:
        return "Baja"


def is_weekend(d: date) -> bool:
    return d.weekday() in (4, 5)


# ------------------------------------------------------------------
# PASO 1: KPIs diarios a nivel hotel (para calcular cuántas reservas
# generar cada día y qué ADR/ocupación objetivo tienen)
# ------------------------------------------------------------------
daily_kpis = []
for i in range(N_DAYS):
    d = START_DATE + timedelta(days=i)
    season = get_season(d)
    weekend = is_weekend(d)
    event_type, event_name = ALL_EVENTS.get(d, ("", ""))

    rooms_ooo = np.random.randint(0, 6)
    rooms_available = TOTAL_ROOMS - rooms_ooo

    if season == "Alta":
        occ = np.random.uniform(0.85, 0.99)
        adr_base = np.random.uniform(150, 285)
        los_base = np.random.uniform(5, 10)
        lead_base = np.random.uniform(60, 190)
    elif season == "Media":
        occ = np.random.uniform(0.50, 0.78)
        adr_base = np.random.uniform(90, 155)
        los_base = np.random.uniform(3, 6)
        lead_base = np.random.uniform(25, 95)
    else:
        occ = np.random.uniform(0.18, 0.48)
        adr_base = np.random.uniform(55, 95)
        los_base = np.random.uniform(1, 3.5)
        lead_base = np.random.uniform(2, 45)

    if weekend:
        occ += np.random.uniform(0.03, 0.08)
    if event_type:
        if event_type in ("Concierto", "Deporte"):
            occ += np.random.uniform(0.10, 0.20)
            adr_base *= np.random.uniform(1.10, 1.35)
        elif event_type == "Congreso":
            occ += np.random.uniform(0.08, 0.15)
            adr_base *= np.random.uniform(1.02, 1.10)
        else:
            occ += np.random.uniform(0.08, 0.15)
            adr_base *= np.random.uniform(1.05, 1.25)

    occ = min(occ, 0.99)
    rooms_sold = int(round(rooms_available * occ))

    daily_kpis.append({
        "date": d, "season": season, "weekend": weekend,
        "event_type": event_type, "event_name": event_name,
        "rooms_available": rooms_available, "rooms_ooo": rooms_ooo,
        "rooms_sold": rooms_sold, "occupancy": round(occ * 100, 2),
        "adr_base": adr_base, "los_base": los_base, "lead_base": lead_base,
    })

daily_df = pd.DataFrame(daily_kpis)

# ------------------------------------------------------------------
# PASO 2: generar RESERVAS individuales a partir de los KPIs diarios
# ------------------------------------------------------------------
bookings = []
booking_counter = 100000

for _, day in daily_df.iterrows():
    d = day["date"]
    season = day["season"]
    canal_w, segmento_w, nac_w = pesos_por_temporada(season)

    n_bookings = max(1, int(round(day["rooms_sold"] / max(day["los_base"], 1))))

    for _ in range(n_bookings):
        booking_counter += 1
        los = max(1, int(round(np.random.normal(day["los_base"], 1.2))))
        lead_time = max(0, int(round(np.random.normal(day["lead_base"], 15))))
        adr = round(max(30, np.random.normal(day["adr_base"], day["adr_base"] * 0.12)), 2)
        departure = d + timedelta(days=los)
        booking_date = d - timedelta(days=lead_time)

        is_cancelled = np.random.random() < (
            0.05 if season == "Alta" else 0.09 if season == "Media" else 0.14
        )
        is_walk_in = lead_time == 0 and np.random.random() < 0.3

        bookings.append({
            "Booking_ID": f"HPS-{booking_counter}",
            "Booking_Date": booking_date,
            "Arrival_Date": d,
            "Departure_Date": departure,
            "Day_of_Week": d.strftime("%A"),
            "Season": season,
            "Is_Weekend": day["weekend"],
            "Event_Type": day["event_type"],
            "Event_Name": day["event_name"],
            "Rooms_Available": day["rooms_available"],
            "Rooms_Sold": day["rooms_sold"],
            "Occupancy_%": day["occupancy"],
            "ADR": adr,
            "Room_Revenue": round(adr * los, 2),
            "RevPAR": round((day["rooms_sold"] * day["adr_base"]) / day["rooms_available"], 2),
            "Distribution_Channel": np.random.choice(DISTRIBUTION_CHANNELS, p=canal_w),
            "Market_Segment": np.random.choice(MARKET_SEGMENTS, p=segmento_w),
            "Length_of_Stay": los,
            "Lead_Time_Days": lead_time,
            "Is_Cancelled": is_cancelled,
            "Is_Walk_in": is_walk_in,
            "Nationality": np.random.choice(NATIONALITIES, p=nac_w),
            "Room_Type": np.random.choice(ROOM_TYPES, p=[0.30, 0.28, 0.20, 0.14, 0.08]),
            "Rate_Plan": np.random.choice(RATE_PLANS, p=[0.30, 0.15, 0.25, 0.15, 0.10, 0.05]),
        })

df = pd.DataFrame(bookings)
print(f"Dataset LIMPIO generado: {len(df)} reservas, {len(df.columns)} columnas")

df.to_csv("hotel_playa_serena_reservas_LIMPIO.csv", index=False, encoding="utf-8-sig")


# ------------------------------------------------------------------
# PASO 3: ENSUCIAR el dataset a propósito, para practicar limpieza
# ------------------------------------------------------------------
def ensuciar_dataset(df_in, frac_afectada=0.12, seed=SEED):
    """
    Introduce errores típicos de datos reales sobre una copia del dataframe:
    - Valores nulos / placeholders raros ("N/A", "-", "desconocido", "")
    - Inconsistencias de mayúsculas/minúsculas y espacios en texto
    - Typos en categorías (nacionalidad, canal)
    - Tipos de dato mezclados en columnas numéricas (texto, comas decimales, símbolo €)
    - Outliers / valores imposibles (ocupación >100%, ADR negativo)
    - Fechas en formatos distintos dentro de la misma columna
    - Filas duplicadas
    - Columna "índice fantasma" típica de exportaciones de Excel
    """
    rng = np.random.default_rng(seed)
    df_dirty = df_in.copy()
    n = len(df_dirty)

    placeholders_nulos = ["N/A", "-", "", "desconocido", "n/d", None]
    for col in ["Nationality", "Distribution_Channel", "Rate_Plan", "Lead_Time_Days"]:
        df_dirty[col] = df_dirty[col].astype(object)
        idx = rng.choice(n, size=int(n * frac_afectada * 0.5), replace=False)
        df_dirty.loc[idx, col] = rng.choice(placeholders_nulos, size=len(idx))

    def ensuciar_texto(valor):
        if pd.isna(valor):
            return valor
        opcion = rng.random()
        if opcion < 0.25:
            return str(valor).upper()
        elif opcion < 0.45:
            return str(valor).lower()
        elif opcion < 0.65:
            return f"  {valor}  "
        elif opcion < 0.80:
            v = str(valor)
            if len(v) > 3:
                pos = rng.integers(1, len(v) - 1)
                v = v[:pos] + v[pos] + v[pos:]
            return v
        return valor

    for col in ["Nationality", "Distribution_Channel", "Room_Type", "Market_Segment", "Rate_Plan"]:
        idx = rng.choice(n, size=int(n * frac_afectada), replace=False)
        df_dirty.loc[idx, col] = df_dirty.loc[idx, col].apply(ensuciar_texto)

    idx_adr_texto = rng.choice(n, size=int(n * frac_afectada * 0.4), replace=False)
    df_dirty["ADR"] = df_dirty["ADR"].astype(object)
    for i in idx_adr_texto:
        val = df_dirty.at[i, "ADR"]
        estilo = rng.random()
        if estilo < 0.4:
            df_dirty.at[i, "ADR"] = f"{val}€"
        elif estilo < 0.7:
            df_dirty.at[i, "ADR"] = str(val).replace(".", ",")
        else:
            df_dirty.at[i, "ADR"] = str(val)

    idx_occ_texto = rng.choice(n, size=int(n * frac_afectada * 0.3), replace=False)
    df_dirty["Occupancy_%"] = df_dirty["Occupancy_%"].astype(object)
    for i in idx_occ_texto:
        df_dirty.at[i, "Occupancy_%"] = f"{df_dirty.at[i, 'Occupancy_%']}%"

    idx_outlier_occ = rng.choice(n, size=int(n * 0.01), replace=False)
    for i in idx_outlier_occ:
        val_actual = df_dirty.at[i, "Occupancy_%"]
        if isinstance(val_actual, str):
            continue
        df_dirty.at[i, "Occupancy_%"] = float(val_actual) * rng.choice([1.5, -1])

    idx_outlier_adr = rng.choice(n, size=int(n * 0.01), replace=False)
    for i in idx_outlier_adr:
        if isinstance(df_dirty.at[i, "ADR"], str):
            continue
        df_dirty.at[i, "ADR"] = float(df_dirty.at[i, "ADR"]) * -1

    idx_lead_negativo = rng.choice(n, size=int(n * 0.015), replace=False)
    for i in idx_lead_negativo:
        val = df_dirty.at[i, "Lead_Time_Days"]
        if pd.isna(val) or isinstance(val, str):
            continue
        df_dirty.at[i, "Lead_Time_Days"] = -abs(int(val))

    def formatear_fecha_random(fecha):
        if pd.isna(fecha):
            return fecha
        formato = rng.random()
        if formato < 0.33:
            return pd.Timestamp(fecha).strftime("%d/%m/%Y")
        elif formato < 0.66:
            return pd.Timestamp(fecha).strftime("%Y-%m-%d")
        else:
            return pd.Timestamp(fecha).strftime("%d-%b-%Y")

    for col in ["Arrival_Date", "Booking_Date", "Departure_Date"]:
        df_dirty[col] = df_dirty[col].astype(object)
        idx = rng.choice(n, size=int(n * frac_afectada), replace=False)
        for i in idx:
            df_dirty.at[i, col] = formatear_fecha_random(df_dirty.at[i, col])

    idx_duplicados = rng.choice(n, size=int(n * 0.02), replace=False)
    df_duplicadas = df_dirty.loc[idx_duplicados]
    df_dirty = pd.concat([df_dirty, df_duplicadas], ignore_index=True)

    for col in ["Is_Cancelled", "Is_Walk_in"]:
        df_dirty[col] = df_dirty[col].astype(object)
        idx = rng.choice(len(df_dirty), size=int(len(df_dirty) * frac_afectada * 0.5), replace=False)
        for i in idx:
            valor_original = df_dirty.at[i, col]
            if valor_original in (True, False):
                df_dirty.at[i, col] = str(valor_original) if rng.random() < 0.5 else (
                    "Sí" if valor_original else "No")

    df_dirty.insert(0, "Unnamed: 0", range(len(df_dirty)))
    df_dirty = df_dirty.sample(frac=1, random_state=seed).reset_index(drop=True)

    return df_dirty


df_dirty = ensuciar_dataset(df, frac_afectada=0.12)
print(f"Dataset SUCIO generado: {len(df_dirty)} filas (incluye duplicados)")

df_dirty.to_csv("hotel_playa_serena_reservas_SUCIO.csv", index=False, encoding="utf-8-sig")

print("\nArchivos generados:")
print(" - hotel_playa_serena_reservas_LIMPIO.csv  (dataset de referencia, ya limpio)")
print(" - hotel_playa_serena_reservas_SUCIO.csv   (dataset para practicar limpieza)")
print("\nMuestra de filas sucias:")
print(df_dirty.head(8))