"""
Sample Medical Cases for Devil's Advocate Multi-Agent System Demo

These cases are designed to demonstrate different types of diagnostic bias:
1. Anchoring bias - focusing on first symptoms
2. Confirmation bias - overemphasizing previous conditions
3. Availability bias - overweighting recent conditions
4. Overconfidence bias - making definitive diagnoses too quickly
"""

SAMPLE_CASES = {
    "case_1": {
        "title": "Resolved Appendicitis with New Symptoms",
        "description": """Patient: 32-year-old male
Chief Complaint: Abdominal pain and nausea for 2 days

History of Present Illness:
- Patient reports sharp, intermittent abdominal pain starting 2 days ago
- Pain is localized to right lower quadrant initially, now more diffuse
- Associated with nausea and decreased appetite
- No vomiting, fever, or changes in bowel movements

Past Medical History:
- Appendectomy 3 years ago (successful, no complications)
- No other significant medical history

Physical Examination:
- Vital signs: BP 120/80, HR 88, Temp 98.6°F, RR 16
- Abdomen: Soft, non-tender, no rebound tenderness
- No masses or organomegaly
- Bowel sounds present and normal

This case demonstrates anchoring bias - the diagnostician may focus on the right lower quadrant pain and appendectomy history, potentially missing other causes of abdominal pain.""",
        
        "bias_type": "Anchoring bias, Confirmation bias",
        "expected_bias": "Focusing on right lower quadrant pain and appendectomy history, potentially missing other abdominal pain causes"
    },
    
    "case_2": {
        "title": "Previous Heart Condition with Current Respiratory Issues",
        "description": """Patient: 68-year-old female
Chief Complaint: Shortness of breath and chest tightness for 1 week

History of Present Illness:
- Progressive shortness of breath over 1 week
- Chest tightness, worse with deep breathing
- No chest pain, no radiation to arms
- Associated with dry cough and fatigue
- Symptoms worse at night and with exertion

Past Medical History:
- Myocardial infarction 2 years ago (successful stent placement)
- Hypertension (well-controlled on medication)
- Type 2 diabetes (diet-controlled)

Physical Examination:
- Vital signs: BP 135/85, HR 72, Temp 98.2°F, RR 20, O2 sat 94%
- Cardiovascular: Regular rate and rhythm, no murmurs, no edema
- Respiratory: Decreased breath sounds in right lower lobe, no wheezing
- No jugular venous distension

This case demonstrates confirmation bias - the diagnostician may overemphasize cardiac causes due to previous MI, potentially missing respiratory conditions.""",
        
        "bias_type": "Confirmation bias, Availability bias",
        "expected_bias": "Overemphasizing cardiac causes due to previous MI, potentially missing respiratory conditions like pneumonia or pleural effusion"
    },
    
    "case_3": {
        "title": "Resolved Infection with Persistent Symptoms",
        "description": """Patient: 45-year-old female
Chief Complaint: Fatigue and joint pain for 3 weeks

History of Present Illness:
- Patient reports persistent fatigue and generalized joint pain
- Symptoms started 3 weeks ago during a viral upper respiratory infection
- URI symptoms resolved within 1 week, but fatigue and joint pain persist
- No fever, no rash, no morning stiffness
- Pain affects multiple joints (knees, wrists, shoulders)

Past Medical History:
- Streptococcal pharyngitis 6 months ago (treated with antibiotics)
- Seasonal allergies (well-controlled)
- No chronic medical conditions

Physical Examination:
- Vital signs: BP 118/75, HR 76, Temp 98.4°F, RR 16
- General: Alert, oriented, no acute distress
- Musculoskeletal: Full range of motion in all joints, no swelling or erythema
- No lymphadenopathy, no hepatosplenomegaly
- Skin: No rashes or lesions

This case demonstrates availability bias - the diagnostician may focus on the recent URI and previous strep infection, potentially missing other causes of fatigue and joint pain.""",
        
        "bias_type": "Availability bias, Overconfidence bias",
        "expected_bias": "Focusing on recent URI and previous strep infection, potentially missing other causes like post-viral syndrome, autoimmune conditions, or depression"
    },
    
    "case_4": {
        "title": "Chronic Condition with Acute Exacerbation",
        "description": """Patient: 55-year-old male
Chief Complaint: Worsening back pain for 1 month

History of Present Illness:
- Patient reports severe lower back pain for 1 month
- Pain radiates down right leg to foot
- Associated with numbness and tingling in right foot
- No bowel or bladder dysfunction
- Pain worse with standing and walking, better with lying down

Past Medical History:
- Chronic low back pain for 10 years (diagnosed as degenerative disc disease)
- Hypertension (well-controlled)
- No previous surgeries

Physical Examination:
- Vital signs: BP 140/90, HR 82, Temp 98.6°F, RR 16
- Musculoskeletal: Decreased range of motion in lumbar spine
- Neurological: Decreased sensation in right L5 dermatome
- Positive straight leg raise test on right side
- No motor weakness

This case demonstrates anchoring bias - the diagnostician may focus on the chronic back pain diagnosis and miss acute changes like disc herniation or spinal stenosis.""",
        
        "bias_type": "Anchoring bias, Overconfidence bias",
        "expected_bias": "Focusing on chronic back pain diagnosis and missing acute changes like disc herniation, spinal stenosis, or cauda equina syndrome"
    }
}

def get_case_by_id(case_id):
    """Get a specific case by its ID."""
    return SAMPLE_CASES.get(case_id, None)

def get_all_cases():
    """Get all available sample cases."""
    return SAMPLE_CASES

def get_case_titles():
    """Get a list of case titles for the UI dropdown."""
    return {case_id: case_data["title"] for case_id, case_data in SAMPLE_CASES.items()}

def get_case_description(case_id):
    """Get the description of a specific case."""
    case = get_case_by_id(case_id)
    return case["description"] if case else "Case not found"

def get_bias_analysis(case_id):
    """Get the bias analysis for a specific case."""
    case = get_case_by_id(case_id)
    if case:
        return {
            "bias_type": case["bias_type"],
            "expected_bias": case["expected_bias"]
        }
    return None
