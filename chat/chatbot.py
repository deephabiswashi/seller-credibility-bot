import streamlit as st
from utils.fetch_data import fetch_data
from utils.analyze import combined_analysis

def main():
    st.title("Seller Credibility Bot")
    st.write("Paste the link to a seller's page (e.g., Facebook or Instagram) to check credibility.")

    url = st.text_input("Enter URL:")
    
    if st.button("Analyze"):
        if url:
            st.write("Fetching data...")
            data = fetch_data(url)
            st.write("Analyzing data...")
            analysis = combined_analysis(data)
            st.subheader("Analysis Result:")
            st.write(analysis)
        else:
            st.write("Please enter a valid URL.")

if __name__ == "__main__":
    main()
