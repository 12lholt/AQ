import streamlit as st
import boto3

def main():
    st.title('AWS Transcribe Live Transcription')
    # TODO: Initialize AWS Transcribe client here

    if st.button('Start Recording'):
        # TODO: Start AWS Transcribe live transcription here
        st.write('Recording started...')

    if st.button('Stop Recording'):
        # TODO: Stop AWS Transcribe live transcription here
        transcript = "TODO: Fetch the transcript"
        st.write(transcript)

if __name__ == "__main__":
    main()
