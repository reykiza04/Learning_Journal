import streamlit as st
import numpy as np
#yang di tampilin itu dalam fungction ya
def app():
    st.title('Data Visualization')
    st.markdown('Demo Page untuk data visualisasi')
###################### container with notation#########################################
    st.title ('container using notation')

    with st.container():
        st.write("this is inside container")

        st.bar_chart(np.random.randn(50,3))

        st.write('this is outer container')



st.write('ini di luat fungsi')