import streamlit as st
from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

st.title("SAP T-Code Assistant")

tcode = st.text_input("Enter SAP T-code")

if tcode:

    prompt = f"Explain the SAP transaction code {tcode}. Include its purpose and module."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content

    st.write(answer)
