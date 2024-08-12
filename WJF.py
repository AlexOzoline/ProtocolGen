import tkinter as tk
from tkinter import messagebox
import re
from atlassian import Confluence
import json
import os
from dotenv import load_dotenv




#Dictionary containing definitions from Company name -> ISH number
company_to_ish = {
    "Plato": "ISH01",
    "Quadient": "ISH01",
    "Office Distribution": "ISH02",
    "Aliaxis": "ISH03",
    "Huisman": "ISH03",
    "RSPB": "ISH03",
    "Upergy": "ISH03",
    "Emuca": "ISH04",
    "Jarola-ish04": "ISH04",
    "Miele": "ISH05",
    "Jarola-ish06": "ISH06",
    "VBH": "ISH07",
    "BlockFoods": "ISH08",
    "ERLAU": "ISH08",
    "Laminat Depot": "ISH08",
    "Office Distribution-ish08": "ISH08",
    "Netto": "ISH09",
    "Colas": "ISH10",
    "Alko": "ISH12",
    "Lekkerland": "ISH12",
    "NICE": "ISH12",
    "Bomag": "ISH13",
    "Trumpf": "ISH13",
    "Elefant": "ISH14",
    "Nutreco": "ISH14",
    "Dynapac": "ISH16",
    "Oxford": "ISH16",
    "Wiltec": "ISH16",
    "Dover": "ISH17",
    "Rockwool": "ISH18",
    "SharkNinja": "ISH18",
    "Flamco": "ISH19",
    "TUEVSued": "ISH22",
    "AtlasCopco": "ISH23",
    "CFAO": "ISH24",
    "Ceetrus": "ISH24",
    "DBNext": "ISH24",
    "Trenois Decamps": "ISH24",
    "BeckmanCoulter": "ISH25",
    "AFDB": "ISH26",
    "Paredes": "ISH26",
    "Vanderlande": "ISH26",
    "Staples": "ISH27",
    "Sowa Tool": "ISH28",
    "Breg": "ISH29",
    "Musgrave": "ISH32",
    "Bertus": "ISH34",
    "Buerklin": "ISH34",
    "Burckhardt": "ISH34",
    "RijkZwaan": "ISH34",
    "Camfil": "ISH35",
    "Otis": "ISH35",
    "Reisswolf": "ISH35",
    "Alliance Laundry": "ISH36",
    "Daikin": "ISH36",
    "Douglas Dynamics": "ISH36",
    "KION Group": "ISH36",
    "SureWerx": "ISH36",
    "Mekonomen Pro": "ISH37",
    "Saldoportalen": "ISH37",
    "Whitestuff Oracle": "ISH38",
    "MusicStore": "ISH39",
    "Soennecken": "ISH40",
    "ArgoHytos": "ISH42",
    "Fraisa": "ISH42",
    "Kubota": "ISH42",
    "Motul": "ISH42",
    "Technolit": "ISH42",
    "SharkNinja US": "ISH45",
    "Motul APAC": "ISH52"
}


# To handle cases involving shared infrastructure, may require updating 
shortening_to_full = {
    "pltzz": "Plato",
    "qdntz": "Quadient",
    "ffcds": "Office Distribution-ish02",
    "lxszz": "Aliaxis",
    "hsmnz": "Huisman",
    "nttzz": "Netto",
    "atlsc": "AtlasCopco",
    "msgrv": "Musgrave",
    "dovra": "Dover",
    "vbh24": "VBH",
    "dbnxt": "DBNext"
}

def extract_substring_within_brackets(input_string):
    # Define a regular expression pattern to match substrings within brackets
    pattern = r"\((.*?)\)"
    
    # Use re.findall() to find all matches of the pattern in the input string
    matches = re.findall(pattern, input_string)
    
    # Return the first match (if any), or None if no match is found
    return matches[0] if matches else None

def extract_ish_number(data):
    pattern = re.compile(r'ish\d+')
    for item in data:
        match = pattern.search(item)
        if match:
            return match.group()
    return None

# Function to save content to a file
def save_content_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(content, file, ensure_ascii=False, indent=4)

