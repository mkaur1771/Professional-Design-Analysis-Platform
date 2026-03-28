# Professional-Design-Analysis-Platform
DesignLens AI is an AI-powered system that evaluates visual designs by simulating human attention, measuring cognitive load, and generating actionable insights using computer vision.

## ✨ Features

### Analysis Modes (4 Types)
- **Single Analysis** - Analyze individual designs with comprehensive metrics
- **A/B Testing** - Compare two designs side-by-side
- **Batch Upload** - Analyze 5-50+ designs at once
- **Analytics Dashboard** - Track history and trends over time

### Saliency Detection (3 Algorithms)
- **Spectral Residual** - Fast, global analysis (best for batch processing)
- **Fine Grained** - Detailed, local feature detection
- **Multi-Scale** - Comprehensive analysis across multiple scales

### Design Metrics (10+)
```
✅ Attention Score (0-100)      → How well design captures attention
✅ Cognitive Load (0-100)       → Design complexity
✅ Contrast Ratio               → WCAG compliance
✅ Visual Complexity            → Overall busyness
✅ Color Diversity              → Color variety
✅ Edge Density                 → Detail amount
✅ Brightness Analysis          → Luminance levels
✅ Saturation Level             → Color intensity
✅ Focus Score                  → Attention concentration
✅ Balance Score                → Visual symmetry
```

### Intelligent Recommendations (13+ Types)
Each recommendation includes:
- Specific, actionable title
- Detailed description
-  Impact level (High/Medium/Low)

**Recommendation Categories:**
- Visual Hierarchy & Layout
- Color & Contrast Optimization
- Complexity Reduction
- Element Management
- Visual Balance & Symmetry
- Detail & Texture Adjustments
- Brightness & Saturation Tuning
- Focus Point Creation

###  Viewer Personas (5 Presets + Custom)
- **General Viewer** - Baseline, balanced attention (1.0x)
- **Recruiter** - Text-focused, credential attention (1.1x)
- **Social Media User** - Visual-focused, color attracted (1.3x)
- **E-commerce Shopper** - Product-focused, price attention (1.2x)
- **Mobile User** - Vertical scanning, top-focused (1.15x)
- **Custom Creator** - Define your own persona with custom intensity

###  Export Formats
- **PNG** - Download attention heatmap visualization
- **PDF** - Professional report with scores, insights, and recommendations
- **CSV** - Batch analysis results (batch mode)

###  Performance
- First analysis: **2-3 seconds**
- Cached analysis: **<100ms** (90% faster)
- Batch speed: **500ms per 10 designs**
- Caching system for instant reloads

##  User Interface
- **Glassmorphism Design** - Modern, professional aesthetics
- **Dark Mode** - Eye-friendly interface
- **Responsive Layout** - Works on desktop and tablet
- **Smooth Animations** - Enhanced user experience
- **Color-Coded Indicators** - Easy score interpretation (🟢🟡🔴)

## Usage Examples

### Single Design Analysis
```python
1. Upload your design image (PNG, JPG, JPEG)
2. Select viewer persona
3. Choose analysis algorithm
4. Get results in 2-3 seconds
5. Download PNG heatmap or PDF report
```

### A/B Testing
```python
1. Upload Design A
2. Upload Design B
3. Select persona
4. View side-by-side metrics
5. Identify winning design
```

### Batch Analysis
```python
1. Upload 5-50+ designs
2. Select persona
3. Analyze all at once
4. Export CSV results
5. Get batch statistics
```

## Sample Analysis Results

```
Design: Homepage Banner
Persona: Social Media User
Algorithm: Spectral Residual

SCORES:
├─ Attention Score: 75 ✅ (Excellent)
├─ Cognitive Load: 35 ✅ (Good)
├─ Contrast Ratio: 5.2 ✅ (WCAG AA)
├─ Visual Complexity: 0.45 ✅ (Balanced)
└─ Balance Score: 0.68 ✅ (Well-balanced)

INSIGHTS:
✅ Strong attention capture
✅ Clean and easy to process
⚡ Balanced design with good engagement

RECOMMENDATIONS:
1. Visual Hierarchy (HIGH) - Make important elements 2-3x larger
2. Color Variety (MEDIUM) - Add 2-3 complementary colors
```

