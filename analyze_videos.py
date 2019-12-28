import os
import csv
import json

from google.cloud import videointelligence
from google.protobuf.json_format import MessageToJson

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client_secrets.json"

def export_to_json(result):
    json_results = MessageToJson(result, preserving_proto_field_name=True)

    with open("./database/output.json", "w") as json_output:
        json.dump(json_results, json_output)

# Prcoess segment level label annotations
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
def analyze_shots(result):
    shot_labels = result.annotation_results[0].shot_label_annotations
    responses = []
    for i, shot_label in enumerate(shot_labels):
        responses.append(shot_label.entity.description)

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
    export_to_json(result)
    with open("./database/output.csv", "a") as csv_output:
        writer = csv.writer(csv_output)
        writer.writerow(responses)


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

def analyze_labels(path):
    # Detects labels given a GCS path
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.LABEL_DETECTION]
    operation = video_client.annotate_video(path, features=features)
    print("\nProcessing video for label annotations:")

    result = operation.result(timeout=90)
    print("\nFinished processing.")

    # analyze_segments(result)
    analyze_shots(result)
    # analyze_frames(result)


path = "gs://video-api-bucket/trailer.mp4"

analyze_labels(path)
