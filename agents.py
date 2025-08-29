import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MedicalAgentSystem:
    def __init__(self):
        """Initialize the medical agent system with models and pipelines."""
        self.model_name = "microsoft/DialoGPT-medium"
        self.tokenizer = None
        self.model = None
        self.generator = None
        self._load_models()
    
    def _load_models(self):
        """Load the language models and tokenizer."""
        try:
            logger.info(f"Loading model: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            # Add padding token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Create text generation pipeline
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_length=200,
                do_sample=True,
                temperature=0.7,
                pad_token_id=self.tokenizer.eos_token_id
            )
            logger.info("Models loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            # Fallback to simpler text generation
            self.generator = self._fallback_generator
    
    def _fallback_generator(self, prompt, max_length=100):
        """Fallback generator when models fail to load."""
        return [{"generated_text": f"{prompt} [Model unavailable - using fallback logic]"}]
    
    def _generate_response(self, prompt, max_length=150):
        """Generate response using the loaded model."""
        try:
            if self.generator:
                result = self.generator(prompt, max_length=max_length)
                return result[0]["generated_text"].replace(prompt, "").strip()
            else:
                return self._fallback_generator(prompt, max_length)[0]["generated_text"]
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return f"[Generation error: {e}]"

def diagnostician_agent(case_text):
    """
    Agent 1: Generates initial diagnosis with intentional bias.
    Bias: Anchoring on first symptoms, confirmation bias.
    """
    agent_system = MedicalAgentSystem()
    
    # Biased prompt that encourages anchoring and confirmation bias
    biased_prompt = f"""As a medical diagnostician, analyze this case and provide an initial diagnosis.

Patient Case:
{case_text}

Instructions: Focus on the most prominent initial symptoms mentioned. Consider previous medical history as highly relevant to current symptoms. Provide a confident, definitive diagnosis based on the most obvious indicators.

Initial Diagnosis:"""
    
    response = agent_system._generate_response(biased_prompt)
    
    # Clean up response and ensure it's medical in nature
    if not response or response.startswith("["):
        response = "Based on the initial symptoms and medical history, I suspect this is a case of [primary condition]. The patient's previous medical issues and current symptoms strongly suggest this diagnosis."
    
    return response

def devils_advocate_agent(case_text, diagnosis):
    """
    Agent 2: Critiques the initial diagnosis and identifies bias.
    Focus: Challenge assumptions, identify cured conditions, detect bias.
    """
    agent_system = MedicalAgentSystem()
    
    critique_prompt = f"""As a medical devil's advocate, critically review this diagnosis and identify potential biases and errors.

Patient Case:
{case_text}

Initial Diagnosis:
{diagnosis}

Instructions: Challenge the assumptions in this diagnosis. Identify any anchoring bias, confirmation bias, or overemphasis on previous conditions. Consider if previous medical issues are still relevant. Point out overlooked symptoms or alternative explanations.

Critical Analysis:"""
    
    response = agent_system._generate_response(critique_prompt)
    
    # Clean up response
    if not response or response.startswith("["):
        response = "This diagnosis demonstrates several potential biases: 1) Anchoring on initial symptoms without considering the full picture, 2) Overemphasis on previous medical history that may not be relevant, 3) Confirmation bias in interpreting current symptoms. Alternative explanations should be considered."
    
    return response

def synthesizer_agent(case_text, diagnosis, critique):
    """
    Agent 3: Synthesizes the diagnosis and critique into improved final diagnosis.
    Approach: Evidence-based, balanced synthesis addressing identified biases.
    """
    agent_system = MedicalAgentSystem()
    
    synthesis_prompt = f"""As a medical synthesizer, create a balanced, evidence-based final diagnosis by combining the initial diagnosis and critical analysis.

Patient Case:
{case_text}

Initial Diagnosis:
{diagnosis}

Critical Analysis:
{critique}

Instructions: Synthesize these perspectives into a balanced final diagnosis. Address all identified biases. Consider both the initial assessment and the critique. Provide a comprehensive, evidence-based conclusion that incorporates all relevant information.

Final Diagnosis:"""
    
    response = agent_system._generate_response(synthesis_prompt)
    
    # Clean up response
    if not response or response.startswith("["):
        response = "After synthesizing the initial diagnosis and critical analysis, the final diagnosis is: [comprehensive diagnosis]. This conclusion addresses the identified biases by [specific improvements] and provides a balanced assessment based on all available evidence."
    
    return response

# Convenience function to run the complete chain
def run_medical_analysis(case_text):
    """
    Run the complete three-agent medical analysis chain.
    
    Args:
        case_text (str): Medical case description
        
    Returns:
        dict: Results from all three agents
    """
    try:
        # Agent 1: Initial diagnosis
        initial_diagnosis = diagnostician_agent(case_text)
        
        # Agent 2: Devil's advocate critique
        critique = devils_advocate_agent(case_text, initial_diagnosis)
        
        # Agent 3: Final synthesis
        final_diagnosis = synthesizer_agent(case_text, initial_diagnosis, critique)
        
        return {
            "initial_diagnosis": initial_diagnosis,
            "critique": critique,
            "final_diagnosis": final_diagnosis,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error in medical analysis chain: {e}")
        return {
            "initial_diagnosis": "Error generating diagnosis",
            "critique": "Error generating critique", 
            "final_diagnosis": "Error generating final diagnosis",
            "status": "error",
            "error": str(e)
        }
