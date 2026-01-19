import os
from nicegui import ui
import openai

# -------------------- CONFIG --------------------
ui.page_title('My Public App!')

# Get OpenAI key from environment variables
OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
openai.api_key = OPENAI_KEY

# -------------------- HEADER --------------------
with ui.header().classes('bg-blue-600 text-white'):
    ui.label('My Website').classes('text-h5')
    ui.label('Free No Watermark').classes('text-subtitle2')

# -------------------- TABS --------------------
with ui.tabs().classes('w-full') as tabs:
    home_tab = ui.tab('Home')
    tools_tab = ui.tab('Tools')
    about_tab = ui.tab('About')
    contact_tab = ui.tab('Contact')
    admin_tab = ui.tab('Admin')

with ui.tab_panels(tabs, value=home_tab).classes('w-full'):

    # -------------------- HOME --------------------
    with ui.tab_panel(home_tab):
        ui.label('🏠 Home').classes('text-h4')
        ui.label('Welcome to my NiceGUI app made by Aidan Hallett! Click the buttons below:')

        def hello():
            ui.notify('Hello! Thanks for visiting my app 😄')

        def surprise():
            ui.notify('🎉 Surprise! You found the secret button!')

        ui.button('Say Hello', on_click=hello)
        ui.button('Surprise Me', on_click=surprise).props('color=purple')

    # -------------------- TOOLS --------------------
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

    # -------------------- ABOUT --------------------
    with ui.tab_panel(about_tab):
        ui.label('ℹ️ About').classes('text-h4')
        ui.markdown("""
This website is built using **NiceGUI** and Python.

Features:
- Multiple sections
- Buttons
- Inputs
- Admin panel
- AI Chatbot
- Fully free hosting
- No watermark
        """)

    # -------------------- CONTACT --------------------
    with ui.tab_panel(contact_tab):
        ui.label('📬 Contact').classes('text-h4')

        name = ui.input('Your name')
        message = ui.textarea('Your message')

        def send():
            ui.notify(f'Thanks {name.value}! Message sent to aidanhallett@gmail.com.')
            name.value = ''
            message.value = ''

        ui.button('Send Message', on_click=send).props('color=green')

    # -------------------- ADMIN --------------------
    with ui.tab_panel(admin_tab):
        ui.label('🔒 Admin Login').classes('text-h4')

        username = ui.input('Username')
        password = ui.input('Password', password=True)
        admin_login_panel = ui.column()
        ui.button('Login', on_click=lambda: admin_login())

        # Hidden admin options panel
        admin_options_panel = ui.column().style('display: none')

        def admin_login():
            if username.value == 'aidan' and password.value == 'TTellahnadia':
                ui.notify('✅ Logged in as admin!')
                admin_login_panel.style('display: none')
                admin_options_panel.style('display: flex')
                show_admin_options()
            else:
                ui.notify('❌ Wrong credentials!')

        def show_admin_options():
            ui.label('Welcome Admin!').parent(admin_options_panel)
            ui.button('View Users', on_click=lambda: ui.notify('No users yet')).parent(admin_options_panel)
            ui.button('Shutdown Server', on_click=lambda: ui.notify('Server would shutdown')).parent(admin_options_panel)

# -------------------- AI CHATBOT --------------------
with ui.card().classes('m-4 p-4'):
    ui.label('🤖 Ask AI').classes('text-h5')
    question_input = ui.input('Ask a question...')
    ai_answer = ui.markdown('AI answer will appear here.')

    def ask_ai():
        if not OPENAI_KEY:
            ai_answer.set_text("❌ OpenAI API key not set!")
            return

        async def run():
            try:
                response = await openai.ChatCompletion.acreate(
                    model='gpt-3.5-turbo',
                    messages=[{"role": "user", "content": question_input.value}],
                    temperature=0.7
                )
                ai_answer.set_text(response['choices'][0]['message']['content'])
            except Exception as e:
                ai_answer.set_text(f"❌ Error: {str(e)}")

        ui.run_async(run)

    ui.button('Ask AI', on_click=ask_ai).props('color=blue')

# -------------------- FOOTER --------------------
with ui.footer().classes('bg-gray-200'):
    ui.label('Made with NiceGUI • Free Hosting • No Watermark • By Aidan Hallett')

# -------------------- WATERMARK --------------------
ui.label('Aidan Hallett™').classes('absolute bottom-2 right-2 text-gray-400 opacity-50 text-xs')

# -------------------- RUN --------------------
port = int(os.environ.get("PORT", 8080))
ui.run(host='0.0.0.0', port=port)