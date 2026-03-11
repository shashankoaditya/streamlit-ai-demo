import os
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("SAP T-Code Assistant")

tcode = st.text_input("Enter SAP T-code")

if tcode:

    prompt = f"""
    Explain SAP transaction code {tcode}.
    Include:
    1. Purpose
    2. SAP Module
    3. Typical Business Use
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content
    st.write(answer)

    # ---- NEW PART (Token Usage) ----

    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens
    total_tokens = response.usage.total_tokens

    # Approx cost for GPT-4o-mini
    input_cost = input_tokens * 0.00000015
    output_cost = output_tokens * 0.0000006
    total_cost = input_cost + output_cost

    st.subheader("API Usage")

    st.write(f"Input tokens: {input_tokens}")
    st.write(f"Output tokens: {output_tokens}")
    st.write(f"Total tokens: {total_tokens}")

    st.success(f"Estimated API cost: ${total_cost:.6f}")
