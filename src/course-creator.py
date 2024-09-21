import argparse
from utils import GPT, html_to_pdf, get_image_url, get_html_style, html, save_html
from prompts import layout_system_prompt, layout_user_prompt, element_decider_prompt, heading_content_prompt, element_adder_prompt, styles_colors_prompt
import re
# from test import replace_placeholders


# Paths
content_file_path = "./content.txt"

# Data structure to hold reference HTML, name, and description
elements = {
    "ref1": html("./references/ref1.html"), 
    "ref2": html("./references/ref2.html"), 
    "ref3": html("./references/ref3.html"),
    "ref4": html("./references/ref4.html"), 
    "ref5": html("./references/ref5.html")
}

elements_explained = {
    "ref1": "A rectangular, centered card with rounded corners and a subtle shadow, giving it an elevated appearance. It features a header with an icon on the left and text to the right, followed by a highlighted middle section with a different background color. Below this, four horizontal, colored bars each contain an icon and text, and the card concludes with a footer containing a paragraph. This card style can effectively display performance metrics of a product or service, summarizing key improvements and achievements, or present an overview of a case study, highlighting main results and impacts in an organized, visually appealing manner.",
    "ref2": "A structured, hierarchical layout with a bold, centered title and subtitle at the top, followed by horizontally aligned sections. Each section has a title in a rounded rectangle, and a dashed-line border encloses a list of bullet points. This layout can effectively display categorized instructional materials, such as required tools for different modules or steps and equipment needed for various experiments in a science or engineering class.",
    "ref3": "A checklist organized into sections with blue headers and lists of bullet points. The bold headers categorize items into \"Content and Organization,\" \"Clarity and Coherence,\" \"Language and Style,\" and \"Grammar and Mechanics,\" with each bullet point featuring a question and a corresponding radio button. This checklist can be used for evaluating written work in educational settings, ensuring all key aspects are assessed, or for peer reviews and self-assessments to help students systematically improve their writing skills.",
    "ref4": "A rectangular layout with a prominent title section at the top, followed by an introduction and several horizontally aligned colored boxes arranged in a two-column format. Below the boxes, there is an additional explanatory section and a color-coordinated table that matches the boxes above. This layout, characterized by its clean, structured design and use of distinct background colors for visual separation, can effectively display educational content such as summarizing key concepts and their detailed explanations in a lesson, or presenting different categories of information along with their corresponding details for easy reference.",
    "ref5": "A step-by-step instructional guide formatted into a vertical layout with distinct colored sections. Each section contains a step number with a colored background and a brief description, followed by an example or further explanation in a bordered box. The design uses clear separation between steps with alternating colors to enhance readability and guide the viewer through the process. This type of layout can be used to display instructional content such as tutorials or how-to guides, where each step needs to be clearly distinguished and explained in sequence, or for process documentation in educational materials, helping learners understand complex procedures in a structured and visually appealing manner.",
}

colors = {"bg": "#a0a0a0", 
          "titles": "#00e1ff",
          "terms": "#fb0000",
          "c1": "#2474c0",
          "c2": "#5070ab",
          "c3": "#43b9b3",
          "c4": "#496689",
          }

replace_colors = ["#ccffcc", "#ccccff", "#ffcc99", "#ffccff"]

title_boxes = {
    "title1": """
    <style>
        .title-box {{
            background-color: {bg};
            padding: 20px;
            text-align: center;
            border-radius: 15px;
            margin-bottom: 20px;
        }}
        .title-box h1 {{
            color: {title};
            font-family: 'Optima', 'Arial', sans-serif;
            font-size: 3em;
            font-weight: bold;
            margin: 0;
        }}
        .title-box:not(:first-of-type) {{
            margin-top: 20px; /* Adjust the top margin value as needed */
        }}
    </style>
    """.format(bg=colors["bg"], title=colors["titles"]),
}
# default_table= {
#     """
#     <style>
#         table {
#             width: 80%; /* Adjust the width as needed */
#             margin: 20px auto; /* Center the table horizontally */
#             border-collapse: collapse; /* Ensure borders don't double up */
#         }

#         th, td {
#             padding: 12px 15px; /* Add padding for better readability */
#             border: 1px solid #ddd; /* Add border for clarity */
#             text-align: center; /* Center the text in each cell */
#         }

#         th {
#             background-color: #00e1ff; /* Add a background color to the header */
#             color: #ffffff; /* Text color for the header */
#             font-weight: bold; /* Make the header text bold */
#         }

#         tr:nth-child(even) {
#             background-color: #f2f2f2; /* Add alternating row colors */
#         }

#         tr:hover {
#             background-color: #f5f5f5; /* Highlight row on hover */
#         }
#     </style>
#     """
#     }

