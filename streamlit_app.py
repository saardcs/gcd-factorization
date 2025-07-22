import streamlit as st

# -----------------------
# Problems list
problems = [(12, 18), (24, 30), (15, 20), (28, 35), (50, 75)]

# -----------------------
# Initialize session state variables if missing
if "index" not in st.session_state:
    st.session_state.index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "factors_submitted" not in st.session_state:
    st.session_state.factors_submitted = False
if "gcd_correct" not in st.session_state:
    st.session_state.gcd_correct = False
if "correct_a_factors" not in st.session_state:
    st.session_state.correct_a_factors = []
if "correct_b_factors" not in st.session_state:
    st.session_state.correct_b_factors = []
if "correct_gcd" not in st.session_state:
    st.session_state.correct_gcd = None

# -----------------------
a, b = problems[st.session_state.index]

st.title("💡 GCD Lab")
st.markdown(f"### Problem {st.session_state.index + 1} of {len(problems)}")
st.markdown(f"**What are the factors of {a} and {b}?**")

# -----------------------
# Show factor input only if not submitted yet
if not st.session_state.factors_submitted:
    a_factors_input = st.text_area(f"Factors of {a} (comma separated):", key="a_factors_input")
    b_factors_input = st.text_area(f"Factors of {b} (comma separated):", key="b_factors_input")

    if st.button("Submit Factors"):
        try:
            user_a_factors = set(map(int, a_factors_input.replace(" ", "").split(",")))
            user_b_factors = set(map(int, b_factors_input.replace(" ", "").split(",")))

            correct_a_factors = set(i for i in range(1, a + 1) if a % i == 0)
            correct_b_factors = set(i for i in range(1, b + 1) if b % i == 0)

            if user_a_factors != correct_a_factors:
                st.error("❌ Incorrect factors for A.")
            elif user_b_factors != correct_b_factors:
                st.error("❌ Incorrect factors for B.")
            else:
                st.session_state.factors_submitted = True
                st.session_state.correct_a_factors = sorted(correct_a_factors)
                st.session_state.correct_b_factors = sorted(correct_b_factors)
                st.session_state.correct_gcd = max(correct_a_factors & correct_b_factors)
                st.experimental_rerun()
        except Exception:
            st.error("❌ Invalid input. Please enter comma-separated numbers.")

# -----------------------
# If factors submitted, show confirmed factors
if st.session_state.factors_submitted:
    st.markdown(f"✔️ Factors of {a}: {', '.join(map(str, st.session_state.correct_a_factors))}")
    st.markdown(f"✔️ Factors of {b}: {', '.join(map(str, st.session_state.correct_b_factors))}")

# -----------------------
# Show GCD input if factors submitted and GCD not yet correct
if st.session_state.factors_submitted and not st.session_state.gcd_correct:
    gcd_input = st.number_input(f"What is the GCD of {a} and {b}?", min_value=1, step=1, key="gcd_input")
    if st.button("Submit GCD"):
        if gcd_input == st.session_state.correct_gcd:
            st.success(f"✅ Correct! The GCD of {a} and {b} is {gcd_input}.")
            st.session_state.gcd_correct = True
            st.session_state.score += 1
            st.experimental_rerun()
        else:
            st.error("❌ Incorrect GCD. Try again.")

# -----------------------
# After correct GCD, show Next Problem button or completion message
if st.session_state.gcd_correct:
    if st.session_state.index < len(problems) - 1:
        if st.button("➡️ Next Problem"):
            # Reset for next problem
            st.session_state.index += 1
            st.session_state.factors_submitted = False
            st.session_state.gcd_correct = False
            st.session_state.correct_a_factors = []
            st.session_state.correct_b_factors = []
            st.session_state.correct_gcd = None
            # Clear input widgets
            for key in ["a_factors_input", "b_factors_input", "gcd_input"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.experimental_rerun()
    else:
        st.success(f"🎉 You completed all {len(problems)} problems!")
        st.write(f"Final Score: {st.session_state.score} / {len(problems)}")
        if st.button("🔄 Restart"):
            st.session_state.index = 0
            st.session_state.score = 0
            st.session_state.factors_submitted = False
            st.session_state.gcd_correct = False
            st.session_state.correct_a_factors = []
            st.session_state.correct_b_factors = []
            st.session_state.correct_gcd = None
            for key in ["a_factors_input", "b_factors_input", "gcd_input"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.experimental_rerun()
