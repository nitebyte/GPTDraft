import os
import json
import func

def print_ascii_art():
    print(r"╔═════════════════════════════════════════════════════════════════════════════════╗")
    print(r"║_____/\\\\\\\\\\\\__/\\\\\\\\\\\\\____/\\\\\\\\\\\\\\\__/\\\\\\\\\\\\____        ║")
    print(r"║ ___/\\\//////////__\/\\\/////////\\\_\///////\\\/////__\/\\\////////\\\__       ║")
    print(r"║  __/\\\_____________\/\\\_______\/\\\_______\/\\\_______\/\\\______\//\\\_      ║")
    print(r"║   _\/\\\____/\\\\\\\_\/\\\\\\\\\\\\\/________\/\\\_______\/\\\_______\/\\\_     ║")
    print(r"║    _\/\\\___\/////\\\_\/\\\/////////__________\/\\\_______\/\\\_______\/\\\_    ║")
    print(r"║     _\/\\\_______\/\\\_\/\\\___________________\/\\\_______\/\\\_______\/\\\_   ║")
    print(r"║      _\/\\\_______\/\\\_\/\\\___________________\/\\\_______\/\\\_______/\\\__  ║")
    print(r"║       _\//\\\\\\\\\\\\/__\/\\\___________________\/\\\_______\/\\\\\\\\\\\\/___ ║")
    print(r"║        __\////////////____\///____________________\///________\////////////_____║")
    print(r"╠═════════════════════════════════════════════════════════════════════════════════╝")


