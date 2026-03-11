import os
import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("SAP T-Code Assistant")

tcode = st.text_input("Enter SAP T-code")

if tcode:

    prompt = f"""
    Explain SAP transaction code {tcode} in maximum 2–3 lines.
    Mention:
    - What the transaction does
    - Which SAP module it belongs to
    Keep the answer short and simple.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content
    st.write(answer)

    # ----- Token Usage -----

    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens
    total_tokens = response.usage.total_tokens

    # ----- Cost Calculation (gpt-4o-mini pricing approx) -----

    INPUT_PRICE = 0.00000015
    OUTPUT_PRICE = 0.0000006

    input_cost = input_tokens * INPUT_PRICE
    output_cost = output_tokens * OUTPUT_PRICE

    total_cost = input_cost + output_cost

    # ----- Convert USD → INR -----

    USD_TO_INR = 83
    cost_in_inr = total_cost * USD_TO_INR

    st.subheader("API Usage")

    st.write(f"Input tokens: {input_tokens}")
    st.write(f"Output tokens: {output_tokens}")
    st.write(f"Total tokens: {total_tokens}")

    st.success(f"Estimated API cost: ${total_cost:.6f}")
    st.success(f"Estimated API cost in INR: ₹{cost_in_inr:.4f}")
