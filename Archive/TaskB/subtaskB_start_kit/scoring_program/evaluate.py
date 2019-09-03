#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: Shuailong
# @Email: liangshuailong@gmail.com
# @Date: 2019-08-14 15:26:03
# @Last Modified by: Shuailong
# @Last Modified time: 2019-08-14 15:26:48
# Modified from https://github.com/allenai/aristo-leaderboard/blob/master/openbookqa/evaluator/evaluator.py

import argparse
import csv
from typing import *
import logging
import sys
import json
import os


EXIT_STATUS_ANSWERS_MALFORMED = 1
EXIT_STATUS_PREDICTIONS_MALFORMED = 2
EXIT_STATUS_PREDICTIONS_EXTRA = 3
EXIT_STATUS_PREDICTION_MISSING = 4


def calculate_accuracy(gold_labels: Dict[str, str], predictions: Dict[str, List[str]]) -> float:
    score = 0.0

    for instance_id, answer in gold_labels.items():
        try:
            predictions_for_current = predictions[instance_id]
        except KeyError:
            logging.error("Missing prediction for question '%s'.", instance_id)
            sys.exit(EXIT_STATUS_PREDICTION_MISSING)

        if answer == predictions_for_current:
            score += 1.0 / len(predictions_for_current)

        del predictions[instance_id]

    if len(predictions) > 0:
        logging.error("Found %d extra predictions, for example: %s", len(
            predictions), ", ".join(list(predictions.keys())[:3]))
        sys.exit(EXIT_STATUS_PREDICTIONS_EXTRA)

    return score / len(gold_labels)


def read_gold(filename: str) -> Dict[str, str]:
    answers = {}

    with open(filename, "rt", encoding="UTF-8", errors="replace") as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                try:
                    instance_id = row[0]
                    answer = row[1]
                except IndexError as e:
                    logging.error(
                        "Error reading value from CSV file %s on line %d: %s", filename, reader.line_num, e)
                    sys.exit(EXIT_STATUS_ANSWERS_MALFORMED)

                if instance_id in answers:
                    logging.error("Key %s repeated in %s",
                                  instance_id, filename)
                    sys.exit(EXIT_STATUS_ANSWERS_MALFORMED)

                answers[instance_id] = answer

        except csv.Error as e:
            logging.error('file %s, line %d: %s', filename, reader.line_num, e)
            sys.exit(EXIT_STATUS_ANSWERS_MALFORMED)

    if len(answers) == 0:
        logging.error("No answers found in file %s", filename)
        sys.exit(EXIT_STATUS_ANSWERS_MALFORMED)

    return answers


def read_predictions(filename: str) -> Dict[str, List[str]]:
    predictions = {}

    with open(filename, "rt", encoding="UTF-8", errors="replace") as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                try:
                    instance_id = row[0]
                    prediction = row[1]
                except IndexError as e:
                    logging.error(
                        "Error reading value from CSV file %s on line %d: %s", filename, reader.line_num, e)
                    sys.exit(EXIT_STATUS_PREDICTIONS_MALFORMED)

                if instance_id in predictions:
                    logging.error("Key %s repeated in file %s on line %d",
                                  instance_id, filename, reader.line_num)
                    sys.exit(EXIT_STATUS_PREDICTIONS_MALFORMED)

                if instance_id == "":
                    logging.error(
                        "Key is empty in file %s on line %d", filename, reader.line_num)
                    sys.exit(EXIT_STATUS_PREDICTIONS_MALFORMED)

                # prediction labels cannot be empty strings
                if prediction == "":
                    logging.error("Key %s has empty labels for prediction in file %s on line %d",
                                  instance_id, filename, reader.line_num)
                    sys.exit(EXIT_STATUS_PREDICTIONS_MALFORMED)
                predictions[instance_id] = prediction

        except csv.Error as e:
            logging.error('file %s, line %d: %s', filename, reader.line_num, e)
            sys.exit(EXIT_STATUS_PREDICTIONS_MALFORMED)

    return predictions


def main():

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    submit_dir = os.path.join(input_dir, 'res')
    truth_dir = os.path.join(input_dir, 'ref')

    if not os.path.isdir(submit_dir):
        print(f"{submit_dir} doesn't exist")

    if os.path.isdir(submit_dir) and os.path.isdir(truth_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_filename = os.path.join(output_dir, 'scores.txt')
        output_file = open(output_filename, 'wb')

        gold_labels_file = os.path.join(truth_dir, "answers.csv")
        gold_labels = read_gold(gold_labels_file)

        submission_answer_file = os.path.join(submit_dir, "answers.csv")

        pred_labels = read_predictions(submission_answer_file)
        accuracy = calculate_accuracy(gold_labels, pred_labels)

        output_file.write(f'Accuracy: {accuracy*100:.4f}')
        output_file.close()


if __name__ == '__main__':
    main()
