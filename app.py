import streamlit as st 

with open('style.css')as f:
 st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

col1, col2, col3 = st.columns(3)

with col2:
   st.write("This is a container")
   st.button("Push me!")


st.write("This is outside the container")
