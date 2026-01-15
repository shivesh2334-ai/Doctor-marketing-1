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
            {'name': 'Clinical Trials', 'tools': ['Research institutions', 'Pharma companies', 'Ethics boards'], 'desc': 'Participate in clinical research', 'cost': '$$$$'}
        ]
    },
    'specialized_certifications': {
        'name': 'Specialized Certifications & Training',
        'focus': 'Expert Positioning',
        'time': 'Long-term',
        'budget': 'High',
        'resources': [
            {'name': 'Advanced Certifications', 'tools': ['International boards', 'Specialty certifications', 'Fellowships'], 'desc': 'Advanced qualifications', 'cost': '$$$$'},
            {'name': 'Skill Workshops', 'tools': ['Medical workshops', 'Hands-on training', 'Simulation labs'], 'desc': 'New procedure training', 'cost': '$$$'},
            {'name': 'Quality Accreditations', 'tools': ['NABH', 'ISO', 'Hospital standards'], 'desc': 'Clinic/hospital accreditations', 'cost': '$$$$'},
            {'name': 'International Training', 'tools': ['Overseas fellowships', 'International conferences', 'Global certifications'], 'desc': 'International exposure', 'cost': '$$$$$'}
        ]
    },
    'premium_services': {
        'name': 'Premium & Concierge Services',
        'focus': 'High-value Patients',
        'time': 'Medium-term',
        'budget': 'High',
        'resources': [
            {'name': 'Concierge Medicine', 'tools': ['VIP services', '24/7 availability', 'Home visits'], 'desc': 'Premium practice model', 'cost': '$$$$'},
            {'name': 'Health Packages', 'tools': ['Comprehensive checkups', 'Preventive packages', 'Corporate health'], 'desc': 'Packaged services', 'cost': '$$'},
            {'name': 'International Patient Services', 'tools': ['Medical tourism', 'Multilingual staff', 'Travel arrangements'], 'desc': 'International patients', 'cost': '$$$'},
            {'name': 'Executive Health Programs', 'tools': ['Corporate partnerships', 'Executive checkups', 'Wellness programs'], 'desc': 'Corporate executive health', 'cost': '$$$'}
        ]
    }
}

# Helper Functions
def get_experience_based_strategy():
    experience = st.session_state.years_experience
    if not experience:
        return {}
    
    strategies = {
        '0-5 years': {
            'focus': 'Establishing credibility and building initial patient base',
            'key_actions': [
                'Network with senior doctors for referrals',
                'Build strong online presence with patient reviews',
                'Offer competitive pricing to attract initial patients',
                'Participate in local health camps and community events'
            ],
            'branding_priorities': ['Professional website', 'Patient testimonials', 'Local SEO'],
            'budget_allocation': '70% digital marketing, 30% community outreach'
        },
        '6-10 years': {
            'focus': 'Expanding practice and establishing specialization',
            'key_actions': [
                'Develop niche specialization within field',
                'Build systematic referral networks',
                'Enhance patient experience with technology',
                'Start academic contributions through publications'
            ],
            'branding_priorities': ['Specialization branding', 'Patient referral system', 'Advanced certifications'],
            'budget_allocation': '50% specialization marketing, 30% patient retention, 20% professional development'
        },
        '11-15 years': {
            'focus': 'Leadership positioning and practice expansion',
            'key_actions': [
                'Mentor junior doctors and build team',
                'Increase academic involvement and speaking engagements',
                'Diversify practice with premium services',
                'Develop standardized patient care protocols'
            ],
            'branding_priorities': ['Thought leadership', 'Team branding', 'Premium services'],
            'budget_allocation': '40% team building, 30% premium services, 30% academic presence'
        },
        '16-20 years': {
            'focus': 'Legacy building and practice succession',
            'key_actions': [
                'Develop junior partners for practice succession',
                'Systematize practice operations',
                'Increase community leadership roles',
                'Focus on complex and interesting cases'
            ],
            'branding_priorities': ['Institutional reputation', 'Succession planning', 'Complex case branding'],
            'budget_allocation': '50% institutional branding, 30% team development, 20% community impact'
        },
        '>20 years': {
            'focus': 'Thought leadership and lasting legacy',
            'key_actions': [
                'Publish expertise through books and papers',
                'Take industry leadership positions',
                'Focus on philanthropy and social contribution',
                'Develop training programs for next generation'
            ],
            'branding_priorities': ['Industry influence', 'Philanthropy branding', 'Training center establishment'],
            'budget_allocation': '40% industry leadership, 30% social impact, 30% training programs'
        }
    }
    return strategies.get(experience, {})

