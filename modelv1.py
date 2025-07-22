import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

pd.set_option('display.max_columns', None)


df = pd.read_csv("df_bp1.csv")


features = ["OBP_162_h", "OBP_162_v", "SLG_162_h", "SLG_162_v",
            "OBP_30_h", "OBP_30_v", "SLG_30_h", "SLG_30_v",]

target = "home_victory"

X = df.loc[:,features]
y = df[target]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))