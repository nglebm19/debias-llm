---
title: Devil's Advocate Multi-Agent Medical Analysis System
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: "1.0.0"
app_file: app.py
pinned: false
---

# 🏥 Devil's Advocate Multi-Agent Medical Analysis System

A demonstration web application that shows how multiple AI agents can overcome diagnostic bias by simulating a clinical review process. This system demonstrates the power of multi-agent collaboration in reducing cognitive biases in medical decision-making.

## 🎯 Project Overview

This demo showcases a three-agent system designed to simulate and overcome common diagnostic biases:

1. **Agent 1 (Diagnostician)**: Provides initial diagnosis using all available information (HPI + PMH + Physical Exam)
2. **Agent 2 (Independent Devil's Advocate)**: Diagnoses from symptoms and physical exam only, then evaluates overlap with past medical history
3. **Agent 3 (Synthesizer)**: Combines both perspectives to create improved final diagnosis with impact analysis

## 🚀 Key Features

- **Multi-Agent Architecture**: Three specialized AI agents working in sequence
- **Bias Detection**: Agent 2 independently evaluates symptoms vs. past medical history
- **Overlap Scoring**: Qualitative assessment (High/Medium/Low) of current symptoms vs. past conditions
- **Interactive Web Interface**: Clean, intuitive Gradio-based UI
- **Sample Medical Cases**: Pre-built cases demonstrating different bias types
- **Custom Case Input**: Support for user-defined medical scenarios
- **Real LLM Outputs**: All agents generate concrete diagnostic content using Hugging Face models

## 🏗️ Architecture

```
User Input → Agent 1 (Diagnostician) → Agent 2 (Devil's Advocate) → Agent 3 (Synthesizer) → Final Output
                ↓                           ↓                           ↓
            Full-case Diagnosis      Symptoms+Exam Dx +        Balanced Synthesis +
            (HPI + PMH + Exam)      Overlap Score            Impact Analysis
```

## 📋 Prerequisites

- Python 3.8 or higher
- 4GB+ RAM (for model loading)
- Internet connection (for initial model download)

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nglebm19/debias-llm.git
   cd debias-llm
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

### Local Development

1. **Run the application:**
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to `http://localhost:7860`

3. **Select a sample case** from the dropdown or input your own medical case

4. **Click "Run Analysis"** to see the three-agent process in action

5. **Review the results** to see how each agent contributes to the final diagnosis

### Sample Cases

The system includes four pre-built medical cases demonstrating different bias types:

- **Case 1**: Resolved Appendicitis with New Symptoms (Anchoring bias)
- **Case 2**: Previous Heart Condition with Current Respiratory Issues (Confirmation bias)
- **Case 3**: Resolved Infection with Persistent Symptoms (Availability bias)
- **Case 4**: Chronic Condition with Acute Exacerbation (Anchoring bias)

## 🔧 Configuration

### Model Selection

The system uses `microsoft/DialoGPT-medium` by default. You can modify the model in `agents.py`:

```python
self.model_name = "microsoft/DialoGPT-medium"  # Change this line
```

### Alternative Models

For faster inference or different capabilities, consider:

- `microsoft/DialoGPT-small` (117M parameters)
- `gpt2` (124M parameters)
- `distilbert-base-uncased` (66M parameters)

### Performance Tuning

Adjust generation parameters in `agents.py`:

```python
self.generator = pipeline(
    "text-generation",
    model=self.model,
    tokenizer=self.tokenizer,
    max_new_tokens=200,        # Adjust for longer/shorter outputs
    do_sample=True,
    temperature=0.7,           # Lower = more focused, Higher = more creative
    pad_token_id=self.tokenizer.eos_token_id
)
```

## 🌐 Deployment

### Hugging Face Spaces

1. **Create a new Space** on Hugging Face
2. **Upload your files** to the Space
3. **Set the Space SDK** to Gradio
4. **Configure the Space** with appropriate hardware requirements

### Docker Deployment

1. **Build the Docker image:**
   ```bash
   docker build -t debias-llm .
   ```

2. **Run the container:**
   ```bash
   docker run -p 7860:7860 debias-llm
   ```

### Cloud Deployment

The application can be deployed on:
- **Google Colab** (with modifications)
- **AWS SageMaker**
- **Azure ML**
- **Google Cloud Run**

## 📊 Understanding the Output

### Agent 1: Full-Case Diagnosis
- **Purpose**: Comprehensive initial assessment using all available information
- **Input**: History of Present Illness + Past Medical History + Physical Examination
- **Output**: Initial diagnosis with clinical reasoning

### Agent 2: Independent Devil's Advocate
- **Purpose**: Independent evaluation and overlap assessment
- **Phase 1**: Diagnosis based only on current symptoms and physical exam
- **Phase 2**: Overlap score (High/Medium/Low) with past medical history
- **Output**: Independent diagnosis + overlap score + rationale

### Agent 3: Final Synthesis
- **Purpose**: Combines both perspectives for balanced final assessment
- **Approach**: Evidence-based synthesis with impact analysis
- **Output**: Final diagnosis + differential + impact of past disease + next steps

## 🧠 Bias Types Demonstrated

1. **Anchoring Bias**: Focusing on initial symptoms or first impressions
2. **Confirmation Bias**: Seeking information that confirms initial diagnosis
3. **Availability Bias**: Overweighting recent or memorable conditions
4. **Overconfidence Bias**: Making definitive diagnoses too quickly

## 🔍 Troubleshooting

### Common Issues

1. **Model Loading Errors**
   - Ensure sufficient RAM (4GB+)
   - Check internet connection for model download
   - Verify transformers library version

2. **Generation Errors**
   - Check input text length and format
   - Verify model compatibility
   - Review error logs in console

3. **Performance Issues**
   - Use smaller models for faster inference
   - Reduce max_new_tokens parameter
   - Consider GPU acceleration if available

### Error Handling

The system includes comprehensive error handling:
- Graceful fallbacks for model failures
- Clear error messages for users
- Logging for debugging

## 📚 Learning Resources

### Medical Decision Making
- Cognitive biases in clinical reasoning
- Multi-perspective diagnostic approaches
- Evidence-based medicine principles

### AI and Bias
- Algorithmic bias detection
- Multi-agent systems
- Bias mitigation strategies

### Technical Implementation
- Hugging Face Transformers
- Gradio web applications
- Python multi-agent systems

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

1. **Additional Bias Types**: Implement more cognitive biases
2. **Enhanced Models**: Integrate larger, more capable models
3. **UI Improvements**: Better visualization of bias patterns
4. **Case Library**: Expand sample medical cases
5. **Performance**: Optimize for faster inference

## 📄 License

This project is for educational and demonstration purposes. Please ensure compliance with local regulations regarding medical AI systems.

## ⚠️ Disclaimer

**Important**: This is a demonstration system for educational purposes only. The AI agents simulate medical reasoning but should not be used for actual clinical decision-making. Always consult qualified healthcare professionals for medical advice.

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Review the code comments
3. Open an issue in the repository
4. Contact the development team

---

**Built with ❤️ for medical education and AI bias research**