## 🔧 Project Structure

```
designlens-ai/
├── app.py                 # Main Streamlit application
├── saliency.py           # Saliency detection algorithms
├── scoring.py            # Metrics calculation
├── insights.py           # Insights & recommendations
├── persona.py            # Viewer persona management
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## File Descriptions

### `app.py` (500+ lines)
Main application with:
- 4 analysis modes
- UI management
- Session state handling
- Caching system
- File export functionality

### `saliency.py` (300+ lines)
Saliency detection with:
- 3 detection algorithms
- Image processing utilities
- Heatmap generation
- Region extraction

### `scoring.py` (200+ lines)
Metrics calculation:
- 10+ design metrics
- Quality scoring
- Comparison tools
- Rating system

### `insights.py` (250+ lines)
AI insights generation:
- 13+ recommendation types
- Impact rating
- Design checklist
- Improvement priorities

### `persona.py` (200+ lines)
Persona management:
- 5 predefined personas
- Custom persona creator
- Spatial weighting
- Persona comparison

## How to Interpret Scores

### Attention Score (0-100)
```
🔴 0-40:   Too subtle, needs emphasis
🟡 40-60:  Moderate, acceptable
🟢 60-80:  Good, well-noticed
🟢 80-100: Excellent, very prominent
```

### Cognitive Load (0-100)
```
🟢 0-25:   Minimal (might be too simple)
🟢 25-50:  Optimal (just right!)
🟡 50-75:  High (getting complex)
🔴 75-100: Very high (too cluttered)
```

## Best Practices

### For Optimal Analysis
1. ✅ Use high-quality images (300px+ width)
2. ✅ Test with multiple personas
3. ✅ Use A/B testing for comparisons
4. ✅ Prioritize HIGH-impact recommendations
5. ✅ Re-analyze after implementing changes

### For Batch Processing
1. ✅ Upload 5-50+ designs for bulk review
2. ✅ Use same persona for consistency
3. ✅ Export CSV for stakeholder reports
4. ✅ Identify patterns across designs
5. ✅ Track improvements over time

##  Troubleshooting

### "Analysis is slow"
→ Use Spectral Residual algorithm or reduce image size

### "Low attention score"
→ Check recommendations: increase contrast, add focal points

### "High cognitive load"
→ Simplify design: remove elements, increase whitespace

### "PDF export not working"
→ Install reportlab: `pip install reportlab`

##  Performance Benchmarks

```
Single Analysis:
├─ First run: 2-3 seconds
├─ Cached: <100ms
└─ Memory: ~150MB

Batch Analysis (10 designs):
├─ Total time: ~5 seconds
├─ Per design: ~500ms
└─ Memory: ~300MB

Algorithm Comparison:
├─ Spectral Residual: Fastest (1-2s)
├─ Fine Grained: Balanced (2-3s)
└─ Multi-Scale: Comprehensive (3-4s)
```

## 📈 Use Cases

### For Designers
- Optimize designs before presentation
- A/B test design variations
- Get data-driven feedback
- Track improvements over time

### For Marketing Teams
- Evaluate marketing materials
- Compare campaign designs
- Ensure brand consistency
- Optimize visual impact

### For Product Teams
- Analyze UI/UX designs
- Test design iterations
- Validate design decisions
- Document design quality

### For Agencies
- Batch review client work
- Generate professional reports
- Build design portfolio
- Educate clients on design metrics

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) - The fastest way to build ML apps
- Uses [OpenCV](https://opencv.org/) - Computer vision library
- Powered by [NumPy](https://numpy.org/) - Numerical computing
