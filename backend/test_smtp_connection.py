#!/usr/bin/env python3
"""
SMTP Connection Test Script for CampusEats
Tests Gmail SMTP configuration before deployment
"""
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ANSI color codes for pretty output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_header(text):
    """Print formatted header"""
    print(f"\n{BLUE}{BOLD}{'='*60}{RESET}")
    print(f"{BLUE}{BOLD}{text.center(60)}{RESET}")
    print(f"{BLUE}{BOLD}{'='*60}{RESET}\n")

def print_success(text):
    """Print success message"""
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    """Print error message"""
    print(f"{RED}❌ {text}{RESET}")

def print_warning(text):
    """Print warning message"""
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_info(text):
    """Print info message"""
    print(f"{BLUE}ℹ️  {text}{RESET}")

def test_smtp_connection():
    """Test SMTP connection to Gmail"""

    print_header("CampusEats SMTP Connection Test")

    # Get configuration from environment
    smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_email = os.getenv('SMTP_EMAIL', '')
    smtp_password = os.getenv('SMTP_PASSWORD', '')
    smtp_from_name = os.getenv('SMTP_FROM_NAME', 'CampusEats')
    test_recipient = os.getenv('TEST_EMAIL', smtp_email)

    print_info(f"SMTP Host: {smtp_host}")
    print_info(f"SMTP Port: {smtp_port}")
    print_info(f"SMTP Email: {smtp_email}")
    print_info(f"From Name: {smtp_from_name}")
    print_info(f"Test Recipient: {test_recipient}")

    # Validate configuration
    if not smtp_email:
        print_error("SMTP_EMAIL not set in .env file")
        return False

    if not smtp_password:
        print_error("SMTP_PASSWORD not set in .env file")
        print_warning("Generate Gmail App Password at: https://myaccount.google.com/apppasswords")
        return False

    print(f"\n{BOLD}Running SMTP connection tests...{RESET}\n")

    try:
        # Test 1: Connect to SMTP server
        print_info("Test 1: Connecting to SMTP server...")
        context = ssl.create_default_context()
        server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
        print_success("Connected to SMTP server")

        # Test 2: STARTTLS
        print_info("Test 2: Upgrading to TLS...")
        server.starttls(context=context)
        print_success("TLS upgrade successful")

        # Test 3: Authentication
        print_info("Test 3: Authenticating with Gmail...")
        server.login(smtp_email, smtp_password)
        print_success("Authentication successful")

        # Test 4: Send test email (optional)
        send_test = input(f"\n{YELLOW}Do you want to send a test email to {test_recipient}? (y/n): {RESET}").lower()

        if send_test == 'y':
            print_info("Test 4: Sending test email...")

            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = "CampusEats - SMTP Test Email"
            message['From'] = f'{smtp_from_name} <{smtp_email}>'
            message['To'] = test_recipient

            # HTML content
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); padding: 40px; text-align: center; border-radius: 10px;">
        <h1 style="color: white; margin: 0; font-size: 32px;">🍽️ CampusEats</h1>
        <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 16px;">SMTP Test Successful!</p>
    </div>

    <div style="background: #f8f9fa; padding: 30px; margin-top: 20px; border-radius: 10px;">
        <h2 style="color: #1e3a8a; margin-top: 0;">✅ Configuration Working!</h2>
        <p style="color: #475569; font-size: 16px; line-height: 1.6;">
            Your Gmail SMTP configuration is working correctly. You can now send OTP emails to users.
        </p>

        <div style="background: #e0f2fe; border-left: 4px solid #3b82f6; padding: 15px; margin: 20px 0;">
            <strong style="color: #1e3a8a;">Configuration Details:</strong><br>
            <span style="color: #64748b;">SMTP Host: {smtp_host}</span><br>
            <span style="color: #64748b;">SMTP Port: {smtp_port}</span><br>
            <span style="color: #64748b;">From Email: {smtp_email}</span>
        </div>

        <p style="color: #64748b; font-size: 14px; margin-top: 30px;">
            This is an automated test email from your CampusEats backend.
        </p>
    </div>

    <div style="text-align: center; padding: 20px; color: #94a3b8; font-size: 14px;">
        © 2025 CampusEats - Email Configuration Test
    </div>
</body>
</html>
            """

            # Plain text version
            text_content = f"""
CampusEats - SMTP Test Email

✅ Configuration Working!

Your Gmail SMTP configuration is working correctly.
You can now send OTP emails to users.

Configuration Details:
- SMTP Host: {smtp_host}
- SMTP Port: {smtp_port}
- From Email: {smtp_email}

This is an automated test email from your CampusEats backend.

© 2025 CampusEats - Email Configuration Test
            """

            # Attach both versions
            text_part = MIMEText(text_content, 'plain')
            html_part = MIMEText(html_content, 'html')
            message.attach(text_part)
            message.attach(html_part)

            # Send email
            server.send_message(message)
            print_success(f"Test email sent to {test_recipient}")
            print_info(f"Check your inbox (and spam folder) for the test email")

        # Close connection
        server.quit()
        print_success("SMTP connection closed")

        # Success summary
        print_header("Test Results: ALL PASSED ✅")
        print(f"{GREEN}Your Gmail SMTP configuration is working correctly!{RESET}")
        print(f"\n{BOLD}Next Steps:{RESET}")
        print(f"1. Set EMAIL_TESTING_MODE=false in your .env or Render")
        print(f"2. Add these environment variables to Render:")
        print(f"   - SMTP_EMAIL={smtp_email}")
        print(f"   - SMTP_PASSWORD=[your-app-password]")
        print(f"   - SMTP_HOST={smtp_host}")
        print(f"   - SMTP_PORT={smtp_port}")
        print(f"3. Deploy and test registration with real emails")

        return True

    except smtplib.SMTPAuthenticationError as e:
        print_error(f"Authentication failed: {str(e)}")
        print_warning("Check your Gmail App Password")
        print_info("Generate new one at: https://myaccount.google.com/apppasswords")
        print_info("Make sure 2-Step Verification is enabled")
        return False

    except smtplib.SMTPException as e:
        print_error(f"SMTP error: {str(e)}")
        return False

    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        success = test_smtp_connection()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Test cancelled by user{RESET}")
        exit(1)
