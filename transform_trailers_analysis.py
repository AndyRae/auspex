import os
import csv
import json
import argparse
from local_settings import cloud_bucket

from google.cloud import videointelligence
from google.cloud import storage
from google.protobuf.json_format import MessageToJson

# Uses Google video API to extract video annotations

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client_secrets.json"


def export_to_json(result):
    json_results = MessageToJson(result, preserving_proto_field_name=True)

    with open("./database/output.json", "w") as json_output:
        json.dump(json_results, json_output)


def export_to_csv(shot_labels, title):
    responses = []
    for shot_label in shot_labels:
        shots = []
        count = 0
        for segments in shot_label.segments:
            count += 1
        shots.append(title)
        shots.append(shot_label.entity.description)
        shots.append(count)
        responses.append(shots)

    with open("./database/annotations/" + title + "output.csv", "a") as csv_output:
        writer = csv.writer(csv_output)
        writer.writerows(responses)


# Process segment level label annotations
def analyze_segments(result):
    segment_labels = result.annotation_results[0].segment_label_annotations
    for i, segment_label in enumerate(segment_labels):
        print("Video label description: {}".format(segment_label.entity.description))
        for category_entity in segment_label.category_entities:
            print(
                "\tLabel category description: {}".format(category_entity.description)
            )

        for i, segment in enumerate(segment_label.segments):
            start_time = (
                segment.segment.start_time_offset.seconds
                + segment.segment.start_time_offset.nanos / 1e9
            )
            end_time = (
                segment.segment.end_time_offset.seconds
                + segment.segment.end_time_offset.nanos / 1e9
            )
            positions = "{}s to {}s".format(start_time, end_time)
            confidence = segment.confidence
            print("\tSegment {}: {}".format(i, positions))
            print("\tConfidence: {}".format(confidence))
        print("\n")


# Process shot level label annotations
def analyze_shots(result, title):
    shot_labels = result.annotation_results[0].shot_label_annotations
    for i, shot_label in enumerate(shot_labels):

        print("Shot label description: {}".format(shot_label.entity.description))
        for category_entity in shot_label.category_entities:
            print(
                "\tLabel category description: {}".format(category_entity.description)
            )

        for i, shot in enumerate(shot_label.segments):
            start_time = (
                shot.segment.start_time_offset.seconds
                + shot.segment.start_time_offset.nanos / 1e9
            )
            end_time = (
                shot.segment.end_time_offset.seconds
                + shot.segment.end_time_offset.nanos / 1e9
            )
            positions = "{}s to {}s".format(start_time, end_time)
            confidence = shot.confidence
            print("\tSegment {}: {}".format(i, positions))
            print("\tConfidence: {}".format(confidence))
        print("\n")
    # export_to_json(result)
    export_to_csv(shot_labels, title)


def analyze_frames(result):
    frame_labels = result.annotation_results[0].frame_label_annotations
    responses = []
    for i, frame_label in enumerate(frame_labels):
        print("Frame label description: {}".format(frame_label.entity.description))
        for category_entity in frame_label.category_entities:
            print(
                "\tLabel category description: {}".format(category_entity.description)
            )

        # Each frame_label_annotation has many frames,
        # here we print information only about the first frame.
        frame = frame_label.frames[0]
        time_offset = frame.time_offset.seconds + frame.time_offset.nanos / 1e9
        print("\tFirst frame time offset: {}s".format(time_offset))
        print("\tFirst frame confidence: {}".format(frame.confidence))
        print("\n")
        responses.append(frame_label.entity.description)
    print(responses)


def analyze_labels(path, title):
    # Detects labels given a GCS path
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.LABEL_DETECTION]
    operation = video_client.annotate_video(path, features=features)
    print("\nProcessing video for label annotations:" + title)

    result = operation.result(timeout=90)
    print("\nFinished processing.")

    # analyze_segments(result)
    analyze_shots(result, title)
    # analyze_frames(result)


def analyze_input():
    bucket = cloud_bucket
    bucket_path = "gs://" + bucket + "/"
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket)
    for file in blobs:
        analyze_labels(bucket_path + file.name, file.name)


def main(file):
    bucket = cloud_bucket
    bucket_path = "gs://" + bucket + "/"
    storage_client = storage.Client()   
    with open("./database/" + file, "r") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            analyze_labels(row[30], row[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze videos using the Google Video AI")
    parser.add_argument("file", type=str, help="CSV file in /database/ to use.")
    args = parser.parse_args()
    main(args.file)