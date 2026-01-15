# app.py - Medical Professional Marketing Strategy Tool

import streamlit as st
import urllib.parse

# Page configuration
st.set_page_config(
    page_title="Medical Professional Marketing Strategy Tool",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .medical-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
        transition: transform 0.3s;
    }
    .medical-card:hover {
        transform: translateY(-5px);
    }
    .priority-high {
        background-color: #10b981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .priority-medium {
        background-color: #f59e0b;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .doctor-specialty {
        background-color: #3b82f6;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        display: inline-block;
        margin: 0.25rem;
    }
    .brand-strategy-box {
        background-color: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
    }
    .stProgress > div > div > div > div {
        background-color: #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = 'Doctor Marketing Strategy'
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'specialty' not in st.session_state:
    st.session_state.specialty = None
if 'years_experience' not in st.session_state:
    st.session_state.years_experience = None
if 'practice_type' not in st.session_state:
    st.session_state.practice_type = None
if 'patient_types' not in st.session_state:
    st.session_state.patient_types = []
if 'services_offered' not in st.session_state:
    st.session_state.services_offered = []
if 'competitive_positioning' not in st.session_state:
    st.session_state.competitive_positioning = {}
if 'marketing_focus' not in st.session_state:
    st.session_state.marketing_focus = None
if 'selected_strategies' not in st.session_state:
    st.session_state.selected_strategies = []

# Data Definitions

# Medical Specialties
MEDICAL_SPECIALTIES = {
    'cardiology': {
        'name': 'Cardiology',
        'desc': 'Heart and cardiovascular system specialists',
        'color': '#ef4444',
        'procedures': ['CAG', 'PTCA', 'Angioplasty', 'Pacemaker', 'Echocardiography'],
        'marketing_focus': ['Heart health education', 'Preventive cardiology', 'Advanced cardiac care']
    },
    'general_practice': {
        'name': 'General Practice',
        'desc': 'Primary care and family medicine',
        'color': '#3b82f6',
        'procedures': ['General Consultation', 'Health Checkup', 'Vaccination'],
        'marketing_focus': ['Family health', 'Preventive care', 'Holistic wellness']
    },
    'family_medicine': {
        'name': 'Family Medicine',
        'desc': 'Comprehensive healthcare for all ages',
        'color': '#8b5cf6',
        'procedures': ['Preventive Care', 'Chronic Disease Management', 'Family Planning'],
        'marketing_focus': ['Multi-generational care', 'Long-term health partnerships', 'Preventive medicine']
    },
    'internal_medicine': {
        'name': 'Internal Medicine',
        'desc': 'Adult medicine and complex diagnoses',
        'color': '#10b981',
        'procedures': ['Diagnostic Procedures', 'Chronic Disease Management', 'Hospital Care'],
        'marketing_focus': ['Complex case management', 'Adult healthcare', 'Hospital medicine']
    },
    'neurology': {
        'name': 'Neurology',
        'desc': 'Brain and nervous system disorders',
        'color': '#f59e0b',
        'procedures': ['EEG', 'EMG', 'Nerve Conduction Studies', 'Botulinum Toxin Therapy'],
        'marketing_focus': ['Brain health', 'Neurological disorders', 'Advanced diagnostics']
    },
    'gastroenterology': {
        'name': 'Gastroenterology',
        'desc': 'Digestive system and gastrointestinal disorders',
        'color': '#ec4899',
        'procedures': ['Endoscopy', 'Colonoscopy', 'ERCP', 'Liver Biopsy'],
        'marketing_focus': ['Digestive health', 'Preventive screening', 'Advanced endoscopy']
    },
    'pulmonology': {
        'name': 'Pulmonology',
        'desc': 'Respiratory system and lung disorders',
        'color': '#6366f1',
        'procedures': ['Bronchoscopy', 'PFT', 'Sleep Studies', 'Thoracentesis'],
        'marketing_focus': ['Respiratory health', 'Sleep medicine', 'Lung cancer screening']
    },
    'orthopedics': {
        'name': 'Orthopedics',
        'desc': 'Musculoskeletal system and joints',
        'color': '#f97316',
        'procedures': ['Arthroscopy', 'Joint Replacement', 'Fracture Management'],
        'marketing_focus': ['Joint health', 'Sports medicine', 'Pain management']
    },
    'pediatrics': {
        'name': 'Pediatrics',
        'desc': 'Healthcare for infants, children, and adolescents',
        'color': '#06b6d4',
        'procedures': ['Vaccination', 'Growth Monitoring', 'Developmental Assessment'],
        'marketing_focus': ['Child health', 'Vaccination awareness', 'Developmental care']
    },
    'obstetrics_gynecology': {
        'name': 'Obstetrics & Gynecology',
        'desc': "Women's health and reproductive system",
        'color': '#8b5cf6',
        'procedures': ['Delivery', 'Pap Smear', 'Hysteroscopy', 'Laparoscopy'],
        'marketing_focus': ["Women's health", 'Maternal care', 'Reproductive wellness']
    },
    'dermatology': {
        'name': 'Dermatology',
        'desc': 'Skin, hair, and nail disorders',
        'color': '#f59e0b',
        'procedures': ['Skin Biopsy', 'Laser Therapy', 'Chemical Peels', 'Cryotherapy'],
        'marketing_focus': ['Skin health', 'Cosmetic dermatology', 'Skin cancer prevention']
    },
    'psychiatry': {
        'name': 'Psychiatry',
        'desc': 'Mental health and behavioral disorders',
        'color': '#10b981',
        'procedures': ['Psychotherapy', 'Medication Management', 'ECT'],
        'marketing_focus': ['Mental wellness', 'Stress management', 'Therapeutic care']
    }
}

# Years of Experience
YEARS_EXPERIENCE = ['0-5 years', '6-10 years', '11-15 years', '16-20 years', '>20 years']

# Practice Types
PRACTICE_TYPES = {
    'individual_clinic': {
        'name': 'Individual Clinic (with basic diagnostics)',
        'desc': 'Solo practice with basic lab/ECG/PFT facilities',
        'scale': 'Small',
        'marketing_needs': 'Local reputation, patient referrals',
        'marketing_budget': '5-10% of revenue',
        'team_needs': 'Front desk + basic marketing'
    },
    'group_practice': {
        'name': 'Group Clinical Practice',
        'desc': 'Partnership with other doctors, shared facilities',
        'scale': 'Medium',
        'marketing_needs': 'Group branding, cross-referrals',
        'marketing_budget': '8-12% of revenue',
        'team_needs': 'Marketing coordinator + reception'
    },
    'nursing_home': {
        'name': 'Nursing Home/Aged Care Facility',
        'desc': 'Associated with long-term care facility',
        'scale': 'Medium',
        'marketing_needs': 'Family trust, institutional credibility',
        'marketing_budget': '6-10% of revenue',
        'team_needs': 'Relationship manager + admin'
    },
    'multi_specialty_hospital': {
        'name': 'Multi-Specialty Hospital',
        'desc': 'Part of larger hospital with multiple departments',
        'scale': 'Large',
        'marketing_needs': 'Hospital reputation, inter-departmental referrals',
        'marketing_budget': '10-15% of revenue',
        'team_needs': 'Marketing team + coordinators'
    },
    'super_specialty_hospital': {
        'name': 'Super Specialty Hospital',
        'desc': 'Advanced specialized care facility',
        'scale': 'Large',
        'marketing_needs': 'Expert positioning, complex case referrals',
        'marketing_budget': '12-18% of revenue',
        'team_needs': 'Specialized marketing + PR'
    },
    'standalone_hospital': {
        'name': 'Standalone Hospital',
        'desc': 'Independent hospital with full facilities',
        'scale': 'Large',
        'marketing_needs': 'Comprehensive care reputation, emergency services',
        'marketing_budget': '10-16% of revenue',
        'team_needs': 'Full marketing department'
    },
    'corporate_chain': {
        'name': 'Corporate Hospital Chain',
        'desc': 'Part of national/international healthcare chain',
        'scale': 'Very Large',
        'marketing_needs': 'Brand association, standardized care reputation',
        'marketing_budget': '15-20% of revenue',
        'team_needs': 'Corporate marketing team'
    }
}

# Patient Types
PATIENT_TYPES = {
    'surgical': {
        'name': 'Surgical Patients',
        'desc': 'Requiring operative procedures',
        'services': ['Pre-op Consultation', 'Surgery', 'Post-op Care', 'Follow-up'],
        'marketing_channels': ['Surgeon referrals', 'Hospital partnerships', 'Specialized websites']
    },
    'icu': {
        'name': 'ICU/Critical Care',
        'desc': 'Critically ill patients requiring intensive monitoring',
        'services': ['Critical Care', 'Ventilator Management', 'Hemodynamic Monitoring'],
        'marketing_channels': ['Hospital referrals', 'Emergency services', 'Ambulance services']
    },
    'ward_ipd': {
        'name': 'Ward IPD',
        'desc': 'Inpatient department admissions',
        'services': ['Hospital Admission', 'Daily Rounds', 'Discharge Planning'],
        'marketing_channels': ['GP referrals', 'Insurance tie-ups', 'Corporate health programs']
    },
    'daycare_surgery': {
        'name': 'Daycare Surgical Procedures',
        'desc': 'Minor surgeries without overnight stay',
        'services': ['Minor Surgeries', 'Pain Management', 'Same-day Discharge'],
        'marketing_channels': ['Direct marketing', 'Online booking', 'Health insurance']
    },
    'daycare_medical': {
        'name': 'Daycare Medical Procedures',
        'desc': 'Medical procedures without admission',
        'services': ['Chemotherapy', 'Dialysis', 'Blood Transfusions'],
        'marketing_channels': ['Specialist referrals', 'Support groups', 'Medical associations']
    },
    'specialty_procedures': {
        'name': 'Specialty Procedures',
        'desc': 'Advanced specialized interventions',
        'services': ['CAG', 'PTCA', 'Endoscopy', 'Colonoscopy', 'Advanced Imaging'],
        'marketing_channels': ['Doctor referrals', 'Academic conferences', 'Research publications']
    },
    'opd': {
        'name': 'OPD/Outpatient',
        'desc': 'Outpatient consultations and follow-ups',
        'services': ['Consultations', 'Prescriptions', 'Basic Procedures', 'Follow-ups'],
        'marketing_channels': ['Online platforms', 'Local advertising', 'Patient referrals']
    },
    'emergency': {
        'name': 'Emergency Care',
        'desc': 'Acute/urgent medical attention',
        'services': ['Emergency Consultation', 'Trauma Care', 'Acute Management'],
        'marketing_channels': ['Ambulance services', 'Hospital networks', 'Community awareness']
    }
}

# Diagnostic Facilities
DIAGNOSTIC_FACILITIES = {
    'ecg': 'ECG Machine',
    'tmt': 'Treadmill Test (TMT)',
    'pft': 'Pulmonary Function Test (PFT)',
    'xray': 'X-ray Facility',
    'usg': 'Ultrasound (USG)',
    'lab': 'Basic Laboratory',
    'advanced_lab': 'Advanced Laboratory',
    'ct': 'CT Scan',
    'mri': 'MRI',
    'endoscopy': 'Endoscopy Unit',
    'holter': 'Holter Monitoring',
    'eeg': 'EEG Machine',
    'emg': 'EMG/NCS'
}

# Competitive Positioning Factors
COMPETITIVE_FACTORS = {
    'expertise': {
        'name': 'Clinical Expertise & Outcomes',
        'aspects': ['Success Rates', 'Complication Rates', 'Patient Recovery'],
        'improvement_strategies': ['Continuous education', 'Case audits', 'Peer reviews']
    },
    'technology': {
        'name': 'Technology & Equipment',
        'aspects': ['Latest Equipment', 'Digital Records', 'Telemedicine'],
        'improvement_strategies': ['Technology upgrades', 'Digital integration', 'Remote monitoring']
    },
    'patient_experience': {
        'name': 'Patient Experience',
        'aspects': ['Waiting Time', 'Staff Behavior', 'Comfort Facilities'],
        'improvement_strategies': ['Process optimization', 'Staff training', 'Facility upgrades']
    },
    'cost': {
        'name': 'Cost & Insurance',
        'aspects': ['Pricing Transparency', 'Insurance Acceptance', 'Payment Options'],
        'improvement_strategies': ['Insurance partnerships', 'Payment plans', 'Cost breakdowns']
    },
    'accessibility': {
        'name': 'Accessibility',
        'aspects': ['Location', 'Timings', 'Emergency Availability'],
        'improvement_strategies': ['Extended hours', 'Multiple locations', 'Emergency services']
    },
    'reputation': {
        'name': 'Reputation & Trust',
        'aspects': ['Years in Practice', 'Patient Reviews', 'Awards & Recognition'],
        'improvement_strategies': ['Review management', 'Award applications', 'Testimonial collection']
    }
}

# Marketing Focus Areas
MARKETING_FOCUS_AREAS = {
    'new_patients': {
        'name': 'Acquiring New Patients',
        'key_metrics': ['New patient appointments', 'Website inquiries', 'Call volume'],
        'strategies': ['Digital marketing', 'Health camps', 'Referral programs']
    },
    'patient_retention': {
        'name': 'Retaining Existing Patients',
        'key_metrics': ['Patient satisfaction', 'Repeat visits', 'Follow-up rate'],
        'strategies': ['Loyalty programs', 'Patient education', 'Regular follow-ups']
    },
    'referral_volume': {
        'name': 'Increasing Referrals',
        'key_metrics': ['Referral numbers', 'Referring doctor satisfaction', 'Conversion rate'],
        'strategies': ['Doctor networking', 'Case discussions', 'Referral incentives']
    },
    'premium_services': {
        'name': 'Premium Service Promotion',
        'key_metrics': ['Premium service revenue', 'VIP patient count', 'Service utilization'],
        'strategies': ['Concierge services', 'Health packages', 'Exclusive programs']
    },
    'expert_positioning': {
        'name': 'Expert Positioning in Specialty',
        'key_metrics': ['Complex cases', 'Research publications', 'Conference invitations'],
        'strategies': ['Academic publishing', 'Speaking engagements', 'Specialized training']
    },
    'institutional_reputation': {
        'name': 'Building Institutional Reputation',
        'key_metrics': ['Brand recognition', 'Media mentions', 'Accreditations'],
        'strategies': ['Quality certifications', 'Community programs', 'Media relations']
    }
}

# Brand Building Strategies
BRAND_STRATEGIES = {
    'digital_presence': {
        'name': 'Digital Presence & Online Reputation',
        'focus': 'Both',
        'time': 'Short-term',
        'budget': 'Low-Moderate',
        'resources': [
            {'name': 'Professional Website', 'tools': ['WordPress', 'Wix', 'Squarespace'], 'desc': 'Create a professional doctor website', 'cost': '$$'},
            {'name': 'Social Media Management', 'tools': ['Canva', 'Hootsuite', 'Buffer'], 'desc': 'Regular health content posting', 'cost': '$'},
            {'name': 'Google My Business', 'tools': ['Google', 'Review management tools'], 'desc': 'Local search optimization', 'cost': 'Free'},
            {'name': 'Patient Review System', 'tools': ['Practo', 'Lybrate', 'Google Reviews'], 'desc': 'Collect and manage patient reviews', 'cost': '$$'}
        ]
    },
    'content_marketing': {
        'name': 'Health Content Marketing',
        'focus': 'Patient Education',
        'time': 'Medium-term',
        'budget': 'Moderate',
        'resources': [
            {'name': 'Health Blog', 'tools': ['Medium', 'WordPress', 'LinkedIn'], 'desc': 'Regular health articles', 'cost': '$'},
            {'name': 'Patient Education Videos', 'tools': ['Canva Video', 'InVideo', 'YouTube'], 'desc': 'Educational video content', 'cost': '$$'},
            {'name': 'Health Newsletters', 'tools': ['Mailchimp', 'ConvertKit', 'Sendinblue'], 'desc': 'Monthly patient newsletters', 'cost': '$'},
            {'name': 'Infographics', 'tools': ['Canva', 'Visme', 'Adobe Express'], 'desc': 'Visual health information', 'cost': '$'}
        ]
    },
    'patient_relationship': {
        'name': 'Patient Relationship Management',
        'focus': 'Patient Retention',
        'time': 'Long-term',
        'budget': 'Moderate',
        'resources': [
            {'name': 'Appointment System', 'tools': ['Calendly', 'Zocdoc', 'Practo'], 'desc': 'Online appointment booking', 'cost': '$$'},
            {'name': 'Follow-up Automation', 'tools': ['WhatsApp Business', 'CRM software', 'Excel'], 'desc': 'Automated patient follow-ups', 'cost': '$'},
            {'name': 'Patient Feedback System', 'tools': ['Google Forms', 'SurveyMonkey', 'Typeform'], 'desc': 'Patient satisfaction surveys', 'cost': 'Free'},
            {'name': 'Health Records Portal', 'tools': ['Electronic Health Records', 'Patient portals'], 'desc': 'Digital health records access', 'cost': '$$$'}
        ]
    },
    'referral_network': {
        'name': 'Referral Network Building',
        'focus': 'Professional',
        'time': 'Long-term',
        'budget': 'Moderate',
        'resources': [
            {'name': 'Doctor Networking', 'tools': ['LinkedIn', 'Medical conferences', 'Local associations'], 'desc': 'Build professional network', 'cost': '$$'},
            {'name': 'Hospital Partnerships', 'tools': ['Professional visits', 'Joint workshops', 'Case discussions'], 'desc': 'Institutional referrals', 'cost': '$$'},
            {'name': 'GP Network Development', 'tools': ['Regular meetings', 'Educational sessions', 'Referral forms'], 'desc': 'Primary care referrals', 'cost': '$'},
            {'name': 'Specialist Collaboration', 'tools': ['Multi-specialty meetings', 'Joint clinics', 'Teleconsultation'], 'desc': 'Cross-specialty referrals', 'cost': '$$'}
        ]
    },
    'community_outreach': {
        'name': 'Community Outreach Programs',
        'focus': 'Community',
        'time': 'Medium-term',
        'budget': 'Low-Moderate',
        'resources': [
            {'name': 'Health Camps', 'tools': ['Local partnerships', 'Volunteer networks', 'Basic equipment'], 'desc': 'Free health checkup camps', 'cost': '$$'},
            {'name': 'Public Health Talks', 'tools': ['Schools', 'Corporate offices', 'Community centers'], 'desc': 'Health education sessions', 'cost': '$'},
            {'name': 'Media Appearances', 'tools': ['Local TV', 'Radio', 'Newspaper columns'], 'desc': 'Health expert appearances', 'cost': 'Free'},
            {'name': 'Health Awareness Campaigns', 'tools': ['Social media campaigns', 'Posters', 'Brochures'], 'desc': 'Disease awareness programs', 'cost': '$$'}
        ]
    },
    'academic_presence': {
        'name': 'Academic & Research Presence',
        'focus': 'Professional Reputation',
        'time': 'Long-term',
        'budget': 'High',
        'resources': [
            {'name': 'Research Publications', 'tools': ['PubMed journals', 'ResearchGate', 'ORCID'], 'desc': 'Medical research papers', 'cost': '$$$'},
            {'name': 'Conference Presentations', 'tools': ['Medical conferences', 'Workshops', 'CME programs'], 'desc': 'Present research findings', 'cost': '$$$'},
            {'name': 'Teaching Appointments', 'tools': ['Medical colleges', 'Training programs', 'Guest lectures'], 'desc': 'Academic teaching roles', 'cost': '$$'},
            {'name': 'Clinical Trials', 'tools': ['Research institutions', 'Pharma co
