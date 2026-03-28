import cv2
import numpy as np
from scipy import ndimage

def get_saliency_map(image, algorithm="Spectral Residual"):
    """
    Generate a saliency map showing areas of visual attention in an image.
    
    Args:
        image: Input image as numpy array (BGR or RGB)
        algorithm: Type of saliency detection
                   - "Spectral Residual": Fast, global method
                   - "Fine Grained": Detailed local detection
                   - "Multi-Scale": Combines multiple scales
    
    Returns:
        Blended image with saliency heatmap overlaid (RGB for display)
    """
    # Ensure image is uint8
    image = image.astype("uint8")

    # Convert RGBA -> RGB if needed
    if image.shape[-1] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    elif len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    # Convert RGB -> BGR for OpenCV processing
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # Select algorithm
    if algorithm == "Spectral Residual":
        saliency_map = _spectral_residual_saliency(image_bgr)
    elif algorithm == "Fine Grained":
        saliency_map = _fine_grained_saliency(image_bgr)
    elif algorithm == "Multi-Scale":
        saliency_map = _multi_scale_saliency(image_bgr)
    else:
        saliency_map = _spectral_residual_saliency(image_bgr)
    
    # Normalize saliency map to 0-255 range
    saliency_map = (saliency_map * 255).astype("uint8")
    
    # Apply JET colormap for heatmap visualization
    heatmap = cv2.applyColorMap(saliency_map, cv2.COLORMAP_JET)
    
    # Blend original image (60%) with heatmap (40%)
    blended = cv2.addWeighted(image_bgr, 0.6, heatmap, 0.4, 0)

    # Convert BGR -> RGB for display in Streamlit
    blended = cv2.cvtColor(blended, cv2.COLOR_BGR2RGB)
    
    return blended


def _spectral_residual_saliency(image):
    """
    Spectral Residual saliency detection.
    Fast global method based on frequency domain analysis.
    """
    saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
    success, saliency_map = saliency.computeSaliency(image)
    
    if not success:
        raise Exception("Spectral Residual saliency detection failed")
    
    return saliency_map


def _fine_grained_saliency(image):
    """
    Fine-grained saliency detection.
    More detailed local feature detection.
    """
    saliency = cv2.saliency.StaticSaliencyFineGrained_create()
    success, saliency_map = saliency.computeSaliency(image)
    
    if not success:
        raise Exception("Fine-grained saliency detection failed")
    
    return saliency_map


def _multi_scale_saliency(image):
    """
    Multi-scale saliency detection.
    Combines saliency detection at multiple image scales.
    """
    # Get saliency maps at different scales
    scales = [0.5, 1.0, 1.5]
    saliency_maps = []
    
    for scale in scales:
        h, w = image.shape[:2]
        resized = cv2.resize(image, (int(w * scale), int(h * scale)))
        
        saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
        success, smap = saliency.computeSaliency(resized)
        
        if success:
            # Resize back to original size
            smap = cv2.resize(smap, (w, h))
            saliency_maps.append(smap)
    
    if not saliency_maps:
        raise Exception("Multi-scale saliency detection failed")
    
    # Combine multi-scale maps
    combined = np.mean(saliency_maps, axis=0)
    return combined


def get_multi_saliency_maps(image):
    """
    Generate saliency maps using all available algorithms.
    
    Args:
        image: Input image as numpy array
    
    Returns:
        Dictionary with saliency maps for each algorithm
    """
    results = {}
    algorithms = ["Spectral Residual", "Fine Grained", "Multi-Scale"]
    
    for algo in algorithms:
        try:
            results[algo] = get_saliency_map(image, algo)
        except Exception as e:
            results[algo] = None
    
    return results


def enhance_saliency_map(saliency_map, enhancement_type="contrast"):
    """
    Enhance saliency map visualization.
    
    Args:
        saliency_map: Input saliency map (0-255)
        enhancement_type: Type of enhancement
                         - "contrast": Increase contrast
                         - "brightness": Increase brightness
                         - "sharpen": Sharpen features
    
    Returns:
        Enhanced saliency map
    """
    if enhancement_type == "contrast":
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(saliency_map)
    
    elif enhancement_type == "brightness":
        # Increase brightness
        enhanced = np.clip(saliency_map.astype(float) * 1.2, 0, 255).astype("uint8")
    
    elif enhancement_type == "sharpen":
        # Apply unsharp masking
        blurred = cv2.GaussianBlur(saliency_map, (0, 0), 1.0)
        enhanced = cv2.addWeighted(saliency_map, 1.5, blurred, -0.5, 0)
        enhanced = np.clip(enhanced, 0, 255).astype("uint8")
    
    else:
        enhanced = saliency_map
    
    return enhanced


def get_attention_regions(saliency_map, num_regions=3, threshold_percentile=75):
    """
    Extract the most attended regions from a saliency map.
    
    Args:
        saliency_map: Input saliency map
        num_regions: Number of regions to extract
        threshold_percentile: Percentile for thresholding
    
    Returns:
        List of bounding boxes for attention regions
    """
    # Convert to grayscale if needed
    if len(saliency_map.shape) == 3:
        gray = cv2.cvtColor(saliency_map, cv2.COLOR_BGR2GRAY)
    else:
        gray = saliency_map
    
    # Threshold based on percentile
    threshold = np.percentile(gray, threshold_percentile)
    binary = (gray > threshold).astype("uint8") * 255
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort by area and get top regions
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:num_regions]
    
    regions = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        regions.append((x, y, w, h))
    
    return regions


def create_heatmap_video(saliency_map, num_frames=10):
    """
    Create an animated heatmap showing gradual attention buildup.
    
    Args:
        saliency_map: Input saliency map
        num_frames: Number of frames for animation
    
    Returns:
        List of animated frames
    """
    frames = []
    
    for i in range(num_frames):
        # Gradually increase opacity of heatmap
        alpha = (i + 1) / num_frames
        
        # Create frame with gradually revealed heatmap
        frame = cv2.applyColorMap(saliency_map, cv2.COLORMAP_JET)
        frame = cv2.addWeighted(frame, alpha, np.zeros_like(frame), 1 - alpha, 0)
        
        frames.append(frame)
    
    return frames