def get_specialty_based_recommendations():
    specialty = st.session_state.specialty
    if not specialty:
        return {}
    
    spec_data = MEDICAL_SPECIALTIES.get(specialty, {})
    
    recommendations = {
        'digital_content_types': [],
        'networking_groups': [],
        'patient_education_topics': [],
        'brand_differentiators': [],
        'referral_sources': []
    }
    
    if specialty == 'cardiology':
        recommendations['digital_content_types'] = ['Heart health tips', 'Exercise ECG explanations', 'Cholesterol management videos']
        recommendations['networking_groups'] = ['Cardiology associations', 'General physicians', 'Hospital ER departments', 'Diabetologists']
        recommendations['patient_education_topics'] = ['Blood pressure management', 'Heart attack prevention', 'Medication adherence']
        recommendations['brand_differentiators'] = ['24/7 cardiac emergency access', 'Advanced cardiac imaging', 'Comprehensive rehabilitation']
        recommendations['referral_sources'] = ['General physicians', 'Diabetologists', 'Corporate wellness programs', 'Fitness centers']
    
    elif specialty == 'general_practice':
        recommendations['digital_content_types'] = ['Seasonal health tips', 'Vaccination schedules', 'Common illness management']
        recommendations['networking_groups'] = ['Local community groups', 'Schools', 'Corporate HR departments', 'Senior citizen groups']
        recommendations['patient_education_topics'] = ['Preventive health screenings', 'Lifestyle modifications', 'Mental wellness']
        recommendations['brand_differentiators'] = ['Family-friendly approach', 'Extended hours', 'Home visits', 'Telemedicine options']
        recommendations['referral_sources'] = ['Family networks', 'Local businesses', 'Schools', 'Community centers']
    
    elif specialty == 'neurology':
        recommendations['digital_content_types'] = ['Brain health information', 'Migraine management tips', 'Neurological examination explanations']
        recommendations['networking_groups'] = ['Neurology associations', 'Rehabilitation centers', 'Psychiatrists', 'Physiotherapists']
        recommendations['patient_education_topics'] = ['Stroke prevention', 'Headache management', 'Sleep disorder information']
        recommendations['brand_differentiators'] = ['Advanced neurodiagnostics', 'Multidisciplinary approach', 'Research participation']
        recommendations['referral_sources'] = ['General physicians', 'Physiotherapists', 'Psychiatrists', 'Rehabilitation centers']
    
    elif specialty == 'gastroenterology':
        recommendations['digital_content_types'] = ['Gut health information', 'Dietary recommendations', 'Endoscopy procedure explanations']
        recommendations['networking_groups'] = ['Gastroenterology societies', 'Nutritionists', 'Oncologists', 'General surgeons']
        recommendations['patient_education_topics'] = ['Irritable bowel management', 'Liver health', 'Colon cancer screening']
        recommendations['brand_differentiators'] = ['Advanced endoscopic procedures', 'Motility studies', 'Nutritional counseling']
        recommendations['referral_sources'] = ['General physicians', 'Oncologists', 'Nutritionists', 'Corporate wellness programs']
    
    return recommendations

def get_practice_type_recommendations():
    practice = st.session_state.practice_type
    if not practice:
        return {}
    
    practice_data = PRACTICE_TYPES.get(practice, {})
    
    recommendations = {
        'marketing_channels': [],
        'team_structure': [],
        'technology_needs': [],
        'partnership_opportunities': []
    }
    
    scale = practice_data.get('scale', '')
    
    if scale == 'Small':
        recommendations['marketing_channels'] = ['Local SEO', 'Google My Business', 'Community newspapers', 'Local health camps']
        recommendations['team_structure'] = ['Receptionist with basic marketing skills', 'Part-time social media manager', 'Billing assistant']
        recommendations['technology_needs'] = ['Basic website', 'Appointment software', 'Electronic medical records', 'Payment gateway']
        recommendations['partnership_opportunities'] = ['Local pharmacies', 'Gymnasiums', 'Community centers', 'Local corporations']
    
    elif scale == 'Medium':
        recommendations['marketing_channels'] = ['Digital marketing mix', 'Local TV/radio', 'Health magazines', 'Corporate tie-ups']
        recommendations['team_structure'] = ['Dedicated reception staff', 'Marketing coordinator', 'Patient relationship manager']
        recommendations['technology_needs'] = ['Advanced website with booking', 'CRM system', 'Telemedicine platform', 'Analytics tools']
        recommendations['partnership_opportunities'] = ['Insurance companies', 'Corporate HR departments', 'Other specialist clinics', 'Diagnostic centers']
    
    elif scale == 'Large':
        recommendations['marketing_channels'] = ['Comprehensive digital strategy', 'TV commercials', 'National publications', 'Medical tourism portals']
        recommendations['team_structure'] = ['Full marketing team', 'PR manager', 'Digital marketing specialists', 'Patient experience team']
        recommendations['technology_needs'] = ['Enterprise software', 'Advanced analytics', 'Mobile apps', 'AI integration']
        recommendations['partnership_opportunities'] = ['International hospitals', 'Medical device companies', 'Research institutions', 'Government programs']
    
    elif scale == 'Very Large':
        recommendations['marketing_channels'] = ['Brand campaigns', 'International marketing', 'Research publications', 'Industry conferences']
        recommendations['team_structure'] = ['Corporate marketing department', 'Brand managers', 'International marketing team', 'Research coordinators']
        recommendations['technology_needs'] = ['Global systems', 'Advanced data analytics', 'International telemedicine', 'Research databases']
        recommendations['partnership_opportunities'] = ['Global health organizations', 'International universities', 'Pharmaceutical companies', 'Government health departments']
    
    return recommendations

