import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import StackingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


class CreditStackingPipeline:
    """
    Credit default prediction pipeline using Stacking Classifier
    """
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.model = None
        self.accuracy = None
        self.classification_rep = None
        self.confusion_mat = None
        
    def load_data(self):
        """Load data from CSV file"""
        self.data = pd.read_csv(self.data_path)
        print(f"Data loaded successfully. Shape: {self.data.shape}")
        return self.data
    
    def check_null_values(self):
        """Check for null values"""
        null_counts = self.data.isnull().sum()
        print("Null values:\n", null_counts)
        return null_counts
    
    def handle_missing_values(self):
        """Handle missing values with median imputation"""
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if self.data[col].isnull().sum() > 0:
                self.data[col] = self.data[col].fillna(self.data[col].median())
        
        print("Missing values handled")
        return self.data
    
    def split_data(self, test_size=0.2, random_state=42):
        """Split data into training and testing sets"""
        # Drop only the target column, keep all features
        X = self.data.drop('default', axis=1)
        y = self.data['default']
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        print(f"Data split into train: {self.X_train.shape}, test: {self.X_test.shape}")
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def build_and_train_model(self):
        """Build and train the stacking classifier"""
        # Define base learners
        estimators = [
            ('lr', LogisticRegression(max_iter=1000, random_state=42)),
            ('dt', DecisionTreeClassifier(random_state=42)),
            ('svc', SVC(probability=True, random_state=42)),
            ('rf', RandomForestClassifier(n_estimators=100, random_state=42))
        ]
        
        # Create stacking classifier with LogisticRegression as final estimator
        self.model = StackingClassifier(
            estimators=estimators,
            final_estimator=LogisticRegression(max_iter=1000, random_state=42),
            cv=5
        )
        
        print("Training the stacking classifier...")
        self.model.fit(self.X_train, self.y_train)
        print("Model trained successfully")
        
        return self.model
    
    def evaluate_model(self):
        """Evaluate the trained model"""
        y_pred = self.model.predict(self.X_test)
        
        self.accuracy = accuracy_score(self.y_test, y_pred)
        self.classification_rep = classification_report(self.y_test, y_pred)
        self.confusion_mat = confusion_matrix(self.y_test, y_pred)
        
        print(f"Accuracy Score: {self.accuracy:.4f}")
        print(f"\nClassification Report:\n{self.classification_rep}")
        print(f"\nConfusion Matrix:\n{self.confusion_mat}")
        
        return self.accuracy, self.classification_rep, self.confusion_mat
    
    def predict(self, X):
        """Make predictions on new data"""
        if self.model is None:
            raise ValueError("Model has not been trained yet")
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """Get prediction probabilities"""
        if self.model is None:
            raise ValueError("Model has not been trained yet")
        return self.model.predict_proba(X)
    
    def save_model(self, model_path='credit_stacking_model.pkl'):
        """Save the trained model to file"""
        if self.model is None:
            raise ValueError("Model has not been trained yet")
        
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"Model saved to {model_path}")
    
    def load_model(self, model_path='credit_stacking_model.pkl'):
        """Load a trained model from file"""
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        print(f"Model loaded from {model_path}")
        return self.model
    
    def get_feature_names(self):
        """Get feature names from the training data"""
        return self.X_train.columns.tolist()
    
    def full_pipeline(self):
        """Execute the complete pipeline"""
        self.load_data()
        self.check_null_values()
        self.handle_missing_values()
        self.split_data()
        self.build_and_train_model()
        self.evaluate_model()
        return self.model


if __name__ == "__main__":
    # Example usage
    data_path = r'credit_data.csv'
    
    pipeline = CreditStackingPipeline(data_path)
    pipeline.full_pipeline()
    pipeline.save_model('credit_stacking_model.pkl')
