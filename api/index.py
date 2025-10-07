# api/index.py
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

# Correct paths for templates and static folders
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

# Flask-Mail config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")

mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        message_body = request.form.get('message')
        if email and message_body:
            try:
                msg = Message(
                    subject="Good News!",
                    recipients=[os.getenv("MAIL_USERNAME")]
                )
                
                # Plain text fallback
                msg.body = f"From: {email}\n\nMessage:\n{message_body}"
                
                # HTML version with beautiful styling
                msg.html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                </head>
                <body style="margin: 0; padding: 0; background-color: #f6f9fc; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
                    <table role="presentation" style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td align="center" style="padding: 40px 0;">
                                <table role="presentation" style="width: 600px; max-width: 100%; border-collapse: collapse; background: #ffffff; border-radius: 16px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07); overflow: hidden;">
                                    <!-- Header -->
                                    <tr>
                                        <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center;">
                                            <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 600; letter-spacing: -0.5px;">
                                                📬 New Log!
                                            </h1>
                                            <p style="margin: 10px 0 0; color: rgba(255, 255, 255, 0.9); font-size: 14px;">
                                                Someone has contacted you through your website
                                            </p>
                                        </td>
                                    </tr>
                                    
                                    <!-- Content -->
                                    <tr>
                                        <td style="padding: 40px 30px;">
                                            <!-- From Section -->
                                            <div style="margin-bottom: 20px;">
                                                <div style="display: inline-block; background: #f0f4ff; padding: 8px 16px; border-radius: 8px; margin-bottom: 10px;">
                                                    <span style="font-size: 12px; font-weight: 600; color: #667eea; text-transform: uppercase; letter-spacing: 0.5px;">From</span>
                                                </div>
                                                <div style="background: #f8fafc; border-left: 4px solid #667eea; padding: 16px 20px; border-radius: 8px;">
                                                    <a href="mailto:{email}" style="color: #1e293b; text-decoration: none; font-size: 16px; font-weight: 500;">
                                                        {email}
                                                    </a>
                                                </div>
                                            </div>
                                            
                                            <!-- Message Section -->
                                            <div>
                                                <div style="background: #f8fafc; border-left: 4px solid #667eea; padding: 16px 20px; border-radius: 8px; line-height: 1.5;">
                                                    <span style="color: #1e293b; font-size: 16px; font-weight: 500;">{message_body}</span>
                                                </div>
                                            </div>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </body>
                </html>
                """
                
                mail.send(msg)
            except Exception as e:
                print("Mail sending failed:", e)
        return redirect(url_for('index'))
    return render_template('index.html')

# For Vercel serverless deployment, export the app object
app