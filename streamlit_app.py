import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="KI-Trading-Wächter", page_icon="📈")

st.title("🚀 Dein KI-Trading-Wächter")
st.write("Verpasse nie wieder den Ausstieg!")

# 1. EINGABE: Was hast du gekauft?
with st.sidebar:
    st.header("Deine Bestände")
    mein_ticker = st.text_input("Aktie im Depot (Kürzel)", "NVDA").upper()
    kaufpreis = st.number_input("Dein Kaufpreis ($)", value=100.0)
    st.info("Die KI berechnet für dich den 'Trailing Stop-Loss' (Sicherheitsnetz).")

# 2. ANALYSE-LOGIK
if mein_ticker:
    data = yf.Ticker(mein_ticker)
    df = data.history(period="1mo")
    
    if not df.empty:
        aktueller_kurs = df['Close'][-1]
        hoechstkurs_seit_kauf = df['High'].max()
        
        # Die goldene Regel: Verkaufe, wenn die Aktie 10% vom Höchststand fällt
        stopp_kurs = hoechstkurs_seit_kauf * 0.90
        gewinn_verlust = ((aktueller_kurs - kaufpreis) / kaufpreis) * 100

        # Anzeige
        col1, col2 = st.columns(2)
        col1.metric("Aktueller Kurs", f"{round(aktueller_kurs, 2)} $", f"{round(gewinn_verlust, 2)} %")
        col2.metric("Dein Sicherheitsnetz", f"{round(stopp_kurs, 2)} $")

        # 3. DIE ENTSCHEIDUNG (Die 'Dummen-Sichere' Anzeige)
        st.divider()
        
        if aktueller_kurs <= stopp_kurs:
            st.error("🚨 ALARM: JETZT VERKAUFEN!")
            st.subheader(f"Zieh die Reißleine bei {round(aktueller_kurs, 2)} $!")
            st.write("Die Aktie hat ihr Momentum verloren. Sichere deine Gewinne oder begrenzt den Verlust.")
        elif aktueller_kurs > kaufpreis * 1.20:
            st.success("💰 GEWINNE LAUFEN LASSEN")
            st.write("Du bist fett im Plus. Setze deinen mentalen Stopp auf den 'Sicherheitsnetz'-Wert oben.")
        else:
            st.warning("😴 FÜSSE STILLHALTEN")
            st.write("Kein Grund zur Panik. Die Aktie schwankt im normalen Bereich.")

# 4. AUTOMATISIERUNG: Erinnerung erstellen
st.divider()
st.subheader("⏰ Benachrichtigung einrichten")
st.write("Willst du, dass ich dich in einer Stunde an den Check erinnere?")

if st.button("Erinnerung in 1 Std. erstellen"):
    # Hier nutzen wir das System-Tool für Erinnerungen
    st.info("Ich bereite die Erinnerung vor...")
