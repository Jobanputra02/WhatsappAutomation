## Features

- Automated login using saved browser session data
- Create WhatsApp groups and add participants
- Open individual or group chats
- Send text messages and files (images, videos, documents)
- Extract contact numbers from contact names
- Automatic base64 encoding and decoding for media handling
- Custom folders for browser data and media storage

## Installation and Setup

1. Clone the repository

```
git clone https://github.com/yourusername/whatsapp-automation.git
cd whatsapp-automation
```

2. (Optional) Create and activate a virtual environment

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages

```
pip install -r requirements.txt
```

4. Download and set up ChromeDriver

Automatically handled via webdriver_manager, but make sure Chrome is installed and chromedriver version is matched.

5. Run the script

```
python main.py
```
The browser will launch, and WhatsApp Web will open. If it's the first run, scan the QR code. Future sessions will be auto-logged in using saved browser data.

## Usage

Here are the core functions you can use through the whatsappautomation class:

### Authentication
```whatsapp_automate.whatsapp_authenticated()```

### Open Chat
```whatsapp_automate.open_contact(contact_number="1234567890")```

```whatsapp_automate.open_group(group_id="yourGroupID")```

### Send Message
```whatsapp_automate.send_msg("Hello, this is an automated message.")```

### Send File
```whatsapp_automate.send_file(filepath=r"path_to_your_file")```
### Create Group
```whatsapp_automate.create_group("Group Name", ["1234567890", "9876543210"])```

### Extract Numbers from Contact Name
```
numbers = whatsapp_automate.get_contact_number_from_name("John Doe")
```

## Project Structure

```WhatsApp Automation Data/
├── Browser Data/       # Stores session info to avoid re-login
└── WhatsApp Media/     # Stores uploaded/downloaded media files
```

## Known Limitations
- UI of WhatsApp Web changes frequently, so selectors may break.
- Requires manual QR code scanning every session.
- Paths are hardcoded for local testing, adjust them for different environments.
- Error handling for stale elements and unresponsive pages can be improved.

## Notes
- Ensure the contact numbers include the country code and are in international format (e.g., +491234567890).
- The file path for media should be absolute.
- This script is for educational purposes only. Automating WhatsApp may violate its terms of service. Use responsibly and at your own risk.
- Author is not responsible for any blockage or violating official terms and conditions for your usage.

## Author
Chaitanya Jobanputra

