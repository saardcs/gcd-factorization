import streamlit as st
import qrcode
import io

# --------------------------
# Problem Set
problems = [
    (12, 18), (24, 30), (15, 20),
    (28, 35), (50, 75)
]

# --------------------------
# Session State Initialization
if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.factors_submitted = False
    st.session_state.correct_factors = False
    st.session_state.user_gcd = None
    st.session_state.correct_gcd = None
    st.session_state.correct_a_factors = []
    st.session_state.correct_b_factors = []

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

    if not st.session_state.factors_submitted:
        a_input = st.text_area(f"List the factors of **{a}** (separate by commas):", key="a_factors", help="Example: 1, 2, 3, 4, 6, 12")
        b_input = st.text_area(f"List the factors of **{b}** (separate by commas):", key="b_factors", help="Example: 1, 2, 3, 6, 9, 18")

        if st.button("Submit Factors"):
            try:
                a_factors = set(map(int, a_input.replace(" ", "").split(",")))
                b_factors = set(map(int, b_input.replace(" ", "").split(",")))

                correct_a = set(i for i in range(1, a + 1) if a % i == 0)
                correct_b = set(i for i in range(1, b + 1) if b % i == 0)

                if a_factors != correct_a:
                    st.error("❌ Incorrect factors for A. Please check your list and try again!")
                    st.session_state.correct_factors = False
                elif b_factors != correct_b:
                    st.error("❌ Incorrect factors for B. Please check your list and try again!")
                    st.session_state.correct_factors = False
                else:
                    st.session_state.factors_submitted = True
                    st.session_state.correct_factors = True
                    st.session_state.correct_a_factors = sorted(correct_a)
                    st.session_state.correct_b_factors = sorted(correct_b)
                    st.session_state.correct_gcd = max(correct_a & correct_b)
            except ValueError:
                st.error("❌ Invalid input. Please list the factors correctly (e.g., 1, 2, 3).")

    # Always show correct factors and GCD input if factors are valid
    if st.session_state.factors_submitted and st.session_state.correct_factors:
        st.success(f"✅ Factors are correct! Now, enter the GCD of **{a}** and **{b}**.")

        st.markdown(f"**✔️ Factors of {a}:** {', '.join(map(str, st.session_state.correct_a_factors))}")
        st.markdown(f"**✔️ Factors of {b}:** {', '.join(map(str, st.session_state.correct_b_factors))}")

        user_gcd = st.number_input(
            f"What is the GCD of **{a}** and **{b}**?",
            min_value=1, step=1, key="gcd_input"
        )

        if st.button("Submit GCD"):
            if user_gcd == st.session_state.correct_gcd:
                st.success(f"✅ Correct! The GCD of **{a}** and **{b}** is indeed {st.session_state.correct_gcd}.")
                st.session_state.score += 1
                st.session_state.index += 1
                st.session_state.factors_submitted = False
                st.session_state.correct_factors = False
                st.session_state.user_gcd = None
                st.session_state.correct_gcd = None
                st.session_state.correct_a_factors = []
                st.session_state.correct_b_factors = []
                st.session_state.gcd_input = 1
                st.rerun()
            else:
                st.error("❌ Incorrect GCD. Try again!")

else:
    st.success("🎉 You've completed all problems!")
    st.write(f"Your score: **{st.session_state.score} / {len(problems)}**")

    if st.button("🔁 Start Over"):
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.factors_submitted = False
        st.session_state.correct_factors = False
        st.session_state.user_gcd = None
        st.session_state.correct_gcd = None
        st.session_state.correct_a_factors = []
        st.session_state.correct_b_factors = []
        st.session_state.gcd_input = 1
        st.rerun()
