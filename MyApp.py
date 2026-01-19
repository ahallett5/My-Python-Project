import os
from nicegui import ui
import openai
import smtplib
from email.message import EmailMessage

# ---------- CONFIG ----------
ADMIN_USER = 'aidan'
ADMIN_PASS = 'TTellahnadia'

users = {}  # store users: username -> password
messages = []  # messages sent via contact form
current_user = {'name': None}

# OpenAI API key from environment
OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
openai.api_key = OPENAI_KEY

# ---------- HEADER ----------
ui.page_title('My Public App!')

with ui.header().classes('bg-blue-600 text-white'):
    ui.label('My Website by Aidan Hallett').classes('text-h5')
    ui.label('Free • No Watermark').classes('text-subtitle2')

# ---------- TABS ----------
with ui.tabs().classes('w-full') as tabs:
    home_tab = ui.tab('Home')
    tools_tab = ui.tab('AI Chatbot')
    admin_tab = ui.tab('Admin')
    contact_tab = ui.tab('Contact')

with ui.tab_panels(tabs, value=home_tab).classes('w-full'):

    # ---------- HOME ----------
    with ui.tab_panel(home_tab):
        ui.label('🏠 Home').classes('text-h4')
        ui.markdown("""
Welcome to my NiceGUI website made by **Aidan Hallett**!

Use the tabs to explore tools, AI chatbot, contact form, and admin features.
        """)

    # ---------- AI CHATBOT ----------
    with ui.tab_panel(tools_tab):
        ui.label('🤖 AI Chatbot').classes('text-h4')
        ui.markdown('Ask questions or get suggestions about your website.')

        question_input = ui.textarea('Ask me something...')
        ai_answer = ui.markdown('')

        def ask_ai():
            if not OPENAI_KEY:
                ai_answer.set_text("❌ OpenAI API key not set!")
                return
            try:
                response = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=[{"role": "user", "content": question_input.value}],
                    temperature=0.7
                )
                ai_answer.set_text(response['choices'][0]['message']['content'])
            except Exception as e:
                ai_answer.set_text(f"❌ Error: {str(e)}")

        ui.button('Ask AI', on_click=ask_ai)

    # ---------- ADMIN ----------
    with ui.tab_panel(admin_tab):
        ui.label('🔐 Admin Login').classes('text-h4')

        login_user = ui.input('Username')
        login_pass = ui.input('Password', password=True)
        admin_panel = ui.column().classes('hidden')

        user_list_label = ui.markdown('No users yet')
        messages_label = ui.markdown('No messages yet')

        def update_user_list():
            user_list_label.set_text('\n'.join(f'- {u}' for u in users.keys()) or 'No users yet')

        def update_messages():
            messages_label.set_text('\n'.join(f"- From {m['name']}: {m['message']}" for m in messages) or 'No messages yet')

        def login_admin():
            if login_user.value == ADMIN_USER and login_pass.value == ADMIN_PASS:
                admin_panel.classes(remove='hidden')
                ui.notify('✅ Admin logged in')
                update_user_list()
                update_messages()
            else:
                ui.notify('❌ Invalid credentials', color='red')

        ui.button('Login', on_click=login_admin)

        with admin_panel:
            ui.label('👑 Admin Panel').classes('text-h5')
            ui.markdown('### Registered Users:')
            user_list_label
            ui.markdown('### Messages Received:')
            messages_label

            # Example admin actions
            def clear_messages():
                messages.clear()
                update_messages()
                ui.notify('✅ Messages cleared')

            def clear_users():
                users.clear()
                update_user_list()
                ui.notify('✅ Users cleared')

            ui.button('Clear Messages', on_click=clear_messages).props('color=red')
            ui.button('Clear Users', on_click=clear_users).props('color=orange')

    # ---------- CONTACT ----------
    with ui.tab_panel(contact_tab):
        ui.label('📬 Contact').classes('text-h4')
        ui.markdown('Send a message to **Aidan Hallett**.')

        name_input = ui.input('Your name')
        message_input = ui.textarea('Your message')

        def send_email():
            msg_content = f"From: {name_input.value}\nMessage:\n{message_input.value}"
            messages.append({'name': name_input.value, 'message': message_input.value})  # store in memory

            # Optional: send email
            try:
                email = EmailMessage()
                email['From'] = os.environ['EMAIL_USER']
                email['To'] = 'aidanhallett@gmail.com'
                email['Subject'] = 'New Website Message'
                email.set_content(msg_content)

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
                    smtp.send_message(email)

                ui.notify('✅ Message sent!')
                name_input.value = ''
                message_input.value = ''
            except Exception as e:
                ui.notify(f"❌ Could not send email: {str(e)}", color='red')

        ui.button('Send Message', on_click=send_email).props('color=green')

# ---------- FOOTER ----------
with ui.footer().classes('bg-gray-200'):
    ui.label('Made with NiceGUI by Aidan Hallett • Free Hosting • No Watermark')

ui.label('Aidan Hallett™').classes('absolute bottom-2 right-2 text-gray-400 opacity-50 text-xs')

# ---------- RUN ----------
port = int(os.environ.get("PORT", 8080))
ui.run(host='0.0.0.0', port=port)