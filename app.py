# Progress bar
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
