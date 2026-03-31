import smtplib
from email.mime.text import MIMEText

# Test credentials
email = "projectfire672@gmail.com"
password = "xskrglbrwlngaxmz"

print("🔍 Testing Gmail SMTP connection...")
print(f"📧 Email: {email}")
print(f"🔑 Password: {password}\n")

try:
    # Connect to Gmail SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    print("✅ Connected to SMTP server")
    
    server.starttls()
    print("✅ TLS enabled")
    
    server.login(email, password)
    print("✅ LOGIN SUCCESSFUL!")
    
    # Send a test email
    msg = MIMEText("Test email from Fire Detection System")
    msg['Subject'] = '🔥 Test Email'
    msg['From'] = email
    msg['To'] = 'padirishitha13@gmail.com'
    
    server.send_message(msg)
    print("✅ Test email sent successfully!")
    
    server.quit()
    print("\n✅ ALL TESTS PASSED! Email configuration is working correctly.")
    
except smtplib.SMTPAuthenticationError as e:
    print(f"\n❌ AUTHENTICATION FAILED!")
    print(f"Error: {e}")
    print("\n💡 Possible solutions:")
    print("1. Enable 2-Step Verification: https://myaccount.google.com/security")
    print("2. Generate App Password: https://myaccount.google.com/apppasswords")
    print("3. Allow less secure apps (not recommended)")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
