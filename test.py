from transformers import pipeline

model = pipeline("sentiment-analysis", model="distilbert-base-multilingual-cased")

print(model("Hôm nay tôi rất vui"))


