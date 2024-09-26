# WJF

## Overview

WJF is a tool designed to automate the logging of daily alerts to the Protol document (also known as WJF). This tool simplifies the process of recording incidents and updating the WJF in an efficient manner.

## Installation

Before running WJF, ensure you have the necessary dependencies installed. You can install them using pip:

```bash
pip install -r requirements.txt
```

## Configuration
In order to configure the tool a correctly structured .env file in the root directory of the project is required. This file should contain your Intershop Confluence API key and email address. Use the following structure:

CONFLUENCE_API_KEY='YOUR_API_KEY_HERE'

CONFLUENCE_EMAIL='YOUR_EMAIL_HERE'

## Running the Script
To execute the script, use the following command:

```bash 
python WJF.py
```

Follow the on-screen instructions to automatically generate and update the APAC confluence document [Alert Copy Space](https://intershop-apac.atlassian.net/wiki/spaces/MSAPAC/pages/620033507365/Alert+Copy+Space).

From there you can copy and paste the text over easily, and quickly.

## Notes
Make sure to update the .env file with your actual API key and email address.
If you encounter any issues, check the script's output in your cmd window for error messages.

## Contribution
If you would like to contribute to the development of WJF, please fork the repository and submit a pull request with your changes. Ensure that you follow best practices and include tests for any new features.

## License
This project is licensed under the MIT License.
