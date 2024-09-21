from icrawler.builtin import GoogleImageCrawler

# Function to download images using a search term
def download_images(search_term, max_num=10, download_dir='images'):
    google_crawler = GoogleImageCrawler(storage={'root_dir': download_dir})
    
    google_crawler.crawl(keyword=search_term, max_num=max_num)

# Main execution
if __name__ == "__main__":
    # Manually enter your search term
    search_term = input("Enter the search term for Google Images: ")

    # Number of images to download
    max_num = int(input("Enter the number of images to download: "))

    # Optional: Specify a directory to save the images
    download_dir = input("Enter the directory to save images (default is 'images'): ") or 'images'

    # Download images
    download_images(search_term, max_num=max_num, download_dir=download_dir)

    print(f"Downloaded {max_num} images for search term '{search_term}' into directory '{download_dir}'")
