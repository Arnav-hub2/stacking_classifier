# Deployment Guide - Streamlit Cloud

Complete guide to deploy your Credit Default Prediction application to Streamlit Cloud.

## Prerequisites

Before deploying, ensure you have:
- A GitHub account
- Your code pushed to GitHub
- `requirements.txt` in your repository
- `app.py` as your main application file

## Step-by-Step Deployment

### Step 1: Prepare Your Repository

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit your changes
git commit -m "Credit Default Prediction App - Initial deployment"

# Add your GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/your-repo-name.git

# Push to GitHub
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit: https://streamlit.io/cloud
   - Sign up or log in with your GitHub account

2. **Create New App**
   - Click "New app" button
   - Select "From existing repo"

3. **Configure Deployment**
   - **Repository**: Select your GitHub repository
     - e.g., `YOUR_USERNAME/Stacking-classification`
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `app.py`

4. **Click "Deploy"**
   - Streamlit will build and deploy your app
   - Wait for deployment to complete (usually 2-3 minutes)

5. **Access Your App**
   - Your app will be available at:
     ```
     https://YOUR-USERNAME-STACKING-CLASSIFICATION.streamlit.app/
     ```

## Troubleshooting Deployment

### 1. Import Errors
**Problem**: `ModuleNotFoundError: No module named 'pipeline'`

**Solution**:
- Ensure `pipeline.py` is in the same directory as `app.py`
- Check that all files are committed and pushed to GitHub
- Redeploy the app after pushing changes

### 2. Missing Dependencies
**Problem**: `ModuleNotFoundError: No module named 'scikit-learn'`

**Solution**:
- Verify `requirements.txt` exists in your repo
- Check all required packages are listed
- Redeploy after updating requirements.txt
- Use exact versions for consistency:
  ```
  scikit-learn==1.3.0
  pandas==2.0.3
  ```

### 3. Data File Not Found
**Problem**: `FileNotFoundError: [Errno 2] No such file or directory: 'credit_data.csv'`

**Solution**:
- In the app, use file uploader instead of hardcoded paths
- The app.py already does this - no changes needed
- Users upload data through the interface

### 4. Model Not Loading
**Problem**: `FileNotFoundError: [Errno 2] No such file or directory: 'credit_stacking_model.pkl'`

**Solution**:
- This is expected on first deployment
- Users must train a model first using "Train Model" page
- Model is saved locally on Streamlit's filesystem

## Performance Optimization

For faster deployments and better performance:

### 1. Update Caching
Add caching to avoid retraining:

```python
import streamlit as st

@st.cache_resource
def load_model():
    with open('credit_stacking_model.pkl', 'rb') as f:
        return pickle.load(f)
```

### 2. Reduce Model Size
Use model compression:
```python
import joblib
joblib.dump(model, 'model.joblib', compress=3)
```

### 3. Optimize Dependencies
Keep only necessary packages in requirements.txt

## Monitoring Your Deployment

### 1. View Logs
- Go to your app on Streamlit Cloud
- Click settings icon → "Manage app"
- View logs in the "Activity" tab

### 2. Check App Health
- Monitor resource usage
- Check for errors in browser console (F12)
- Test all features regularly

## Updating Your App

To update your deployed app:

1. **Make changes locally**
   ```bash
   # Edit files
   git add .
   git commit -m "Update app features"
   git push
   ```

2. **Redeployment**
   - Streamlit automatically detects changes
   - App redeploys within 1-2 minutes
   - No manual action needed

## Security Best Practices

### 1. Secrets Management
For sensitive data (API keys, credentials):

```bash
# Create .streamlit/secrets.toml (NOT in git)
# Add your secrets:
# api_key = "your-secret-key"
```

### 2. User Data
- No personal data is stored permanently
- Training data is temporary
- Use secure connections (HTTPS - automatic with Streamlit Cloud)

## Advanced Configuration

### 1. Custom Domain
- Streamlit Cloud Business plan allows custom domains
- Contact Streamlit support for setup

### 2. Private Apps
- Enterprise plan required
- Control who can access your app

### 3. Environment Variables
In `app.py`:
```python
import os
API_KEY = os.getenv("MY_API_KEY", "default_value")
```

Set on Streamlit Cloud:
- Go to app settings
- Add secrets in `.streamlit/secrets.toml`

## Cost Considerations

**Streamlit Cloud (Free Tier)**:
- ✅ Free hosting for public apps
- ✅ Up to 3 apps
- ✅ 1GB storage
- ✅ Good for prototyping

**Community Cloud**:
- Same features as free tier
- Great for learning and demos

**Business/Enterprise**:
- Custom domains
- Private deployment
- Advanced monitoring

## Scaling Your App

As your app grows:

1. **Increase model efficiency**
   - Use model pruning
   - Optimize hyperparameters

2. **Add caching**
   - Cache model predictions
   - Cache data transformations

3. **Split features**
   - Separate pages for different models
   - Lazy load heavy components

4. **Consider Streamlit Business**
   - More resources
   - Better performance
   - Custom support

## Backup and Recovery

### 1. Backup Your Code
Keep a local copy:
```bash
git clone https://github.com/YOUR_USERNAME/your-repo.git
```

### 2. Model Backup
Download trained models:
- Download from Streamlit Cloud filesystem
- Keep local copies
- Version control important models

### 3. Data Backup
Keep original data:
```bash
# Include in git (if not too large)
git add credit_data.csv
git commit -m "Backup original data"
```

## Getting Help

### Resources
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-cloud)
- [Streamlit Community Forum](https://discuss.streamlit.io/)
- [GitHub Issues](https://github.com/streamlit/streamlit/issues)

### Common Issues Repository
Check `.streamlit/deployment_issues.md` for solutions

## Post-Deployment Checklist

- [ ] App loads without errors
- [ ] All pages are accessible
- [ ] File upload works
- [ ] Model training completes
- [ ] Predictions return correct results
- [ ] Visualizations display properly
- [ ] Mobile view is responsive
- [ ] Performance is acceptable

## Next Steps

After successful deployment:

1. **Share your app**
   - Share the URL with others
   - Add to portfolio
   - Use for demonstrations

2. **Gather feedback**
   - Monitor user interactions
   - Improve based on feedback
   - Add new features

3. **Maintain your app**
   - Update dependencies monthly
   - Monitor Streamlit updates
   - Add new functionality

---

**Deployment Status**: Ready for production
**Last Updated**: May 2026
**Version**: 1.0
