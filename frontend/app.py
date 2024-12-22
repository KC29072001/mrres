import streamlit as st
import requests
import pandas as pd

def main():
    st.title("AI Use Case Generator")
    st.write("Generate AI/ML use cases for your company or industry")

    # Input form
    with st.form("research_form"):
        company_name = st.text_input("Company Name")
        industry = st.text_input("Industry")
        submitted = st.form_submit_button("Generate Use Cases")

    if submitted:
        try:
            # Call backend API
            response = requests.post(
                "http://localhost:8000/analyze",
                json={"company_name": company_name, "industry": industry}
            )

            if response.status_code == 200:
                data = response.json()

                # Display company and industry information
                st.header("Company Profile")
                st.write(f"**Name:** {data['company_profile']['name']}")
                st.write(f"**Description:** {data['company_profile']['description']}")
                st.write("**Focus Areas:**")
                for area in data['company_profile']['focus_areas']:
                    st.write(f"- {area}")
                st.write("**Technologies:**")
                for tech in data['company_profile']['technologies']:
                    st.write(f"- {tech}")

                st.header("Industry Analysis")
                st.write(f"**Industry:** {data['industry_analysis']['industry_type']}")
                st.write(f"**Market Position:** {data['industry_analysis']['market_position']}")
                st.write("**Key Trends:**")
                for trend in data['industry_analysis']['key_trends']:
                    st.write(f"- {trend}")
                st.write("**Competitors:**")
                for competitor in data['industry_analysis']['competitors']:
                    st.write(f"- {competitor}")

                # Display use cases
                st.header("Recommended Use Cases")
                for use_case in data['use_cases']:
                    with st.expander(use_case['title']):
                        st.write(f"**Description:** {use_case['description']}")
                        st.write("**Benefits:**")
                        for benefit in use_case['benefits']:
                            st.write(f"- {benefit}")
                        st.write(f"**Implementation Complexity:** {use_case['implementation_complexity']}")

                # Display resources
                st.header("Resources")
                
                # Handle datasets
                st.subheader("Datasets")
                if data['resources']['datasets']:
                    for dataset in data['resources']['datasets']:
                        st.markdown(f"- [{dataset['name']}]({dataset['url']})")
                else:
                    st.write("No datasets available")

                # Handle code repositories
                st.subheader("GitHub Repositories")
                if data['resources']['code_repositories']:
                    for repo in data['resources']['code_repositories']:
                        st.markdown(f"- [{repo['name']}]({repo['url']})")
                else:
                    st.write("No repositories available")

        except Exception as e:
            st.error(f"Error occurred: {str(e)}")
            st.write("Please try again or contact support if the issue persists.")

if __name__ == "__main__":
    main()