import openai
import os
import csv
from io import BytesIO
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def define_API(key):
    openai.api_key = key
    

def PR(prompt, system_content="", token=24, temperature=0.35, pp=0.15, fp=0.05):
    try:
        # Create a list of messages containing the system content and user prompt
        if len(system_content) > 0:
            messages = [{'role': 'system', 'content': system_content}, {'role': 'user', 'content': prompt}]
        else:
            messages = [{'role': 'user', 'content': prompt}]
        

        # Call the OpenAI API to generate a chat completion given the messages and parameters
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, temperature=temperature, max_tokens=token, presence_penalty=pp, frequency_penalty=fp)

        # Get the system message from the API response
        system_message = response.choices[0].get('message', {}).get('content', '').strip()

        # Get the number of tokens used from the API response
        tokens = response.get('usage', {}).get('total_tokens', 0)

        # Calculates the cost of the API response
        cost = tokens * 0.000002

        # Get the user prompt message and remove any leading or trailing whitespace
        prompt_message = prompt.strip()

        # Return a dictionary containing the status of the message, the number of tokens used, and the system message
        return {"status": 1, "tokens": tokens, "cost": cost, "content": system_message}
    except Exception as e:
        # If an exception occurs, return a dictionary containing the status of the message and the error message
        return {"status": 0, "tokens":0, "cost": "", "content": str(e)}



def append_text_to_file(text, file_name):
    # Open a file in "append+" mode, which creates the file if it does not exist and appends new content to the end of the file
    with open(file_name, "a+") as f:
        # Write the given text to the end of the file, followed by a newline character
        f.write(text + "\n")



def bookArray(chapterListRaw):
    chapterList = chapterListRaw.split('\n')

    book = [[[None]]]

    for chapter in chapterList:
        if not chapter.strip():  # Check if the line is empty or contains only whitespace
            continue              # Skip empty lines
        parts = chapter.split(' ')
        chapterNum = int(parts[0].split('.')[0])
        sectionNum = int(parts[0].split('.')[1])
        partNum = int(parts[0].split('.')[2])
        title = ' '.join(parts[1:])
  
        while len(book) < chapterNum+1:
            book.append([[[None]]])
        while len(book[chapterNum]) < sectionNum+1:
            book[chapterNum].append([[[None]]])
        while len(book[chapterNum][sectionNum]) < partNum+1:
            book[chapterNum][sectionNum].append([None])
  
        book[chapterNum][sectionNum][partNum] = title
    return book



def print_book(book, pre=""):
    for chapterNum, chapter in enumerate(book):
        for sectionNum, section in enumerate(chapter):
            for partNum, part in enumerate(section):
                if part is not None:  # Check if part is not empty
                    space = ""
                    if sectionNum > 0:
                        space += "  "
                    if partNum > 0:
                        space += "  "
                    print(f"{pre}{space}{chapterNum}.{sectionNum}.{partNum} {part}")





def serialize_book(book):
    serialized = ""
    for chapterNum, chapter in enumerate(book):
        for sectionNum, section in enumerate(chapter):
            for partNum, part in enumerate(section):
                if part:
                    serialized += f"{chapterNum}.{sectionNum}.{partNum} {part},"
    return serialized.rstrip(",")  # Remove the trailing comma before returning



def count_parts(book):
    num = 0
    for chapterNum, chapter in enumerate(book):
        for sectionNum, section in enumerate(chapter):
            for partNum, part in enumerate(section):
                if part:
                    num+=1
    return num


def Title(text, place):
    return text[6:]

def txt_to_docx(txt_file, docx_file,town):
    # Create a new Document
    document = Document()
    # Set the page size and margins
    section = document.sections[0]
    section.page_width = Inches(4)
    section.page_height = Inches(6)
    section.left_margin = Inches(0.4)
    section.right_margin = Inches(0.4)
    section.top_margin = Inches(0.4)
    section.bottom_margin = Inches(0.4)

     # Add title page
    title_paragraph = document.add_paragraph()
    title_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_paragraph.add_run("Exploring " + town)
    title_run.font.size = Pt(18)
    title_run.bold = True
    title_paragraph.add_run("\n\nYour Guide to History, Culture, and Fun")
    document.add_page_break()

    # Add copyright page
    copyright_paragraph = document.add_paragraph()
    copyright_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    copyright_paragraph.add_run("Copyright 2023 {Your Name}").font.size = Pt(8)

    # Set the position of the copyright notice to the bottom of the copyright page
    copyright_paragraph_format = copyright_paragraph.paragraph_format
    copyright_paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    copyright_paragraph_format.space_after = Pt(0)
    document.add_page_break()

    # Add dedication page
    dedication_paragraph = document.add_paragraph()
    dedication_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    dedication_paragraph.add_run("Dedication\n\n")
    dedication_paragraph.add_run(PR("Please write me 1 paragraph for the dedication of a history, culture, reference, and travel guide for " + town + ", considering it was written by one person and should be a generic dedication to travelers and explorers.", "You are a professional writer for Lonely Planet writing the dedication page of a book about the history, culture, reference, and travel guide for small town of " + town + ".Make sure to vary your words and grammar so phrases do not repeat too much.", 0.5, 1024)).italic = True
    document.add_page_break()

    # Read the input text file
    with open(txt_file, 'r') as f:
        txt_lines = f.readlines()
        txt_lines = [line for line in txt_lines if line.strip()]

    # Process the text file lines
    for line in txt_lines:
        if line.startswith('H1'):
            document.add_page_break()
            title = line[2:].strip()
            heading = document.add_heading(level=1)
            heading_run = heading.add_run(title)
            heading_run.font.size = Pt(18)
            heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer api_key"
            }
            imgprompt = PR("I want you to write a DALL-E image generation prompt to generate an image related to " + title + " in the town of " + town, "You write image generation prompts for DALL-E from the given input request. For example, if you were asked to write a prompt for an image about the geography of Damascus, Virginia, you may output: Mountainous terrain with dense forests and trees, peaceful and serene, in the vicinity of Damascus, VA, USA. Shot on a Canon EOS R6 with a Canon RF 24-105mm f/4L IS USM Lens, 4K film still, natural lighting, vibrant colors, crisp details, and soft shadows.", 0.5, 2048)
            print("Generating Image For: " + title + " : " + town)
            data = {
                "prompt": imgprompt,
                "n": 1,
                "size": "1024x1024"
            }

            response = requests.post(url, headers=headers, data=json.dumps(data))

            if response.status_code == 200:
                result = response.json()
                # Download the image from a link
                image_url = result['data'][0]['url']
                response = requests.get(image_url)
                img = BytesIO(response.content)
                # Add a paragraph with an image
                paragraph = document.add_paragraph()
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER  # center the paragraph
                run = paragraph.add_run()
                run.add_picture(img, width=Inches(3))  # adjust width as necessary

        elif line.startswith('H2'):
            title = line[2:].strip()
            heading = document.add_heading(level=2)
            heading_run = heading.add_run(title)
            heading_run.font.size = Pt(16)
            heading.alignment = WD_ALIGN_PARAGRAPH.CENTER

        else:
            content = line.strip()
            paragraph = document.add_paragraph(content)
            paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Save the generated DOCX file
    document.save(docx_file)


def read_csv(csv_file):
    towns = []

    with open(csv_file, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            town, state = row[0].split(', ')
            towns.append([town, state])

    return towns



