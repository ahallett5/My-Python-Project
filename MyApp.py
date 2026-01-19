import os
import smtplib
from email.message import EmailMessage
from nicegui import ui

ui.page_title('My Public App!')

# ---------- AUTH ----------
ADMIN_USER = 'aidan'
ADMIN_PASS = 'TTellahnadia'
admin_logged_in = {'value': False}

# ---------- HEADER ----------
with ui.header().classes('bg-blue-600 text-white'):
    ui.label('My Website').classes('text-h5')
    ui.label('Free • No Watermark').classes('text-subtitle2')

# ---------- TABS ----------
with ui.tabs().classes('w-full') as tabs:
    home = ui.tab('Home')
    tools = ui.tab('Tools')
    admin = ui.tab('Admin')
    contact = ui.tab('Contact')

with ui.tab_panels(tabs, value=home).classes('w-full'):

    # ---------- HOME ----------
    with ui.tab_panel(home):
        ui.label('🏠 Home').classes('text-h4')
        ui.label('Welcome to my NiceGUI website!')

    # ---------- TOOLS ----------
    with ui.tab_panel(tools):
        ui.label('🛠 Tools').classes('text-h4')
        ui.notify('More tools coming soon!')

    # ---------- ADMIN ----------
    with ui.tab_panel(admin):
        ui.label('🔐 Admin Login').classes('text-h4')

        username = ui.input('Username')
        password = ui.input('Password', password=True)
        admin_area = ui.column().classes('hidden')

        def login():
            if username.value == ADMIN_USER and password.value == ADMIN_PASS:
                admin_logged_in['value'] = True
                admin_area.classes(remove='hidden')
                ui.notify('✅ Admin logged in')
            else:
                ui.notify('❌ Invalid credentials', color='red')

        ui.button('Login', on_click=login)

        with admin_area:
            ui.separator()
            ui.label('👑 Admin Panel').classes('text-h5')
            ui.label('Welcome, Aidan!')
            ui.button('Restart App', on_click=lambda: ui.notify('Restart not enabled'))

    # ---------- CONTACT ----------
    with ui.tab_panel(contact):
        ui.label('📬 Contact').classes('text-h4')

        name = ui.input('Your name')
        message = ui.textarea('Your message')

        def send_email():
            try:
                email = EmailMessage()
                email['From'] = os.environ['EMAIL_USER']
                email['To'] = 'aidanhallett@gmail.com'
                email['Subject'] = 'New Website Message'
                email.set_content(f'From: {name.value}\n\n{message.value}')

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(
                        os.environ['EMAIL_USER'],
                        os.environ['EMAIL_PASS']
                    )
                    smtp.send_message(email)

                ui.notify('✅ Message sent!')
                name.value = ''
                message.value = ''

            except Exception as e:
                ui.notify('❌ Failed to send email', color='red')

        ui.button('Send Message', on_click=send_email).props('color=green')

# ---------- FOOTER ----------
with ui.footer().classes('bg-gray-200'):
    ui.label('Made with NiceGUI • Free Hosting • No Watermark')

ui.label('Aidan Hallett™').classes(
    'absolute bottom-2 right-2 text-gray-400 opacity-50 text-xs'
)

# ---------- RUN ----------
port = int(os.environ.get("PORT", 8080))
ui.run(host='0.0.0.0', port=port)