def replace_inline_colors(html_content, replace_colors, colors):
    for i, old_color in enumerate(replace_colors):
        new_color = colors[f'c{i+1}']
        pattern = re.compile(rf'background-color:\s*{re.escape(old_color)}', re.IGNORECASE)
        html_content = pattern.sub(f'background-color: {new_color}', html_content)
    
    # Replace specific background-color value for #C4C8F3 with the "titles" color
    titles_pattern = re.compile(r'background-color:\s*#C4C8F3', re.IGNORECASE)
    html_content = titles_pattern.sub(f'background-color: {colors["titles"]}', html_content)
    
    # Replace specific background-color value for #000000 with the "bg" color
    bg_pattern = re.compile(r'background-color:\s*#000000', re.IGNORECASE)
    html_content = bg_pattern.sub(f'background-color: {colors["bg"]}', html_content)
    
    # Replace specific color value for #5F6AE8 with the "terms" color
    terms_pattern = re.compile(r'color:\s*#5F6AE8', re.IGNORECASE)
    html_content = terms_pattern.sub(f'color: {colors["terms"]}', html_content)

    return html_content




def create_section_content(heading, topic, use_file, element_descriptions):
    if use_file:
        # Read section content from a file
        with open(content_file_path, "r") as file:
            content = file.read().split("\n\n")
        section_content = content.pop(0) if content else ""
    else:
        # Generate section content using AI
        section_content = GPT("You are a professional course creator and content writer.", heading_content_prompt(topic, heading))
        # Save the content immediately after generating
        with open(content_file_path, "a") as file:
            file.write(section_content + "\n\n")
    return section_content

def create_section_html(heading, topic, use_file, curr_elements):
    element_descriptions = ""
    proper_elements = {}
    if curr_elements:
        for element in curr_elements:
            if element in elements_explained:
                element_descriptions += "\n".join([f"{element}: {elements_explained[element]}"])
                proper_elements[element] = elements[element]
    
    section_content = create_section_content(heading, topic, use_file, element_descriptions)
    print("Elements being used in this section:", list(proper_elements.keys()))
    section_html = GPT("You are a professional HTML/CSS Developer", element_adder_prompt(topic, section_content, proper_elements, element_descriptions)) + "\n"
    return section_html

def get_section_elements(heading, previous_sections, all_elements_used):
    curr_elements = ""
    elements_prompt = element_decider_prompt(course_topic, heading, elements_explained, previous_sections)
    curr_elements = GPT("You are a professional planner for course creation", elements_prompt).split("\n")
    return curr_elements

def remove_code_markers(input_string):
    # Replace all occurrences of "```html" and "```" with an empty string
    cleaned_string = input_string.replace("```html", "").replace("```", "")
    return cleaned_string.strip()

