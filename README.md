# Certificate Generator

## Overview

This Flask application allows users to upload an Excel file containing names, email addresses, and positions. The application generates personalized certificates based on the uploaded data and sends them via email to the specified addresses.

## Features

- Upload an Excel file with user details
- Generate personalized certificates
- Send certificates via email

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/certificate-generator.git
    cd certificate-generator
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - **On Windows:**

        ```bash
        venv\Scripts\activate
        ```

    - **On macOS/Linux:**

        ```bash
        source venv/bin/activate
        ```

4. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. **Update Email Settings:**

    Edit the `app.py` file to configure your email settings:

    ```python
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SENDER_EMAIL = 'your-email@gmail.com'
    SENDER_PASSWORD = 'your-email-password'
    ```

2. **Font Paths:**

    Ensure that the font paths specified in the `generate_certificate` function are correct and point to valid font files on your system.

## Usage

1. **Run the Flask application:**

    ```bash
    python app.py
    ```

2. **Navigate to `http://127.0.0.1:5000` in your web browser.**

3. **Upload an Excel file:**

    - The Excel file should have columns: `Name`, `Email`, and `Position`.

4. **Click the upload button.**

    The application will generate certificates and send them to the provided email addresses.

## File Structure

- `app.py`: Main Flask application file
- `requirements.txt`: Python dependencies
- `uploads/`: Directory to store uploaded files
- `certificates/`: Directory to store generated certificates
- `templates/`: Directory for HTML templates

## Contributing

1. **Fork the repository**
2. **Create a new branch:**

    ```bash
    git checkout -b feature/your-feature
    ```

3. **Make your changes and commit:**

    ```bash
    git add .
    git commit -m 'Add new feature'
    ```

4. **Push to the branch:**

    ```bash
    git push origin feature/your-feature
    ```

5. **Create a pull request**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [Pandas](https://pandas.pydata.org/)
- [Pillow](https://pillow.readthedocs.io/en/stable/)
- [SMTP Library](https://docs.python.org/3/library/smtplib.html)