def generate_comprehensive_strategy():
    strategy = {
        'personal_branding': [],
        'patient_acquisition': [],
        'patient_retention': [],
        'professional_development': [],
        'reputation_management': [],
        'financial_planning': []
    }
    
    # Experience-based strategies
    exp_strategy = get_experience_based_strategy()
    if exp_strategy:
        strategy['personal_branding'].extend(exp_strategy.get('branding_priorities', []))
    
    # Specialty-based recommendations
    spec_rec = get_specialty_based_recommendations()
    if spec_rec:
        strategy['patient_acquisition'].extend(spec_rec.get('referral_sources', []))
        strategy['reputation_management'].extend(spec_rec.get('brand_differentiators', []))
    
    # Practice type recommendations
    practice_rec = get_practice_type_recommendations()
    if practice_rec:
        strategy['professional_development'].extend(practice_rec.get('technology_needs', []))
    
    # Add universal strategies
    strategy['patient_acquisition'].extend([
        'Online appointment booking optimization',
        'Referral incentive program implementation',
        'Health camp participation strategy',
        'Corporate health program development'
    ])
    
    strategy['patient_retention'].extend([
        'Systematic follow-up protocol',
        'Patient education program development',
        'Loyalty benefits for returning patients',
        'Annual health review system'
    ])
    
    strategy['reputation_management'].extend([
        'Quarterly patient feedback collection',
        'Online review management system',
        'Transparent outcome reporting mechanism',
        'Quality accreditation pursuit'
    ])
    
    strategy['financial_planning'].extend([
        'Marketing budget allocation planning',
        'Revenue diversification strategy',
        'Cost optimization analysis',
        'ROI tracking system'
    ])
    
    return strategy

def get_recommended_strategies():
    focus = st.session_state.marketing_focus
    if not focus:
        return []
    
    recommendations = []
    
    for key, strategy in BRAND_STRATEGIES.items():
        score = 0
        reasoning = ''
        
        if focus == 'new_patients':
            if strategy['focus'] in ['Both', 'Patient Education']:
                score = 3
                reasoning = 'Directly attracts new patients through education and awareness building'
        elif focus == 'patient_retention':
            if strategy['name'] == 'Patient Relationship Management':
                score = 3
                reasoning = 'Focuses on retaining existing patients through relationship building'
        elif focus == 'referral_volume':
            if strategy['name'] == 'Referral Network Building':
                score = 3
                reasoning = 'Specifically designed to increase referrals from other professionals'
        elif focus == 'premium_services':
            if strategy['name'] == 'Premium & Concierge Services':
                score = 3
                reasoning = 'Directly promotes and develops premium service offerings'
        elif focus == 'expert_positioning':
            if strategy['name'] in ['Academic & Research Presence', 'Specialized Certifications & Training']:
                score = 3
                reasoning = 'Establishes expertise through credentials and research'
        elif focus == 'institutional_reputation':
            if strategy['focus'] in ['Professional', 'Community']:
                score = 3
                reasoning = 'Builds institutional credibility and community trust'
        
        if score > 0:
            recommendations.append({
                'name': strategy['name'],
                'score': score,
                'reasoning': reasoning,
                'focus': strategy['focus'],
                'time': strategy['time'],
                'budget': strategy['budget'],
                'resources': strategy['resources']
            })
    
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    return recommendations[:6]

def calculate_marketing_budget():
    practice = st.session_state.practice_type
    if not practice:
        return "Not available - select practice type"
    
    practice_data = PRACTICE_TYPES.get(practice, {})
    budget_range = practice_data.get('marketing_budget', 'Not specified')
    
    # Add recommendations based on experience
    exp_strategy = get_experience_based_strategy()
    if exp_strategy:
        budget_allocation = exp_strategy.get('budget_allocation', '')
        return f"{budget_range} - Allocation: {budget_allocation}"
    
    return budget_range

# Sidebar navigation
with st.sidebar:
    st.title("🏥 Navigation")
    st.session_state.app_mode = st.radio(
        "Select Tool:",
        ["Doctor Marketing Strategy", "Brand Building Activities"],
        index=0 if st.session_state.app_mode == "Doctor Marketing Strategy" else 1
    )
    
    st.markdown("---")
    
    # Show current selection summary
    if st.session_state.specialty:
        specialty = MEDICAL_SPECIALTIES[st.session_state.specialty]['name']
        st.info(f"**Specialty:** {specialty}")
    
    if st.session_state.years_experience:
        st.info(f"**Experience:** {st.session_state.years_experience}")
    
    st.markdown("---")
    st.markdown("### About")
    st.info("""
    **Doctor Marketing Strategy:**
    6-step framework for medical practice growth
    
    **Brand Building Activities:**
    Specific strategies with implementation tools
    """)

