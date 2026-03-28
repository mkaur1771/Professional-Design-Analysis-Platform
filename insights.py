def generate_insights(scores):
    """
    Generate actionable design insights based on analysis scores.
    
    Args:
        scores: Dictionary containing 'Attention Score' and 'Cognitive Load'
    
    Returns:
        List of insight strings with design recommendations
    """
    insights = []
    attention = scores["Attention Score"]
    load = scores["Cognitive Load"]

    # Attention Score feedback
    if attention < 30:
        insights.append("⚠️ Very low visual attention - Consider redesigning with stronger focal points or increased contrast.")
    elif attention < 40:
        insights.append("📌 Low visual attention - Consider increasing contrast or adding a focal point.")
    elif attention > 80:
        insights.append("🎯 Exceptional attention capture - Key elements are highly visually prominent.")
    elif attention > 70:
        insights.append("✅ Strong attention capture — key elements are visually prominent.")
    elif attention >= 40 and attention <= 70:
        insights.append("👁️ Moderate attention - Viewers notice the design reasonably well.")

    # Cognitive Load feedback
    if load > 70:
        insights.append("🚨 Extremely high cognitive load - Design feels very cluttered. Urgent simplification needed.")
    elif load > 60:
        insights.append("⚠️ High cognitive load — design may feel cluttered. Try simplifying elements.")
    elif load < 15:
        insights.append("✨ Extremely low cognitive load - design is pristine and minimalist.")
    elif load < 30:
        insights.append("🎨 Low cognitive load — design is clean and easy to process.")
    elif load >= 30 and load <= 60:
        insights.append("📊 Moderate cognitive load - Design has reasonable complexity.")

    # Balanced design feedback
    if 40 <= attention <= 70 and 30 <= load <= 60:
        insights.append("⚡ Balanced design — good combination of clarity and engagement.")
    
    # Special cases
    if attention > 70 and load < 30:
        insights.append("🏆 Outstanding design - Strong attention with minimal complexity. Excellent balance!")
    
    if attention < 40 and load > 60:
        insights.append("🎭 Challenging design - Low attention with high complexity. Needs redesign focus.")

    return insights