# TODO: Image proper URLs
def generate_course(course_topic, use_file):
    print("Generating course on", course_topic)

    if use_file:
        # Read headings and content from a file
        with open(content_file_path, "r") as file:
            headings_and_content = file.read().split("\n\n")
            headings = headings_and_content[0].split("\n")
            content_sections = headings_and_content[1:]
        print("Loaded headings and content from file.")
    else:
        # Generate headings using AI
        course_layout = GPT(layout_system_prompt, layout_user_prompt + course_topic)
        headings = course_layout.split("\n")

        # Save the headings to a file immediately
        with open(content_file_path, "w") as file:
            file.write("\n".join(headings) + "\n\n")

    previous_sections = []
    all_elements_used = set()
    all_content = ""
    
    for heading in headings:
        print("Creating section for:", heading)
        # Create section content and HTML
        curr_elements = get_section_elements(heading, previous_sections, all_elements_used)
        # print("Using elements:", curr_elements)
        all_elements_used.update(curr_elements)
        previous_sections.append(curr_elements)
        section_html = create_section_html(heading, course_topic, use_file, curr_elements)
        section_html_header =  f"<div class=\"title-box\"> <h1>{heading}</h1> </div>"
        
        all_content  += section_html_header + section_html

    all_styles = title_boxes["title1"]
    for element in elements:
        if element in all_elements_used:
            print("Adding style in all_styles for:", element)
            all_styles += get_html_style(elements[element]) + "\n"

    # Include a consistent style similar to the reference HTML
    final_style = """
    <style>
        @font-face {
            font-family: 'Optima';
            src: local('Optima'), local('Optima-Regular');
        }

        body {
            background-color: #000000;
            font-family: 'Optima', 'Arial', sans-serif;
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 20px;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        .title-box {
            background-color: #C4C8F3;
            padding: 20px;
            text-align: center;
            border-radius: 15px;
            margin-bottom: 20px;
        }
        .title-box h1 {
            color: #fff;
            font-family: 'Optima', 'Arial', sans-serif;
            font-size: 3em;
            font-weight: bold;
            margin: 0;
        }
        .subheading-box {
            background-color: #DDDFF5;
            padding: 15px;
            margin-top: 1.5em;
            border-radius: 15px;
            margin-bottom: 20px;
        }
        .subheading-box h2 {
            color: #336699;
            font-family: 'Optima', 'Arial', sans-serif;
            font-size: 1.75em;
            font-weight: bold;
            margin: 0 0 10px 0;
        }
        p, ul, ol, li {
            font-family: 'Optima', 'Arial', sans-serif;
        }
        p {
            margin-bottom: 20px;
            font-size: 1.1em;
            line-height: 1.6;
        }
        ul, ol {
            margin: 0 0 1.5em 1.5em;
            padding: 0;
            font-size: 1.1em;
            line-height: 1.6;
        }
        ul li, ol li {
            margin-bottom: 10px;
            padding: 0;
        }
        ul li strong, ol li strong {
            color: #5F6AE8;
        }
        .highlight {
            background-color: #cceeff;
            border-left: 4px solid #007acc;
            padding: 10px;
            margin-bottom: 1.5em;
        }
        .content-image {
            display: block;
            margin: 20px auto;
            max-width: 100%;
            height: auto;
            border-radius: 15px;
        }
        .circular-image {
            float: left;
            margin: 0 20px 20px 0;
            border-radius: 50%;
            width: 150px;
            height: 150px;
            object-fit: cover;
        }
        a {
            color: #007acc;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .footer {
            text-align: center;
            padding: 10px;
            margin-top: 20px;
            background-color: #f2f2f2;
            border-radius: 8px;
        }
        .clearfix::after {
            content: "";
            clear: both;
            display: table;
        }
        .container, h1, h2, p, .highlight, .footer {
            page-break-inside: avoid;
        }
        .bold {
            font-weight: bold;
        }
        .underline {
            text-decoration: underline;
        }
        .blue-text {
            color: #007acc;
        }
        .image-placeholder {
            height: 250px;
            width: 400px;
            margin: 0 auto; /* This centers the div horizontally */
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        table:not(.ref6) {
        width: 80%; /* Adjust the width as needed */
        margin: 20px auto; /* Center the table horizontally */
        border-collapse: collapse; /* Ensure borders don't double up */
        }

        th:not(.ref6), td:not(.ref6) {
            padding: 12px 15px; /* Add padding for better readability */
            border: 1px solid #ddd; /* Add border for clarity */
            text-align: center; /* Center the text in each cell */
        }

        th:not(.ref6) {
            background-color: #00e1ff; /* Add a background color to the header */
            color: #ffffff; /* Text color for the header */
            font-weight: bold; /* Make the header text bold */
        }

        tr:not(.ref6):nth-child(even) {
            background-color: #f2f2f2; /* Add alternating row colors */
        }

        tr:not(.ref6):hover {
            background-color: #f5f5f5; /* Highlight row on hover */
        }
        
        /* Prevent page breaks inside these elements */
        h1, h2, h3, p, table, img, div {
            page-break-inside: avoid;
        }

        /* For containers or sections */
        .container, .section, .header {
            page-break-inside: avoid;
            page-break-before: auto;
            page-break-after: auto;
        }

    </style>
    """
    all_styles += final_style
    for i, color in enumerate(replace_colors):
        color_key = f'c{i+1}'
        all_styles = replace_inline_colors(all_styles, replace_colors, colors)

    # Replace the color in all_content and all_styles based on background-color
    all_content = replace_inline_colors(all_content, replace_colors, colors)
    all_styles = replace_inline_colors(all_styles, replace_colors, colors)
    
    # Replace placeholder images with actual images based on section content
    # List of random search terms for testing
    random_search_terms = [
        'nature', 'technology', 'artificial intelligence', 
        'robots', 'cityscape', 'abstract', 'animals', 
        'mountains', 'ocean', 'cars'
    ]

    # all_content = replace_placeholders(all_content, random_search_terms)
    
    # print(all_content)  # Debugging: Print the output HTML to ensure replacements





    # Combine all subcontents + headings to make final course
    final_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{course_topic}</title>
        {all_styles}
    </head>
    <body>
        <div class="container">
            {all_content}
        </div>
    </body>
    </html>
    """
    
    final_html = remove_code_markers(final_html)
    
    final_path = "./FINAL.html"
    # print("Final HTML:\n", final_html)
    save_html(final_html, final_path)
    # html_to_pdf(final_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some arguments.')
    parser.add_argument('--use-file', action='store_true', help='Set this flag to use file')
    args = parser.parse_args()
    
    use_file = args.use_file

    course_topic = "refer to headings test"
    # Give AI content/topic
    if not use_file:
        course_topic = input("What would you like to create the course about?\n")
    generate_course(course_topic, use_file)
