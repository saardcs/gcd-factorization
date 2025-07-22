import streamlit as st
import random
import math
import qrcode
import io

# --------------------------
# Updated Problem Set (smaller numbers for listing)
problems = [
    (12, 18), (24, 30), (15, 20), 
    (28, 35), (50, 75)  # Smaller numbers for easier listing
]

# --------------------------
# Session State Initialization (no shuffle)
if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.score = 0

# --------------------------
# Suggest Method Hint
def suggest_method(a, b):
    idx = st.session_state.index
    if idx <= 1:
        return "Try using **Prime Factorization** (listing the factors)."
    elif idx <= 3:
        return "Hint: Try **Euclidean Subtraction** method."
    else:
        return "Hint: Use the **Euclidean Division** method."

# --------------------------
# Header
st.title("💡 GCD Lab")
st.markdown("Type the factors of the two numbers, then calculate the GCD based on the common factors.")

# Sidebar with QR code
st.sidebar.header("Scan This QR Code to View Menu Online")
qr_link = "https://gcd-lab.streamlit.app"
qr = qrcode.make(qr_link)
buf = io.BytesIO()
qr.save(buf)
buf.seek(0)
st.sidebar.image(buf, width=300, caption=qr_link)

# --------------------------
# Problem Display
if st.session_state.index < len(problems):
    a, b = problems[st.session_state.index]
    st.subheader(f"🔢 Problem {st.session_state.index + 1} of {len(problems)}")
    st.write(f"What are the factors of **{a}** and **{b}**?")

    st.info(suggest_method(a, b))  # 👈 Hint display

    # Input for listing factors
    a_factors = st.text_area("List factors of A (separate by commas):", key="a_factors", help="Example: 1, 2, 3, 4, 6, 12")
    b_factors = st.text_area("List factors of B (separate by commas):", key="b_factors", help="Example: 1, 2, 3, 6, 9, 18")

    # Submit button
    if st.button("Submit"):
        # Clean up the input to remove non-numeric and spaces
        try:
            a_factors = set(map(int, a_factors.replace(" ", "").split(",")))
            b_factors = set(map(int, b_factors.replace(" ", "").split(",")))

            # Correct factors
            correct_a_factors = set([i for i in range(1, a + 1) if a % i == 0])
            correct_b_factors = set([i for i in range(1, b + 1) if b % i == 0])

            # Check if factors are correct
            if a_factors != correct_a_factors:
                st.error("❌ Incorrect factors for A. Please check your list and try again!")
            elif b_factors != correct_b_factors:
                st.error("❌ Incorrect factors for B. Please check your list and try again!")
            else:
                # Calculate GCD from common factors
                common_factors = a_factors & b_factors  # Intersection of sets
                correct_gcd = max(common_factors)

                # Ask for GCD after listing the factors
                user_gcd = st.number_input(f"Now, what is the GCD of {a} and {b}?", min_value=1, step=1)

                if user_gcd == correct_gcd:
                    st.success("✅ Correct! The GCD is indeed " + str(correct_gcd))
                    st.session_state.score += 1
                    st.session_state.index += 1
                    st.rerun()
                else:
                    st.error("❌ Incorrect GCD. Try again!")

        except ValueError:
            st.error("❌ Invalid input. Please list the factors correctly (e.g., 1, 2, 3).")

else:
    st.success("🎉 You've completed all problems!")
    st.write(f"Your score: **{st.session_state.score} / {len(problems)}**")

    if st.button("🔁 Start Over"):
        st.session_state.index = 0
        st.session_state.score = 0
        st.rerun()
