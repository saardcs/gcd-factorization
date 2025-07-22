import streamlit as st
import random
import math
import qrcode
import io

# --------------------------
# Problem Set (smaller numbers for easier listing)
problems = [
    (12, 18), (24, 30), (15, 20),
    (28, 35), (50, 75)  # Smaller numbers for easier listing
]

# --------------------------
# Session State Initialization
if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.factors_submitted = False  # Track whether factors are confirmed
    st.session_state.correct_factors = False  # Track if factors are correct
    st.session_state.user_gcd = None  # Track user GCD input
    st.session_state.correct_gcd = None  # Track correct GCD for comparison

# --------------------------
# Header
st.title("💡 GCD Lab")
st.markdown("Type the factors of the two numbers below, then calculate the GCD based on the common factors.")

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

    # If factors not submitted yet
    if not st.session_state.factors_submitted:
        a_factors = st.text_area(f"List the factors of **{a}** (separate by commas):", key="a_factors", help="Example: 1, 2, 3, 4, 6, 12")
        b_factors = st.text_area(f"List the factors of **{b}** (separate by commas):", key="b_factors", help="Example: 1, 2, 3, 6, 9, 18")

        # Submit button for factors
        if st.button("Submit Factors"):
            try:
                # Clean up the input to remove non-numeric and spaces
                a_factors = set(map(int, a_factors.replace(" ", "").split(",")))
                b_factors = set(map(int, b_factors.replace(" ", "").split(",")))

                # Correct factors
                correct_a_factors = set([i for i in range(1, a + 1) if a % i == 0])
                correct_b_factors = set([i for i in range(1, b + 1) if b % i == 0])

                # Check if factors are correct
                if a_factors != correct_a_factors:
                    st.error("❌ Incorrect factors for A. Please check your list and try again!")
                    st.session_state.correct_factors = False
                elif b_factors != correct_b_factors:
                    st.error("❌ Incorrect factors for B. Please check your list and try again!")
                    st.session_state.correct_factors = False
                else:
                    # After correctly listing the factors, set a flag to show the GCD input
                    st.session_state.factors_submitted = True  # Factors confirmed
                    st.session_state.correct_factors = True  # Factors are correct
                    common_factors = a_factors & b_factors  # Intersection of sets
                    correct_gcd = max(common_factors)  # The GCD is the largest common factor
                    st.session_state.correct_gcd = correct_gcd  # Store correct GCD

                    st.success(f"✅ Factors are correct! Now, enter the GCD of **{a}** and **{b}**.")
                    
                    # Display GCD input only now
                    user_gcd = st.number_input(f"Now, what is the GCD of **{a}** and **{b}**?", min_value=1, step=1)

                    st.session_state.user_gcd = user_gcd  # Track user GCD input

                    # Submit button for GCD
                    if st.button("Submit GCD"):
                        if st.session_state.user_gcd == st.session_state.correct_gcd:
                            st.success(f"✅ Correct! The GCD of **{a}** and **{b}** is indeed {st.session_state.correct_gcd}.")
                            st.session_state.score += 1
                            st.session_state.index += 1
                            st.session_state.factors_submitted = False  # Reset for next problem
                            st.session_state.correct_factors = False  # Reset factors check
                            st.session_state.user_gcd = None  # Reset user GCD
                            st.session_state.correct_gcd = None  # Reset correct GCD
                            st.rerun()  # Move to the next problem after correct answer
                        else:
                            st.error("❌ Incorrect GCD. Try again!")
                            # Only reset the GCD input, not the factors input
                            st.session_state.user_gcd = None  # Reset user GCD so they can try again
                            st.experimental_rerun()  # Refresh to keep GCD input visible for retry
            except ValueError:
                st.error("❌ Invalid input. Please list the factors correctly (e.g., 1, 2, 3).")
    
    # If factors are confirmed, prompt for GCD input
    elif st.session_state.factors_submitted and not st.session_state.correct_factors:
        st.write("Please submit the correct factors to proceed.")

else:
    st.success("🎉 You've completed all problems!")
    st.write(f"Your score: **{st.session_state.score} / {len(problems)}**")

    if st.button("🔁 Start Over"):
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.factors_submitted = False  # Reset the state for factors submission
        st.session_state.correct_factors = False  # Reset factors check
        st.session_state.user_gcd = None  # Reset GCD
        st.session_state.correct_gcd = None  # Reset correct GCD
        st.rerun()