def update_confluence(new_string, confirmation):
    # Confluence configuration - username = your email, password = personal API key
    # Load environment variables from .env file
    load_dotenv()
    confluence_api_key = os.getenv("CONFLUENCE_API_KEY")
    confluence_username = os.getenv("CONFLUENCE_EMAIL")
    confluence = Confluence(
        url='https://intershop-apac.atlassian.net',
        username=confluence_username,
        password=confluence_api_key
    )

    if confirmation:
        print("new string = ", new_string)
        payload = {
            "value": new_string,
            "representation": "storage"
        }
        response = confluence.append_page(
            page_id=620033507365,
            append_body=new_string,
            title='Alert Copy Space'
        )


# Manually parsing of input to form html
def generate_confluence_link(confirmation):
    input_block = input_text.get("1.0", "end-1c")  # Get text from input field
    start_time = start_time_entry.get()
    splitted = start_time.split(':')
    tmp_hour = int(splitted[0])
    tmp_hour = tmp_hour - 10
    if tmp_hour < 0:
        tmp_hour = tmp_hour + 24
    start_time = str(tmp_hour) + ':' + splitted[1]
    end_time = end_time_entry.get()
    splitted = end_time.split(':')
    tmp_hour = int(splitted[0])
    tmp_hour = tmp_hour - 10
    if tmp_hour < 0:
        tmp_hour = tmp_hour + 24
    end_time = str(tmp_hour) + ':' + splitted[1]
    comments = comments_text.get("1.0", "end-1c")
    # Replace -> in comments with appropriate right arrow emoji
    comments = comments.replace('->', '&rarr;')
    checkmark_emoji = """<ac:emoticon ac:name="tick" ac:emoji-shortname=":check_mark:" ac:emoji-id="atlassian-check_mark" ac:emoji-fallback=":check_mark:" />"""
    warning_emoji = """<ac:emoticon ac:name="warning" ac:emoji-shortname=":warning:" ac:emoji-id="atlassian-warning" ac:emoji-fallback=":warning:" />"""
    print("input block = " + input_block)
    first_space = False
    quote_start = False
    quote_end = False
    for i in range(len(input_block)):
        curr_ltr = input_block[i]
        if not first_space and curr_ltr == " ":
            first_space = True
            company = input_block[0:i]
        elif curr_ltr == "-" and input_block[i - 2] == ")":
            print("found start of alert at i = ", i)
            quote_start = i + 2
        elif curr_ltr == "(" and input_block[i - 2] == "'":
            quote_end = i - 1
            url_start = i + 1
            break
    #debugging
    #print(quote_start)
    #print(quote_end)
    quoted_text = input_block[quote_start: quote_end]

    # Change any "<" chars to &lt, to prevent some rare html parsing errors
    quoted_text = quoted_text.replace('<', '&lt;')

    url = input_block[url_start: -1]

    print("company = ", company)
    print("quoted_text = ", quoted_text)
    print("url = ", url)

    # Deal with 'shared infrastructure' cases
    if company == "Shared":
        bracket_text = extract_substring_within_brackets(input_block)
        bracket_text = bracket_text.split('/')
        shortening = bracket_text[-3]
        company = shortening_to_full[shortening]
    elif company != "shrkndpl":    
        symbols = []
        if green_check_var.get():
            symbols.append(checkmark_emoji)
        if yellow_warning_var.get():
            symbols.append(warning_emoji)
        symbols_str = " ".join(symbols)
        
        #define environment
        if prod_lv_var.get():
            environment = "Prod (LV)"
        elif prod_ed_var.get():
            environment = "Prod (ED)"
        elif UAT_lv_var.get():
            environment = "UAT (LV)"
        elif UAT_ed_var.get():
            environment = "UAT (ED)"
        elif not_applicable_check.get():
            environment = ""
        print(environment)   
        if company in company_to_ish:
            print("THIS IS RUNNING")
            ish_num = company_to_ish[company]
            confluence_link = f'<li><p>{symbols_str} {ish_num} ({company}): {start_time}-{end_time} UTC &rarr; {environment} &rarr; <a href="{url}"> {quoted_text} </a>&rarr; {comments}</p></li>'
            preview_text = f'{symbols_str} {ish_num} ({company}): {start_time}-{end_time} UTC -> {environment}  -> {quoted_text} -> {comments}'
        else:
            confluence_link = f'<li><p>{symbols_str} ({company}): {start_time}-{end_time} UTC &rarr; {environment} &rarr; <a href="{url}"> {quoted_text} </a>&rarr; {comments}</p></li>'
            preview_text = f'{symbols_str} ({company}): {start_time}-{end_time} UTC -> {environment} -> {quoted_text} -> {comments}'
    else:
        symbols = []
        if green_check_var.get():
            symbols.append(checkmark_emoji)
        if yellow_warning_var.get():
            symbols.append(warning_emoji)
        symbols_str = " ".join(symbols)
        confluence_link = f'<li><p>{symbols_str} ISH18 (SharkNinja - EMEA): {start_time}-{end_time} UTC &rarr; <a href="{url}"> example alert </a>&rarr; Deployment </p></li>'
        preview_text = f'{symbols_str} ISH18 (SharkNinja - EMEA): {start_time}-{end_time} UTC -> example alert -> deployment'

    output_text.delete("1.0", "end")
    output_text.insert("1.0", preview_text)
    update_confluence(confluence_link, confirmation)

