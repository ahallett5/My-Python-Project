import os
from nicegui import ui
from openai import OpenAI

# ---------- AI ----------
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def ask_ai(prompt: str) -> str:
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': 'You are a helpful web design assistant.'},
            {'role': 'user', 'content': prompt}
        ],
        max_tokens=300
    )
    return response.choices[0].message.content

# ---------- AUTH ----------
ADMIN_USER = 'aidan'
ADMIN_PASS = 'TTellahnadia'

users = {}  # simple in-memory user store
current_user = {'name': None}
admin_logged_in = {'value': False}

# ---------- UI ----------
ui.page_title('My Public App')

with ui.header().classes('bg-blue-600 text-white'):
    ui.label('My Website').classes('text-h5')
    ui.label('AI • Accounts • Tools').classes('text-subtitle2')

with ui.tabs().classes('w-full') as tabs:
    home = ui.tab('Home')
    tools = ui.tab('Tools')
    ai_tab = ui.tab('AI Designer')
    account = ui.tab('Account')
    admin = ui.tab('Admin')

with ui.tab_panels(tabs, value=home).classes('w-full'):

    # ---------- HOME ----------
    with ui.tab_panel(home):
        ui.label('🏠 Home').classes('text-h4')
        ui.label('Welcome to my AI-powered NiceGUI website!')

    # ---------- TOOLS ----------
    with ui.tab_panel(tools):
        ui.label('🛠 Tools').classes('text-h4')

        text_input = ui.input('Text to transform')
        result = ui.label()

        def uppercase():
            result.set_text(text_input.value.upper())

        def word_count():
            result.set_text(f'Word count: {len(text_input.value.split())}')

        ui.button('UPPERCASE', on_click=uppercase)
        ui.button('Word Count', on_click=word_count)

        ui.separator()

        number = ui.number('Number')
        ui.button(
            'Square',
            on_click=lambda: ui.notify(f'Result: {number.value ** 2}')
        )

    # ---------- AI CHATBOT ----------
    with ui.tab_panel(ai_tab):
        ui.label('🤖 AI Website Designer').classes('text-h4')
        ui.label('Ask for redesign ideas, features, colors, layouts, etc.')

        chat = ui.column().classes('w-full')
        prompt = ui.textarea('Ask the AI...')

        def send_prompt():
            chat.clear()
            chat.add(ui.label('🤖 Thinking...'))
            reply = ask_ai(prompt.value)
            chat.clear()
            chat.add(ui.markdown(reply))

        ui.button('Ask AI', on_click=send_prompt).props('color=purple')

    # ---------- USER ACCOUNTS ----------
    with ui.tab_panel(account):
        ui.label('👤 User Account').classes('text-h4')

        username = ui.input('Username')
        password = ui.input('Password', password=True)
        status = ui.label()

        def register():
            if username.value in users:
                status.set_text('❌ User already exists')
            else:
                users[username.value] = password.value
                status.set_text('✅ Registered successfully')

        def login():
            if users.get(username.value) == password.value:
                current_user['name'] = username.value
                status.set_text(f'✅ Logged in as {username.value}')
            else:
                status.set_text('❌ Invalid login')

        ui.button('Register', on_click=register)
        ui.button('Login', on_click=login)

    # ---------- ADMIN ----------
    with ui.tab_panel(admin):
        ui.label('🔐 Admin Login').classes('text-h4')

        a_user = ui.input('Admin Username')
        a_pass = ui.input('Admin Password', password=True)
        admin_area = ui.column().classes('hidden')

        def admin_login():
            if a_user.value == ADMIN_USER and a_pass.value == ADMIN_PASS:
                admin_logged_in['value'] = True
                admin_area.classes(remove='hidden')
                ui.notify('Admin logged in')
            else:
                ui.notify('Invalid admin credentials', color='red')

        ui.button('Login', on_click=admin_login)

        with admin_area:
            ui.separator()
            ui.label('👑 Admin Panel')
            ui.label('Registered Users:')
            ui.markdown(lambda: '\n'.join(f'- {u}' for u in users.keys()) or 'No users yet')

# ---------- FOOTER ----------
with ui.footer().classes('bg-gray-200'):
    ui.label('Built with NiceGUI • AI Powered • No Watermark')

ui.label(
    'Aidan Hallett™',
    classes='absolute bottom-2 right-2 text-gray-400 opacity-50 text-xs'
)

# ---------- RUN ----------
port = int(os.environ.get('PORT', 8080))
ui.run(host='0.0.0.0', port=port)