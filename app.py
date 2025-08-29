import gradio as gr
import time
import re
from agents import run_medical_analysis
from cases import get_case_titles, get_case_description, get_bias_analysis

# Global variable to store current analysis results
current_results = None

def extract_dynamic_biases(critique_text: str) -> str:
	"""Extract a dynamic list of biases from the Devil's Advocate output."""
	if not critique_text:
		return "No critique available."
	# Look for the "Identified Biases:" section and parse bullet lines
	section_match = re.search(r"Identified Biases:\n([\s\S]*)", critique_text)
	if not section_match:
		return "Identified Biases: None detected."
	section = section_match.group(1)
	# Stop at next empty line or section-like header
	section = re.split(r"\n\s*\n|\n[A-Z][A-Za-z ]+:\n", section, maxsplit=1)[0]
	bullets = []
	for line in section.splitlines():
		line = line.strip()
		if line.startswith("-"):
			bullets.append(line.lstrip("- "))
	# Fallback if model wrote a single-line "None detected."
	if not bullets:
		if "none" in section.lower():
			return "**Identified Biases:** None detected."
		return "**Identified Biases:** Unable to parse."
	# Render nicely
	rendered = "\n".join([f"- {b}" for b in bullets])
	return f"**Identified Biases (dynamic):**\n\n{rendered}"

def analyze_medical_case(case_input, custom_case_text=""):
	"""
	Run the complete medical analysis using the three-agent system.
	
	Args:
		case_input (str): Selected case ID from dropdown
		custom_case_text (str): Custom case text input
		
	Returns:
		tuple: (case_display, agent1_output, agent2_output, agent3_output, bias_analysis)
	"""
	global current_results
	
	# Determine which case to analyze
	if case_input == "custom" and custom_case_text.strip():
		case_text = custom_case_text.strip()
		case_display = f"**Custom Case:**\n\n{case_text}"
		static_bias = ""
	else:
		case_text = get_case_description(case_input)
		case_display = f"**{get_case_titles()[case_input]}**\n\n{case_text}"
		bias_info = get_bias_analysis(case_input)
		static_bias = f"\n\n> Static bias hint: {bias_info['bias_type']} — {bias_info['expected_bias']}" if bias_info else ""
	
	# Run the three-agent analysis
	try:
		results = run_medical_analysis(case_text)
		current_results = results
		
		if results["status"] == "success":
			dynamic_bias = extract_dynamic_biases(results.get("critique", ""))
			return (
				case_display,
				f"**Agent 1 (Diagnostician) - Initial Diagnosis:**\n\n{results['initial_diagnosis']}",
				f"**Agent 2 (Devil's Advocate) - Critical Analysis:**\n\n{results['critique']}",
				f"**Agent 3 (Synthesizer) - Final Diagnosis:**\n\n{results['final_diagnosis']}",
				f"{dynamic_bias}{static_bias}"
			)
		else:
			error_msg = f"Error in analysis: {results.get('error', 'Unknown error')}"
			return (
				case_display,
				f"**Error:** {error_msg}",
				f"**Error:** {error_msg}",
				f"**Error:** {error_msg}",
				""
			)
			
	except Exception as e:
		error_msg = f"Unexpected error: {str(e)}"
		return (
			case_display,
			f"**Error:** {error_msg}",
			f"**Error:** {error_msg}",
			f"**Error:** {error_msg}",
			""
		)

def clear_analysis():
	"""Clear all analysis outputs."""
	global current_results
	current_results = None
	return "", "", "", "", ""

def get_learning_points():
	"""Generate learning points based on the current analysis."""
	if not current_results or current_results.get("status") != "success":
		return "No analysis results available. Please run an analysis first."
	
	learning_points = """
## 🎯 Key Learning Points from This Analysis

### 1. **Bias Identification**
- **Anchoring Bias**: Focusing on initial symptoms or first impressions
- **Confirmation Bias**: Seeking information that confirms initial diagnosis
- **Availability Bias**: Overweighting recent or memorable conditions

### 2. **Devil's Advocate Role**
- Challenges assumptions and initial conclusions
- Identifies overlooked symptoms or alternative explanations
- Questions the relevance of previous medical history

### 3. **Synthesis Process**
- Combines multiple perspectives for balanced assessment
- Addresses identified biases systematically
- Provides evidence-based final diagnosis

### 4. **Clinical Decision Making**
- Multiple perspectives reduce diagnostic errors
- Systematic bias detection improves accuracy
- Evidence-based synthesis leads to better outcomes

### 5. **Multi-Agent Benefits**
- **Agent 1**: Provides initial assessment (may be biased)
- **Agent 2**: Identifies and challenges biases
- **Agent 3**: Synthesizes for improved final diagnosis
"""
	return learning_points

