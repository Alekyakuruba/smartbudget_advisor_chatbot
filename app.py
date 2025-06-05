import os
import streamlit as st
import openai

# Load API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("OpenAI API key not found! Please set OPENAI_API_KEY as a secret on Streamlit Cloud.")
    st.stop()

openai.api_key = OPENAI_API_KEY

def get_advice(prompt: str) -> str:
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {e}"

def main():
    st.title("💡 Smart Budget Advisor Chatbot")

    income = st.number_input("Monthly Income (after tax)", min_value=0.0, format="%.2f")

    st.subheader("Monthly Expenses")
    if "expenses" not in st.session_state:
        st.session_state.expenses = {}

    with st.form("add_expense", clear_on_submit=True):
        category = st.text_input("Expense category")
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        submitted = st.form_submit_button("Add Expense")
        if submitted:
            if category.strip() != "":
                st.session_state.expenses[category] = amount
                st.success(f"Added {category}: ${amount:.2f}")

    if st.session_state.expenses:
        st.write("### Current Expenses")
        for cat, amt in st.session_state.expenses.items():
            st.write(f"- {cat}: ${amt:.2f}")

    if st.button("Clear Expenses"):
        st.session_state.expenses = {}

    if st.button("Get Budget Advice"):
        if income == 0:
            st.warning("Please enter your monthly income.")
            return
        if not st.session_state.expenses:
            st.warning("Please add at least one expense.")
            return

        total_expenses = sum(st.session_state.expenses.values())
        remaining = income - total_expenses

        st.write("---")
        st.write(f"**Monthly Income:** ${income:.2f}")
        st.write(f"**Total Expenses:** ${total_expenses:.2f}")
        st.write(f"**Remaining Balance:** ${remaining:.2f}")
        st.write("---")

        prompt = f"""
You are a helpful financial advisor. Based on the user's financial data, provide personalized budget advice.

Monthly income: ${income:.2f}
Monthly expenses:
"""
        for cat, amt in st.session_state.expenses.items():
            prompt += f"- {cat}: ${amt:.2f}\n"
        prompt += f"Total expenses: ${total_expenses:.2f}\n"
        prompt += f"Remaining balance: ${remaining:.2f}\n\n"
        prompt += "Provide practical advice for saving money and improving financial health."

        advice = get_advice(prompt)
        st.markdown("### 💡 Budget Advice")
        st.write(advice)

if __name__ == "__main__":
    main()
