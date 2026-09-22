import gradio as gr
from agents import run_medical_analysis
from cases import get_case_titles, get_case_description, strip_bias_note

NO_CASE = "Select a case..."

_OVERLAP_CLASS = {"Low": "overlap-low", "Medium": "overlap-medium", "High": "overlap-high"}


def analyze_medical_case(case_input, custom_case_text=""):
	"""Run the three-agent analysis on the custom text if given, else the selected sample case."""
	if custom_case_text and custom_case_text.strip():
		case_text = custom_case_text.strip()
		case_display = f"**Custom Case**\n\n{case_text}"
	elif case_input in get_case_titles():
		full = get_case_description(case_input)
		case_text = strip_bias_note(full)
		case_display = f"**{get_case_titles()[case_input]}**\n\n{full}"
	else:
		msg = "Select a sample case or enter a custom case to begin."
		return "", msg, "", "", gr.update(value="", elem_classes=["overlap-card"]), gr.update(visible=False)

	results = run_medical_analysis(case_text)
	if results["status"] != "success":
		err = f"**Error:** {results.get('error', 'Unknown error')}"
		return case_display, err, err, err, gr.update(value="", elem_classes=["overlap-card"]), gr.update(visible=False)

	score = results["structured"]["agent2_overlap"]["score"]
	overlap_classes = ["overlap-card", _OVERLAP_CLASS.get(score, "")]
	banner = gr.update(
		value="**Demo mode** — no `ANTHROPIC_API_KEY` configured, showing canned mock output below, not a real diagnosis.",
		visible=bool(results.get("mock")),
	)
	return (
		case_display,
		results["agent1"],
		results["agent2"],
		results["agent3"],
		gr.update(value=results["overlap"], elem_classes=overlap_classes),
		banner,
	)


def clear_analysis():
	"""Clear all analysis outputs."""
	return "", "", "", "", gr.update(value="", elem_classes=["overlap-card"]), gr.update(visible=False)


_CSS = """
.gradio-container { max-width: 900px !important; margin: 0 auto !important; }
#title { text-align: center; margin-bottom: 0.25rem; }
#subtitle { text-align: center; color: #6b7280; margin-bottom: 1.5rem; font-size: 0.95rem; }

.case-display, .overlap-card {
	background: #ffffff; color: #111827;
	border: 1px solid #e5e7eb; border-radius: 10px;
	padding: 16px 18px; margin: 8px 0;
}
.case-display *, .overlap-card * { color: inherit !important; }

.overlap-card { border-left: 4px solid #9ca3af; }
.overlap-low { border-left-color: #16a34a; }
.overlap-medium { border-left-color: #d97706; }
.overlap-high { border-left-color: #dc2626; }

.result-tabs .tab-nav { border-bottom: 1px solid #e5e7eb; }

.demo-banner {
	background: #fffbeb; color: #92400e; border: 1px solid #fde68a;
	border-radius: 10px; padding: 10px 16px; margin-bottom: 12px; text-align: center;
}
.demo-banner * { color: inherit !important; }
"""


def create_interface():
	"""Create and configure the Gradio interface."""

	with gr.Blocks(
		title="Devil's Advocate Multi-Agent Medical Analysis System",
		theme=gr.themes.Soft(primary_hue="indigo", neutral_hue="slate", radius_size="lg"),
		css=_CSS,
	) as interface:

		gr.Markdown("# 🏥 Devil's Advocate", elem_id="title")
		gr.Markdown(
			"Agent 1 sees the full case. Agent 2 diagnoses blind to past history, then rates the overlap. "
			"Agent 3 synthesizes both.",
			elem_id="subtitle",
		)
		demo_banner = gr.Markdown(visible=False, elem_classes=["demo-banner"])

		with gr.Row():
			with gr.Column(scale=1):
				case_dropdown = gr.Dropdown(
					choices=[NO_CASE] + list(get_case_titles().keys()),
					label="Sample Case",
					value=NO_CASE,
				)
				custom_case = gr.Textbox(
					label="Or paste a custom case",
					placeholder="Symptoms, history, exam findings...",
					lines=6,
				)
				with gr.Row():
					analyze_btn = gr.Button("Run Analysis", variant="primary")
					clear_btn = gr.Button("Clear", variant="secondary")

			with gr.Column(scale=2):
				case_display = gr.Markdown(elem_classes=["case-display"])
				overlap_panel = gr.Markdown(elem_classes=["overlap-card"])
				with gr.Tabs(elem_classes=["result-tabs"]):
					with gr.Tab("Agent 1 · Diagnostician"):
						agent1_output = gr.Markdown()
					with gr.Tab("Agent 2 · Devil's Advocate"):
						agent2_output = gr.Markdown()
					with gr.Tab("Agent 3 · Final"):
						agent3_output = gr.Markdown()

		analyze_btn.click(
			fn=analyze_medical_case,
			inputs=[case_dropdown, custom_case],
			outputs=[case_display, agent1_output, agent2_output, agent3_output, overlap_panel, demo_banner],
		)

		clear_btn.click(
			fn=clear_analysis,
			outputs=[case_display, agent1_output, agent2_output, agent3_output, overlap_panel, demo_banner],
		)

		gr.Markdown(
			"<div style='text-align:center;color:#9ca3af;font-size:0.85rem;margin-top:1.5rem;'>"
			"For education only, not clinical advice.</div>"
		)

	return interface


if __name__ == "__main__":
	interface = create_interface()
	interface.launch(server_name="0.0.0.0", server_port=7860, share=False, show_error=True, quiet=False)
