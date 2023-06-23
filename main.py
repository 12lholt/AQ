import streamlit as st
import boto3
import time
import requests

s3 = boto3.client('s3', region_name='us-east-2')
transcribe = boto3.client('transcribe', region_name='us-east-2')

def main():
    st.title('AWS Transcribe Audio Transcription')
    
    uploaded_file = st.file_uploader("Upload an audio file", type=['wav', 'mp3', 'mp4', 'm4a', 'flac'])

    if st.button('Send File to Amazon Transcribe'):
        if uploaded_file is not None:
            file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
            st.write(file_details)
            
            # Create unique name for transcription job
            transcribe_job_name = f"transcribeJob-{int(time.time() * 1000)}"
            
            # Upload file to S3
            s3_upload = s3.put_object(Bucket='aqbucket-test-200', Key=uploaded_file.name, Body=uploaded_file.getvalue())
            st.write('File Successfully Uploaded to S3')
            
            # Start transcription job
            transcribe.start_transcription_job(
                TranscriptionJobName=transcribe_job_name,
                Media={'MediaFileUri': f"s3://aqbucket-test-200/{uploaded_file.name}"},
                MediaFormat=uploaded_file.type.split('/')[-1],
                LanguageCode='en-US'
            )
            
            while True:
                status = transcribe.get_transcription_job(TranscriptionJobName=transcribe_job_name)
                if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                    break
                st.write("Not ready yet...")
                time.sleep(10)

            # Fetch the transcript
            if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
                transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
                transcript_json = requests.get(transcript_uri).json()
                transcript = " ".join([item['alternatives'][0]['content'] for item in transcript_json['results']['items']])
                st.write(transcript)
            else:
                st.write('Transcription job failed')
        else:
            st.write("Please upload a file")

if __name__ == "__main__":
    main()
