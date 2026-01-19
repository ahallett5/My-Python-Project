import os
from nicegui import ui
import openai

# ---------------- CONFIG ----------------
ui.page_title('My Public App!')

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# ---------------- GLOBAL DATA ----------------
users = {}  # username -> password (very simple in-memory storage)
current_user = {'username': None}

# ---------------- HEADER ----------------
with ui.header().classes('bg-blue-600 text-white'):
    ui.label('My Website').classes('text-h5')
    ui.label('Free No Watermark').classes('text-subtitle2')

# ---------------- TABS ----------------
with ui.tabs() as tabs:
    home_tab = ui.tab('Home')
    tools_tab = ui.tab('Tools')
    about_tab = ui.tab('About')
    contact_tab = ui.tab('Contact')
    admin_tab = ui.tab('Admin')
    account_tab = ui.tab('Account')

# ---------------- TAB PANELS ----------------
with ui.tab_panels(tabs, value=home_tab):

    # ----- HOME -----
    with ui.tab_panel(home_tab):
        ui.label('🏠 Home').classes('text-h4')
        ui.markdown("""
Welcome to my **NiceGUI app** by **Aidan Hallett™**!

Click the buttons below:
        """)

        def hello():
            ui.notify('Hello! Thanks for visiting my app 😄')

        def surprise():
            ui.notify('🎉 Surprise! You found the secret button!')

        ui.button('Say Hello', on_click=hello)
        ui.button('Surprise Me', on_click=surprise).props('color=purple')

    # ----- TOOLS -----
    with ui.tab_panel(tools_tab):
        ui.label('🛠 Tools & AI Chat').classes('text-h4')

        # Simple text tool
        text_input = ui.input('Type something')
        def show_text():
            ui.notify(f'You typed: {text_input.value}')
        ui.button('Show Text', on_click=show_text)

        # Counter tool
        count = {'value': 0}
        counter_label = ui.label('Counter: 0')
        def increase():
            count['value'] += 1
            counter_label.set_text(f'Counter: {count["value"]}')
        ui.button('Increase Counter', on_click=increase)

        # AI Chatbot
        ui.separator()
        ai_input = ui.input('Ask AI a question:')
        ai_response = ui.label('AI Response will appear here')

        def ask_ai():
            if not ai_input.value.strip():
                ui.notify('Please type a question first')
                return
            try:
                response = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=[{"role": "user", "content": ai_input.value}]
                )
                ai_response.set_text(response['choices'][0]['message']['content'])
            except Exception as e:
                ai_response.set_text(f"Error: {e}")

        ui.button('Ask AI', on_click=ask_ai).props('color=purple')

    # ----- ABOUT -----
    with ui.tab_panel(about_tab):
        ui.label('ℹ️ About').classes('text-h4')
        ui.markdown("""
This website is built using **NiceGUI** and Python.

**Features:**
- Multiple sections
- Buttons & Inputs
- AI Chatbot
- Admin Login with privileges
- User Accounts (Signup/Login)
- Free hosting & no watermark

**Made by Aidan Hallett™**
        """)

    # ----- CONTACT -----
    with ui.tab_panel(contact_tab):
        ui.label('📬 Contact').classes('text-h4')
        name_input = ui.input('Your name')
        message_input = ui.textarea('Your message')

        def send_message():
            ui.notify(f'Thanks {name_input.value}! Message sent.')
            name_input.value = ''
            message_input.value = ''

        ui.button('Send Message', on_click=send_message).props('color=green')

    # ----- ADMIN -----
    with ui.tab_panel(admin_tab):
        ui.label('🔒 Admin Login').classes('text-h4')
        username_input = ui.input('Username')
        password_input = ui.input('Password', password=True)
        login_status = ui.label('')

        # Admin actions (hidden until login)
        admin_actions = ui.column()
        admin_actions.set_visible(False)

        def admin_login():
            if username_input.value == 'aidan' and password_input.value == 'TTellahnadia':
                login_status.set_text('✅ Logged in as Admin!')
                ui.notify('Welcome Admin! You now have special privileges.')
                admin_actions.set_visible(True)
            else:
                login_status.set_text('❌ Invalid login')
                ui.notify('Wrong credentials')

        ui.button('Login', on_click=admin_login)
        ui.label('Admin Actions:').classes('text-h6')
        ui.button('Do Admin Task', on_click=lambda: ui.notify('Admin did something!'), parent=admin_actions)

    # ----- ACCOUNT -----
    with ui.tab_panel(account_tab):
        ui.label('👤 User Account').classes('text-h4')

        signup_username = ui.input('Signup Username')
        signup_password = ui.input('Signup Password', password=True)
        signup_status = ui.label('')

        def signup():
            if signup_username.value in users:
                signup_status.set_text('❌ Username already exists')
            else:
                users[signup_username.value] = signup_password.value
                signup_status.set_text('✅ Signup successful!')
                ui.notify(f'Welcome {signup_username.value}! You can now login.')

        ui.button('Signup', on_click=signup)

        login_username = ui.input('Login Username')
        login_password = ui.input('Login Password', password=True)
        login_status_user = ui.label('')

        def login():
            if login_username.value in users and users[login_username.value] == login_password.value:
                login_status_user.set_text(f'✅ Logged in as {login_username.value}')
                current_user['username'] = login_username.value
                ui.notify(f'Welcome {login_username.value}!')
            else:
                login_status_user.set_text('❌ Wrong credentials')

        ui.button('Login', on_click=login)

# ---------------- FOOTER ----------------
with ui.footer().classes('bg-gray-200'):
    ui.label('Made with NiceGUI • Free Hosting • No Watermark • By Aidan Hallett™')

# ---------------- RUN ----------------
port = int(os.environ.get('PORT', 8080))
ui.run(host='0.0.0.0', port=port)