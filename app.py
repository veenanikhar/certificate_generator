from flask import Flask, request, render_template, redirect, url_for, flash
import pandas as pd
import os
from PIL import Image, ImageDraw, ImageFont
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

# Define the path to save uploaded files
UPLOAD_FOLDER = 'uploads'
CERTIFICATES_FOLDER = 'certificates'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads and certificates directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CERTIFICATES_FOLDER, exist_ok=True)

# Configure email settings
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'abc@gmail.com'
SENDER_PASSWORD = 'abc@2024'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        # Save the file to the uploads folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Read the saved Excel file using pandas
        data = pd.read_excel(file_path)

        # Generate certificates and send emails
        for index, row in data.iterrows():
            name = row['Name']
            email = row['Email']
            position = row['Position']
            
            # Generate the certificate
            cert_path = generate_certificate(name, position)

        # Send the certificate via email
        send_certificate(email, cert_path)
        flash('Certificates have been sent successfully!')
        return redirect(url_for('index'))

def generate_certificate(name, position):
    # Create a blank white image as the base for the certificate
    width, height = 1200, 800
    certificate = Image.new('RGB', (width, height), 'white')

    # Set font paths and sizes (Update the paths with the correct paths on your system)
    title_font_path = 'C:/Windows/Fonts/Arialbd.ttf'  # Example path for bold font
    content_font_path = 'C:/Windows/Fonts/Arial.ttf'  # Example path for regular font

    try:
        # Load fonts
        title_font = ImageFont.truetype(title_font_path, 80)
        content_font = ImageFont.truetype(content_font_path, 50)
        signature_font = ImageFont.truetype(content_font_path, 40)
    except OSError as e:
        print(f"Font file not found: {e}")
        return None  # Return None if there's an error

    # Initialize ImageDraw
    draw = ImageDraw.Draw(certificate)

    # Add Certificate title
    title_text = "Certificate of Achievement"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) / 2, 50), title_text, font=title_font, fill='black')

    # Add the main content of the certificate
    cert_body = "This is to certify that"
    cert_body_bbox = draw.textbbox((0, 0), cert_body, font=content_font)
    cert_body_width = cert_body_bbox[2] - cert_body_bbox[0]
    draw.text(((width - cert_body_width) / 2, 200), cert_body, font=content_font, fill='black')

    # Add the name
    name_text = f"Name: {name}"
    name_bbox = draw.textbbox((0, 0), name_text, font=content_font)
    draw.text(((width - name_bbox[2] + name_bbox[0]) / 2, 300), name_text, font=content_font, fill='black')

    # Add the position
    position_text = f"Position: {position}"
    position_bbox = draw.textbbox((0, 0), position_text, font=content_font)
    draw.text(((width - position_bbox[2] + position_bbox[0]) / 2, 400), position_text, font=content_font, fill='black')

    # Add signature line
    signature_text = "Signature: ____________________"
    signature_bbox = draw.textbbox((0, 0), signature_text, font=signature_font)
    draw.text(((width - signature_bbox[2] + signature_bbox[0]) / 2, 600), signature_text, font=signature_font, fill='black')

    # Save the generated certificate
    output_path = os.path.join(CERTIFICATES_FOLDER, f"{name.replace(' ', '_')}_certificate.png")
    certificate.save(output_path)
    print(f"Certificate saved at {output_path}")

    return output_path  # Ensure the function returns the certificate path


def send_certificate(to_email, cert_path):
    # Setup the MIME
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = "Your Certificate from Astrikos"

    # Body of the email
    body = "Congratulations! Please find your certificate attached."
    msg.attach(MIMEText(body, 'plain'))

    # Attach the certificate
    with open(cert_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(cert_path)}')
        msg.attach(part)

    # Connect to the server and send the email
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()

if __name__ == '__main__':
    app.secret_key = 'supersecretkey'
    app.run(debug=True)
