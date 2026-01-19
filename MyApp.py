import os
from nicegui import ui
import openai

# ------------------- CONFIG -------------------
ui.page_title('My Public App!')

# Load OpenAI key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Admin credentials
ADMIN_USERNAME = "aidan"
ADMIN_PASSWORD = "TTellahnadia"

# ------------------- HEADER -------------------
with ui.header().classes('bg-blue-600 text-white'):
    ui.label('My Website').classes('text-h5')
    ui.label('Free No Watermark').classes('text-subtitle2')

# ------------------- TABS -------------------
tabs = ui.tabs().classes('w-full')

home_tab = ui.tab('Home', parent=tabs)
tools_tab = ui.tab('Tools', parent=tabs)
about_tab = ui.tab('About', parent=tabs)
contact_tab = ui.tab('Contact', parent=tabs)
ai_tab = ui.tab('AI Chat', parent=tabs)
admin_tab = ui.tab('Admin', parent=tabs)

tab_panels = ui.tab_panels(tabs, value=home_tab).classes('w-full')

# ------------------- HOME -------------------
with ui.tab_panel(home_tab):
    ui.label('🏠 Home').classes('text-h4')
    ui.label('Welcome to my NiceGUI app made by Aidan Hallett! Click the buttons below:')

    def hello():
        ui.notify('Hello! Thanks for visiting my app 😄')

    def surprise():
        ui.notify('🎉 Surprise! You found the secret button!')

    ui.button('Say Hello', on_click=hello)
    ui.button('Surprise Me', on_click=surprise).props('color=purple')

# ------------------- TOOLS -------------------
with ui.tab_panel(tools_tab):
    ui.label('🛠 Tools').classes('text-h4')

    user_input = ui.input('Type something')

    def show_text():
        ui.notify(f'You typed: {user_input.value}')

    ui.button('Show my text', on_click=show_text)

    count = {'value': 0}

    def increase():
        count['value'] += 1
        counter_label.set_text(f'Counter: {count["value"]}')

    counter_label = ui.label('Counter: 0')
    ui.button('Increase Counter', on_click=increase)

# ------------------- ABOUT -------------------
with ui.tab_panel(about_tab):
    ui.label('ℹ️ About').classes('text-h4')
    ui.markdown("""
This website is built using **NiceGUI** and Python.

Features:

- Multiple sections
- Buttons
- Inputs
- Fully free hosting
- No watermark
- Shareable public URL
Made by Aidan Hallett
""")

# ------------------- CONTACT -------------------
with ui.tab_panel(contact_tab):
    ui.label('📬 Contact').classes('text-h4')

    name_input = ui.input('Your name')
    message_input = ui.textarea('Your message')

    def send_message():
        ui.notify(f'Thanks {name_input.value}! Message sent to aidanhallett@gmail.com')
        name_input.value = ''
        message_input.value = ''

    ui.button('Send Message', on_click=send_message).props('color=green')

# ------------------- AI CHAT -------------------
with ui.tab_panel(ai_tab):
    ui.label('🤖 Ask the AI a question!').classes('text-h4')

    question_input = ui.input('Your question here')
    ai_response_label = ui.label('')

    def ask_ai():
        q = question_input.value.strip()
        if not q:
            ui.notify("Please type a question first!")
            return
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": q}
                ]
            )
            answer = response.choices[0].message.content
            ai_response_label.set_text(answer)
        except Exception as e:
            ai_response_label.set_text(f"Error: {str(e)}")

    ui.button("Ask AI", on_click=ask_ai).props('color=blue')

# ------------------- ADMIN -------------------
with ui.tab_panel(admin_tab):
    ui.label('🔒 Admin Login').classes('text-h4')

    username_input = ui.input('Username')
    password_input = ui.input('Password', password=True)
    login_status = ui.label('')

    admin_actions_container = ui.column()
    admin_actions_container.hide()  # Initially hidden

    def login_admin():
        if username_input.value == ADMIN_USERNAME and password_input.value == ADMIN_PASSWORD:
            ui.notify("Admin login successful!")
            login_status.set_text("Logged in as Admin")
            admin_actions_container.show()
        else:
            ui.notify("Incorrect username or password!")
            login_status.set_text("Login failed")
            admin_actions_container.hide()

    ui.button("Login", on_click=login_admin).props('color=red')

    # Admin-only actions
    with admin_actions_container:
        ui.label("⚙️ Admin Actions")
        def reset_counter():
            count['value'] = 0
            counter_label.set_text('Counter: 0')
            ui.notify("Counter reset!")

        ui.button("Reset Counter", on_click=reset_counter)

        def show_admin_message():
            ui.notify("Hello Admin! This is your special privilege.")

        ui.button("Admin Message", on_click=show_admin_message).props('color=purple')

# ------------------- FOOTER -------------------
with ui.footer().classes('bg-gray-200'):
    ui.label('Made with NiceGUI • Free Hosting • No Watermark • By Aidan Hallett')

# ------------------- WATERMARK -------------------
ui.label('Aidan Hallett™').classes('absolute bottom-2 right-2 text-gray-400 opacity-50 text-xs')

# ------------------- RUN -------------------
port = int(os.environ.get("PORT", 8080))
ui.run(host='0.0.0.0', port=port)