def generate_actionable_recommendations(scores, metrics):
    """
    Generate specific, actionable recommendations to improve the design.
    
    Args:
        scores: Basic scores dictionary
        metrics: Detailed metrics dictionary
    
    Returns:
        List of recommendation dictionaries with title, description, and impact
    """
    recommendations = []
    
    attention = scores['Attention Score']
    load = scores['Cognitive Load']
    
    # Attention-based recommendations
    if attention < 40:
        recommendations.append({
            'title': '🔆 Boost Visual Hierarchy',
            'description': 'Create a clear visual hierarchy with size, color, and position differences. Make important elements 2-3x larger than supporting elements.',
            'impact': 'High - Can increase attention by 20-30%'
        })
    
    if attention < 50:
        recommendations.append({
            'title': '🎨 Increase Color Contrast',
            'description': 'Use complementary colors or increase the brightness difference between foreground and background. Aim for WCAG AA contrast ratio of 4.5:1.',
            'impact': 'High - Improves visibility and attention'
        })
    
    # Cognitive Load recommendations
    if load > 60:
        recommendations.append({
            'title': '🧹 Remove Unnecessary Elements',
            'description': 'Eliminate decorative elements that don\'t serve a purpose. Follow the principle of "less is more". Remove clutter systematically.',
            'impact': 'High - Can reduce load by 25-35%'
        })
    
    if load > 55:
        recommendations.append({
            'title': '📐 Improve Spacing and Layout',
            'description': 'Increase white space between elements. Use a consistent grid system. Ensure proper padding and margins around text and images.',
            'impact': 'Medium - Improves readability and perception of order'
        })
    
    # Contrast recommendations
    contrast = metrics.get('Contrast Ratio', 1)
    if contrast < 3:
        recommendations.append({
            'title': '🌓 Enhance Contrast Ratio',
            'description': 'Current contrast ratio is below optimal levels. Darken dark elements or lighten light elements. Aim for at least 4.5:1 for text.',
            'impact': 'High - Improves accessibility and visibility'
        })
    
    # Color recommendations
    color_diversity = metrics.get('Color Diversity', 0)
    if color_diversity < 0.2:
        recommendations.append({
            'title': '🎭 Add Color Variety',
            'description': 'Your design uses limited colors. Add complementary or analogous colors to create visual interest while maintaining harmony.',
            'impact': 'Medium - Increases visual appeal'
        })
    
    if color_diversity > 0.7:
        recommendations.append({
            'title': '🎨 Harmonize Color Palette',
            'description': 'Too many different colors may overwhelm viewers. Limit your palette to 3-5 main colors and use variations of these.',
            'impact': 'Medium - Creates cohesion'
        })
    
    # Edge/Detail recommendations
    edge_density = metrics.get('Edge Density', 0)
    if edge_density < 0.05:
        recommendations.append({
            'title': '✏️ Add Visual Details',
            'description': 'Design lacks detail and texture. Add subtle patterns, borders, or textures to create visual interest.',
            'impact': 'Low - Enhances visual appeal'
        })
    
    if edge_density > 0.3:
        recommendations.append({
            'title': '🧹 Reduce Visual Noise',
            'description': 'Too many edges and details create visual noise. Simplify shapes, reduce texture, and use cleaner lines.',
            'impact': 'Medium - Improves clarity'
        })
    
    # Balance recommendations
    balance_score = metrics.get('Balance Score', 0.5)
    if balance_score < 0.4:
        recommendations.append({
            'title': '⚖️ Improve Visual Balance',
            'description': 'Design appears off-balance. Distribute visual weight more evenly across the canvas. Consider symmetrical or asymmetrical balance.',
            'impact': 'Medium - Creates stability and harmony'
        })
    
    # Focus recommendations
    focus_score = metrics.get('Focus Score', 0.5)
    if focus_score < 0.3:
        recommendations.append({
            'title': '🎯 Create Clear Focus Points',
            'description': 'Viewers don\'t have a clear focal point. Use size, color, or position to guide attention to your most important element.',
            'impact': 'High - Improves user experience'
        })
    
    # Complexity recommendations
    visual_complexity = metrics.get('Visual Complexity', 0)
    if visual_complexity > 0.6:
        recommendations.append({
            'title': '📉 Reduce Overall Complexity',
            'description': 'Design is highly complex. Systematically simplify by combining elements, using consistent styles, and removing redundancy.',
            'impact': 'High - Improves user comprehension'
        })
    
    # Brightness recommendations
    brightness = metrics.get('Brightness Mean', 0.5)
    if brightness < 0.3:
        recommendations.append({
            'title': '☀️ Increase Brightness',
            'description': 'Design is too dark and may feel heavy. Increase background brightness or use lighter accent colors.',
            'impact': 'Medium - Improves mood and accessibility'
        })
    
    if brightness > 0.8:
        recommendations.append({
            'title': '🌙 Reduce Brightness',
            'description': 'Design is too bright and may strain eyes. Add darker elements or reduce overall luminance.',
            'impact': 'Medium - Improves comfort'
        })
    
    # Return top recommendations (max 5)
    return recommendations[:5] if recommendations else [
        {
            'title': '✅ Design Optimized',
            'description': 'Your design performs well across all metrics. Consider this version as a strong baseline.',
            'impact': 'Excellent - No urgent improvements needed'
        }
    ]


def get_improvement_priority(recommendations):
    """
    Prioritize recommendations by impact.
    
    Args:
        recommendations: List of recommendation dictionaries
    
    Returns:
        Sorted list with highest impact recommendations first
    """
    impact_order = {'High': 0, 'Medium': 1, 'Low': 2}
    
    sorted_recs = sorted(
        recommendations,
        key=lambda x: impact_order.get(x['impact'].split(' - ')[0], 999)
    )
    
    return sorted_recs


def generate_design_checklist(scores, metrics):
    """
    Generate a design quality checklist.
    
    Args:
        scores: Scores dictionary
        metrics: Metrics dictionary
    
    Returns:
        Dictionary with checklist items and completion status
    """
    checklist = {
        'Attention': {
            'passed': scores['Attention Score'] > 40,
            'description': 'Design captures viewer attention'
        },
        'Simplicity': {
            'passed': scores['Cognitive Load'] < 60,
            'description': 'Design is easy to understand'
        },
        'Contrast': {
            'passed': metrics.get('Contrast Ratio', 1) > 3,
            'description': 'Good contrast between elements'
        },
        'Balance': {
            'passed': metrics.get('Balance Score', 0) > 0.5,
            'description': 'Visual elements are balanced'
        },
        'Focus': {
            'passed': metrics.get('Focus Score', 0) > 0.4,
            'description': 'Clear focal points present'
        },
        'Color Harmony': {
            'passed': 0.2 < metrics.get('Color Diversity', 0) < 0.7,
            'description': 'Color palette is harmonious'
        }
    }
    
    return checklist