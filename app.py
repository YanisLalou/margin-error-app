import math
import streamlit as st

def margin_of_error(p_hat, n, confidence=0.95):
    Z = 1.96 if confidence == 0.95 else 2.58
    se = math.sqrt(p_hat * (1 - p_hat) / n)
    return Z * se

st.title("📊 Margin of Error Calculator")

p_hat = st.number_input("Enter p̂ (proportion)", value=0.0143, format="%.5f")
n = st.number_input("Enter sample size (n)", value=38000, step=1)
confidence = st.selectbox("Confidence Level", [0.95, 0.99])

if st.button("Calculate"):
    E = margin_of_error(p_hat, n, confidence)
    st.success(f"Margin of error ≈ {E:.4f} ({E*100:.2f}%)")
