import streamlit as st
import pandas as pd
import os
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
background-color: #4158D0;
background-image: linear-gradient(315deg, #4F2991 3%, #7DC4FF 38%, #36CFCC 68%, #A92ED3 98%);
}
[data-testid="stHeader"] {
background: rgba(0,0,0,0);
}
[data-testid="stToolbar"] {
right: 2rem;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
import streamlit as st
import pandas as pd
def load_data(file):
    return pd.read_csv(file)
def consolidate_forms(files):
    dfs = []
    for file in files:
        df = load_data(file)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)
def main():
    st.title("*Google Forms Consolidator*")
    st.header(":gray[Future Improvements]:sparkles::")
    st.subheader("Connect to snowflake flood data or get access to available APIs that would provide more information than the free subscriptions.")
    st.sidebar.title("Upload Google Forms CSV Files")
    uploaded_files = st.sidebar.file_uploader("Upload CSV files", accept_multiple_files=True, type='csv')
    if uploaded_files:
        st.header("Consolidated Responses")
        consolidated_df = consolidate_forms(uploaded_files)
        st.write(consolidated_df)
if __name__ == "__main__":
    main()