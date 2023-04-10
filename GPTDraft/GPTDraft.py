import uuid
import os
import openai
import hashlib
import ebooklib
import csv
import requests
import json
import sys
from io import BytesIO
import func
import start


#Run the start function to initialize the program and check for settings.gptd
start.init()

# Open the JSON file containing the settings data
with open("settings.gptd", "r") as f:
    # Load the JSON data from the file into a Python object
    settingsObj = json.load(f)

# Extract the settings data from each dictionary in settingsObj
# and assign it to variables for easier access
sizeAssign = ["256x256","512x512","1024x1024"]
for settings in settingsObj:
    a_key = settings["a_key"]     # Your OpenAI API key for GPT
    d_key = settings["d_key"]     # Your OpenAI API key for DALL-E 2. This can be the same as the GPT key or different.
    d_size = sizeAssign[int(settings["d_size"])-1]   # The size of the DALL-E Image
    d_sec = settings["d_sec"]     # Determines if Dall-E is used for sections and chapters, or just chapters
    g_temp = float(settings["g_temp"])  # The temperature to use for generating the results
    g_freq = float(settings["g_freq"])   # The frequency penalty to use for generating the results
    g_pres = float(settings["g_pres"])   # The presence penalty to use for generating the results
    g_tok = int(settings["g_tok"])     # Man tokens to use in the results

# Load your API key from an environment variable or secret management service
openai.api_key = a_key

#Set URL for DALL-E
url = "https://api.openai.com/v1/images/generations"

#Global Variables
tokens = 0
totalCost = 0
globaldesc=""
#------------------------------------------------------------------------------------------------------------------------------------------------

while True:
    # Prompt the user to enter the subject and document type
    print("╠═════════════════════════════════════════════════════════════════════════════════")
    subject = input("║ Enter the subject of the document: ")
    print("╠═════════════════════════════════════════════════════════════════════════════════")
    documentType = input("║ Enter the document type: ")
    
    # Prompt GPT to use the chapter/section/part summary and generate the 3D book array
    print("╠═════════════════════════════════════════════════════════════════════════════════")
    chapterListRaw = func.PR("You are a professional book editor. Please generate me a list of chapters, sections (sub-chapters), and parts (sub-sections) for a " + documentType + " about " + subject + ". Enter each chapter/section/part on it's own line, and only give the chapter/section/part number and title. There is no set requirement for the amount of chapters, sections, and parts - you may use as many or as few as long as you give a comprehensive coverage of the requested topic; if there is a chapter that has extensive information, make sure to use a large number of sections to cover all of the information in separate sections; and if there is a section with a large amount of information, use multiple parts in that section. Numbering should be three level - 1.0.0 would be a chapter; 1.1.0, 1.1.1, 1.1.2, and so on would be sections under that chapter, and 1.1.1, 1.1.2, 1.1.3 would be parts of the first section of the first chapter.","",2048,0.85,0,0)['content']
    book = func.bookArray(chapterListRaw)
    #book = book[1:]
    # Print out the chapter/section/part summary using the print_book function and prompt the user for confirmation
    func.print_book(book,"║ ")
    print("╠═════════════════════════════════════════════════════════════════════════════════")
    if input("║ Is this chapter/section/part summary acceptable? Y/N: ").upper() == "Y":
        break


total_chars = 0
total_words = 0
total_sections = func.count_parts(book)
completed_sections = 0

print("Title: "+subject+"")
savefile = subject + ".txt"

serialBook = func.serialize_book(book)

for i, chapter in enumerate(book):
    for j, section in enumerate(chapter):
        for k, part in enumerate(section):
            if book[i][j][k] is not None:
                print("Writing About The " + str(book[i][j][k]) + " of " + subject)
                if(j==0):
                    prompt = "Write me a 1 paragraph brief introduction for a chapter about the " + book[i][j][k] + " of " + subject + "."
                else:
                    prompt = "Write me 8-10 extensive detailed and informative paragraphs for a chapter named '" + book[i][j][k] + "' in a book about the subject of " + subject + ". Only write strictly about " + book[i][j][k] + " and do not progess into any other topics/eras/areas/sections that lie outside of the " + book[i][j][k] + ". Remember you need not introduce the topic/subject of the book as it's already been covered in previous chapters."
                Repo = func.PR("You are a professional writer.  For reference of what NOT to write about, here are the chpaters of the book:" + serialBook + ". " + prompt, "", 2048, 0.85)
                response = "\n\n" + book[i][j][k] + "\n" + Repo['content']
                tokens += Repo['tokens']
                totalCost += Repo['cost']
                num_chars = len(response)
                num_words = len(response.split(' '))
                total_chars += num_chars
                total_words += num_words
                completed_sections += 1
                print(f" {completed_sections}/{total_sections} sections completed ({completed_sections/total_sections*100:.2f}%). {num_chars} CHAR. {num_words} WORDS. Total: {total_chars} CHAR. {total_words} WORDS. Saving...")
                func.append_text_to_file(response, savefile)

print(f"All sections completed. {total_chars} CHAR. {total_words} WORDS saved!") 

outputfile = savefile.replace('.txt', '.docx')
func.txt_to_docx(savefile,outputfile,town)

