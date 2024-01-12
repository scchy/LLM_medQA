# python3
# Create Date: 2024-01-12
# Author: Scc_hy
# Func: data prepare
# =======================================================================
import pandas as pd 
from tqdm.auto import tqdm
import json 
import random


def xlsx2json(file, output_file):
    df = pd.read_excel(file)
    # Answer数据中存在NA
    df = df[~df.Answer.isna()].reset_index(drop=True)
    need_cols = ['system', 'Question', 'Answer']
    df['system'] = "You are a professional, highly experienced doctor professor. You always provide accurate, comprehensive, and detailed answers based on the patients' questions."
    final_res = []
    for idx, row in tqdm(df[need_cols].rename(
            columns=dict(zip(need_cols[1:], ['input', 'output']))
        ).iterrows(), total=df.shape[0]):
        final_res.append({"conversation":[row.T.to_dict()]})
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_res, f, indent=4)
    print(f"Conversion complete. Output written to {output_file}")
    print(final_res[0])


def split_train_test(file, out_train_file, out_test_file):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data_len = len(data)    
    random.shuffle(data)
    split_point = int(data_len * 0.7)
    # Split the data into train and test
    train_data = data[:split_point]
    test_data = data[split_point:]
    with open(out_train_file, 'w', encoding='utf-8') as f:
        json.dump(train_data, f, indent=4)
    with open(out_test_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=4)
    print(f"Split complete. Train data written to {out_train_file}, Test data written to {out_test_file}")


if __name__ == '__main__':
    file = 'MedInfo2019-QA-Medications.xlsx'
    xlsx2json(file, 'output.jsonl')
    split_train_test('output.jsonl', 'MedQA2019-structured-train.jsonl', 'MedQA2019-structured-test.jsonl')

