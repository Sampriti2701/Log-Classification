import os
import pandas as pd
from processor_regex import classify_with_regex
from processor_bert import classify_with_bert
from processor_llm import classify_with_llm


def classify(logs):
    labels = []
    for source, log_msg in logs:
        label = classify_log(source, log_msg)
        labels.append(label)
    return labels


def classify_log(source, log_msg):
    if source == "LegacyCRM":
        label = classify_with_llm(log_msg)
    else:
        label = classify_with_regex(log_msg)
        if not label:
            label = classify_with_bert(log_msg)
    return label


def classify_csv(input_file):
    file_path = r"E:\\code\\classification-logs\\resources\\" + input_file  # Ensure correct path

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return None

    df = pd.read_csv(file_path)
    df["target_label"] = classify(list(zip(df["source"], df["log_message"])))

    output_file = r"E:\\code\\classification-logs\\resources\\output.csv"
    df.to_csv(output_file, index=False)

    print(f"Classification completed. Output saved to {output_file}")
    return output_file


if __name__ == '__main__':
    classify_csv("test.csv")
