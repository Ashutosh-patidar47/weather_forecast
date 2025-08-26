import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Render HTML email
def render_html(city, current, forecast):
    forecast_html = ""
    for d in forecast:
        forecast_html += f"""
        <div style="margin:10px;padding:10px;border:1px solid #ddd;border-radius:8px;background:#f9f9f9;">
            <b>{d['date']}</b><br>
            {d['desc']} | 🌡️ {d['min']}°C – {d['max']}°C
        </div>
        """

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background:#f5f7fa; padding:20px;">
        <h2 style="color:#1e3c72;">🌤 Weather Forecast for {city}</h2>
        <div style="padding:12px;background:#ffffff;border-radius:10px;box-shadow:0 2px 6px rgba(0,0,0,0.1);">
            <h3>Current Weather</h3>
            <p><b>{current['temp']}°C</b> · {current['desc']}</p>
            <p>💧 Humidity: {current['humidity']}% · 🌬️ Wind: {current['wind']} m/s</p>
        </div>
        <h3 style="margin-top:20px;">📅 3-Day Forecast</h3>
        {forecast_html}
    </body>
    </html>
    """
    return html

# Send email
def send_email(to_email, subject, html_body, text_body, sender, password, smtp_server, port):
    msg = MIMEMultipart("alternative")
    msg["From"] = sender
    msg["To"] = to_email
    msg["Subject"] = subject

    part1 = MIMEText(text_body, "plain")
    part2 = MIMEText(html_body, "html")

    msg.attach(part1)
    msg.attach(part2)

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
