# 🏥 Devil's Advocate Multi-Agent Medical Analysis System
[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/nglebm19/debias-llm)

This repository contains a web application that demonstrates how multiple AI agents can collaborate to overcome cognitive biases in medical diagnostics by simulating a clinical review process.

## 🎯 Project Overview

This demo showcases a three-agent system designed to simulate and counteract common diagnostic biases like anchoring, confirmation, and availability bias.

1.  **Agent 1 (Diagnostician)**: Provides an initial diagnosis using all available information (History of Present Illness, Past Medical History, and Physical Exam).
2.  **Agent 2 (Independent Devil's Advocate)**: Forms a diagnosis using only the current symptoms and physical exam results. It then evaluates the degree of overlap between the current presentation and the patient's past medical history.
3.  **Agent 3 (Synthesizer)**: Analyzes the outputs from the first two agents to formulate an improved final diagnosis, including an impact analysis of past conditions.

## 🚀 Key Features

*   **Multi-Agent Architecture**: Three specialized AI agents work sequentially to refine a medical diagnosis.
*   **Bias Detection**: Agent 2's independent evaluation helps identify and challenge potential cognitive biases.
*   **Overlap Scoring**: Provides a qualitative assessment (High/Medium/Low) of the relationship between current symptoms and past conditions.
*   **Interactive Web Interface**: A clean and intuitive UI built with Gradio.
*   **Sample Medical Cases**: Includes pre-built cases that highlight different types of diagnostic bias.
*   **Custom Case Input**: Allows users to input their own medical scenarios for analysis.

## 🏗️ Architecture

The system follows a sequential pipeline where each agent builds upon the last to de-bias the final conclusion.

```
User Input → Agent 1 (Diagnostician) → Agent 2 (Devil's Advocate) → Agent 3 (Synthesizer) → Final Output
                ↓                           ↓                           ↓
            Full-case Diagnosis      Symptoms+Exam Dx +        Balanced Synthesis +
            (HPI + PMH + Exam)      Overlap Score            Impact Analysis
```

## 📋 Prerequisites

*   Python 3.8+
*   4GB+ RAM (for loading the language model)
*   Internet connection (for downloading models on first run)

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/nglebm19/debias-llm.git
    cd debias-llm
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Usage

1.  **Run the application:**
    ```bash
    python app.py
    ```

2.  **Open your browser** and navigate to the local URL provided, typically `http://localhost:7860`.

3.  **Select a sample case** from the dropdown menu or enter your own medical scenario in the custom case text box.

4.  **Click "Run Analysis"** to initiate the three-agent process.

5.  **Review the results** from each agent to see how the diagnosis evolves and how potential biases are addressed.

### Sample Cases

The application includes four pre-built medical cases to demonstrate different cognitive biases:

*   **Case 1**: Resolved Appendicitis with New Symptoms (Anchoring bias)
*   **Case 2**: Previous Heart Condition with Current Respiratory Issues (Confirmation bias)
*   **Case 3**: Resolved Infection with Persistent Symptoms (Availability bias)
*   **Case 4**: Chronic Condition with Acute Exacerbation (Anchoring bias)

## 🔧 Configuration

The system uses `microsoft/DialoGPT-medium` by default. You can change the model or its generation parameters by editing `agents.py`.

*   **Model Selection**: Modify the `self.model_name` variable in the `MedicalAgentSystem` class.
*   **Performance Tuning**: Adjust parameters like `max_new_tokens` and `temperature` within the `pipeline` setup in the `_load_models` method to control output length and creativity.

## 🤝 Contributing

Contributions are welcome. Potential areas for improvement include:

*   Integrating larger, more capable language models.
*   Expanding the library of sample cases to cover more biases and medical scenarios.
*   Enhancing the UI to better visualize the flow of information and bias mitigation.
*   Optimizing model inference for faster performance.

## ⚠️ Disclaimer

**This is a demonstration system for educational purposes only.** The AI agents simulate medical reasoning and are not a substitute for professional medical advice, diagnosis, or treatment. The outputs should not be used for actual clinical decision-making. Always consult a qualified healthcare professional for any medical concerns.
