
from openai import OpenAI
import requests, re
import pdfkit
import fitz  # PyMuPDF
import os

client = OpenAI(
    api_key='sk-proj-mCWQQDHRasr5LcSqAqHsT3BlbkFJ4GmldcHKovwMsHwFto5j',
)

def GPT(system_prompt, user_prompt, model = "gpt-3.5-turbo"):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
        model=model,
    )
    message_content = chat_completion.choices[0].message.content
    if (message_content.startswith('"') and message_content.endswith('"')) or (message_content.startswith("'") and message_content.endswith("'")):
        return message_content[1:-1]
    return message_content

def save_html(html_string, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_string)
    print("HTML SAVED")

def html_to_pdf(html_path):
    # Define the paths
    # temp_pdf_path = '../temp_course.pdf'
    output_pdf_path = './test.pdf'
    
    # Define the path to wkhtmltopdf.exe
    path_to_wkhtmltopdf = r'./wkhtmltopdf/bin/wkhtmltopdf.exe' 
    
    # Configure pdfkit to use the installed wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

    # Define the options to set margins to zero
    options = {
        'margin-top': '0',
        'margin-right': '0',
        'margin-bottom': '0',
        'margin-left': '0',
        'page-size': 'A4',
        'enable-local-file-access': None,
        'quiet': '',  # Verbose output for debugging
        'load-error-handling': 'ignore',  # Ignore missing resource errors
    }

    
    # Convert the HTML to a temporary PDF
    pdfkit.from_file(html_path, output_pdf_path, options=options, configuration=config)

    # Change the background color of the PDF
    # background_color = extract_bg_color(input_html_path)

    # doc = fitz.open(temp_pdf_path)
    # for page in doc:
    #     page.draw_rect(page.rect, color=None, fill=background_color, overlay=False)

    # doc.ez_save(output_pdf_path)
    # doc.close()
    # os.rename(temp_pdf_path, output_pdf_path)
    # print("PDF generated and saved to", output_pdf_path)

def get_image_url(search_term):
    api_key = 'xIUNnZUTr5MqhvJvHPFcQFVvEUYrsnC1gaz17PC9agUFxq40N9TcideL'
    url = f'https://api.pexels.com/v1/search?query={search_term}&per_page=1'
    headers = {
        'Authorization': api_key
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['photos']:
            return data['photos'][0]['src']['original']
        else:
            return "No images found for this search term."
    else:
        return f"Error: {response.status_code}"

def extract_bg_color(input_html_path):
    with open(input_html_path, 'r') as file:
        html_content = file.read()
    # Regular expression to match the background-color in CSS
    bg_color_pattern = re.compile(r'background-color:\s*(#[0-9a-fA-F]{6}|rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\))\s*;')
    
    match = bg_color_pattern.search(html_content)
    if not match:
        raise ValueError("Background color not found in HTML content")
    
    bg_color = match.group(1)
    
    if bg_color.startswith('#'):
        # Hex color format
        r = int(bg_color[1:3], 16) / 255
        g = int(bg_color[3:5], 16) / 255
        b = int(bg_color[5:7], 16) / 255
    elif bg_color.startswith('rgb'):
        # RGB color format
        rgb_values = re.findall(r'\d+', bg_color)
        r = int(rgb_values[0]) / 255
        g = int(rgb_values[1]) / 255
        b = int(rgb_values[2]) / 255
    else:
        raise ValueError("Unknown color format")
    
    return (r, g, b)

def html(html_path):
    with open(html_path, 'r') as file:
        html_content = file.read()
    return html_content

def get_html_style(html_content):
    # Regular expression to match the style tag in HTML
    style_pattern = re.compile(r'(<style.*?>.*?</style>)', re.DOTALL)
    
    match = style_pattern.search(html_content)
    if not match:
        print("Style tag not found in HTML content")
        return None
    
    style = match.group(1)
    
    return style

if __name__ == "__main__":
    html_to_pdf("./FINAL.html")