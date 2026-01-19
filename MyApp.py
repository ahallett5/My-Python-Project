import os
from nicegui import ui
import openai

# ---------- CONFIG ----------
OPENAI_API_KEY = "sk-your-openai-key-here"  # Replace with your actual key
openai.api_key = OPENAI_API_KEY

# Admin credentials
ADMIN_USERNAME = "aidan"
ADMIN_PASSWORD = "TTellahnadia"

# ---------- GLOBAL STATE ----------
logged_in = {"status": False}

# ---------- HEADER ----------
ui.page_title('My Public App!')
with ui.header().classes('bg-blue-600 text-white'):
    ui.label('My Website').classes('text-h5')
    ui.label('Free No Watermark').classes('text-subtitle2')

# ---------- LOGIN ----------
with ui.dialog() as login_dialog, ui.card().classes('p-6'):
    ui.label("Admin Login").classes("text-h5")
    username_input = ui.input("Username")
    password_input = ui.input("Password").props("type=password")

    def do_login():
        if username_input.value == ADMIN_USERNAME and password_input.value == ADMIN_PASSWORD:
            logged_in["status"] = True
            ui.notify("Logged in as admin ✅")
            login_dialog.close()
            admin_actions.set_visibility(True)
        else:
            ui.notify("Invalid credentials ❌")

    ui.button("Login", on_click=do_login).props("color=blue")

# ---------- TABS ----------
tabs = ui.tabs().classes("w-full")
home_tab = ui.tab("Home", parent=tabs)
tools_tab = ui.tab("Tools", parent=tabs)
about_tab = ui.tab("About", parent=tabs)
contact_tab = ui.tab("Contact", parent=tabs)
admin_tab = ui.tab("Admin", parent=tabs)

# ---------- HOME ----------
with ui.tab_panels(tabs, value=home_tab):
    with ui.tab_panel(home_tab):
        ui.label("🏠 Home").classes("text-h4")
        ui.label("Welcome to my NiceGUI app made by **Aidan Hallett**! Click the buttons below:")

        def hello():
            ui.notify("Hello! Thanks for visiting my app 😄")

        def surprise():
            ui.notify("🎉 Surprise! You found the secret button!")

        ui.button("Say Hello", on_click=hello)
        ui.button("Surprise Me", on_click=surprise).props("color=purple")

# ---------- TOOLS ----------
    with ui.tab_panel(tools_tab):
        ui.label("🛠 Tools").classes("text-h4")
        user_input = ui.input("Type something")

        def show_text():
            ui.notify(f"You typed: {user_input.value}")

        ui.button("Show my text", on_click=show_text)

        # Counter tool
        count = {"value": 0}
        counter_label = ui.label("Counter: 0")

        def increase():
            count["value"] += 1
            counter_label.set_text(f"Counter: {count['value']}")

        ui.button("Increase Counter", on_click=increase)

# ---------- ABOUT ----------
    with ui.tab_panel(about_tab):
        ui.label("ℹ️ About").classes("text-h4")
        ui.markdown("""
This website is built using **NiceGUI** and Python.

**Features:**
- Multiple sections
- Buttons
- Inputs
- Fully free hosting
- No watermark
- Shareable public URL
- AI Chatbot
- Admin section
        """)

# ---------- CONTACT ----------
    with ui.tab_panel(contact_tab):
        ui.label("📬 Contact").classes("text-h4")
        name_input = ui.input("Your name")
        message_input = ui.textarea("Your message")

        def send():
            ui.notify(f"Thanks {name_input.value}! Message sent.")
            name_input.value = ""
            message_input.value = ""

        ui.button("Send Message", on_click=send).props("color=green")

# ---------- ADMIN ----------
    with ui.tab_panel(admin_tab):
        ui.label("🔒 Admin").classes("text-h4")
        ui.label("Login to see admin actions")

        admin_actions = ui.column()  # Hidden until login
        admin_actions.set_visibility(False)

        def do_admin_action(action):
            ui.notify(f"Admin action executed: {action}")

        with admin_actions:
            ui.label("Admin Actions:").classes("text-h6")
            ui.button("View Users", on_click=lambda: ui.notify("No users yet"))
            ui.button("Send Test Email", on_click=lambda: ui.notify("Pretend email sent to aidanhallett@gmail.com"))
            ui.button("Restart App", on_click=lambda: ui.notify("App would restart now (demo)"))

# ---------- AI CHATBOT ----------
with ui.card().classes("p-6 m-4"):
    ui.label("🤖 Ask AI").classes("text-h5")
    question_input = ui.input("Type your question")
    ai_response_label = ui.label("")

    def ask_ai():
        if not question_input.value.strip():
            ui.notify("Please type a question first ❌")
            return
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role":"user","content":question_input.value}]
            )
            answer = response.choices[0].message.content
            ai_response_label.set_text(answer)
        except Exception as e:
            ai_response_label.set_text(f"Error: {e}")

    ui.button("Ask AI", on_click=ask_ai)

# ---------- FOOTER ----------
with ui.footer().classes("bg-gray-200"):
    ui.label("Made with NiceGUI • Free Hosting • No Watermark • Created by Aidan Hallett")

# ---------- WATERMARK ----------
ui.label("Aidan Hallett™").classes("absolute bottom-2 right-2 text-gray-400 opacity-50 text-xs")

# ---------- RUN ----------
port = int(os.environ.get("PORT", 8080))
ui.run(host="0.0.0.0", port=port)