def init():
    print_ascii_art()
    # Define the filename and create the path to the file
    filename = "settings.gptd"
    path = "" + filename

    # Check if the file exists
    if not os.path.isfile(path):
        # If the file does not exist, prompt the user to enter their API key
        print("║ It seems like", filename, "does not exist.\n║ You need to set up the program for the first time.\n║ This will only need to be done once.")
        print("╠═════════════════════════════════════════════════════════════════════════════════")
        while True:
            try:
                if input("║ Do you have an API Key from OpenAI.com? Y/N: ").upper() == "Y":
                    print("╠═════════════════════════════════════════════════════════════════════════════════")
                    a_key = input("║ Please enter your API Key: ")
                    func.define_API(a_key)
                    apiVerify = func.PR("X","",1,0)
                    if apiVerify.get('status') == 1:
                        print(f"║ Validated API key using {apiVerify['tokens']} tokens. Cost: ${apiVerify['cost']:.6f}")
                        print("╠═════════════════════════════════════════════════════════════════════════════════")
                        break  # Exit the loop if the API call was successful
                    else:
                        print("║ API ERROR. Invalid API Key.")
                else:
                    # If the user does not have an API key, provide instructions for getting one
                    print("╠═════════════════════════════════════════════════════════════════════════════════")
                    print("║ To use this program, you need an API key from OpenAI.com. Here's how to get one:\n║ 1. Go to https://platform.openai.com/\n║ 2. Fill out the signup form and follow the instructions to create an account.\n║ 3. Go to https://platform.openai.com/account/api-keys to create an API key.\n║ 4. Copy your API key and paste it into this program when prompted.")
                    print("╠═════════════════════════════════════════════════════════════════════════════════")
            except Exception as e:
                a_key = ""

        # Prompt the user to enter an API key for DALL-E or use the same API key as before
        if input("║ Do you want to use the same API key for DALL-E? Y/N: ").upper() == "N":
            while True:
                try:
                    d_key = input("║ Please enter your DALL-E API Key: ")
                    func.define_API(d_key)
                    apiVerify = func.PR("X","",1,0)
                    if apiVerify.get('status') == 1:
                        print(f"║ Validated API key using {apiVerify['tokens']} tokens. Cost: ${apiVerify['cost']:.6f}")
                        print("╠═════════════════════════════════════════════════════════════════════════════════")
                        break  # Exit the loop if the API call was successful
                    else:
                        print("║ API ERROR. Invalid API Key.")
                except Exception as e:
                    a_key = ""
        else:
            d_key = a_key


        # Prompt the user to edit some optional configuration settings
        if input("║ There are some optional settings. Would you like to edit these? Y/N: ").upper() == "Y":
            print("╠═════════════════════════════════════════════════════════════════════════════════")
            while True:
                try:
                    # Prompt the user to enter an integer value for DALL-E image size
                    d_size = int(input("║ DALL-E supports 3 images sizes:\n║ 1. 256x256 @ $0.0016/Image\n║ 2. 512x512 @ $0.0018/Image\n║ 3. 1024x1024 @ $0.0020/Image (Default)\n║ Please Choose 1, 2, or 3: "))
                    # Check if the input value is valid
                    if d_size not in [1, 2, 3]:
                        # If the input value is not valid, raise a ValueError and display an error message
                        raise ValueError
                    # If the input value is valid, exit the loop
                    break
                except ValueError:
                    # If a ValueError is raised, display an error message and prompt the user to enter a valid input
                    print("║ Invalid input. Please enter 1, 2, or 3.")
            print("╠═════════════════════════════════════════════════════════════════════════════════")
            # Repeat the same process for the remaining configuration settings
            while True:
                try:
                    d_sec = input("║ DALL-E is set by default to only generate images for chapters, not sections.\n║ Would you like DALL-E to generate images for sections? Y/N: ").upper()
                    if d_sec.upper() not in ["Y", "N"]:
                        raise ValueError
                    break
                except ValueError:
                    print("║ Invalid input. Please enter Y or N.")
            print("╠═════════════════════════════════════════════════════════════════════════════════")
            while True:
                try:
                    g_temp = float(input("║ GPT3.5 has a temperature setting between 0.00 and 1.00. Default is 0.35\n║ The higher the number, the higher the level of randomness & creativity.\n║ Enter a value of 0.00 to 1.00: "))
                    if not 0 <= g_temp <= 1:
                        raise ValueError
                    break
                except ValueError:
                    print("║ Invalid input. Please enter a value between 0.00 and 1.00.")
            print("╠═════════════════════════════════════════════════════════════════════════════════")
            while True:
                try:
                    g_freq = float(input("║ GPT3.5 has a frequency penalty setting between 0.00 and 2.00. Default is 0.15\n║ The higher the number, the lower the chance the response will be repeated verbatim\n║ Enter a value of 0.00 to 2.00: "))
                    if not 0 <= g_freq <= 2:
                        raise ValueError
                    break
                except ValueError:
                    print("║ Invalid input. Please enter a value between 0.00 and 2.00.")
            print("╠═════════════════════════════════════════════════════════════════════════════════")
            while True:
                try:
                    g_pres = float(input("║ GPT3.5 has a presence penalty setting between 0.00 and 2.00. Default is 0.05\n║ The higher the number, the more likely the response will deviate from the given topic.\n║ Enter a value of 0.00 to 2.00: "))
                    if not 0 <= g_pres <= 2:
                        raise ValueError
                    break
                except ValueError:
                    print("║ Invalid input. Please enter a value between 0.00 and 2.00.")
            print("╠═════════════════════════════════════════════════════════════════════════════════")
            while True:
                try:
                    g_tok = int(input("║ GPT3.5 has a token limit between 1 - 2048. Default is 2048.\n║ The higher the number, the longer the maximum length of the response.\n║ Enter a value of 0 to 2048: "))
                    if not 0 <= g_tok <= 2048:
                        raise ValueError
                    break
                except ValueError:
                    print("║ Invalid input. Please enter a value between 0 and 2048.")
            print("╠═════════════════════════════════════════════════════════════════════════════════")
        else:
            d_size = 3
            d_sec = 0
            g_temp = 0.35
            g_freq = 0.15
            g_pres = 0.05
            g_tok = 2048

        # Array of data
        settingsArray = [
            {"a_key": a_key, "d_key": d_key, "d_size": d_size, "d_sec": d_sec, "g_temp": g_temp, "g_freq": g_freq, "g_pres": g_pres, "g_tok": g_tok}
        ]

        # Append the array to a JSON file
        with open("settings.gptd", "w") as f:
            json_str = json.dumps(settingsArray)
            f.write(json_str)

        print("╠═════════════════════════════════════════════════════════════════════════════════")
        print("║ settings.gptd has been saved in a JSON format.")
        print("╠═════════════════════════════════════════════════════════════════════════════════")
        print("║ GPT Draft is ready.\n║ Brief Tutorial: You will be asked to enter a subject followed by a document\n║ type. For instance, if you want a travel guide to Victor Colorado, you would\n║ enter 'Victor, Colorado' as the subject and enter 'Travel Guide' as the document\n║ type. The program will then attempt to generate a suitable chapter summary for\n║ you to approve. Once you approve it, the program will begin writing.\n║ Please be aware this may take several minutes.")



