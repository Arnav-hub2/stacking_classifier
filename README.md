# Credit Default Prediction System

A machine learning application that predicts credit default risk using a Stacking Classifier ensemble model. Built with Streamlit for easy deployment and interaction.

## 📋 Overview

This project implements a **Stacking Classifier** that combines multiple machine learning models to predict whether a customer will default on their credit:

- **Base Models**: Logistic Regression, Decision Tree, SVM, Random Forest
- **Meta-Learner**: Logistic Regression
- **Target**: Credit Default (Binary Classification)

## 📁 Project Structure

```
Stacking classification/
├── credit_data.csv          # Input credit data
├── stacking.ipynb           # Original Jupyter notebook
├── pipeline.py              # ML pipeline module
├── app.py                   # Streamlit application
├── requirements.txt         # Python dependencies
├── credit_stacking_model.pkl # Trained model (generated after training)
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📱 Application Features

### Home Page
- Overview of the application
- Explanation of the stacking classifier concept
- Quick navigation to other sections

### Train Model
- Upload your own credit_data.csv file
- Automatically trains the stacking classifier
- Displays model accuracy and metrics
- Saves the trained model for future use

### Make Prediction
- Input customer information:
  - Annual Income
  - Age
  - Loan Amount
  - Credit Score
  - Employment Years
  - Previous Default History
- Get real-time default risk predictions
- View probability visualizations

### Model Performance
- View detailed model metrics
- See confusion matrix visualization
- Review classification report
- Compare train/test set performance

### About
- Learn about the model architecture
- Understand how stacking works
- Find links to documentation

## 📊 Model Architecture

```
Input Features
    ↓
[Base Learners]
  - Logistic Regression
  - Decision Tree
  - SVM
  - Random Forest
    ↓
[Predictions to Meta-Learner]
    ↓
[Meta-Learner: Logistic Regression]
    ↓
Final Prediction (Default: Yes/No)
```

## 💾 Data Format

The input CSV should contain:

- **Features**: income, age, loan, credit_score, employment_years, default_history
- **Target**: default (0 = No default, 1 = Default)

Example:
```csv
income,age,loan,credit_score,employment_years,default_history,default
50000,35,10000,650,5,0,0
60000,45,15000,720,8,0,0
```

## 🌐 Deployment to Streamlit Cloud

### Steps:

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [Streamlit Cloud](https://streamlit.io/cloud)
   - Sign up with GitHub
   - Click "New app"
   - Select your repository
   - Set main file to `app.py`
   - Click "Deploy"

3. **Access Your App**
   - Your app will be available at: `https://[username]-stacking-app.streamlit.app/`

### Requirements for Deployment:
- GitHub repository with your code
- `requirements.txt` file (already included)
- `app.py` as main application file
- `pipeline.py` as pipeline module

## 🛠️ Local Development

### Using Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

## 📈 Model Performance

- **Accuracy**: Typically 85%+ (depends on data quality)
- **Algorithm**: Stacking Classifier with 5-fold CV
- **Training Time**: A few seconds on standard hardware
- **Prediction Time**: <100ms per prediction

## 🔧 Customization

### Modify Base Models
Edit `pipeline.py` line 56-61 to change base learners:
```python
estimators = [
    ('lr', LogisticRegression(max_iter=1000)),
    ('dt', DecisionTreeClassifier()),
    # Add or modify models here
]
```

### Change Prediction Features
Edit `app.py` line 238-245 to add/remove input fields

### Customize Styling
Edit the CSS in `app.py` line 20-28 or Streamlit configuration

## 📝 Pipeline Usage

### Training New Model
```python
from pipeline import CreditStackingPipeline

pipeline = CreditStackingPipeline('credit_data.csv')
pipeline.full_pipeline()
pipeline.save_model('my_model.pkl')
```

### Making Predictions
```python
pipeline.load_model('my_model.pkl')
predictions = pipeline.predict(new_data)
probabilities = pipeline.predict_proba(new_data)
```

## 🐛 Troubleshooting

### "Model not trained yet"
- Train a model first on the "Train Model" page
- Or upload your credit_data.csv and click "Train Stacking Classifier"

### "ImportError: No module named..."
- Install missing dependencies: `pip install -r requirements.txt`

### App crashes on prediction
- Ensure input data has the same features as training data
- Check that all numeric inputs are valid

## 📚 Resources

- [Scikit-learn Stacking](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.StackingClassifier.html)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/)

## ⚖️ License

This project is free to use and modify.

## 🤝 Contributing

Feel free to fork, modify, and improve this project!

## 📧 Support

For issues or questions, please check the code comments or refer to the documentation links above.

---

**Last Updated**: May 2026
**Version**: 1.0