# Main Application Logic
if st.session_state.app_mode == "Doctor Marketing Strategy":
    st.title("🏥 Medical Professional Marketing Strategy Tool")
    st.markdown("*Strategic framework for doctor branding and practice growth*")
    
    # Progress bar - MOVED INSIDE THE CONDITIONAL BLOCK
    progress = (st.session_state.step - 1) / 5
    st.progress(progress)
    
    # Step indicator
    cols = st.columns(6)
    step_names = ['Profile', 'Practice', 'Services', 'Positioning', 'Focus', 'Strategy']
    for i, (col, name) in enumerate(zip(cols, step_names), 1):
        with col:
            if i < st.session_state.step:
                st.markdown(f"**✓ {name}**")
            elif i == st.session_state.step:
                st.markdown(f"**→ {name}**")
            else:
                st.markdown(f"{name}")
    
    st.markdown("---")
    
    # Step 1: Doctor Profile
    if st.session_state.step == 1:
        st.header("Step 1: Medical Professional Profile")
        st.markdown("Define your specialty and experience level")
        
        st.subheader("Medical Specialty")
        cols = st.columns(3)
        specialty_keys = list(MEDICAL_SPECIALTIES.keys())
        
        for i, key in enumerate(specialty_keys):
            specialty = MEDICAL_SPECIALTIES[key]
            with cols[i % 3]:
                button_style = f"""
                <style>
                    div[data-testid="stButton"] button[data-testid="baseButton-secondary"] {{
                        background-color: {specialty['color']}20;
                        border-color: {specialty['color']};
                        color: {specialty['color']};
                    }}
                </style>
                """
                st.markdown(button_style, unsafe_allow_html=True)
                
                if st.button(
                    f"**{specialty['name']}**\n\n{specialty['desc']}",
                    key=f"spec_{key}",
                    use_container_width=True
                ):
                    st.session_state.specialty = key
        
        if st.session_state.specialty:
            specialty = MEDICAL_SPECIALTIES[st.session_state.specialty]
            st.success(f"✓ Selected: {specialty['name']}")
            
            # Show specialty details
            with st.expander("Specialty Details", expanded=True):
                cols = st.columns(2)
                with cols[0]:
                    st.markdown("**Common Procedures:**")
                    for proc in specialty['procedures']:
                        st.markdown(f"- {proc}")
                with cols[1]:
                    st.markdown("**Marketing Focus Areas:**")
                    for focus in specialty['marketing_focus']:
                        st.markdown(f"- {focus}")
        
        st.subheader("Years of Clinical Experience")
        cols = st.columns(5)
        for i, years in enumerate(YEARS_EXPERIENCE):
            with cols[i]:
                if st.button(years, key=f"exp_{years}", use_container_width=True):
                    st.session_state.years_experience = years
        
        if st.session_state.years_experience:
            st.success(f"✓ Selected: {st.session_state.years_experience}")
            exp_strategy = get_experience_based_strategy()
            if exp_strategy:
                st.info(f"**Strategy Focus:** {exp_strategy.get('focus', '')}")
    
    # Step 2: Practice Setup
    elif st.session_state.step == 2:
        st.header("Step 2: Practice Type & Facilities")
        st.markdown("Define your practice setup and available facilities")
        
        st.subheader("Type of Practice")
        cols = st.columns(2)
        practice_keys = list(PRACTICE_TYPES.keys())
        
        for i, key in enumerate(practice_keys):
            practice = PRACTICE_TYPES[key]
            with cols[i % 2]:
                if st.button(
                    f"**{practice['name']}**\n\n*{practice['desc']}*\n\nScale: {practice['scale']}",
                    key=f"practice_{key}",
                    use_container_width=True
                ):
                    st.session_state.practice_type = key
        
        if st.session_state.practice_type:
            practice = PRACTICE_TYPES[st.session_state.practice_type]
            st.success(f"✓ Selected: {practice['name']}")
            
            with st.expander("Practice Details", expanded=True):
                cols = st.columns(2)
                with cols[0]:
                    st.markdown("**Marketing Needs:**")
                    st.markdown(f"- {practice['marketing_needs']}")
                    st.markdown(f"**Recommended Budget:** {practice['marketing_budget']}")
                with cols[1]:
                    st.markdown("**Team Requirements:**")
                    st.markdown(f"- {practice['team_needs']}")
        
        st.subheader("Diagnostic Facilities Available")
        st.markdown("Select all diagnostic facilities in your practice:")
        
        cols = st.columns(4)
        facility_keys = list(DIAGNOSTIC_FACILITIES.keys())
        
        selected_facilities = []
        for i, key in enumerate(facility_keys):
            facility = DIAGNOSTIC_FACILITIES[key]
            with cols[i % 4]:
                if st.checkbox(facility, key=f"fac_{key}"):
                    selected_facilities.append(facility)
        
        if selected_facilities:
            st.session_state.services_offered = selected_facilities
            st.success(f"✓ Selected {len(selected_facilities)} diagnostic facilities")
    
    # Step 3: Patient Types & Services
    elif st.session_state.step == 3:
        st.header("Step 3: Patient Types & Services Offered")
        st.markdown("Select the types of patients you treat and services provided")
        
        st.subheader("Patient Types")
        cols = st.columns(2)
        patient_keys = list(PATIENT_TYPES.keys())
        
        for i, key in enumerate(patient_keys):
            patient_type = PATIENT_TYPES[key]
            with cols[i % 2]:
                if st.checkbox(
                    f"**{patient_type['name']}**\n\n{patient_type['desc']}",
                    key=f"patient_{key}"
                ):
                    if key not in st.session_state.patient_types:
                        st.session_state.patient_types.append(key)
                else:
                    if key in st.session_state.patient_types:
                        st.session_state.patient_types.remove(key)
        
        if st.session_state.patient_types:
            st.success(f"✓ Selected {len(st.session_state.patient_types)} patient types")
            
            # Show services for selected patient types
            st.subheader("Services Provided")
            for key in st.session_state.patient_types:
                patient_type = PATIENT_TYPES[key]
                st.markdown(f"**{patient_type['name']}:**")
                cols = st.columns(2)
                with cols[0]:
                    for service in patient_type['services'][:2]:
                        st.markdown(f"- {service}")
                with cols[1]:
                    for service in patient_type['services'][2:4]:
                        st.markdown(f"- {service}")
        
        # Additional services
        st.subheader("Additional Services")
        additional_services = st.multiselect(
            "Select additional value-added services:",
            [
                'Telemedicine Consultations',
                'Second Opinion Services',
                'Home Visits',
                'Corporate Health Programs',
                'Medical Tourism Services',
                'Executive Health Checkups',
                'Diet & Nutrition Counseling',
                'Physical Therapy Services',
                'Psychological Counseling',
                'Alternative Medicine Options'
            ]
        )
        
        if additional_services:
            st.info(f"**Value-Added Services:** {', '.join(additional_services)}")
    
    # Step 4: Competitive Positioning
    elif st.session_state.step == 4:
        st.header("Step 4: Competitive Positioning Analysis")
        st.markdown("Rate your competitive advantages in key areas")
        
        st.info("**Rate each factor (1 = Needs Improvement, 2 = Average, 3 = Strong Advantage)**")
        
        for key, factor in COMPETITIVE_FACTORS.items():
            st.subheader(factor['name'])
            
            # Show aspects
            if factor.get('aspects'):
                st.caption(f"**Key Aspects:** {', '.join(factor['aspects'])}")
            
            cols = st.columns(3)
            ratings = {
                '1': 'Needs Improvement',
                '2': 'Average/Competitive',
                '3': 'Strong Advantage'
            }
            
            for rating_num, rating_text in ratings.items():
                col_idx = int(rating_num) - 1
                with cols[col_idx]:
                    if st.button(
                        f"{rating_num}: {rating_text}",
                        key=f"rate_{key}_{rating_num}",
                        use_container_width=True
                    ):
                        st.session_state.competitive_positioning[key] = {
                            'rating': rating_num,
                            'text': rating_text
                        }
            
            if key in st.session_state.competitive_positioning:
                rating_info = st.session_state.competitive_positioning[key]
                if rating_info['rating'] == '3':
                    st.success(f"✓ Strength: {rating_info['text']}")
                elif rating_info['rating'] == '2':
                    st.info(f"✓ Competitive: {rating_info['text']}")
                else:
                    st.warning(f"✓ Area for Improvement: {rating_info['text']}")
        
        # Show summary
        if st.session_state.competitive_positioning:
            st.markdown("---")
            st.subheader("Competitive Position Summary")
            
            strong_areas = [k for k, v in st.session_state.competitive_positioning.items() if v['rating'] == '3']
            weak_areas = [k for k, v in st.session_state.competitive_positioning.items() if v['rating'] == '1']
            
            cols = st.columns(2)
            with cols[0]:
                if strong_areas:
                    st.success("**Your Competitive Strengths:**")
                    for area in strong_areas:
                        factor = COMPETITIVE_FACTORS[area]
                        st.markdown(f"- {factor['name']}")
                        if factor.get('improvement_strategies'):
                            with st.expander(f"Maintain {factor['name']}"):
                                for strat in factor['improvement_strategies']:
                                    st.markdown(f"• {strat}")
            
            with cols[1]:
                if weak_areas:
                    st.warning("**Areas for Improvement:**")
                    for area in weak_areas:
                        factor = COMPETITIVE_FACTORS[area]
                        st.markdown(f"- {factor['name']}")
                        if factor.get('improvement_strategies'):
                            with st.expander(f"Improve {factor['name']}"):
                                for strat in factor['improvement_strategies']:
                                    st.markdown(f"• {strat}")
    
    # Step 5: Marketing Focus
    elif st.session_state.step == 5:
        st.header("Step 5: Marketing Focus Area")
        st.markdown("Select your primary marketing objective")
        
        st.subheader("What is your main marketing goal?")
        cols = st.columns(2)
        focus_keys = list(MARKETING_FOCUS_AREAS.keys())
        
        for i, key in enumerate(focus_keys):
            focus = MARKETING_FOCUS_AREAS[key]
            with cols[i % 2]:
                if st.button(
                    f"**{focus['name']}**",
                    key=f"focus_{key}",
                    use_container_width=True,
                    help=f"Key metrics: {', '.join(focus['key_metrics'])}"
                ):
                    st.session_state.marketing_focus = key
        
        if st.session_state.marketing_focus:
            focus = MARKETING_FOCUS_AREAS[st.session_state.marketing_focus]
            st.success(f"✓ Selected Focus: {focus['name']}")
            
            # Show focus details
            with st.expander("Focus Area Details", expanded=True):
                cols = st.columns(3)
                with cols[0]:
                    st.markdown("**Key Metrics to Track:**")
                    for metric in focus['key_metrics']:
                        st.markdown(f"- {metric}")
                with cols[1]:
                    st.markdown("**Recommended Strategies:**")
                    for strategy in focus['strategies']:
                        st.markdown(f"- {strategy}")
                with cols[2]:
                    st.markdown("**Expected Outcomes:**")
                    if st.session_state.marketing_focus == 'new_patients':
                        st.markdown("- 20-30% increase in new patients")
                        st.markdown("- Improved online visibility")
                        st.markdown("- Better conversion rates")
                    elif st.session_state.marketing_focus == 'patient_retention':
                        st.markdown("- 15-25% increase in repeat visits")
                        st.markdown("- Higher patient satisfaction")
                        st.markdown("- Reduced patient churn")
    
    # Step 6: Comprehensive Strategy
    elif st.session_state.step == 6:
        st.header("Step 6: Complete Marketing Strategy")
        st.markdown("Your personalized marketing strategy based on all inputs")
        
        # Generate comprehensive strategy
        strategy = generate_comprehensive_strategy()
        exp_strategy = get_experience_based_strategy()
        spec_rec = get_specialty_based_recommendations()
        practice_rec = get_practice_type_recommendations()
        
        st.success("### 🎯 Your Personalized Medical Practice Marketing Strategy")
        
        # Professional Profile Summary
        cols = st.columns(4)
        with cols[0]:
            specialty_name = MEDICAL_SPECIALTIES.get(st.session_state.specialty, {}).get('name', 'Not Selected')
            st.metric("Specialty", specialty_name)
        with cols[1]:
            st.metric("Experience", st.session_state.years_experience or "Not Selected")
        with cols[2]:
            practice_name = PRACTICE_TYPES.get(st.session_state.practice_type, {}).get('name', 'Not Selected')
            st.metric("Practice Type", practice_name)
        with cols[3]:
            st.metric("Marketing Budget", calculate_marketing_budget())
        
        st.markdown("---")
        
        # Experience-based Strategy
        if exp_strategy:
            st.info("### 📊 Experience-Based Strategy")
            cols = st.columns(3)
            with cols[0]:
                st.markdown("**Focus:**")
                st.markdown(f"{exp_strategy.get('focus', '')}")
            with cols[1]:
                st.markdown("**Key Actions:**")
                for action in exp_strategy.get('key_actions', [])[:3]:
                    st.markdown(f"- {action}")
            with cols[2]:
                st.markdown("**Branding Priorities:**")
                for priority in exp_strategy.get('branding_priorities', []):
                    st.markdown(f"- {priority}")
        
        # Practice Recommendations
        if practice_rec:
            st.info("### 🏢 Practice Infrastructure Plan")
            cols = st.columns(2)
            with cols[0]:
                st.markdown("**Marketing Channels:**")
                for channel in practice_rec.get('marketing_channels', [])[:4]:
                    st.markdown(f"- {channel}")
            with cols[1]:
                st.markdown("**Technology Needs:**")
                for tech in practice_rec.get('technology_needs', [])[:4]:
                    st.markdown(f"- {tech}")
        
        # Complete Strategy Framework
        st.info("### 🎨 Complete Marketing Strategy Framework")
        
        tabs = st.tabs(["Patient Acquisition", "Patient Retention", "Brand Building", "Professional Growth", "Financial Planning"])
        
        with tabs[0]:
            st.markdown("**Patient Acquisition Strategies:**")
            for i, item in enumerate(strategy.get('patient_acquisition', []), 1):
                st.markdown(f"{i}. {item}")
        
        with tabs[1]:
            st.markdown("**Patient Retention Strategies:**")
            for i, item in enumerate(strategy.get('patient_retention', []), 1):
                st.markdown(f"{i}. {item}")
        
        with tabs[2]:
            st.markdown("**Brand Building Strategies:**")
            for i, item in enumerate(strategy.get('personal_branding', []), 1):
                st.markdown(f"{i}. {item}")
        
        with tabs[3]:
            st.markdown("**Professional Development Strategies:**")
            for i, item in enumerate(strategy.get('professional_development', []), 1):
                st.markdown(f"{i}. {item}")
        
        with tabs[4]:
            st.markdown("**Financial Planning Strategies:**")
            for i, item in enumerate(strategy.get('financial_planning', []), 1):
                st.markdown(f"{i}. {item}")
        
        # Implementation Timeline
        st.markdown("---")
        st.warning("### 🚀 12-Month Implementation Plan")
        
        timeline_cols = st.columns(4)
        with timeline_cols[0]:
            st.markdown("**Months 1-3:**")
            st.markdown("- Foundation Building")
            st.markdown("- Digital Presence Setup")
            st.markdown("- Team Training")
        
        with timeline_cols[1]:
            st.markdown("**Months 4-6:**")
            st.markdown("- Strategy Implementation")
            st.markdown("- Marketing Campaigns")
            st.markdown("- Network Building")
        
        with timeline_cols[2]:
            st.markdown("**Months 7-9:**")
            st.markdown("- Performance Analysis")
            st.markdown("- Strategy Refinement")
            st.markdown("- Service Expansion")
        
        with timeline_cols[3]:
            st.markdown("**Months 10-12:**")
            st.markdown("- Scale Successful Programs")
            st.markdown("- Advanced Brand Building")
            st.markdown("- Annual Review")
        
        # Action Items
        st.markdown("---")
        st.info("### ✅ Immediate Action Items (Next 30 Days)")
        
        action_cols = st.columns(3)
        with action_cols[0]:
            st.markdown("**Week 1-2:**")
            st.markdown("1. Set up Google My Business")
            st.markdown("2. Create social media profiles")
            st.markdown("3. Design patient intake forms")
        
        with action_cols[1]:
            st.markdown("**Week 3-4:**")
            st.markdown("1. Launch basic website")
            st.markdown("2. Set up appointment system")
            st.markdown("3. Create patient education materials")
        
        with action_cols[2]:
            st.markdown("**Metrics to Track:**")
            st.markdown("- New patient inquiries")
            st.markdown("- Website traffic")
            st.markdown("- Patient satisfaction")
            st.markdown("- Revenue growth")
        
        # Link to Brand Building Activities
        st.markdown("---")
        st.success("### 🎨 Ready to implement specific strategies?")
        if st.button("Go to Brand Building Activities →", type="primary", use_container_width=True):
            st.session_state.app_mode = "Brand Building Activities"
            st.rerun()
    
    # Navigation buttons
    st.markdown("---")
    nav_cols = st.columns([1, 1])
    
    with nav_cols[0]:
        if st.session_state.step > 1:
            if st.button("← Previous", use_container_width=True):
                st.session_state.step -= 1
                st.rerun()
    
    with nav_cols[1]:
        can_proceed = False
        if st.session_state.step == 1:
            can_proceed = st.session_state.specialty and st.session_state.years_experience
        elif st.session_state.step == 2:
            can_proceed = st.session_state.practice_type
        elif st.session_state.step == 3:
            can_proceed = len(st.session_state.patient_types) > 0
        elif st.session_state.step == 4:
            can_proceed = len(st.session_state.competitive_positioning) == len(COMPETITIVE_FACTORS)
        elif st.session_state.step == 5:
            can_proceed = st.session_state.marketing_focus
        
        if st.session_state.step < 6:
            if st.button("Next →", disabled=not can_proceed, use_container_width=True, type="primary"):
                st.session_state.step += 1
                st.rerun()
        else:
            if st.button("🔄 Start New Strategy", use_container_width=True, type="primary"):
                st.session_state.step = 1
                st.session_state.specialty = None
                st.session_state.years_experience = None
                st.session_state.practice_type = None
                st.session_state.patient_types = []
                st.session_state.services_offered = []
                st.session_state.competitive_positioning = {}
                st.session_state.marketing_focus = None
                st.session_state.selected_strategies = []
                st.rerun()

