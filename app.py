import math
import streamlit as st
import numpy as np # Used for cleaner formatting of the number of minority samples

# The core statistical function remains correct: E = Z * sqrt(p(1-p)/n)
def calculate_margin_of_error(p_hat, N, Z):
    """Calculates the Margin of Error (E) for a proportion."""
    # Standard Error (SE)
    se = math.sqrt(p_hat * (1 - p_hat) / N)
    # Margin of Error (E = Z * SE)
    return Z * se

# --- Streamlit App Layout ---

st.title("📊 Precision Analyzer for Imbalanced Data")
st.markdown("Calculate the **actual Margin of Error** given your total dataset size and the rare event's proportion.")

# --- Input Section ---

st.header("1. Input Data")

# Input for the proportion (p_hat)
p_hat = st.number_input(
    "Observed Proportion of the Minority Class (p̂)",
    value=0.0143,
    min_value=0.0,
    max_value=1.0,
    format="%.5f",
    help="e.g., 0.0143 if the rare event is 1.43% of the total dataset."
)

# Input for the total sample size (N)
N = st.number_input(
    "Total Dataset Size (N)",
    value=38000,
    min_value=1,
    step=1000,
    format="%d",
    help="The total number of samples/rows in your dataset."
)

# Confidence Level selection
confidence = st.selectbox(
    "Confidence Level (Z-score)",
    options=[0.95, 0.99, 0.90],
    index=0,
    format_func=lambda x: f"{int(x*100)}%"
)

# --- Z-Score Selection ---

# Determine the Z-score based on the selected confidence level
if confidence == 0.95:
    Z = 1.96
elif confidence == 0.99:
    Z = 2.58
elif confidence == 0.90:
    Z = 1.645 # Common Z-score for 90% confidence
else:
    Z = 1.96 # Default fallback

# --- Calculation & Output ---

if st.button("Analyze Precision"):
    # Calculate the number of minority samples
    n_minority = N * p_hat

    # Perform the core calculation
    E = calculate_margin_of_error(p_hat, N, Z)

    st.header("2. Results")

    # Display key stats first
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Total Samples ($N$)",
            value=f"{N:,}"
        )
    with col2:
        # Use a consistent display format
        st.metric(
            label="Minority Samples ($n_{minority}$)",
            value=f"{int(round(n_minority)):,}"
        )

    # Display the final margin of error
    st.subheader("Final Margin of Error ($E$)")
    st.success(f"**Margin of Error** ($E$) for your $\\hat{{p}}$ is:")
    st.markdown(f"""
    $$\\approx \\pm \\mathbf{{{E*100:.2f}\\%}} \\quad (\\pm {E:.4f})$$
    """)
    st.info(f"We are {int(confidence*100)}% confident that the true population proportion is within $\\pm {E*100:.2f}\\%$ of your observed $\\hat{{p}} = {p_hat:.4f}$.")

    st.markdown("---")
    st.caption(f"**Z-Score Used:** {Z}")
    st.latex(f"E = {Z} \\cdot \\sqrt{{\\frac{{{p_hat:.4f} \\cdot (1 - {p_hat:.4f})}}{{{N}}}}}")
