import streamlit as st
import numpy as np
from PIL import Image
import json
import time
from datetime import datetime
from utils.saliency import get_saliency_map, get_multi_saliency_maps
from utils.scoring import calculate_scores, get_detailed_metrics
from utils.insights import generate_insights, generate_actionable_recommendations
from utils.persona import apply_persona, create_custom_persona


# Export helper functions
def create_png_export(image):
    """Convert image to PNG bytes for download"""
    import io
    img_io = io.BytesIO()
    Image.fromarray(image.astype('uint8')).save(img_io, format='PNG')
    img_io.seek(0)
    return img_io.getvalue()
 
def create_pdf_export(scores, metrics, insights, recommendations):
    """Create PDF report"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        import io
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#6366f1'),
            spaceAfter=30
        )
        elements.append(Paragraph("DesignLens AI - Design Analysis Report", title_style))
        elements.append(Spacer(1, 12))
        
        # Scores Table
        elements.append(Paragraph("Scores", styles['Heading2']))
        scores_data = [
            ['Metric', 'Score'],
            ['Attention Score', f"{scores.get('Attention Score', 'N/A')}"],
            ['Cognitive Load', f"{scores.get('Cognitive Load', 'N/A')}"],
        ]
        scores_table = Table(scores_data)
        scores_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(scores_table)
        elements.append(Spacer(1, 12))
        
        # Insights
        elements.append(Paragraph("Insights", styles['Heading2']))
        for insight in insights:
            elements.append(Paragraph(f"• {insight}", styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Recommendations
        elements.append(Paragraph("Recommendations", styles['Heading2']))
        for rec in recommendations:
            elements.append(Paragraph(f"<b>{rec['title']}</b>", styles['Normal']))
            elements.append(Paragraph(rec['description'], styles['Normal']))
            elements.append(Paragraph(f"Impact: {rec['impact']}", styles['Normal']))
            elements.append(Spacer(1, 6))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
    except ImportError:
        return None

# Page configuration
st.set_page_config(
    page_title="DesignLens AI",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme toggle
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "history" not in st.session_state:
    st.session_state.history = []
if "cache" not in st.session_state:
    st.session_state.cache = {}

# Custom CSS for enhanced UI
st.markdown("""
<style>
:root {
    --primary: #6366f1;
    --secondary: #8b5cf6;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --dark-bg: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    --glass: rgba(255, 255, 255, 0.08);
}

/* Dark theme */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stToolbar"] {
    right: 2rem;
}

[data-testid="stAppViewContainer"] {
    padding: 2rem;
}

/* Glass morphism cards */
.glass, [data-testid="stMetric"], [data-testid="stFileUploader"] {
    background: rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(12px);
    padding: 20px;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Text colors */
h1, h2, h3, h4, h5, h6, p, span, label {
    color: #e2e8f0 !important;
}

/* Button styling */
button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    border-radius: 8px !important;
    border: none !important;
    transition: all 0.3s ease !important;
}

button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 16px rgba(99, 102, 241, 0.3) !important;
}

/* Tabs styling */
[data-testid="stTabs"] {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 1rem;
}

/* Score cards */
.score-card {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2));
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}

.score-excellent {
    color: #10b981;
}

.score-good {
    color: #3b82f6;
}

.score-average {
    color: #f59e0b;
}

.score-poor {
    color: #ef4444;
}

/* Insight boxes */
.insight-box {
    background: rgba(255, 255, 255, 0.06);
    border-left: 4px solid #6366f1;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
}

.recommendation-box {
    background: rgba(16, 185, 129, 0.1);
    border-left: 4px solid #10b981;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
}

/* Comparison table */
.comparison-table {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    padding: 15px;
}

