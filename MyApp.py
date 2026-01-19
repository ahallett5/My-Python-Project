import os
from nicegui import ui
import openai

# ---------------------- CONFIG ----------------------
openai.api_key = os.environ.get("OPENAI_API_KEY")  # Set in Render environment
ADMIN_USERNAME = 'aidan'
ADMIN_PASSWORD = 'TTellahnadia'

# ---------------------- PAGE TITLE ----------------------
ui.page_title('My Public App!')

# ---------------------- HEADER ----------------------
with ui.header().classes('bg-blue-600 text-white'):
    ui.label('My Website').classes('text-h5')
    ui.label('Free No Watermark').classes('text-subtitle2')

# ---------------------- TABS ----------------------
with ui.tabs().classes('w-full') as tabs:
    home_tab = ui.tab('Home')
    tools_tab = ui.tab('Tools')
    about_tab = ui.tab('About')
    contact_tab = ui.tab('Contact')

with ui.tab_panels(tabs, value=home_tab).classes('w-full'):

    # ----- HOME -----
    with ui.tab_panel(home_tab):
        ui.label('🏠 Home').classes('text-h4')
        ui.label('Welcome to my NiceGUI app made by Aidan Hallett! Click the buttons below:')

        def hello():
            ui.notify('Hello! Thanks for visiting my app 😄')

        def surprise():
            ui.notify('🎉 Surprise! You found the secret button!')

        ui.button('Say Hello', on_click=hello)
        ui.button('Surprise Me', on_click=surprise).props('color=purple')

    # ----- TOOLS -----
    with ui.tab_panel(tools_tab):
        ui.label('🛠 Tools').classes('text-h4')

        # Text input
        user_input = ui.input('Type something')

        def show_text():
            ui.notify(f'You typed: {user_input.value}')

        ui.button('Show my text', on_click=show_text)

        # Counter
        count = {'value': 0}
        counter_label = ui.label('Counter: 0')

        def increase():
            count['value'] += 1
            counter_label.set_text(f'Counter: {count["value"]}')

        ui.button('Increase Counter', on_click=increase)

# ----- ABOUT -----
with ui.tab_panel(about_tab):
    ui.label('ℹ️ About').classes('text-h4')
    ui.markdown("""
This website is built using **NiceGUI** and Python.

**Features:**
- Multiple sections
- Buttons
- Inputs
- AI Chatbot
- Admin Panel with special privileges
- Fully free hosting
- No watermark
- Shareable public URL
    """)

# ----- CONTACT -----
with ui.tab_panel(contact_tab):
    ui.label('📬 Contact').classes('text-h4')
    name_input = ui.input('Your name')
    message_input = ui.textarea('Your message')

    def send_message():
        ui.notify(f'Thanks {name_input.value}! Message sent.')
        # You can integrate email sending here
        name_input.value = ''
        message_input.value = ''

    ui.button('Send Message', on_click=send_message).props('color=green')

# ---------------------- ADMIN LOGIN ----------------------
ui.label('🔒 Admin Login').classes('text-h5')

username_input = ui.input('Username')
password_input = ui.input('Password', password=True)

admin_actions_container = ui.column()
admin_actions_container.style('display: none')  # hidden at start

with admin_actions_container:
    ui.label('⚡ Admin Panel').classes('text-h5 text-red-600')

    def show_users():
        ui.notify('Showing all users (example)')

    def reset_counter():
        count['value'] = 0
        counter_label.set_text(f'Counter: {count["value"]}')
        ui.notify('Counter reset!')

    ui.button('Show Users', on_click=show_users).props('color=blue')
    ui.button('Reset Counter', on_click=reset_counter).props('color=red')

def login():
    if username_input.value == ADMIN_USERNAME and password_input.value == ADMIN_PASSWORD:
        ui.notify('✅ Logged in as admin!')
        admin_actions_container.style('display: flex')
    else:
        ui.notify('❌ Invalid username or password')

ui.button('Login', on_click=login).props('color=green')

# ---------------------- AI CHATBOT ----------------------
ui.label('🤖 Ask AI').classes('text-h5')
ai_question_input = ui.textarea('Type your question here')
ai_response_label = ui.label('')  # response will appear here

def ask_ai():
    question = ai_question_input.value.strip()
    if not question:
        ui.notify('Please ask a question!')
        return
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}],
            temperature=0.7
        )
        answer = response.choices[0].message.content
        ai_response_label.set_text(answer)
    except Exception as e:
        ai_response_label.set_text(f"Error: {e}")

ui.button('Ask AI', on_click=ask_ai).props('color=purple')

# ---------------------- FOOTER ----------------------
with ui.footer().classes('bg-gray-200'):
    ui.label('Made with NiceGUI by Aidan Hallett • Free Hosting • No Watermark')

# ---------------------- WATERMARK ----------------------
ui.label('Aidan Hallett™').classes('absolute bottom-2 right-2 text-gray-400 opacity-50 text-xs')

# ---------------------- RUN ----------------------
port = int(os.environ.get("PORT", 8080))
ui.run(host='0.0.0.0', port=port)