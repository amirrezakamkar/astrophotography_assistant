import streamlit as st

def main():
    # Streamlit app title
    st.title("Celestial Events Viewer")

    # Embed the Light Pollution Map website using HTML iframe
    iframe_code = '''
    <iframe src="https://www.lightpollutionmap.info/#zoom=3.62&lat=47.2401&lon=12.7945&state=eyJiYXNlbWFwIjoiTGF5ZXJCaW5nUm9hZCIsIm92ZXJsYXkiOiJ3YV8yMDE1Iiwib3ZlcmxheWNvbG9yIjpmYWxzZSwib3ZlcmxheW9wYWNpdHkiOjYwLCJmZWF0dXJlc29wYWNpdHkiOjg1fQ==" width="800" height="600" frameborder="0"></iframe>
    '''
    st.markdown(iframe_code, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
