import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Load the dataset
data = pd.read_csv('tracker/dataset/daily_transactions.csv')

# Prepare the data
data = data[data["Income/Expense"] == "Expense"]

# select columns
data = data[["Note","Category"]]

#rename columns
data.columns = ["description","category"]

#remove empty rows
data = data.dropna()

x = data["description"]
y = data["category"]

# ML pipeline
model = Pipeline([
    ("vectorizer", TfidfVectorizer()),
    ("classifier", MultinomialNB())
])

# train model

model.fit(x,y)

# save model
pickle.dump(model,open("tracker/expense_model.pkl","wb"))

print("Model trained and saved successfully!")

