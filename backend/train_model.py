# train_model.py
# This file trains the AI model

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle
import os

print("=" * 50)
print("TRAINING HOUSE PRICE PREDICTOR MODEL")
print("=" * 50)

# Step 1: Create sample data
print("\n📊 Creating training data...")
data = {
    'square_feet': [800, 1000, 1200, 1400, 1500, 1600, 1800, 2000, 2200, 2500, 2800, 3000, 3500, 4000, 4500, 5000],
    'bedrooms': [1, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5],
    'bathrooms': [1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4],
    'price': [2200000, 2800000, 3400000, 3900000, 4200000, 4700000, 5200000, 5800000, 8000000, 8800000, 9800000, 11000000, 12200000, 13500000, 15000000, 16500000]
}

df = pd.DataFrame(data)
print(f"✅ Created dataset with {len(df)} houses")
print("\nSample data:")
print(df.head())

# Step 2: Prepare features (X) and target (y)
print("\n🎯 Preparing features...")
X = df[['square_feet', 'bedrooms', 'bathrooms']]  # Input
y = df['price']                                     # Output (what we predict)
print("✅ Features prepared")

# Step 3: Split data (80% training, 20% testing)
print("\n📈 Splitting data (80% train, 20% test)...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"✅ Training samples: {len(X_train)}")
print(f"✅ Testing samples: {len(X_test)}")

# Step 4: Train the model
print("\n🤖 Training AI model...")
model = LinearRegression()
model.fit(X_train, y_train)
print("✅ Model trained!")

# Step 5: Test accuracy
print("\n📊 Evaluating model...")
train_accuracy = model.score(X_train, y_train)
test_accuracy = model.score(X_test, y_test)
print(f"✅ Training Accuracy: {train_accuracy:.2%}")
print(f"✅ Testing Accuracy: {test_accuracy:.2%}")

# Step 6: Save the model
print("\n💾 Saving model...")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'model.pkl')
pickle.dump(model, open(model_path, 'wb'))
print(f"✅ Model saved as: {model_path}")

# Show some predictions
print("\n🔮 Sample Predictions:")
print("-" * 50)
sample_inputs = [
    [2000, 3, 2],      # 2000 sq ft, 3 bed, 2 bath
    [1500, 2, 1.5],    # 1500 sq ft, 2 bed, 1.5 bath
    [3000, 4, 3],      # 3000 sq ft, 4 bed, 3 bath
]

for inp in sample_inputs:
    pred = model.predict([inp])[0]
    print(f"Input: {inp[0]} sq ft, {inp[1]} bed, {inp[2]} bath → Price: ${pred:,.0f}")

print("\n" + "=" * 50)
print("✅ TRAINING COMPLETE!")
print("=" * 50)