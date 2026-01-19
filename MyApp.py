import os
from nicegui import ui
import openai

# Use environment variable for OpenAI key
openai.api_key = os.environ.get("OPENAI_API_KEY")

ui.page_title('My Public App! - by Aidan Hallett')

# ---------------- HEADER ----------------
with ui.header().classes('bg-blue-600 text-white'):
    ui.label('My Website').classes('text-h5')
    ui.label('Free No Watermark').classes('text-subtitle2')

# ---------------- TABS ----------------
with ui.tabs().classes('w-full') as tabs:
    home_tab = ui.tab('Home')
    tools_tab = ui.tab('Tools')
    about_tab = ui.tab('About')
    contact_tab = ui.tab('Contact')
    admin_tab = ui.tab('Admin')  # Admin tab

with ui.tab_panels(tabs, value=home_tab).classes('w-full'):

    # ----- HOME -----
    with ui.tab_panel(home_tab):
        ui.label('🏠 Home').classes('text-h4')
        ui.label('Welcome to my NiceGUI app made by Aidan Hallett!')

    # ----- TOOLS -----
    with ui.tab_panel(tools_tab):
        ui.label('🛠 Tools').classes('text-h4')
        user_input = ui.input('Type something')
        def show_text():
            ui.notify(f'You typed: {user_input.value}')
        ui.button('Show my text', on_click=show_text)

    # ----- ABOUT -----
    with ui.tab_panel(about_tab):
        ui.label('ℹ️ About').classes('text-h4')
        ui.markdown("""
This website is built using **NiceGUI** and Python.

Features:
- Multiple sections
- Admin panel
- AI chatbot
- Fully free hosting
- No watermark
        """)

    # ----- CONTACT -----
    messages = []
    with ui.tab_panel(contact_tab):
        ui.label('📬 Contact').classes('text-h4')
        name = ui.input('Your name')
        message = ui.textarea('Your message')

        def send():
            messages.append({'name': name.value, 'message': message.value})
            ui.notify(f'Thanks {name.value}! Message sent.')
            name.value = ''
            message.value = ''

        ui.button('Send Message', on_click=send).props('color=green')

    # ----- ADMIN -----
    admin_logged_in = {'status': False}

    with ui.tab_panel(admin_tab):
        ui.label('🔒 Admin Panel').classes('text-h4')
        
        # Login section
        username = ui.input('Username')
        password = ui.input('Password', password=True)

        login_button = ui.button('Login', on_click=lambda: None)
        
        admin_options_panel = ui.column().style('display: none')  # hidden by default

        def login():
            if username.value == 'aidan' and password.value == 'TTellahnadia':
                ui.notify('✅ Admin logged in!')
                admin_logged_in['status'] = True
                username.value = ''
                password.value = ''
                admin_options_panel.style('display: flex')
            else:
                ui.notify('❌ Wrong credentials!')

        login_button.on('click', login)

        # ---------------- Admin Privileges ----------------
        with admin_options_panel:
            ui.label('🎯 Admin Options').classes('text-h5')

            # View messages
            def show_messages():
                if messages:
                    msg_text = '\n'.join(f"{m['name']}: {m['message']}" for m in messages)
                    ui.dialog().add(ui.label(msg_text)).open()
                else:
                    ui.notify('No messages yet.')

            ui.button('View Messages', on_click=show_messages)

            # Clear messages
            def clear_messages():
                messages.clear()
                ui.notify('All messages cleared!')

            ui.button('Clear Messages', on_click=clear_messages, color='red')

            # Send announcement
            announcement_input = ui.input('Announcement')
            def send_announcement():
                if announcement_input.value:
                    ui.notify(f"Admin Announcement: {announcement_input.value}")
                    announcement_input.value = ''
            ui.button('Send Announcement', on_click=send_announcement, color='orange')

            # AI Chatbot testing
            question_input = ui.input('Ask AI')
            ai_response = ui.label('')

            def ask_ai():
                if question_input.value:
                    try:
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": question_input.value}]
                        )
                        ai_response.set_text(response.choices[0].message.content)
                    except Exception as e:
                        ai_response.set_text(f"Error: {e}")
                    question_input.value = ''

            ui.button('Ask AI', on_click=ask_ai)
            ui.add(ai_response)

# ---------------- FOOTER ----------------
with ui.footer().classes('bg-gray-200'):
    ui.label('Made with NiceGUI • Free Hosting • No Watermark • by Aidan Hallett')

# Cloud hosting
import os
port = int(os.environ.get("PORT", 8080))
ui.run(host='0.0.0.0', port=port)