# Brand Building Activities Tool
else:
    st.title("🎨 Medical Professional Brand Building Activities")
    st.markdown("*Get specific strategies and tools to build your medical brand and reputation*")
    
    # Input section
    with st.container():
        st.subheader("Configure Your Brand Building Strategy")
        
        cols = st.columns(3)
        
        with cols[0]:
            specialty_names = [MEDICAL_SPECIALTIES[s]['name'] for s in MEDICAL_SPECIALTIES]
            specialty_input = st.selectbox(
                "🩺 Specialty",
                [''] + specialty_names,
                index=0
            )
        
        with cols[1]:
            experience_input = st.selectbox(
                "📈 Years of Experience",
                [''] + YEARS_EXPERIENCE,
                index=0
            )
        
        with cols[2]:
            focus_options = [MARKETING_FOCUS_AREAS[f]['name'] for f in MARKETING_FOCUS_AREAS]
            focus_input = st.selectbox(
                "🎯 Marketing Focus",
                [''] + focus_options,
                index=0
            )
        
        if st.button("🔍 Generate Brand Building Strategies", type="primary", use_container_width=True):
            if specialty_input and experience_input and focus_input:
                # Find the focus key
                focus_key = None
                for key, value in MARKETING_FOCUS_AREAS.items():
                    if value['name'] == focus_input:
                        focus_key = key
                        break
                
                if focus_key:
                    st.session_state.marketing_focus = focus_key
                    st.session_state.selected_strategies = []
                    st.rerun()
    
    # Results section
    if st.session_state.marketing_focus and experience_input:
        st.markdown("---")
        st.header("Your Brand Building Strategy")
        
        # Insights
        cols = st.columns(2)
        with cols[0]:
            st.info(f"**📈 Experience-Based Insight**")
            exp_strat = get_experience_based_strategy()
            if exp_strat:
                st.markdown(f"**Focus:** {exp_strat.get('focus', '')}")
                st.markdown("**Key Actions for Your Experience Level:**")
                for action in exp_strat.get('key_actions', [])[:3]:
                    st.markdown(f"- {action}")
        
        with cols[1]:
            focus_data = MARKETING_FOCUS_AREAS[st.session_state.marketing_focus]
            st.info(f"**🎯 {focus_data['name']} Focus**")
            st.markdown("**Key Metrics to Track:**")
            for metric in focus_data['key_metrics'][:3]:
                st.markdown(f"- {metric}")
            st.markdown("**Recommended Approaches:**")
            for strategy in focus_data['strategies'][:3]:
                st.markdown(f"- {strategy}")
        
        st.markdown("---")
        
        # Get recommendations
        recommendations = get_recommended_strategies()
        
        if recommendations:
            # Header with count
            header_cols = st.columns([3, 1])
            with header_cols[0]:
                st.subheader("Recommended Brand Building Strategies")
            with header_cols[1]:
                if st.session_state.selected_strategies:
                    st.success(f"✓ {len(st.session_state.selected_strategies)} Selected")
            
            # Strategy cards
            for rec in recommendations:
                with st.expander(f"{'✓ ' if rec['name'] in st.session_state.selected_strategies else ''}**{rec['name']}**", 
                               expanded=False):
                    
                    # Strategy details
                    cols = st.columns([3, 1])
                    with cols[0]:
                        st.markdown(f"**Focus:** {rec['focus']}")
                        st.markdown(f"**Timeframe:** {rec['time']}")
                        st.markdown(f"**Budget Level:** {rec['budget']}")
                    with cols[1]:
                        priority_class = "priority-high" if rec['score'] == 3 else "priority-medium"
                        priority_text = "High Priority" if rec['score'] == 3 else "Medium Priority"
                        st.markdown(f'<span class="{priority_class}">{priority_text}</span>', unsafe_allow_html=True)
                    
                    # Reasoning
                    st.markdown(f"**Why this works:** {rec['reasoning']}")
                    
                    # Toggle selection
                    if rec['name'] in st.session_state.selected_strategies:
                        if st.button(f"Remove from Plan", key=f"remove_{rec['name']}", use_container_width=True):
                            st.session_state.selected_strategies.remove(rec['name'])
                            st.rerun()
                    else:
                        if st.button(f"Add to Plan", key=f"add_{rec['name']}", type="primary", use_container_width=True):
                            st.session_state.selected_strategies.append(rec['name'])
                            st.rerun()
                    
                    # Implementation resources
                    if rec['resources']:
                        st.markdown("---")
                        st.markdown("**🛠️ Implementation Resources:**")
                        
                        for resource in rec['resources']:
                            with st.container():
                                st.markdown(f"**{resource['name']}**")
                                st.markdown(f"*{resource['desc']}*")
                                
                                col1, col2, col3 = st.columns([2, 2, 1])
                                with col1:
                                    st.markdown(f"**Tools:** {', '.join(resource['tools'][:3])}")
                                with col2:
                                    st.markdown(f"**Cost Level:** {resource['cost']}")
                                with col3:
                                    if st.button("Learn More", key=f"learn_{resource['name']}_{rec['name']}"):
                                        st.info(f"Detailed implementation guide for {resource['name']} coming soon!")
            
            # Selected strategies summary
            if st.session_state.selected_strategies:
                st.markdown("---")
                st.success("### 🎯 Your Selected Brand Building Plan")
                
                # Implementation timeline
                tabs = st.tabs(["Phase 1: Foundation (0-3 months)", "Phase 2: Growth (4-9 months)", "Phase 3: Maturity (10-18 months)"])
                
                with tabs[0]:
                    short_term = [s for s in st.session_state.selected_strategies 
                                if any(x in s for x in ['Digital Presence', 'Content Marketing', 'Patient Relationship'])]
                    if short_term:
                        for strategy in short_term:
                            st.markdown(f"✓ {strategy}")
                    else:
                        st.info("Add Phase 1 strategies to your plan")
                
                with tabs[1]:
                    medium_term = [s for s in st.session_state.selected_strategies 
                                 if any(x in s for x in ['Community Outreach', 'Premium Services', 'Referral Network'])]
                    if medium_term:
                        for strategy in medium_term:
                            st.markdown(f"✓ {strategy}")
                    else:
                        st.info("Add Phase 2 strategies to your plan")
                
                with tabs[2]:
                    long_term = [s for s in st.session_state.selected_strategies 
                               if any(x in s for x in ['Academic Presence', 'Specialized Certifications'])]
                    if long_term:
                        for strategy in long_term:
                            st.markdown(f"✓ {strategy}")
                    else:
                        st.info("Add Phase 3 strategies to your plan")
                
                # Budget Planning
                st.markdown("---")
                st.info("### 💰 Budget Planning Guide")
                
                budget_cols = st.columns(3)
                with budget_cols[0]:
                    st.markdown("**Low Budget (< $5,000/yr):**")
                    st.markdown("- Focus on free tools")
                    st.markdown("- DIY content creation")
                    st.markdown("- Local networking")
                
                with budget_cols[1]:
                    st.markdown("**Medium Budget ($5,000-$20,000/yr):**")
                    st.markdown("- Professional website")
                    st.markdown("- Basic marketing campaigns")
                    st.markdown("- Training programs")
                
                with budget_cols[2]:
                    st.markdown("**High Budget ($20,000+/yr):**")
                    st.markdown("- Full marketing team")
                    st.markdown("- Advanced technology")
                    st.markdown("- Research projects")
                
                # Next Steps
                st.markdown("---")
                st.warning("### 🚀 Next Steps & Implementation")
                
                step_cols = st.columns(3)
                with step_cols[0]:
                    if st.button("📋 Create Action Plan", use_container_width=True):
                        st.info("Action plan template will be generated")
                
                with step_cols[1]:
                    if st.button("📅 Schedule Implementation", use_container_width=True):
                        st.info("Calendar scheduling coming soon")
                
                with step_cols[2]:
                    if st.button("📊 Track Progress", use_container_width=True):
                        st.info("Progress tracking dashboard coming soon")
            
            # Pro tip
            st.markdown("---")
            st.warning("""
            **💡 Pro Tips for Medical Brand Building:**
            
            1. **Start with Foundation:** Build digital presence before advanced strategies
            2. **Be Consistent:** Regular content and engagement build trust
            3. **Measure Everything:** Track metrics to understand what works
            4. **Patient-Centric:** Always focus on patient needs and experiences
            5. **Ethical First:** Maintain medical ethics in all marketing activities
            
            **Remember:** Building a medical brand takes time - focus on consistency and quality.
            """)
    
    else:
        st.info("👆 Fill in the details above and click 'Generate Brand Building Strategies' to get personalized recommendations.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>Medical Professional Marketing Strategy Tool</strong></p>
    <p>Built for Doctors & Medical Practices | Version 2.0</p>
    <p style='font-size: 0.8rem; margin-top: 10px;'>
        Disclaimer: This tool provides marketing guidance only. Always follow medical ethics guidelines, 
        maintain patient confidentiality, and comply with local medical advertising regulations.
    </p>
</div>
""", unsafe_allow_html=True)
