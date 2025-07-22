import streamlit as st
import random

st.set_page_config(page_title="GCD Lab", page_icon="💡")

# --- INITIAL SETUP ---
if "problem_index" not in st.session_state:
    st.session_state.problem_index = 0
if "factors_submitted" not in st.session_state:
    st.session_state.factors_submitted = False
if "gcd_submitted" not in st.session_state:
    st.session_state.gcd_submitted = False
if "correct_gcd" not in st.session_state:
    st.session_state.correct_gcd = None
if "correct_factors" not in st.session_state:
    st.session_state.correct_factors = False
if "correct_a_factors" not in st.session_state:
    st.session_state.correct_a_factors = []
if "correct_b_factors" not in st.session_state:
    st.session_state.correct_b_factors = []

# Problems (list of tuples)
problems = [(12, 18), (24, 36), (20, 30), (14, 35), (16, 40)]
a, b = problems[st.session_state.problem_index]

# --- UI HEADER ---
st.title("💡 GCD Lab")
st.markdown("Type the factors of the two numbers below, then calculate the GCD based on the common factors.")
st.markdown(f"### 🔢 Problem {st.session_state.problem_index + 1} of {len(problems)}")
st.markdown(f"**What are the factors of {a} and {b}?**")

# --- FACTOR ENTRY (only if not submitted) ---
if not st.session_state.factors_submitted:
    with st.form("factor_form", clear_on_submit=False):
        a_input = st.text_area(f"List the factors of **{a}** (separate by commas):", key="a_input")
        b_input = st.text_area(f"List the factors of **{b}** (separate by commas):", key="b_input")
        submit_factors = st.form_submit_button("✅ Submit Factors")

        if submit_factors:
            try:
                a_factors = set(map(int, a_input.replace(" ", "").split(",")))
                b_factors = set(map(int, b_input.replace(" ", "").split(",")))
                correct_a = set(i for i in range(1, a + 1) if a % i == 0)
                correct_b = set(i for i in range(1, b + 1) if b % i == 0)

                if a_factors != correct_a:
                    st.error("❌ Incorrect factors for A. Please check your list.")
                elif b_factors != correct_b:
                    st.error("❌ Incorrect factors for B. Please check your list.")
                else:
                    st.success("✅ Factors are correct! Now, enter the GCD of the two numbers.")
                    st.session_state.factors_submitted = True
                    st.session_state.correct_a_factors = sorted(correct_a)
                    st.session_state.correct_b_factors = sorted(correct_b)
                    st.session_state.correct_gcd = max(correct_a & correct_b)
            except ValueError:
                st.error("❌ Invalid input. Use commas and numbers only.")

# --- SHOW CORRECT FACTORS IF SUBMITTED ---
if st.session_state.factors_submitted:
    st.markdown(f"✔️ **Factors of {a}:** {', '.join(map(str, st.session_state.correct_a_factors))}")
    st.markdown(f"✔️ **Factors of {b}:** {', '.join(map(str, st.session_state.correct_b_factors))}")

# --- GCD INPUT ---
if st.session_state.factors_submitted and not st.session_state.gcd_submitted:
    gcd_input = st.number_input(f"What is the GCD of {a} and {b}?", min_value=1, step=1, key="gcd_input")
    if st.button("Submit GCD"):
        if gcd_input == st.session_state.correct_gcd:
            st.success(f"✅ Correct! The GCD of {a} and {b} is indeed {gcd_input}.")
            st.session_state.gcd_submitted = True
        else:
            st.error("❌ That's not correct. Please try again.")

# --- NEXT PROBLEM ---
if st.session_state.gcd_submitted:
    if st.session_state.problem_index < len(problems) - 1:
        if st.button("➡️ Next Problem"):
            st.session_state.problem_index += 1
            st.session_state.factors_submitted = False
            st.session_state.gcd_submitted = False
            st.session_state.correct_a_factors = []
            st.session_state.correct_b_factors = []
            st.session_state.correct_gcd = None
            st.session_state.a_input = ""
            st.session_state.b_input = ""
    else:
        st.success("🎉 You've completed all the problems!")
