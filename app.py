import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("📚 PDF AI Search")

# ---------------------------
# SESSION START
# ---------------------------

if "session_started" not in st.session_state:
    st.session_state.session_started = False

username = st.text_input("Enter Username")

if st.button("Start Session"):

    res = requests.post(
        f"{API_URL}/start-session/",
        json={"username": username}
    )

    if res.status_code == 200:
        st.session_state.session_started = True
        st.success("Session Started")

    else:
        st.error(res.text)

# ---------------------------
# MAIN APP
# ---------------------------

if st.session_state.session_started:

    st.divider()

    # ---------------------------
    # Upload PDF
    # ---------------------------

    st.subheader("Upload PDF")

    uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])

    if st.button("Upload PDF") and uploaded_file is not None:

        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}

        res = requests.post(
            f"{API_URL}/upload-pdf/",
            files=files
        )

        if res.status_code == 200:
            st.success("PDF uploaded")

        else:
            st.error(res.text)

    st.divider()

    # ---------------------------
    # LIST PDFs
    # ---------------------------

    res = requests.get(f"{API_URL}/list-of-pdfs/")

    pdf_list = []

    if res.status_code == 200:
        pdf_list = res.json()["pdfs"]

    if len(pdf_list) == 0:
        st.warning("No PDFs uploaded")

    else:

        selected_pdf = st.selectbox(
            "Select PDF",
            pdf_list
        )

        st.divider()

        # ---------------------------
        # QUERY
        # ---------------------------

        st.subheader("Ask Question")

        query = st.text_input("Enter question")

        if st.button("Ask"):

            params = {
                "query": query,
                "collection": selected_pdf
            }

            res = requests.get(
                f"{API_URL}/query/",
                params=params
            )

            if res.status_code == 200:
                answer = res.json()["AiReply"]

                st.subheader("AI Answer")
                st.write(answer)

            else:
                st.error(res.text)

        st.divider()

        # ---------------------------
        # DELETE PDF
        # ---------------------------

        if st.button("Delete Selected PDF"):

            res = requests.delete(
                f"{API_URL}/delete-pdf/{selected_pdf}"
            )

            if res.status_code == 200:
                st.success("PDF Deleted")
                st.rerun()

            else:
                st.error(res.text)

    st.divider()

    # ---------------------------
    # END SESSION
    # ---------------------------

    if st.button("End Session"):

        res = requests.post(f"{API_URL}/end-session/")

        if res.status_code == 200:
            st.session_state.session_started = False
            st.success("Session Ended")
            st.rerun()

        else:
            st.error(res.text)