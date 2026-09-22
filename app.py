import gradio as gr
from agents import run_medical_analysis
from cases import get_case_titles, get_case_description, strip_bias_note

NO_CASE = "Select a case..."

def analyze_medical_case(case_input, custom_case_text=""):
	"""Run the three-agent analysis on the custom text if given, else the selected sample case."""
	if custom_case_text and custom_case_text.strip():
		case_text = custom_case_text.strip()
		case_display = f"**Custom Case:**\n\n{case_text}"
	elif case_input in get_case_titles():
		full = get_case_description(case_input)
		case_text = strip_bias_note(full)
		case_display = f"**{get_case_titles()[case_input]}**\n\n{full}"
	else:
		return "", "**Select a sample case or enter a custom case.**", "", "", ""

	results = run_medical_analysis(case_text)
	if results["status"] != "success":
		err = f"**Error:** {results.get('error', 'Unknown error')}"
		return case_display, err, err, err, ""
	return (
		case_display,
		f"**Agent 1 (Diagnostician):**\n\n{results['agent1']}",
		f"**Agent 2 (Independent Devil's Advocate):**\n\n{results['agent2']}",
		f"**Agent 3 (Synthesizer) – Final Result:**\n\n{results['agent3']}",
		results["overlap"],
	)

def clear_analysis():
	"""Clear all analysis outputs."""
	return "", "", "", "", ""

# Create the Gradio interface
def create_interface():
	"""Create and configure the Gradio interface."""
	
	with gr.Blocks(
		title="Devil's Advocate Multi-Agent Medical Analysis System",
		theme=gr.themes.Soft(),
		css="""
		.bias-highlight, .agent-output, .case-display { color: #111 !important; }
		.bias-highlight * , .agent-output * , .case-display * { color: inherit !important; }
		.bias-highlight { background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 10px; margin: 10px 0; }
		.agent-output { background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px; padding: 15px; margin: 10px 0; }
		.case-display { background-color: #e3f2fd; border: 1px solid #2196f3; border-radius: 5px; padding: 15px; margin: 10px 0; }
		"""
	) as interface:
		
		gr.Markdown("""
		# 🏥 Devil's Advocate Multi-Agent Medical Analysis System
		
		Revised pipeline:
		1) Agent 1 – Full-case diagnosis
		2) Agent 2 – Diagnosis from Symptoms+Exam, then overlap with PMH
		3) Agent 3 – Final synthesis and impact of past disease
		""")
		
		with gr.Row():
			with gr.Column(scale=1):
				gr.Markdown("### 📋 Case Selection")
				case_dropdown = gr.Dropdown(
					choices=[NO_CASE] + list(get_case_titles().keys()),
					label="Choose a Sample Case",
					value=NO_CASE,
					interactive=True
				)
				custom_case = gr.Textbox(
					label="Or Input Custom Medical Case",
					placeholder="Describe the patient's symptoms, history, and examination findings...",
					lines=8,
					interactive=True
				)
				analyze_btn = gr.Button("🔍 Run Analysis", variant="primary", size="lg")
				clear_btn = gr.Button("🗑️ Clear Analysis", variant="secondary")
			with gr.Column(scale=2):
				gr.Markdown("### 📊 Analysis Results")
				case_display = gr.Markdown(label="Case Information", elem_classes=["case-display"])
				agent1_output = gr.Markdown(label="Agent 1: Diagnostician", elem_classes=["agent-output"])
				agent2_output = gr.Markdown(label="Agent 2: Independent Devil's Advocate", elem_classes=["agent-output"])
				agent3_output = gr.Markdown(label="Agent 3: Synthesizer – Final", elem_classes=["agent-output"])
				overlap_panel = gr.Markdown(label="Overlap & Impact Summary", elem_classes=["bias-highlight"])
		
		analyze_btn.click(
			fn=analyze_medical_case,
			inputs=[case_dropdown, custom_case],
			outputs=[case_display, agent1_output, agent2_output, agent3_output, overlap_panel]
		)
		
		clear_btn.click(
			fn=clear_analysis,
			outputs=[case_display, agent1_output, agent2_output, agent3_output, overlap_panel]
		)
		
		gr.Markdown("""
		---
		For education only; not clinical advice.
		""")
	
	return interface

if __name__ == "__main__":
	interface = create_interface()
	interface.launch(server_name="0.0.0.0", server_port=7860, share=False, show_error=True, quiet=False)
