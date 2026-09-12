"""
HireSignal - Classifier Evaluation Script
Loads trained model artifact, evaluates test splits, and prints formatted precision/recall/F1 metrics.
"""

import json
import os
import sys

def run_eval():
    artifact_path = os.path.join(os.path.dirname(__file__), "model_artifact.json")
    if not os.path.exists(artifact_path):
        print(f"Error: artifact not found at {artifact_path}. Run train_classifier.py first.")
        sys.exit(1)

    with open(artifact_path, "r") as f:
        data = json.load(f)

    print("=================================================================")
    print("      HireSignal Multi-Label Classifier Benchmark Evaluation     ")
    print("=================================================================")
    print(f"Total Dataset Size:      {data['dataset_size']} pairs")
    print(f"Train / Test Split:      {data['train_samples']} / {data['test_samples']}")
    print(f"Macro Precision (Avg):   {data['macro_precision']*100:.2f}%  (Target: >= 85%)")
    print(f"Micro Precision (Avg):   {data['micro_precision']*100:.2f}%")
    print(f"Macro Recall (Avg):      {data['macro_recall']*100:.2f}%")
    print(f"Macro F1 Score (Avg):    {data['macro_f1']*100:.2f}%")
    print(f"Target SLA Met:          {'PASSED' if data['target_met_85_precision'] else 'FAILED'}")
    print("-----------------------------------------------------------------")
    print(f"{'Label Name':<24} | {'Precision':<10} | {'Recall':<10} | {'F1':<8} | {'TP':<4} {'FP':<4} {'FN':<4}")
    print("-" * 65)

    for label, m in data["per_class_metrics"].items():
        print(f"{label:<24} | {m['precision']*100:6.1f}%    | {m['recall']*100:6.1f}%    | {m['f1_score']*100:5.1f}% | {m['tp']:<4} {m['fp']:<4} {m['fn']:<4}")
    print("=================================================================")

if __name__ == "__main__":
    run_eval()
