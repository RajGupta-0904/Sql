import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize GenerativeModel
model = genai.GenerativeModel('gemini-pro')

def main():
    # Set page configuration
    st.set_page_config(page_title="SQL Query Generator", page_icon=":robot")
    
    # Render HTML content
    st.markdown(
        """
            <div style="text-align:center;">
                <h1>SQL Query Generator</h1>
            </div>
        """,
        unsafe_allow_html=True
    )
    
    text_input = st.text_area("Enter your Query here in plain text:")
    submit = st.button("Generate SQL Query")

    if submit:
        with st.spinner("Generating SQL Query..."):
            template = """
                Create a SQL query snippet using the below text:
                ```
                    {text_input}
                ```
                I just want a SQL query.
            """
            formatted_template = template.format(text_input=text_input)
            st.write(formatted_template)
            
            response = model.generate_content(formatted_template)
            sql_query = response.text.strip().lstrip("```sql").rstrip("```")
            
            expected_output = """
                What would be the expected response of this SQL query snippet:
                ```
                    {sql_query}
                ```
                Provide sample tabular response with no explanation.
            """
            expected_output_formatted = expected_output.format(sql_query=sql_query)
            eoutput = model.generate_content(expected_output_formatted)
            eoutput = eoutput.text.strip()
            
            # Ensure the output is a valid Markdown table format
            if not eoutput.startswith("|"):
                eoutput = f"```\n{eoutput}\n```"
            
            explanation = """
                Explain this SQL query and Explain the sql command with short example:
                ```
                    {sql_query}
                ```
                Please provide a simple and brief explanation.
            """
            explanation_formatted = explanation.format(sql_query=sql_query)
            explanations = model.generate_content(explanation_formatted)
            explanations = explanations.text.strip()
            
            with st.container():
                st.success("SQL Query Generated Successfully!")
                st.code(sql_query, language="sql")

                st.success("Expected Output of this SQL query will be:")
                st.markdown(eoutput, unsafe_allow_html=True)
                
                st.success("Explanation of this SQL query will be:")
                st.markdown(explanations, unsafe_allow_html=True)

# Call the main function
main()
