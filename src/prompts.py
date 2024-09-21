
# 2. Generate a layout/headings for the course.
layout_system_prompt = """You are an expert course designer. You will be given a course topic, and you need to create a list of sections 
    and headings for the course. Each section should have a heading that summarizes the content of that section. The course should cover the 
    basics of the topic and provide a good foundation for beginners. The course should be structured in a logical order, starting with the basics 
    and progressing to more advanced topics. Each new heading or section should be on a newline and do not add anything else such as - or * before 
    the title. Only give a list of the sections and headers in plain text each on a new line and nothing else. Dont give a title, no empty lines, 
    only each heading on a new line each."""
layout_user_prompt = f"""Create a list of 6 sections and headings for a course on """  # Append the topic to this prompt

# Given heading, decide what elements would be best to display.
def element_decider_prompt(course_topic, heading, ref_explained, previous_sections):
    return f"""
    I am creating a course about {course_topic} and this is the heading for a section: \"{heading}\". It will be in HTML and I want it to look visually clean and appealing.
    Below is a list of elements that I have available to be used. I dont want to overuse sections or elements, but I also want each
    section to look unique and appealing. 
    Here is the name and explanation for all elements: {ref_explained}
    Below is a list of the previous sections and what elements were used in that section in order. Make sure that one element is not
    repeated too often and no two sections have the same order of elements while also keeping the elements used relevant to the section.
    Previous sections: {previous_sections}
    In a newline output, give me the name of the elements that would make sense for this section. Only give the names as output and nothing else
    each element name should be on a new line. It could be the case that there could be 1 elements, 1 element, or even 0 elements that would make sense.
    There should be a maximum of 2 elements, but 1 or 0 elements could also work. Do not add anything else such as - or * before the elements. The section names should be
    exactly the same as from the list of all elements I provided, and must be a subset of that list with only the relevant elements for
    this section while keeping the previous section styles in mind. Do not include quotation marks or ``` in the output.
    Give 0-2 elements for the heading \"{heading}\" while keeping the previous sections in mind and avoiding repetition.
    DO NOT GIVE A DESCRIPTION ON WHY YOU PICKED THE ELEMENT. The only output should be the name of the element chosen. One element on each line.
    Example is seen below, no description, only the names of the element, one of each line. If no element is picked then return an empty string.
    
    Example output:
    ref2
    ref4
    """

# Given elements and heading, generate content for the heading while using the elements.
def heading_content_prompt(course_topic, heading):
    return f"""I am creating a digital HTML course about {course_topic}. 
    There are different subsections in this course. For this task we are working with the heading: \"{heading}\".
    
    Your job is to create the content for this section and present it in visually appealing HTML format. 
    Do not give a heading since it is already provided, only give what would go inside the section.
    
    The content should be informative and engaging. Dont just give surface level information.
    The content should be detailed and provide a good understanding of the topic. The content should be in a paragraph format and should be
    at least 4000 chars long. The content should be written in a way that is engaging for the reader.
    
    Give the content in an HTML format. The output should only be the <div> section for the content as the output will be directly placed in inside a HTML file.
    Make it look visually appealing and modern. Use methods such as:
    1. Bullet points
    2. Numbered Lists
    3. Bolding and coloring certain words to put emphasis
    4. Tables
    5. (placeholder) Images
    6. Tabbing and indentation
    7. Paragraphs
    and more
    
    When applicable include placeholder images in the section aswell either big or small. Use placeholder URLs for now and I will fill them in later. Each image placeholder needs to have a url,
    URL must be in this form for all placeholders: https://via.placeholder.com/
    
    Make sure to specify the placeholder image sizes as a height and width in the code. The minimum width and height of placeholders must be 500 each. Make sure placeholders do not cover any other elements or text
    Not every section needs an image so only include a placeholder when you believe this section can benefit from one.
    
    
    Again, only give the <div> section for the content and nothing else. Do not give the <style> tag either and assume that the HTML file will
    already have the styles defined for these elements in the exact same name as present in the example elements. Dont add anything like "``` ```html" or "```" around the output.
    Dont say stuff like "here is the HTML" or "this is the HTML". Just give the HTML <div> content for the section. Do not use <base> or <link> tags in the HTML.
    
    Only give the content for the section and nothing else. Dont put it in quotation marks and done say anything like "sure here it is".
    """

# Given elements and heading, generate content for the heading while using the elements.
def element_adder_prompt(course_topic, content, curr_elements, element_descriptions):
    return f"""I am writing an HTML course about {course_topic}.

    I have created one of the sections which can be seen below. The section is currently displying the information mostly using text formatting.
    While the information is good and is formatted well, I want it to be more visually appealing and engaging. I have a list of elements that I can use to make the section more visually appealing.
    Here are the names and descriptions elements that I have available to use:
    {element_descriptions}
    
    Use these elements as reference and add them to the section to make it more visually appealing.
    The code for the elements is below, it has placeholder content inside of them which you must replace with relevant content for the section.
    Strategically place the elements, they dont have to be at the very end or very start of the code. While they could be, they can also be placed in the middle of the content.
    Do not remove any of the exiting content or text from the current section. Your job is only to add to the section given the element codes.
    
    Current section HTML:
    {content}
    
    Elements code references:
    {curr_elements}
    
    The final output must be in HTML format and should only be the <div> section for the content as the output will be directly placed in inside a HTML file.
    Given the content HTML add the elements to it with relevant content inside the element.
    
    Remember, the reference code only has reference content inside the HTMLs. Replace it with actual relevant content that will fit in with the rest of the section content.
    Dont add anything like "``` ```html" or "```" around the output. Do not use <base> or <link> tags. 
    """
    
def styles_colors_prompt(styles, color1, color2, color3, color4):
    return f"""
    Below is the style reference from my HTML course. There are multiple style blocks with different IDs.
    Alot of these style blocks are using various colors to show in their respective elements.
    
    I want to have color consistency in my course. Other than the colors in the elements there is also an overall background element of the course,
    colors for highlighted words, and so on. I want to have a color scheme that is visually appealing and consistent throughout the course.
    
    I want you to replace all the colors in the style blocks with the colors I have chosen.
    Below are the colors that I have chosen:
    Primary: {color1}
    Secondary: {color2}
    Tertiary: {color3}
    Quaternary: {color4}
    
    Use your best judgement to replace the colors and decide which color should go where. For example the main background color would ofcoarse be the primary color.
    The color scheme should be visually appealing and consistent throughout the course.
    
    Only replace the colors in the style section and nothing else. Your output should only be the style sections like I have laid out.
    Do not change any other names, do not merge the style sections into one, do not remove the IDs of the style sections. Only replace the colors and thats it.
    
    DO NOT REMOVE ANY OTHER STYLING. YOUR ONLY JOB IS TO CHANGE THE COLORS. EVERYTHING ELSE SHOULD REMAIN EXACTLY THE SAME.
    DO NOT COMMENT OUT ANY OF THE OTHER STYLES. ONLY CHANGE THE COLORS.
    Here is the style reference:
    {styles}
    """