# Create the main window
root = tk.Tk()
root.title("Confluence Link Generator")

# Input block
tk.Label(root, text="Copy paste entire alert from telegram NOT including coloured square:").grid(row=0, column=0, sticky="e")
input_text = tk.Text(root, height=10, width=100)
input_text.grid(row=0, column=1)

# Start time
tk.Label(root, text="Start Time: (FORMAT-> hh:mm in AEST 24 hour time)").grid(row=1, column=0, sticky="e")
start_time_entry = tk.Entry(root)
start_time_entry.grid(row=1, column=1)

# End time
tk.Label(root, text="End Time: (FORMAT-> hh:mm in AEST 24 hour time)").grid(row=2, column=0, sticky="e")
end_time_entry = tk.Entry(root)
end_time_entry.grid(row=2, column=1)

# Comments
tk.Label(root, text="Comments:").grid(row=3, column=0, sticky="e")
comments_text = tk.Text(root, height=10, width=100)
comments_text.grid(row=3, column=1)

# Checkbox for green check symbol
green_check_var = tk.BooleanVar()
green_check = tk.Checkbutton(root, text="Green Check", variable=green_check_var)
green_check.grid(row=4, column=1, sticky="w")

# Checkbox for yellow warning symbol
yellow_warning_var = tk.BooleanVar()
yellow_warning = tk.Checkbutton(root, text="Yellow Warning", variable=yellow_warning_var)
yellow_warning.grid(row=5, column=1, sticky="w")

# Environment checkboxes
tk.Label(root, text="Environment:").grid(row=6, column=0, sticky="e")
env_frame = tk.Frame(root)
env_frame.grid(row=6, column=1, sticky="w")

prod_lv_var = tk.BooleanVar()
prod_lv_check = tk.Checkbutton(env_frame, text="Prod (LV)", variable=prod_lv_var)
prod_lv_check.pack(side="left")

prod_ed_var = tk.BooleanVar()
prod_ed_check = tk.Checkbutton(env_frame, text="Prod (ED)", variable=prod_ed_var)
prod_ed_check.pack(side="left")

uat_lv_var = tk.BooleanVar()
uat_lv_check = tk.Checkbutton(env_frame, text="UAT (LV)", variable=uat_lv_var)
uat_lv_check.pack(side="left")

uat_ed_var = tk.BooleanVar()
uat_ed_check = tk.Checkbutton(env_frame, text="UAT (ED)", variable=uat_ed_var)
uat_ed_check.pack(side="left")

not_applicable_var = tk.BooleanVar()
not_applicable_check = tk.Checkbutton(env_frame, text="Not Applicable", variable=not_applicable_var)
not_applicable_check.pack(side="left")

# Submit button
submit_button = tk.Button(root, text="Generate Link", command=lambda: generate_confluence_link(False))
submit_button.grid(row=7, column=1)

# Output block
tk.Label(root, text="Output preview").grid(row=8, column=0, sticky="e")
output_text = tk.Text(root, height=10, width=100)
output_text.grid(row=8, column=1)

# Confirm button
confirm_button = tk.Button(root, text="Confirm and Push to Confluence", command=lambda: generate_confluence_link(True))
confirm_button.grid(row=9, column=1)

# Exit button
exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.grid(row=10, column=1)

# Start the application
root.mainloop()