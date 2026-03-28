import numpy as np

# Predefined personas with detailed characteristics
PERSONAS = {
    "General Viewer": {
        "factor": 1.0,
        "description": "Neutral viewer with balanced attention patterns",
        "focus_areas": ["center", "edges"],
        "attention_bias": 1.0
    },
    "Recruiter": {
        "factor": 1.1,
        "description": "Focuses on text-heavy areas and credentials",
        "focus_areas": ["top", "left"],
        "attention_bias": 1.1
    },
    "Social Media User": {
        "factor": 1.3,
        "description": "Attracted to visual elements and bright colors",
        "focus_areas": ["center", "images"],
        "attention_bias": 1.3
    },
    "E-commerce Shopper": {
        "factor": 1.2,
        "description": "Focuses on product images and price information",
        "focus_areas": ["center", "right"],
        "attention_bias": 1.2
    },
    "Mobile User": {
        "factor": 1.15,
        "description": "Scans vertically, focuses on top elements",
        "focus_areas": ["top", "center"],
        "attention_bias": 1.15
    }
}

def apply_persona(map_data, persona):
    """
    Apply persona-specific adjustments to the saliency map.
    
    Args:
        map_data: The saliency map (numpy array)
        persona: The selected viewer persona (string or dict)
    
    Returns:
        Modified saliency map with persona-specific weighting (numpy array uint8)
    """
    # Get persona factor
    if isinstance(persona, str):
        if persona in PERSONAS:
            factor = PERSONAS[persona]["factor"]
        else:
            # For custom personas, default to 1.0
            factor = 1.0
    else:
        factor = persona.get("factor", 1.0)
    
    # Apply the factor and clip values to valid range [0, 255]
    adjusted = np.clip(map_data.astype(float) * factor, 0, 255).astype("uint8")
    return adjusted


def create_custom_persona(name, focus_intensity, focus_areas=None):
    """
    Create a custom viewer persona with specific characteristics.
    
    Args:
        name: Custom persona name
        focus_intensity: Multiplier for attention (1.0 to 2.0)
        focus_areas: List of focus areas (e.g., ["center", "top"])
    
    Returns:
        Dictionary representing the custom persona
    """
    return {
        "name": name,
        "factor": focus_intensity,
        "description": f"Custom persona with {focus_intensity}x focus intensity",
        "focus_areas": focus_areas or ["center"],
        "attention_bias": focus_intensity
    }


def get_persona_info(persona):
    """
    Get detailed information about a persona.
    
    Args:
        persona: Persona name (string) or persona dict
    
    Returns:
        Dictionary with persona details
    """
    if isinstance(persona, str) and persona in PERSONAS:
        return PERSONAS[persona]
    elif isinstance(persona, dict):
        return persona
    else:
        return PERSONAS["General Viewer"]


def apply_advanced_persona_adjustments(map_data, persona, img_array=None):
    """
    Apply advanced persona adjustments including spatial weighting.
    
    Args:
        map_data: The saliency map (numpy array)
        persona: The persona (string or dict)
        img_array: Optional original image for advanced processing
    
    Returns:
        Enhanced saliency map with persona-specific adjustments
    """
    # Get base adjustment
    adjusted = apply_persona(map_data, persona)
    
    # If we have the original image, apply spatial weighting
    if img_array is not None and isinstance(persona, str):
        persona_info = PERSONAS.get(persona, {})
        focus_areas = persona_info.get("focus_areas", ["center"])
        
        # Create spatial mask based on focus areas
        h, w = adjusted.shape[:2]
        mask = np.zeros((h, w))
        
        if "center" in focus_areas:
            # Enhance center region
            y_center = h // 2
            x_center = w // 2
            y_range = h // 4
            x_range = w // 4
            mask[y_center - y_range:y_center + y_range, 
                 x_center - x_range:x_center + x_range] = 0.3
        
        if "top" in focus_areas:
            # Enhance top region
            mask[:h // 4, :] += 0.2
        
        if "left" in focus_areas:
            # Enhance left region
            mask[:, :w // 4] += 0.2
        
        if "right" in focus_areas:
            # Enhance right region
            mask[:, 3 * w // 4:] += 0.2
        
        # Apply spatial mask to adjusted map
        mask = np.clip(mask, 0, 1)
        if len(adjusted.shape) == 3:
            mask = np.stack([mask] * 3, axis=2)
        
        adjusted = np.clip(adjusted.astype(float) * (1 + mask), 0, 255).astype("uint8")
    
    return adjusted


def compare_personas(map_data, personas_list):
    """
    Compare how different personas perceive the same design.
    
    Args:
        map_data: The original saliency map
        personas_list: List of persona names to compare
    
    Returns:
        Dictionary with adjusted maps for each persona
    """
    results = {}
    for persona in personas_list:
        results[persona] = apply_persona(map_data, persona)
    return results