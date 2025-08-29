# 🚀 Hugging Face Spaces Deployment Guide

This guide explains how to deploy the Devil's Advocate Multi-Agent Medical Analysis System on Hugging Face Spaces.

## 📋 Prerequisites

1. **Hugging Face Account**: Sign up at [huggingface.co](https://huggingface.co)
2. **Git Knowledge**: Basic understanding of Git commands
3. **Project Files**: All project files should be ready

## 🎯 Deployment Steps

### Step 1: Create a New Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Choose settings:
   - **Owner**: Your username or organization
   - **Space name**: `debias-llm` (or your preferred name)
   - **License**: Choose appropriate license (e.g., MIT)
   - **Space SDK**: Select **Gradio**
   - **Space hardware**: Choose based on your needs:
     - **CPU**: Free tier (slower but free)
     - **GPU**: Paid tier (faster inference)

### Step 2: Configure Space Settings

1. **Space Settings** → **Repository secrets**:
   - Add any API keys if needed (not required for this demo)

2. **Space Settings** → **Hardware**:
   - **CPU**: 2 cores, 8GB RAM (minimum)
   - **GPU**: T4 or better for faster inference

### Step 3: Upload Project Files

**Option A: Git Push (Recommended)**
```bash
# Clone the Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/debias-llm
cd debias-llm

# Copy your project files
cp -r /path/to/your/project/* .

# Commit and push
git add .
git commit -m "Initial deployment of Devil's Advocate Multi-Agent System"
git push
```

**Option B: Web Interface**
1. Go to your Space repository
2. Click "Files" tab
3. Upload all project files manually

### Step 4: Required Files

Ensure these files are in your Space:

```
├── app.py              # Main Gradio application
├── agents.py           # Agent functions
├── cases.py            # Sample medical cases
├── requirements.txt    # Dependencies
├── README.md           # Project documentation
└── .gitignore         # Git ignore file
```

### Step 5: Configure Dependencies

**requirements.txt** should contain:
```txt
gradio>=4.0.0
transformers>=4.30.0
torch>=2.0.0
tokenizers>=0.13.0
numpy>=1.24.0
```

## 🔧 Space Configuration

### Hardware Requirements

**Minimum (Free Tier):**
- CPU: 2 cores
- RAM: 8GB
- Storage: 50GB

**Recommended (Paid Tier):**
- CPU: 4+ cores
- RAM: 16GB+
- GPU: T4 or better
- Storage: 100GB+

### Environment Variables

No special environment variables are required for basic functionality.

## 🚀 Launch Configuration

### app.py Launch Settings

The application is configured to launch with:
```python
interface.launch(
    server_name="0.0.0.0",
    server_port=7860,
    share=False,
    show_error=True,
    quiet=False
)
```

**For Spaces deployment, modify to:**
```python
interface.launch(
    server_name="0.0.0.0",
    server_port=7860,
    share=False,
    show_error=True,
    quiet=False,
    # Add these for Spaces
    show_api=False,
    inbrowser=False
)
```

## 📊 Monitoring and Debugging

### Space Logs

1. Go to your Space
2. Click "Logs" tab
3. Monitor for errors or issues

### Common Issues

1. **Model Loading Failures**
   - Check RAM availability
   - Verify model compatibility
   - Check internet connectivity

2. **Dependency Conflicts**
   - Review requirements.txt
   - Check for version conflicts
   - Verify Python version compatibility

3. **Memory Issues**
   - Reduce model size
   - Optimize generation parameters
   - Use smaller models

## 🔄 Updates and Maintenance

### Updating the Space

1. **Local Changes**: Make changes to your local files
2. **Git Push**: Push changes to the Space repository
3. **Auto-reload**: Spaces automatically reload on changes

### Model Updates

1. **Version Updates**: Update requirements.txt
2. **Model Changes**: Modify agents.py
3. **Test Locally**: Verify changes work before pushing

## 🌐 Public Access

### Space URL

Your Space will be available at:
```
https://huggingface.co/spaces/YOUR_USERNAME/debias-llm
```

### Sharing

1. **Public**: Anyone can access and use
2. **Private**: Only you and collaborators can access
3. **Embed**: Use in other websites or applications

## 📈 Performance Optimization

### For Free Tier

1. **Smaller Models**: Use DialoGPT-small instead of medium
2. **Caching**: Implement response caching
3. **Optimization**: Reduce generation parameters

### For Paid Tier

1. **GPU Acceleration**: Enable CUDA support
2. **Larger Models**: Use more capable models
3. **Parallel Processing**: Run agents concurrently

## 🔒 Security Considerations

1. **Input Validation**: Sanitize user inputs
2. **Rate Limiting**: Prevent abuse
3. **Error Handling**: Don't expose sensitive information
4. **Medical Disclaimer**: Clear educational purpose statement

## 📚 Additional Resources

- [Hugging Face Spaces Documentation](https://huggingface.co/docs/hub/spaces)
- [Gradio Documentation](https://gradio.app/docs/)
- [Transformers Documentation](https://huggingface.co/docs/transformers)

## 🆘 Troubleshooting

### Space Won't Start

1. Check logs for errors
2. Verify all required files are present
3. Check requirements.txt syntax
4. Verify Python version compatibility

### Model Loading Issues

1. Check internet connectivity
2. Verify model names are correct
3. Check available memory
4. Use smaller models if needed

### Performance Issues

1. Optimize model parameters
2. Use smaller models
3. Implement caching
4. Consider paid tier for better hardware

---

**Need Help?** Check the main README.md or open an issue in the repository.
