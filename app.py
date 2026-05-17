import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
import os
import pickle
from pipeline import CreditStackingPipeline

# Page configuration
st.set_page_config(
    page_title="Credit Default Prediction",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .metric-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'pipeline' not in st.session_state:
    st.session_state.pipeline = None
if 'model_trained' not in st.session_state:
    st.session_state.model_trained = False

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a page:",
    ["Home", "Train Model", "Make Prediction", "Model Performance", "About"]
)

# Home page
if page == "Home":
    st.title("💳 Credit Default Prediction System")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Welcome!")
        st.write("""
        This application uses a **Stacking Classifier** to predict credit default risk.
        
        ### Features:
        - **Train Model**: Train the stacking classifier on your credit data
        - **Make Predictions**: Predict default risk for individual applicants
        - **Model Performance**: View detailed model metrics and visualizations
        - **About**: Learn more about the model architecture
        
        ### What is Stacking?
        Stacking (Stacked Generalization) combines multiple machine learning models:
        - Base models: Logistic Regression, Decision Tree, SVM, Random Forest
        - Meta-learner: Logistic Regression
        """)
    
    with col2:
        st.info("""
        ### Quick Stats
        - **Algorithm**: Stacking Classifier
        - **Base Models**: 4
        - **Target**: Credit Default
        """)

# Train Model page
elif page == "Train Model":
    st.title("🚀 Train Model")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Data Upload")
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
        
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully!")
            
            st.write("### Data Preview")
            st.dataframe(data.head())
            
            st.write("### Data Info")
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Rows", data.shape[0])
            col_b.metric("Columns", data.shape[1])
            col_c.metric("Null Values", data.isnull().sum().sum())
            
            # Save uploaded file temporarily
            temp_path = "temp_data.csv"
            data.to_csv(temp_path, index=False)
            
            if st.button("Train Stacking Classifier", key="train_btn", use_container_width=True):
                with st.spinner("Training model... This may take a moment."):
                    try:
                        pipeline = CreditStackingPipeline(temp_path)
                        pipeline.full_pipeline()
                        
                        # Save the model
                        pipeline.save_model('credit_stacking_model.pkl')
                        
                        st.session_state.pipeline = pipeline
                        st.session_state.model_trained = True
                        
                        st.success("✅ Model trained successfully!")
                        
                        # Display metrics
                        st.write("### Model Metrics")
                        col_acc, col_precision = st.columns(2)
                        col_acc.metric("Accuracy", f"{pipeline.accuracy:.4f}")
                        
                        # Clean up temp file
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
                        
                    except Exception as e:
                        st.error(f"Error during training: {str(e)}")
        
        else:
            st.info("Please upload a CSV file to get started")
            st.write("""
            ### Required Format:
            Your CSV should have:
            - Features: income, age, loan, etc.
            - Target column: 'default' (0 or 1)
            """)
    
    with col2:
        st.info("""
        ### Training Details
        - **Base Models**: 4
        - **CV Folds**: 5
        - **Final Estimator**: Logistic Regression
        """)

