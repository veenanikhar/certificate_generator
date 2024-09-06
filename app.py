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
SENDER_EMAIL = 'vnikhar01@gmail.com'
SENDER_PASSWORD = 'Cocoa@2024'

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
    # Load the certificate template
    template_path = 'certificate_template.png'
    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)

    # Define the font and size
    font_path = "arial.ttf"  # Ensure this path is correct
    font_name = ImageFont.truetype(font_path, 40)
    font_position = ImageFont.truetype(font_path, 30)

    # Helper function to center text
    def draw_centered_text(draw, text, font, y_position):
        # Use textbbox to get bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = (image.width - text_width) / 2
        text_y = y_position
        draw.text((text_x, text_y), text, font=font, fill="black")

    # Draw the certificate title
    title_text = "Certificate of Achievement"
    draw_centered_text(draw, title_text, font_name, 50)

    # Draw "This is to certify that" text
    subtitle_text = "This is to certify that"
    draw_centered_text(draw, subtitle_text, font_name, 150)

    # Draw placeholders for name and position
    name_text = f"Name: {name}"
    position_text = f"Position: {position}"

    # Adjust y_positions based on your template design
    draw_centered_text(draw, name_text, font_position, 250)
    draw_centered_text(draw, position_text, font_position, 300)

    # Add a signature line
    signature_text = "Signature: ____________________"
    draw_centered_text(draw, signature_text, font_position, image.height - 100)

    # Save the certificate
    cert_path = os.path.join(CERTIFICATES_FOLDER, f"{name}_certificate.png")
    image.save(cert_path)

    return cert_path

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
