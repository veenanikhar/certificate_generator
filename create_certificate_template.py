def generate_certificate(name, position):
    # Load the certificate template
    template_path = 'certificate_template.png'
    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)

    # Define the font and size
    font_path = "arial.ttf"  # Ensure this path is correct
    font_name = ImageFont.truetype(font_path, 40)
    font_position = ImageFont.truetype(font_path, 30)

    # Define text positions based on your template layout
    title_x, title_y = 150, 50
    subtitle_x, subtitle_y = 150, 150
    name_x, name_y = 150, 250
    position_x, position_y = 150, 300
    signature_x, signature_y = 150, image.height - 100

    # Draw the certificate title
    title_text = "Certificate of Achievement"
    draw.text((title_x, title_y), title_text, font=font_name, fill="black")

    # Draw "This is to certify that" text
    subtitle_text = "This is to certify that"
    draw.text((subtitle_x, subtitle_y), subtitle_text, font=font_name, fill="black")

    # Draw name and position
    name_text = f"Name: {name}"
    position_text = f"Position: {position}"
    print(name_text)

    draw.text((name_x, name_y), name_text, font=font_position, fill="black")
    draw.text((position_x, position_y), position_text, font=font_position, fill="black")

    # Add a signature line
    signature_text = "Signature: ____________________"
    draw.text((signature_x, signature_y), signature_text, font=font_position, fill="black")

    # Save the certificate
    cert_path = os.path.join(CERTIFICATES_FOLDER, f"{name}_certificate.png")
    image.save(cert_path)

    return cert_path
