import numpy as np
import cv2

def calculate_scores(image):
    """
    Calculate basic design analysis scores from a saliency map.
    
    Args:
        image: Input image (saliency map) as numpy array
    
    Returns:
        Dictionary with:
        - Attention Score: Average brightness (0-100), higher = more attention capture
        - Cognitive Load: Standard deviation of brightness, higher = more complex
    """
    # Convert to grayscale by averaging RGB channels
    if len(image.shape) == 3:
        gray = np.mean(image, axis=2)
    else:
        gray = image.astype(float)
    
    # Attention Score: Mean intensity normalized to 0-100 scale
    # Higher values indicate more visually prominent/attention-grabbing areas
    attention_score = (np.mean(gray) / 255) * 100
    
    # Cognitive Load: Standard deviation of pixel values
    # Higher values indicate more visual variation/complexity
    cognitive_load = np.std(gray)

    return {
        "Attention Score": round(attention_score, 2),
        "Cognitive Load": round(cognitive_load, 2)
    }


def get_detailed_metrics(saliency_map, original_image=None):
    """
    Calculate detailed visual metrics from images.
    
    Args:
        saliency_map: Saliency map image
        original_image: Optional original image for additional metrics
    
    Returns:
        Dictionary with comprehensive design metrics
    """
    metrics = {}
    
    # Convert to grayscale if needed
    if len(saliency_map.shape) == 3:
        gray_saliency = cv2.cvtColor(saliency_map, cv2.COLOR_RGB2GRAY)
    else:
        gray_saliency = saliency_map.astype("uint8")
    
    # Basic brightness metrics
    metrics['Brightness Mean'] = round(np.mean(gray_saliency) / 255, 2)
    metrics['Brightness Std'] = round(np.std(gray_saliency) / 255, 2)
    
    # Contrast Ratio (using WCAG formula)
    L1 = np.mean(gray_saliency) / 255
    metrics['Contrast Ratio'] = round((L1 + 0.05) / (1 - L1 + 0.05) if L1 < 0.5 else (L1 + 0.05) / (0.05), 2)
    
    # Visual Complexity (based on edge detection)
    edges = cv2.Canny(gray_saliency, 50, 150)
    metrics['Edge Density'] = round(np.sum(edges > 0) / edges.size, 2)
    
    # Color metrics (if original image available)
    if original_image is not None:
        if len(original_image.shape) == 3:
            # Convert to HSV for color analysis
            hsv = cv2.cvtColor(original_image.astype("uint8"), cv2.COLOR_RGB2HSV)
            
            # Saturation analysis
            saturation = hsv[:, :, 1] / 255
            metrics['Saturation Level'] = round(np.mean(saturation), 2)
            
            # Color diversity
            h = hsv[:, :, 0]
            metrics['Color Diversity'] = round(np.std(h) / 180, 2)
        else:
            metrics['Saturation Level'] = 0.0
            metrics['Color Diversity'] = 0.0
    else:
        metrics['Saturation Level'] = 0.0
        metrics['Color Diversity'] = 0.0
    
    # Visual Complexity (overall measure)
    metrics['Visual Complexity'] = round(
        (metrics['Edge Density'] + metrics['Brightness Std'] + metrics['Color Diversity']) / 3,
        2
    )
    
    # Focus Score (concentration of attention)
    hist = cv2.calcHist([gray_saliency], [0], None, [256], [0, 256])
    entropy = -np.sum((hist / hist.sum()) * np.log2(hist / hist.sum() + 1e-10))
    metrics['Focus Score'] = round(1 - (entropy / 8), 2)  # Normalize to 0-1
    
    # Balance Score (symmetry analysis)
    h, w = gray_saliency.shape[:2]
    left = gray_saliency[:, :w // 2]
    right = gray_saliency[:, w // 2:]
    
    # Handle size mismatch
    if right.shape[1] < left.shape[1]:
        left = left[:, :-1]
    elif right.shape[1] > left.shape[1]:
        right = right[:, :-1]
    
    left_mean = np.mean(left)
    right_mean = np.mean(right)
    balance = 1 - (abs(left_mean - right_mean) / 255)
    metrics['Balance Score'] = round(balance, 2)
    
    return metrics


def calculate_design_quality_score(scores, metrics):
    """
    Calculate overall design quality score based on multiple factors.
    
    Args:
        scores: Basic scores dictionary
        metrics: Detailed metrics dictionary
    
    Returns:
        Float value 0-100 representing overall design quality
    """
    # Weight different factors
    weights = {
        'attention': 0.25,      # 25% - Attention capture
        'simplicity': 0.25,     # 25% - Low cognitive load
        'contrast': 0.15,       # 15% - Good contrast
        'balance': 0.15,        # 15% - Visual balance
        'focus': 0.10,          # 10% - Clear focus points
        'color': 0.10           # 10% - Color harmony
    }
    
    # Normalize scores to 0-100
    attention_normalized = min(scores['Attention Score'], 100)
    simplicity_normalized = 100 - min(scores['Cognitive Load'], 100)
    contrast_normalized = min(metrics.get('Contrast Ratio', 1) * 20, 100)
    balance_normalized = metrics.get('Balance Score', 0.5) * 100
    focus_normalized = metrics.get('Focus Score', 0.5) * 100
    color_normalized = min(metrics.get('Color Diversity', 0) * 100, 100)
    
    # Calculate weighted score
    quality_score = (
        attention_normalized * weights['attention'] +
        simplicity_normalized * weights['simplicity'] +
        contrast_normalized * weights['contrast'] +
        balance_normalized * weights['balance'] +
        focus_normalized * weights['focus'] +
        color_normalized * weights['color']
    )
    
    return round(quality_score, 2)


def get_score_rating(score):
    """
    Get a qualitative rating for a numeric score.
    
    Args:
        score: Numeric score (0-100)
    
    Returns:
        String rating and emoji
    """
    if score >= 80:
        return "Excellent", "🟢"
    elif score >= 60:
        return "Good", "🟢"
    elif score >= 40:
        return "Average", "🟡"
    else:
        return "Poor", "🔴"


def compare_scores(scores_list, labels=None):
    """
    Compare multiple design scores.
    
    Args:
        scores_list: List of score dictionaries
        labels: Optional list of labels for each score set
    
    Returns:
        Dictionary with comparison results
    """
    if labels is None:
        labels = [f"Design {i+1}" for i in range(len(scores_list))]
    
    comparison = {
        'labels': labels,
        'attention_scores': [s['Attention Score'] for s in scores_list],
        'cognitive_loads': [s['Cognitive Load'] for s in scores_list],
        'best_attention': labels[np.argmax([s['Attention Score'] for s in scores_list])],
        'best_simplicity': labels[np.argmin([s['Cognitive Load'] for s in scores_list])]
    }
    
    return comparison


def get_score_improvement_suggestions(scores):
    """
    Generate suggestions for improving design scores.
    
    Args:
        scores: Scores dictionary
    
    Returns:
        List of improvement suggestions
    """
    suggestions = []
    
    attention = scores['Attention Score']
    load = scores['Cognitive Load']
    
    if attention < 40:
        suggestions.append("Increase visual contrast to draw more attention")
    elif attention > 70:
        suggestions.append("Design successfully captures attention")
    
    if load > 60:
        suggestions.append("Simplify the design to reduce cognitive load")
    elif load < 20:
        suggestions.append("Design is clean and easy to understand")
    
    return suggestions