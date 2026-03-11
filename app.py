import os
import streamlit as st
from openai import OpenAI

# Page configuration
st.set_page_config(
    page_title="SAP T-Code Assistant",
    page_icon="💡",
    layout="wide"
)

# Gradient background + UI styling
st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
background: linear-gradient(135deg,#dfe9f3,#ffffff,#e2f0cb);
}

.main-title{
font-size:40px;
font-weight:700;
}

.card{
background:white;
padding:20px;
border-radius:12px;
box-shadow:0px 6px 15px rgba(0,0,0,0.1);
}

.result-box{
background:#f9fafc;
padding:18px;
border-radius:10px;
border-left:5px solid #4CAF50;
font-size:17px;
}

</style>
""", unsafe_allow_html=True)

# Initialize OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Title
st.markdown("<p class='main-title'>💡 SAP T-Code Assistant</p>", unsafe_allow_html=True)

# Layout columns
left_col, right_col = st.columns([2,1])

# ---- LEFT SIDE : INPUT + RESPONSE ----
with left_col:

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    tcode = st.text_input("Enter SAP T-Code").upper()

    if tcode:

        with st.spinner("Analyzing T-Code..."):

            prompt = f"Explain SAP transaction code {tcode} in 2 short lines. Mention purpose and SAP module."

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            answer = response.choices[0].message.content

        st.subheader("Explanation")

        st.markdown(f"<div class='result-box'>{answer}</div>", unsafe_allow_html=True)

        # Token usage
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens

        # Cost calculation
        INPUT_PRICE = 0.00000015
        OUTPUT_PRICE = 0.0000006

        input_cost = input_tokens * INPUT_PRICE
        output_cost = output_tokens * OUTPUT_PRICE
        total_cost = input_cost + output_cost

        USD_TO_INR = 83
        cost_in_inr = total_cost * USD_TO_INR

    st.markdown("</div>", unsafe_allow_html=True)


# ---- RIGHT SIDE : COST DASHBOARD ----
with right_col:

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("📊 Cost Dashboard")

    if tcode:

        col1,col2,col3 = st.columns(3)

        col1.metric("Input Tokens", input_tokens)
        col2.metric("Output Tokens", output_tokens)
        col3.metric("Total Tokens", total_tokens)

        st.divider()

        st.metric("Cost (USD)", f"${total_cost:.6f}")
        st.metric("Cost (INR)", f"₹{cost_in_inr:.4f}")

    else:

        st.info("Enter a T-Code to see usage statistics")

    st.markdown("</div>", unsafe_allow_html=True)
