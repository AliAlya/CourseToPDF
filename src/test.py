import re
import os
import uuid
from urllib.parse import urlparse
from icrawler.builtin import GoogleImageCrawler
from icrawler.downloader import ImageDownloader
from openai import OpenAI

# GPT function as provided
client = OpenAI(
    api_key='sk-proj-mCWQQDHRasr5LcSqAqHsT3BlbkFJ4GmldcHKovwMsHwFto5j',
)

def GPT(system_prompt, user_prompt, model="gpt-3.5-turbo"):
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

# Global list to store web URLs and attributions
web_urls = []

# Custom downloader class
class CustomDownloader(ImageDownloader):
    def download(self, task, default_ext, timeout=5, **kwargs):
        web_urls.append(task['file_url'])  # Capture the image URL
        return super().download(task, default_ext, timeout, **kwargs)

# Function to download images and return their local paths along with attribution
def download_image(search_term, download_dir='images', max_num=1):
    global web_urls
    unique_dir = os.path.join(download_dir, str(uuid.uuid4()))  # Create a unique subdirectory
    os.makedirs(unique_dir, exist_ok=True)

    google_crawler = GoogleImageCrawler(downloader_cls=CustomDownloader, storage={'root_dir': unique_dir})
    google_crawler.crawl(keyword=search_term, max_num=max_num)
    
    # Return the first image's local path and the attribution (domain) if available
    for root, dirs, files in os.walk(unique_dir):
        if files:
            image_path = os.path.join(root, files[0])
            if web_urls:
                domain = urlparse(web_urls[-1]).netloc  # Extract the domain name
                return image_path, domain
    return None, None

# Custom generate_search_terms function for textbook-type diagrams/images
def generate_search_terms(html):
    pattern = r'<img[^>]*src="https://via\.placeholder\.com/(\d+)x(\d+)"[^>]*>|<img[^>]*src="https://via\.placeholder\.com/50"[^>]*>'
    matches = re.finditer(pattern, html)

    search_terms = []
    for match in matches:
        surrounding_text = extract_surrounding_text(html, match.start(), match.end())
        system_prompt = "You are an assistant generating image search terms for educational and textbook-like diagrams or images. The goal is to find informative images that effectively complement and illustrate the content in an academic or instructional context."
        user_prompt = f"Generate only a search term for a textbook-style diagram or image based on the following context: {surrounding_text}"
        search_term = GPT(system_prompt, user_prompt)
        search_terms.append(search_term)
        print(f"Generated search term: {search_term}")

    return search_terms

# Helper function to extract surrounding text with words only
def extract_surrounding_text(html, start_idx, end_idx, context_words=50):
    before_text = html[:start_idx].split()
    after_text = html[end_idx:].split()

    surrounding_text = ' '.join(before_text[-context_words:]) + " [IMAGE] " + ' '.join(after_text[:context_words])
    return surrounding_text

def replace_placeholders(html):
    pattern = r'<img[^>]*src="https://via\.placeholder\.com/(\d+)x(\d+)"[^>]*>|<img[^>]*src="https://via\.placeholder\.com/50"[^>]*>'
    matches = re.finditer(pattern, html)
    matches = list(matches)  # Convert to list for easier indexing
    print(f"Total placeholders found: {len(matches)}")

    search_terms = generate_search_terms(html)

    for index, match in enumerate(matches):
        if index < len(search_terms):
            search_term = search_terms[index]
            width, height = re.search(r'(\d+)x(\d+)', match.group(0)).groups() if 'x' in match.group(0) else ('40', '40')

            # Download the image and get the local path along with attribution
            image_path, attribution = download_image(search_term)
            if image_path:
                attribution_text = f'Image source: {attribution}' if attribution else ''
                new_img_tag = f'<img src="{image_path}" width="{width}" height="{height}"><br><small style="display: block; text-align: center;">{attribution_text}</small>'
                html = html.replace(match.group(0), new_img_tag, 1)
                print(f"After replacement: {new_img_tag}, index={index}")
            else:
                print(f"Failed to download image for search term: {search_term}")

    return html


# Load the HTML content from the input file
input_file_path = 'FINAL.html'
output_file_path = 'testerOutput.html'

with open(input_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

updated_html = replace_placeholders(html_content)

with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(updated_html)

print("Placeholders have been replaced and the updated HTML is saved.")

# Print all collected web URLs
print("\nWeb URLs used for images:")
for url in web_urls:
    print(url)