/* Animation */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.animate-fade {
    animation: fadeIn 0.5s ease-in;
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: rgba(99, 102, 241, 0.5);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(99, 102, 241, 0.8);
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    
    # Algorithm selection
    st.markdown("### 🔍 Analysis Settings")
    algorithm = st.selectbox(
        "Saliency Algorithm",
        ["Spectral Residual", "Fine Grained", "Multi-Scale"],
        help="Different algorithms for saliency detection"
    )

    # History section
    st.markdown("### 📊 Analysis History")
    if st.session_state.history:
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()
        
        st.markdown(f"**Total analyses:** {len(st.session_state.history)}")
        
        with st.expander("View History"):
            for idx, item in enumerate(st.session_state.history[-5:], 1):
                st.write(f"{idx}. {item['timestamp']} - {item['persona']}")
    
    st.markdown("---")
    st.markdown("#### 📱 App Info")
    st.info("DesignLens AI v2.0\n\nEnhanced design analysis with AI insights")

# Header
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style='font-size: 48px; background: linear-gradient(135deg, #6366f1, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
    🎨 DesignLens AI
    </h1>
    <p style='font-size: 18px; color: #cbd5f5; margin-top: -10px;'>
    Advanced Design Analysis Powered by AI
    </p>
    <p style='font-size: 14px; color: #94a3b8;'>
    Analyze. Compare. Optimize. Perfect your designs
    </p>
</div>
""", unsafe_allow_html=True)

# Main tabs
main_tabs = st.tabs(["🎯 Single Analysis", "⚖️ A/B Testing", "📚 Batch Upload", "📈 Analytics"])

# ==================== SINGLE ANALYSIS TAB ====================
with main_tabs[0]:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Upload Design")
        uploaded_file = st.file_uploader(
            "Upload your design (PNG, JPG, JPEG)",
            type=["png", "jpg", "jpeg"],
            key="single_upload"
        )
    
    with col2:
        st.markdown("### Viewer Profile")
        profile_type = st.radio(
            "Select profile type",
            ["Preset", "Custom"],
            horizontal=True,
            label_visibility="collapsed"
        )
    
    if profile_type == "Preset":
        personas = ["General Viewer", "Recruiter", "Social Media User", "E-commerce Shopper", "Mobile User"]
        persona = st.selectbox("Select Viewer Persona", personas)
    else:
        st.info("Custom Persona Creator")
        custom_name = st.text_input("Persona Name", "My Custom Persona")
        focus_area = st.slider("Focus Area Intensity", 1.0, 2.0, 1.2, help="How much this persona focuses on specific areas")
        persona = custom_name
        persona_factor = focus_area

    if uploaded_file:
        # Cache check
        cache_key = f"{uploaded_file.name}_{persona}_{algorithm}"
        
        if cache_key in st.session_state.cache:
            st.success("📦 Loaded from cache")
            cached_data = st.session_state.cache[cache_key]
            image = cached_data['image']
            result = cached_data['saliency']
            scores = cached_data['scores']
            metrics = cached_data['metrics']
            insights = cached_data['insights']
            recommendations = cached_data['recommendations']
        else:
            image = Image.open(uploaded_file)
            img_np = np.array(image)
            
            with st.spinner("🔍 Analyzing your design..."):
                time.sleep(0.5)  # For visual feedback
                
                # Get saliency map
                result = get_saliency_map(img_np, algorithm)
                
                # Apply persona
                result_with_persona = apply_persona(result, persona)
                
                # Calculate scores
                scores = calculate_scores(result_with_persona)
                metrics = get_detailed_metrics(result_with_persona, img_np)
                insights = generate_insights(scores)
                recommendations = generate_actionable_recommendations(scores, metrics)
            
            # Cache results
            st.session_state.cache[cache_key] = {
                'image': image,
                'saliency': result,
                'scores': scores,
                'metrics': metrics,
                'insights': insights,
                'recommendations': recommendations
            }
            
            # Add to history
            st.session_state.history.append({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'persona': persona,
                'file': uploaded_file.name
            })
        
        # Display tabs
        analysis_tabs = st.tabs(["🔍 Visual Analysis", "📊 Detailed Scores", "💡 Insights", "✨ Recommendations"])
        
        # ===== Visual Analysis Tab =====
        with analysis_tabs[0]:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Original Design**")
                st.image(image, width=200, use_column_width=True)
            
            with col2:
                st.markdown(f"**Attention Heatmap ({persona})**")
                st.image(result, width=200, use_column_width=True)
            
            # Image info
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Dimensions", f"{image.width}×{image.height}px")
            with col2:
                st.metric("File Size", f"{uploaded_file.size / 1024:.1f}KB")
            with col3:
                st.metric("Algorithm", algorithm)
        
        # ===== Detailed Scores Tab =====
        with analysis_tabs[1]:
            st.markdown("### Score Overview")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                attention = scores['Attention Score']
                color = "🟢" if attention > 60 else "🟡" if attention > 40 else "🔴"
                st.metric("Attention Score", f"{attention}", f"{color}")
            
            with col2:
                load = scores['Cognitive Load']
                color = "🟢" if load < 30 else "🟡" if load < 60 else "🔴"
                st.metric("Cognitive Load", f"{load}", f"{color}")
            
            with col3:
                contrast = metrics.get('Contrast Ratio', 0)
                st.metric("Contrast Ratio", f"{contrast:.2f}")
            
            with col4:
                complexity = metrics.get('Visual Complexity', 0)
                st.metric("Visual Complexity", f"{complexity:.2f}")
            
            # Detailed metrics
            st.markdown("### Advanced Metrics")
            
            metric_cols = st.columns(3)
            metrics_to_show = [
                ("Color Diversity", metrics.get('Color Diversity', 0)),
                ("Edge Density", metrics.get('Edge Density', 0)),
                ("Brightness Mean", metrics.get('Brightness Mean', 0)),
                ("Saturation Level", metrics.get('Saturation Level', 0)),
                ("Focus Score", metrics.get('Focus Score', 0)),
                ("Balance Score", metrics.get('Balance Score', 0))
            ]
            
            for idx, (metric_name, value) in enumerate(metrics_to_show):
                with metric_cols[idx % 3]:
                    st.metric(metric_name, f"{value:.2f}")
            
            # Score breakdown
            st.markdown("### Score Breakdown")
            
            breakdown_data = {
                "Metric": ["Attention", "Complexity", "Contrast", "Color", "Edge", "Balance"],
                "Score": [
                    scores['Attention Score'],
                    scores['Cognitive Load'],
                    metrics.get('Contrast Ratio', 0) * 10,
                    metrics.get('Color Diversity', 0),
                    metrics.get('Edge Density', 0),
                    metrics.get('Balance Score', 0)
                ]
            }
            
            import pandas as pd
            df = pd.DataFrame(breakdown_data)
            st.bar_chart(df.set_index("Metric"))
        
        # ===== Insights Tab =====
        with analysis_tabs[2]:
            st.markdown("### 💡 Design Insights")
            
            if insights:
                for insight in insights:
                    st.markdown(f"""
                    <div class="insight-box">
                    {insight}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No insights available for this design")
        
        # ===== Recommendations Tab =====
        with analysis_tabs[3]:
            st.markdown("### ✨ Actionable Recommendations")
            
            if recommendations:
                for rec in recommendations:
                    st.markdown(f"""
                    <div class="recommendation-box">
                    <strong>{rec['title']}</strong><br>
                    {rec['description']}<br>
                    <small>Impact: {rec['impact']}</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Design is already optimized!")
        
        # Download Report
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # PNG Export
            png_data = create_png_export(result)
            st.download_button(
                label="📱 PNG Heatmap",
                data=png_data,
                file_name=f"heatmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png"
            )
        
        with col2:
            # PDF Export
            pdf_data = create_pdf_export(scores, metrics, insights, recommendations)
            if pdf_data:
                st.download_button(
                    label="📊 PDF Report",
                    data=pdf_data,
                    file_name=f"design_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
            else:
                st.info("📊 Install reportlab: pip install reportlab")
        
        with col3:
            st.info("💾 CSV Batch export in Batch mode")

# ==================== A/B TESTING TAB ====================
with main_tabs[1]:
    st.markdown("### ⚖️ Compare Two Designs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Design A**")
        file_a = st.file_uploader("Upload Design A", type=["png", "jpg", "jpeg"], key="design_a")
    
    with col2:
        st.markdown("**Design B**")
        file_b = st.file_uploader("Upload Design B", type=["png", "jpg", "jpeg"], key="design_b")
    
    if file_a and file_b:
        persona_ab = st.selectbox("Select Persona for Comparison", ["General Viewer", "Recruiter", "Social Media User"])
        
        if st.button("🔄 Compare Designs"):
            img_a = np.array(Image.open(file_a))
            img_b = np.array(Image.open(file_b))
            
            with st.spinner("Comparing designs..."):
                saliency_a = get_saliency_map(img_a)
                saliency_b = get_saliency_map(img_b)
                
                saliency_a = apply_persona(saliency_a, persona_ab)
                saliency_b = apply_persona(saliency_b, persona_ab)
                
                scores_a = calculate_scores(saliency_a)
                scores_b = calculate_scores(saliency_b)
            
            # Comparison view
            comp_col1, comp_col2 = st.columns(2)
            
            with comp_col1:
                st.image(Image.open(file_a), width=200)
                st.write("**Design A Scores**")
                st.metric("Attention", scores_a['Attention Score'])
                st.metric("Cognitive Load", scores_a['Cognitive Load'])
            
            with comp_col2:
                st.image(Image.open(file_b), width=200)
                st.write("**Design B Scores**")
                st.metric("Attention", scores_b['Attention Score'])
                st.metric("Cognitive Load", scores_b['Cognitive Load'])
            
            # Winner
            st.markdown("---")
            st.markdown("### 🏆 Comparison Results")
            
            if scores_a['Attention Score'] > scores_b['Attention Score']:
                st.success("✅ Design A wins on Attention!")
            elif scores_b['Attention Score'] > scores_a['Attention Score']:
                st.success("✅ Design B wins on Attention!")
            else:
                st.info("🤝 Both designs equal on Attention")
            
            if scores_a['Cognitive Load'] < scores_b['Cognitive Load']:
                st.success("✅ Design A wins on Simplicity!")
            elif scores_b['Cognitive Load'] < scores_a['Cognitive Load']:
                st.success("✅ Design B wins on Simplicity!")
            else:
                st.info("🤝 Both designs equal on Simplicity")
            
            # Comparison chart
            import pandas as pd
            comp_data = pd.DataFrame({
                'Metric': ['Attention Score', 'Cognitive Load'],
                'Design A': [scores_a['Attention Score'], scores_a['Cognitive Load']],
                'Design B': [scores_b['Attention Score'], scores_b['Cognitive Load']]
            })
            
            st.bar_chart(comp_data.set_index('Metric'))

# ==================== BATCH UPLOAD TAB ====================
with main_tabs[2]:
    st.markdown("### 📚 Batch Analysis")
    
    uploaded_files = st.file_uploader(
        "Upload multiple designs",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        key="batch_upload"
    )
    
    batch_persona = st.selectbox("Select Persona", ["General Viewer", "Recruiter", "Social Media User"], key="batch_persona")
    
    if uploaded_files and st.button("📊 Analyze Batch"):
        results = []
        progress_bar = st.progress(0)
        
        for idx, file in enumerate(uploaded_files):
            img_np = np.array(Image.open(file))
            
            saliency = get_saliency_map(img_np)
            saliency = apply_persona(saliency, batch_persona)
            scores = calculate_scores(saliency)
            
            results.append({
                'File': file.name,
                'Attention Score': scores['Attention Score'],
                'Cognitive Load': scores['Cognitive Load']
            })
            
            progress_bar.progress((idx + 1) / len(uploaded_files))
        
        # Display results table
        import pandas as pd
        results_df = pd.DataFrame(results)
        st.dataframe(results_df, use_container_width=True)
        
        # Statistics
        st.markdown("### 📈 Batch Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Average Attention", f"{results_df['Attention Score'].mean():.2f}")
        with col2:
            st.metric("Average Cognitive Load", f"{results_df['Cognitive Load'].mean():.2f}")
        with col3:
            st.metric("Total Designs", len(results_df))
        
        # Download batch report
        st.download_button(
            label="📥 Download Batch Report",
            data=results_df.to_csv(index=False),
            file_name=f"batch_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

# ==================== ANALYTICS TAB ====================
with main_tabs[3]:
    st.markdown("### 📈 Analytics Dashboard")
    
    if st.session_state.history:
        st.markdown(f"**Total Analyses:** {len(st.session_state.history)}")
        
        # Persona distribution
        from collections import Counter
        personas_count = Counter([h['persona'] for h in st.session_state.history])
        
        import pandas as pd
        persona_df = pd.DataFrame(list(personas_count.items()), columns=['Persona', 'Count'])
        
        st.markdown("#### Persona Distribution")
        st.bar_chart(persona_df.set_index('Persona'))
        
        # Timeline
        st.markdown("#### Analysis Timeline")
        timeline_data = pd.DataFrame(st.session_state.history)
        st.write(timeline_data)
        
    else:
        st.info("No analysis history yet. Start analyzing designs to see analytics!")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 12px;">
    DesignLens AI v2.0 | Built with ❤️ | Enhanced Design Analysis Platform
</div>
""", unsafe_allow_html=True)