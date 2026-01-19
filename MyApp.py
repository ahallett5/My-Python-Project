import os
from nicegui import ui
import openai
import smtplib
from email.message import EmailMessage

# ---------- CONFIG ----------
ADMIN_USER = 'aidan'
ADMIN_PASS = 'TTellahnadia'

users = {}  # store users: username -> password
current_user = {'name': None}

# OpenAI API key from environment
OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
openai.api_key = OPENAI_KEY

# ---------- HEADER ----------
ui.page_title('My Public App!')

with ui.header().classes('bg-blue-600 text-white'):
    ui.label('My Website').classes('text-h5')
    ui.label('Free • No Watermark').classes('text-subtitle2')

# ---------- TABS ----------
with ui.tabs().classes('w-full') as tabs:
    home_tab = ui.tab('Home')
    tools_tab = ui.tab('Tools')
    admin_tab = ui.tab('Admin')
    contact_tab = ui.tab('Contact')

with ui.tab_panels(tabs, value=home_tab).classes('w-full'):

    # ---------- HOME ----------
    with ui.tab_panel(home_tab):
        ui.label('🏠 Home').classes('text-h4')
        ui.label('Welcome to my NiceGUI website!')

    # ---------- TOOLS ----------
    with ui.tab_panel(tools_tab):
        ui.label('🛠 Tools').classes('text-h4')
        ui.label('Try our AI-powered website suggestions below:')

        user_input = ui.textarea('Describe what you want to improve')
        ai_output = ui.markdown('')

        def get_ai_suggestion():
            prompt = f"Suggest improvements for a website based on this input:\n{user_input.value}"
            try:
                response = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                ai_output.set_text(response['choices'][0]['message']['content'])
            except Exception as e:
                ai_output.set_text(f"❌ Error: {str(e)}")

        ui.button('Get AI Suggestion', on_click=get_ai_suggestion)

    # ---------- ADMIN ----------
    with ui.tab_panel(admin_tab):
        ui.label('🔐 Admin Login').classes('text-h4')

        login_user = ui.input('Username')
        login_pass = ui.input('Password', password=True)
        admin_panel = ui.column().classes('hidden')

        # admin user list display
        user_list_label = ui.markdown('No users yet')

        def update_user_list():
            user_list_label.set_text('\n'.join(f'- {u}' for u in users.keys()) or 'No users yet')

        def login_admin():
            if login_user.value == ADMIN_USER and login_pass.value == ADMIN_PASS:
                admin_panel.classes(remove='hidden')
                ui.notify('✅ Admin logged in')
                update_user_list()
            else:
                ui.notify('❌ Invalid credentials', color='red')

        ui.button('Login', on_click=login_admin)

        with admin_panel:
            ui.label('👑 Admin Panel').classes('text-h5')
            ui.markdown('### Registered Users:')
            ui.markdown('')  # spacer
            user_list_label  # dynamic user list

    # ---------- CONTACT ----------
    with ui.tab_panel(contact_tab):
        ui.label('📬 Contact').classes('text-h4')

        name_input = ui.input('Your name')
        message_input = ui.textarea('Your message')

        def send_email():
            try:
                email = EmailMessage()
                email['From'] = os.environ['EMAIL_USER']
                email['To'] = 'aidanhallett@gmail.com'
                email['Subject'] = 'New Website Message'
                email.set_content(f'From: {name_input.value}\n\n{message_input.value}')

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(
                        os.environ['EMAIL_USER'],
                        os.environ['EMAIL_PASS']
                    )
                    smtp.send_message(email)

                ui.notify('✅ Message sent!')
                name_input.value = ''
                message_input.value = ''

            except Exception as e:
                ui.notify(f'❌ Failed to send email: {str(e)}', color='red')

        ui.button('Send Message', on_click=send_email).props('color=green')

# ---------- FOOTER ----------
with ui.footer().classes('bg-gray-200'):
    ui.label('Made with NiceGUI • Free Hosting • No Watermark')

ui.label('Aidan Hallett™').classes('absolute bottom-2 right-2 text-gray-400 opacity-50 text-xs')

# ---------- RUN ----------
port = int(os.environ.get("PORT", 8080))
ui.run(host='0.0.0.0', port=port)