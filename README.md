# 🏠 House Price Predictor

## Introduction
An **AI-powered House Price Predictor** application that estimates real estate prices using Machine Learning.
Simply enter house details (Square Feet, Bedrooms, Bathrooms) and our AI will predict the estimated price instantly!

## ✨ Features
✅ **AI Price Prediction** - Instant price estimation using Linear Regression  
✅ **Prediction History** - Save and track all past predictions  
✅ **INR Currency Format** - Indian Rupees display  
✅ **Modern UI** - Clean, responsive, user-friendly interface  
✅ **Database Storage** - SQLite for persistent data storage  

## 🛠️ Tech Stack
### Frontend
- HTML5
- CSS3
- JavaScript (Vanilla)

### Backend
- Python 3.12+
- Flask (Web Framework)
- scikit-learn (Machine Learning)
- pandas (Data Processing)
- SQLite (Database)

## 📂 Project Structure
```
house-price-predictor/
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── backend/
│   ├── app.py
│   ├── train_model.py
│   ├── model.pkl
│   └── requirements.txt
├── predictions.db
├── .gitignore
└── README.md
```
## 🚀 Run Locally

### Requirements
- Python 3.12+
- pip
- Git
- VS Code (recommended)

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/akashkalki183-ui/house-price-predictor.git
cd house-price-predictor

# 2. Create Virtual Environment
python -m venv venv

# Activate Virtual Environment - Windows
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train the model (first time only)
cd backend
python train_model.py

# 5. Start Backend Server
python app.py

# 6. Open another terminal for Frontend
cd frontend
python -m http.server 8000

