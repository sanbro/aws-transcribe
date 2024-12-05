import json
import urllib.parse
import boto3
import time
import os

print("Loading function")

s3 = boto3.client("s3")
transcribe = boto3.client("transcribe", "us-east-1")
input_bucket = "transcrive-input-source"
output_bucket = "transcibe-output-source"


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    file_key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )
    try:

        print(f"File uploaded: {file_key} in bucket {bucket}")

        # Check if the file is a valid video type
        if not file_key.lower().endswith((".mp4", ".mov", ".avi")):
            print(f"Invalid file type for transcription: {file_key}")
            return
        job_name = f"transcribe-job-{int(time.time())}"

        # Create the transcription job
        transcribe_job_uri = f"s3://{bucket}/{file_key}"
        response = transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={"MediaFileUri": transcribe_job_uri},
            OutputBucketName=output_bucket,
            OutputKey="my-output-files/{file_key}/",
            LanguageCode="en-US",
            Subtitles={"Formats": ["vtt", "srt"], "OutputStartIndex": 1},
        )
        print(f"Transcription job started: {response}")
        # while True:
        #     status = transcribe.get_transcription_job(TranscriptionJobName = job_name)
        #     if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        #         break
        #     print("Not ready yet...")
        #     time.sleep(5)
        # print(status)
        return {
            "statusCode": 200,
            "body": f"Transcription job started for file: {file_key} and status : {status}",
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"statusCode": 500, "body": f"Error occurred: {str(e)}"}
