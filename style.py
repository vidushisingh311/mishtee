mishtee_css = """
/* Import elegant fonts */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500&family=Inter:wght@300;400&display=swap');

/* Main Container - Off-White Background */
.gradio-container {
    background-color: #FAF9F6 !important;
    font-family: 'Inter', sans-serif !important;
    color: #333333 !important;
}

/* Headings - Sophisticated Serif */
h1, h2, h3, .section-header {
    font-family: 'Playfair Display', serif !important;
    font-weight: 400 !important;
    letter-spacing: 0.05em !important;
    color: #333333 !important;
    margin-bottom: 1.5rem !important;
}

/* Buttons - Sober Terracotta & Sharp Edges */
button.primary, .gr-button-lg {
    background: #C06C5C !important;
    color: white !important;
    border: none !important;
    border-radius: 0px !important; /* Sharp corners */
    padding: 12px 24px !important;
    font-family: 'Inter', sans-serif !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    font-size: 0.85rem !important;
    transition: background 0.3s ease !important;
}

button.primary:hover {
    background: #A65D4F !important;
}

/* Inputs and Boxes - Thin Borders & No Shadows */
.gr-input, .gr-box, .gr-panel {
    border: 1px solid #D1D1D1 !important;
    border-radius: 0px !important;
    background-color: #FFFFFF !important;
    box-shadow: none !important; /* Remove bubbles/shadows */
}

/* Tables - Lightweight Sans-Serif */
table {
    font-family: 'Inter', sans-serif !important;
    font-weight: 300 !important;
    border-collapse: collapse !important;
    width: 100% !important;
}

th, td {
    border-bottom: 1px solid #EEEEEE !important;
    padding: 15px !important;
    text-align: left !important;
}

/* Spacing and Padding - High Whitespace */
.gr-block, .gr-form {
    margin-bottom: 2.5rem !important;
    padding: 20px !important;
}

/* Remove default Gradio focus rings */
*:focus {
    outline: 1px solid #C06C5C !important;
    box-shadow: none !important;
}
"""
