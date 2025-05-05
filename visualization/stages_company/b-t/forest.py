import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

# Load the data
df = pd.read_excel('/Users/asa/PycharmProjects/stages_company/b-t/chi.xlsx')

# Drop rows with NaNs
df.dropna(inplace=True)

# Create features and target variable
X = df[['whether_fund', 'Stage Number', 'cluster']]
y = df['whether_have_patent']


# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the random forest classifier
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

# Predictions on the testing set
y_pred = clf.predict(X_test)

# Print classification report
print(classification_report(y_test, y_pred))

# Feature importances
feature_importances = pd.DataFrame({'Feature': X.columns, 'Importance': clf.feature_importances_})
print(feature_importances)
