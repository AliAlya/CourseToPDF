import pandas as pd
from redmail import gmail
from datetime import datetime, timedelta
import time

# Configure your Gmail credentials
gmail.username = 'teamcolorfication@gmail.com'
gmail.password = 'uujm vmpx djht kwmj'

# Load the CSV file
df = pd.read_csv('contacts.csv')

# Check if 'last_sent' and 'step' columns exist, if not, create them
if 'last_sent' not in df.columns:
    df['last_sent'] = None
if 'step' not in df.columns:
    df['step'] = 0

# Email templates
email_templates = {
    0: """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .greeting {{
                font-size: 1.2em;
            }}
            .content {{
                margin-top: 20px;
            }}
            .highlight {{
                font-weight: bold;
                color: #0056b3;
            }}
            .signoff {{
                margin-top: 20px;
            }}
            .company {{
                font-weight: bold;
                color: #333;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <p class="greeting">Hey {name},</p>

            <div class="content">
                <p>The content you produce and the value you provide are nothing short of amazing! You've built an incredible community of <span class="highlight">nurses</span>. There are creators with smaller audiences than yours making over 10k a month, and we believe you can achieve even more.</p>
                
                <p>We noticed you haven't implemented this strategy yet, which could bring you an additional 10k per month while helping your audience and providing even more value for them. Our team specializes in helping amazing creators like you fully monetize their existing audience. Best of all, there's minimal extra work on your part, and we don't charge anything upfront. Sounds too good to be true, right?</p>
                
                <p>If you're interested, I can send you a quick personal Loom recording detailing exactly how we plan to do this and how we can help you. We only work with a limited number of creators at a time, so let me know if you are interested and I can send it right over!</p>

                <p class="highlight">Looking forward to hearing from you, {name}!</p>
            </div>

            <div class="signoff">
                <p>Best,</p>
                <p>Team,<br><span class="company">HAH Agency</span></p>
            </div>
        </div>
    </body>
    </html>
    """,
    1: "<p>Hello {name},</p><p>This is your step 1 follow-up email.</p>",
    2: "<p>Hi {name},</p><p>This is your step 2 follow-up email.</p>"
}

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    # Determine the step
    step = row['step']
    
    # Extract the first name from the full name
    first_name = row['name'].split()[0]

    followup_time_limit = 120
    time_between_emails = 2
    # Check if 30 minutes have passed since the last email was sent
    time_to_post = pd.isnull(row['last_sent']) or datetime.now() - datetime.strptime(row['last_sent'], '%Y-%m-%d %H:%M:%S') > timedelta(minutes=followup_time_limit)
    
    # Send the email if step is 0 (initial email) or if follow-up step is required
    if time_to_post and step in email_templates:
        # Personalize the email content based on the step
        html_content = email_templates[step].format(
            name=first_name.capitalize(),
            # niche=row['niche'],
            # price=row['price']
        )
        
        gmail.send(
            subject=f"Amazing partnership oppportunity!",
            sender=gmail.username,
            receivers=[row['email']],
            html=html_content
        )
        
        # Update 'last_sent' and 'step' columns
        df.at[index, 'last_sent'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df.at[index, 'step'] = step + 1
        print(f"{row['email']} - Email sent at step {step}")
        time.sleep(time_between_emails)
    else:
        print(f"{row['email']} - Not ready. Skipping")

# Save the updated DataFrame back to the CSV file
df.to_csv('contacts.csv', index=False)

print("Emails sent and history updated successfully!")