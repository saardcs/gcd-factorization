import streamlit as st
import qrcode
import io
import random

# --- Utility: Generate Meaningful Random Problems ---
def generate_problem_set(n=5):
    problems = []
    while len(problems) < n:
        gcd = random.randint(2, 15)
        x = random.randint(2, 10)
        y = random.randint(2, 10)
        a = gcd * x
        b = gcd * y
        if a > 100 or b > 100 or abs(a - b) < 5:
            continue
        problems.append((a, b))
    return problems

# --- One-time Initialization ---
if "problems" not in st.session_state:
    st.session_state.problems = generate_problem_set()
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.correct_factors = False
    st.session_state.correct_gcd = None
    st.session_state.a_factors = ""
    st.session_state.b_factors = ""
    st.session_state.gcd_input = 1

# --- Header ---
st.title("💡 GCD Lab")
st.markdown("Type the factors of the two numbers below, then calculate the GCD based on the common factors.")

# --- Sidebar QR Code ---
st.sidebar.header("Scan This QR Code to View Menu Online")
qr_link = "https://gcd-factorization.streamlit.app"
qr = qrcode.make(qr_link)
buf = io.BytesIO()
qr.save(buf)
buf.seek(0)
st.sidebar.image(buf, width=300, caption=qr_link)

# --- Main Logic ---
if st.session_state.index < len(st.session_state.problems):
    a, b = st.session_state.problems[st.session_state.index]
    st.subheader(f"🔢 Problem {st.session_state.index + 1} of {len(st.session_state.problems)}")
    st.write(f"What are the factors of **{a}** and **{b}**?")

    # --- Inputs ---
    a_input = st.text_area(f"List the factors of **{a}** (separate by commas):", 
                           value=st.session_state.a_factors, key="a_input", help="Example: 1, 2, 3, 4, 6, 12")
    b_input = st.text_area(f"List the factors of **{b}** (separate by commas):", 
                           value=st.session_state.b_factors, key="b_input", help="Example: 1, 2, 3, 6, 9, 18")

    if st.button("Submit Factors"):
        try:
            a_factors = set(map(int, a_input.replace(" ", "").split(",")))
            b_factors = set(map(int, b_input.replace(" ", "").split(",")))
            correct_a = set(i for i in range(1, a + 1) if a % i == 0)
            correct_b = set(i for i in range(1, b + 1) if b % i == 0)

            st.session_state.a_factors = a_input
            st.session_state.b_factors = b_input

            if a_factors != correct_a:
                st.error(f"❌ Incorrect factors for {a}. Please check your list and try again!")
                st.session_state.correct_factors = False
                st.session_state.correct_gcd = None
            elif b_factors != correct_b:
                st.error(f"❌ Incorrect factors for {b}. Please check your list and try again!")
                st.session_state.correct_factors = False
                st.session_state.correct_gcd = None
            else:
                st.success(f"✅ Factors are correct! Now, enter the GCD of **{a}** and **{b}**.")
                st.session_state.correct_factors = True
                st.session_state.correct_gcd = max(correct_a & correct_b)
        except ValueError:
            st.error("❌ Invalid input. Please list the factors correctly (e.g., 1, 2, 3).")
            st.session_state.correct_factors = False
            st.session_state.correct_gcd = None

    if st.session_state.correct_factors:
        user_gcd = st.number_input(f"What is the GCD of **{a}** and **{b}**?", 
                                   min_value=1, step=1, value=st.session_state.gcd_input, key="gcd_input")

        if st.button("Submit GCD"):
            if user_gcd == st.session_state.correct_gcd:
                st.success(f"✅ Correct! The GCD of **{a}** and **{b}** is indeed {st.session_state.correct_gcd}.")

                # Move to next problem
                st.session_state.index += 1
                st.session_state.score += 1
                st.session_state.correct_factors = False
                st.session_state.correct_gcd = None

                # Reset inputs
                st.session_state.a_factors = ""
                st.session_state.b_factors = ""
                st.session_state.gcd_input = 1

                st.rerun()
            else:
                st.error("❌ Incorrect GCD. Try again!")

else:
    st.success("🎉 You've completed all problems!")
    st.write(f"Your score: **{st.session_state.score} / {len(st.session_state.problems)}**")

    if st.button("🔁 Start Over"):
        st.session_state.problems = generate_problem_set()
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.correct_factors = False
        st.session_state.correct_gcd = None
        st.session_state.a_factors = ""
        st.session_state.b_factors = ""
        st.session_state.gcd_input = 1
        st.rerun()