# Make Prediction page
elif page == "Make Prediction":
    st.title("🔮 Make Prediction")
    st.markdown("---")
    
    if not st.session_state.model_trained:
        # Try to load existing model
        if os.path.exists('credit_stacking_model.pkl'):
            try:
                with open('credit_stacking_model.pkl', 'rb') as f:
                    model = pickle.load(f)
                st.session_state.model_trained = True
                st.info("Loaded existing model from saved file")
            except:
                st.warning("⚠️ Model not trained yet. Please train the model first in the 'Train Model' page.")
                st.stop()
        else:
            st.warning("⚠️ Model not trained yet. Please train the model first in the 'Train Model' page.")
            st.stop()
    
    st.subheader("Enter Customer Information")
    
    # Create input columns
    col1, col2 = st.columns(2)
    
    with col1:
        income = st.number_input("Annual Income ($)", min_value=0, step=1000, value=50000)
        age = st.number_input("Age (years)", min_value=18, max_value=100, value=35)
    
    with col2:
        loan = st.number_input("Loan Amount ($)", min_value=0, step=1000, value=10000)
    
    # Load model for prediction
    if os.path.exists('credit_stacking_model.pkl'):
        with open('credit_stacking_model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        # Prepare input data (must match training features)
        input_data = pd.DataFrame({
            'clientid': [0],  # Dummy ID for prediction
            'income': [income],
            'age': [age],
            'loan': [loan]
        })
        
        if st.button("Predict Default Risk", use_container_width=True):
            try:
                prediction = model.predict(input_data)[0]
                probability = model.predict_proba(input_data)[0]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if prediction == 1:
                        st.error(f"⚠️ High Risk - Default Probability: {probability[1]:.2%}")
                    else:
                        st.success(f"✅ Low Risk - Default Probability: {probability[1]:.2%}")
                
                with col2:
                    # Display probability gauge
                    fig, ax = plt.subplots(figsize=(6, 4))
                    categories = ['Non-Default', 'Default']
                    probs = probability
                    colors = ['#2ecc71', '#e74c3c']
                    ax.barh(categories, probs, color=colors)
                    ax.set_xlim(0, 1)
                    ax.set_xlabel('Probability')
                    st.pyplot(fig)
                
            except Exception as e:
                st.error(f"Error during prediction: {str(e)}")

# Model Performance page
elif page == "Model Performance":
    st.title("📊 Model Performance")
    st.markdown("---")
    
    if not st.session_state.model_trained:
        if os.path.exists('credit_stacking_model.pkl') and os.path.exists('temp_data.csv'):
            try:
                pipeline = CreditStackingPipeline('temp_data.csv')
                pipeline.full_pipeline()
                st.session_state.pipeline = pipeline
                st.session_state.model_trained = True
            except:
                st.warning("⚠️ Model not trained yet. Please train the model first in the 'Train Model' page.")
                st.stop()
        else:
            st.warning("⚠️ Model not trained yet. Please train the model first in the 'Train Model' page.")
            st.stop()
    
    if st.session_state.pipeline:
        pipeline = st.session_state.pipeline
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Accuracy", f"{pipeline.accuracy:.4f}")
        col2.metric("Train Set Size", pipeline.X_train.shape[0])
        col3.metric("Test Set Size", pipeline.X_test.shape[0])
        
        st.markdown("---")
        
        # Confusion Matrix
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Confusion Matrix")
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(pipeline.confusion_mat, annot=True, fmt='d', cmap='Blues', ax=ax)
            ax.set_xlabel('Predicted')
            ax.set_ylabel('Actual')
            ax.set_title('Confusion Matrix')
            st.pyplot(fig)
        
        with col2:
            st.subheader("Classification Report")
            st.text(pipeline.classification_rep)

# About page
elif page == "About":
    st.title("ℹ️ About This Application")
    st.markdown("---")
    
    st.write("""
    ## Stacking Classifier for Credit Default Prediction
    
    ### Model Architecture
    This application implements a **Stacking Classifier** that combines multiple machine learning models:
    
    #### Base Models:
    1. **Logistic Regression**: Linear classification model
    2. **Decision Tree**: Tree-based classification
    3. **Support Vector Machine (SVM)**: Kernel-based classification
    4. **Random Forest**: Ensemble of decision trees
    
    #### Meta-Learner:
    - **Logistic Regression**: Combines predictions from base models
    
    ### How It Works:
    1. Each base model makes predictions on the training data
    2. These predictions are used to train the meta-learner
    3. For final predictions, base models predict on test data
    4. Meta-learner makes final prediction based on base model outputs
    
    ### Data Processing:
    - Missing values are imputed with median values
    - Data is split 80% train / 20% test
    - 5-fold cross-validation used during training
    
    ### Features Tracked:
    - Income
    - Age
    - Loan Amount
    - Credit Score
    - Employment Years
    - Previous Default History
    
    ### Use Cases:
    - Credit risk assessment
    - Loan approval prediction
    - Default risk ranking
    
    ---
    
    **Built with Streamlit, Scikit-learn, and Python**
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("📚 For more info about stacking, visit [Scikit-learn Docs](https://scikit-learn.org/)")
    with col2:
        st.info("💡 For more about Streamlit, visit [Streamlit Docs](https://docs.streamlit.io/)")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center">
    <p>Credit Default Prediction System | Built with Streamlit</p>
    </div>
""", unsafe_allow_html=True)
