AI Course PDF Generator
Overview
This project is a Python-based utility designed to create visually appealing and structured course PDFs using AI. It combines elements like HTML templates, AI-generated content, and customizable styles to streamline the creation of course materials. The generator uses OpenAI's GPT models to generate content and integrate it into predefined HTML layouts, which are then converted into PDFs.

Features
AI-Powered Content Creation:

Generate course topics, headings, and content using GPT prompts.
Seamlessly combine AI-generated text with predefined templates.
Customizable Layouts:

Multiple reference HTML templates to style the content.
Automatic inclusion of styles and colors based on user preferences.
Dynamic PDF Generation:

Converts AI-generated HTML content into PDFs with consistent formatting.
Supports inline replacement of placeholder images and colors.
File Integration:

Option to use existing content files for headings and text.
Saves and retrieves content to/from a file for reuse.
Requirements
Python 3.7 or later.
Dependencies:
argparse: Command-line argument parsing.
Custom utilities from utils for interacting with AI, handling HTML/PDF, and managing files.
prompts module for structured GPT interactions.
Key Components
1. AI Integration:
Generates course layout and headings using a prompt system.
Retrieves additional content and suggestions for each section.
2. HTML Templates:
Predefined templates for common layouts, including:
Cards with icons and headers.
Step-by-step guides.
Checklists and tables.
Each template has a detailed description and associated HTML structure.
3. Styles and Colors:
Configurable styles using color codes for background, titles, and elements.
Inline replacement of default colors for enhanced customization.
4. PDF Conversion:
Generates final course content in HTML format.
Converts HTML into a professionally styled PDF.
How to Use
Command-Line Arguments
--use-file: Use existing content.txt for headings and content.
Steps
Generate a New Course:

Run the script without --use-file.
Input the course topic when prompted.
The script will generate headings and content using GPT.
Use Existing Content:

Prepare a content.txt file with headings and content separated by blank lines.
Run the script with --use-file.
Output:

The final HTML is saved as FINAL.html.
PDF generation (if enabled) creates a styled PDF.
File Structure
course-creator.py: Main script for generating courses.
utils.py: Helper functions for interacting with GPT, HTML/PDF conversion, and file operations.
prompts.py: Contains GPT prompts for layout and content generation.
content.txt: Optional file for pre-defined content.
references/: Directory containing HTML templates for different layouts.
Examples
Generating a New Course:
bash
Copy
Edit
python course-creator.py
Follow the prompts to enter a course topic and generate content.

Using Existing Content:
bash
Copy
Edit
python course-creator.py --use-file
Future Enhancements
Image Generation:
Automatically insert AI-generated images relevant to the content.
Enhanced Customization:
Allow user-defined layouts and styles.
Export Options:
Support additional output formats like PowerPoint slides.