# Create the Gradio interface
def create_interface():
	"""Create and configure the Gradio interface."""
	
	with gr.Blocks(
		title="Devil's Advocate Multi-Agent Medical Analysis System",
		theme=gr.themes.Soft(),
		css="""
		/* Ensure dark text for light panels */
		.bias-highlight, .agent-output, .case-display { 
			color: #111 !important;
		}
		.bias-highlight * , .agent-output * , .case-display * {
			color: inherit !important;
		}
		.bias-highlight { 
			background-color: #fff3cd; 
			border-left: 4px solid #ffc107; 
			padding: 10px; 
			margin: 10px 0; 
		}
		.agent-output { 
			background-color: #f8f9fa; 
			border: 1px solid #dee2e6; 
			border-radius: 5px; 
			padding: 15px; 
			margin: 10px 0; 
		}
		.case-display { 
			background-color: #e3f2fd; 
			border: 1px solid #2196f3; 
			border-radius: 5px; 
			padding: 15px; 
			margin: 10px 0; 
		}
		"""
	) as interface:
		
		gr.Markdown("""
		# 🏥 Devil's Advocate Multi-Agent Medical Analysis System
		
		This demo shows how multiple AI agents can overcome diagnostic bias by simulating a clinical review process.
		
		## How It Works:
		1. **Agent 1 (Diagnostician)**: Provides initial diagnosis (may be biased)
		2. **Agent 2 (Devil's Advocate)**: Critiques and identifies bias
		3. **Agent 3 (Synthesizer)**: Creates improved final diagnosis
		
		## Instructions:
		- Select a sample case or input your own medical case
		- Click "Run Analysis" to see the three-agent process
		- Observe how bias is identified and addressed
		""")
		
		with gr.Row():
			with gr.Column(scale=1):
				gr.Markdown("### 📋 Case Selection")
				
				# Case selection dropdown
				case_dropdown = gr.Dropdown(
					choices=["Select a case..."] + list(get_case_titles().keys()),
					label="Choose a Sample Case",
					value="Select a case...",
					interactive=True
				)
				
				# Custom case input
				custom_case = gr.Textbox(
					label="Or Input Custom Medical Case",
					placeholder="Describe the patient's symptoms, history, and examination findings...",
					lines=8,
					interactive=True
				)
				
				# Analysis button
				analyze_btn = gr.Button(
					"🔍 Run Analysis",
					variant="primary",
					size="lg"
				)
				
				# Clear button
				clear_btn = gr.Button(
					"🗑️ Clear Analysis",
					variant="secondary"
				)
				
				# Learning points button
				learning_btn = gr.Button(
					"📚 Show Learning Points",
					variant="secondary"
				)
			
			with gr.Column(scale=2):
				gr.Markdown("### 📊 Analysis Results")
				
				# Case display
				case_display = gr.Markdown(
					label="Case Information",
					elem_classes=["case-display"]
				)
				
				# Agent outputs
				agent1_output = gr.Markdown(
					label="Agent 1: Initial Diagnosis",
					elem_classes=["agent-output"]
				)
				
				agent2_output = gr.Markdown(
					label="Agent 2: Devil's Advocate Critique",
					elem_classes=["agent-output"]
				)
				
				agent3_output = gr.Markdown(
					label="Agent 3: Final Synthesis",
					elem_classes=["agent-output"]
				)
				
				# Bias analysis
				bias_analysis = gr.Markdown(
					label="Expected Bias Analysis",
					elem_classes=["bias-highlight"]
				)
				
				# Learning points
				learning_points = gr.Markdown(
					label="Learning Points",
					visible=False
				)
		
		# Event handlers
		analyze_btn.click(
			fn=analyze_medical_case,
			inputs=[case_dropdown, custom_case],
			outputs=[case_display, agent1_output, agent2_output, agent3_output, bias_analysis]
		)
		
		clear_btn.click(
			fn=clear_analysis,
			outputs=[case_display, agent1_output, agent2_output, agent3_output, bias_analysis]
		)
		
		learning_btn.click(
			fn=get_learning_points,
			outputs=learning_points
		)
		
		# Show learning points when button is clicked
		learning_btn.click(
			fn=lambda: gr.update(visible=True),
			outputs=learning_points
		)
		
		# Auto-select custom case when custom text is entered
		def on_custom_text_change(text):
			if text.strip():
				return "custom"
			return case_dropdown.value
		
		custom_case.change(
			fn=on_custom_text_change,
			inputs=custom_case,
			outputs=case_dropdown
		)
		
		gr.Markdown("""
		---
		**Note**: This is a demonstration system for educational purposes. 
		The AI agents simulate medical reasoning but should not be used for actual clinical decision-making.
		""")
	
	return interface

# Main execution
if __name__ == "__main__":
	# Create and launch the interface
	interface = create_interface()
	interface.launch(
		server_name="0.0.0.0",
		server_port=7860,
		share=False,
		show_error=True,
		quiet=False
	)
