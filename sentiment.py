from transformers import (
    CamembertTokenizer,
    AutoModelForSequenceClassification,
    pipeline
)
from thai2transformers.preprocess import process_transformers

# Load pre-trained tokenizer
tokenizer = CamembertTokenizer.from_pretrained(
    'airesearch/wangchanberta-base-att-spm-uncased',
    revision='main')
tokenizer.additional_special_tokens = ['<s>NOTUSED', '</s>NOTUSED', '<_>']

# Load pre-trained model
model = AutoModelForSequenceClassification.from_pretrained(
    'airesearch/wangchanberta-base-att-spm-uncased',
    revision='finetuned@wisesight_sentiment')

classify_sequence = pipeline(task='sentiment-analysis',
                             tokenizer=tokenizer,
                             model=model)


# input_text = ["ของดีมากๆเลยอ่ะ","พังง่าน","ห้องน้ำสกปรก","นิสัยดีจัง"]

# processed_input_text = process_transformers(input_text)
# print(processed_input_text, '\n')
# print(classify_sequence(processed_input_text))


def get_sentiment(input_text):
    processed_input_text = process_transformers(input_text)
    sent = classify_sequence(processed_input_text)
    return sent[0]['label']