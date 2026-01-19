import os
from nicegui import ui
import openai

# ------------------ CONFIG ------------------
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Admin credentials
ADMIN_USERNAME = "aidan"
ADMIN_PASSWORD = "TTellahnadia"

# In-memory users (demo)
users = {}

# ------------------ HEADER ------------------
ui.page_title("My Public App!")

with ui.header().classes('bg-blue-600 text-white'):
    ui.label("My Website").classes('text-h5')
    ui.label("Free No Watermark").classes('text-subtitle2')

# ------------------ TABS ------------------
with ui.tabs().classes('w-full') as tabs:
    home_tab = ui.tab('Home')
    tools_tab = ui.tab('Tools')
    about_tab = ui.tab('About')
    contact_tab = ui.tab('Contact')
    admin_tab = ui.tab('Admin')

with ui.tab_panels(tabs, value=home_tab).classes('w-full'):

    # ---------- HOME ----------
    with ui.tab_panel(home_tab):
        ui.label("🏠 Home").classes('text-h4')
        ui.label("Welcome to my NiceGUI app made by **Aidan Hallett**! Click the buttons below:")

        def say_hello():
            ui.notify("Hello! Thanks for visiting my app 😄")

        def surprise():
            ui.notify("🎉 Surprise! You found the secret button!")

        ui.button("Say Hello", on_click=say_hello)
        ui.button("Surprise Me", on_click=surprise).props("color=purple")

    # ---------- TOOLS ----------
    with ui.tab_panel(tools_tab):
        ui.label("🛠 Tools").classes('text-h4')
        user_input = ui.input("Type something")

        def show_text():
            ui.notify(f"You typed: {user_input.value}")

        ui.button("Show my text", on_click=show_text)

        # Counter example
        count = {"value": 0}
        counter_label = ui.label("Counter: 0")

        def increase():
            count['value'] += 1
            counter_label.set_text(f"Counter: {count['value']}")

        ui.button("Increase Counter", on_click=increase)

        # AI Chatbot
        ui.label("🤖 Ask AI")
        ai_input = ui.input("Type your question here")
        ai_response_container = ui.column()

        def ask_ai():
            question = ai_input.value.strip()
            if question:
                ai_input.value = ""
                # Call OpenAI API
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": question}]
                    )
                    answer = response.choices[0].message.content
                except Exception as e:
                    answer = f"Error: {e}"

                ui.label(f"🤖 {answer}", parent=ai_response_container)

        ui.button("Ask AI", on_click=ask_ai).props("color=green")

    # ---------- ABOUT ----------
    with ui.tab_panel(about_tab):
        ui.label("ℹ️ About").classes('text-h4')
        ui.markdown("""
This website is built using **NiceGUI** and Python.

Features:
- Multiple sections
- Buttons
- Inputs
- Fully free hosting
- No watermark
- Shareable public URL
""")

    # ---------- CONTACT ----------
    with ui.tab_panel(contact_tab):
        ui.label("📬 Contact").classes('text-h4')
        name = ui.input("Your name")
        message = ui.textarea("Your message")

        def send():
            ui.notify(f"Thanks {name.value}! Message sent.")
            name.value = ""
            message.value = ""

        ui.button("Send Message", on_click=send).props("color=green")

    # ---------- ADMIN ----------
    with ui.tab_panel(admin_tab):
        ui.label("🔑 Admin Login").classes('text-h4')
        username_input = ui.input("Username")
        password_input = ui.input("Password").props("type=password")
        admin_actions_container = ui.column(visible=False)

        def login():
            if username_input.value == ADMIN_USERNAME and password_input.value == ADMIN_PASSWORD:
                ui.notify("Admin login successful!")
                admin_actions_container.visible = True
            else:
                ui.notify("Invalid credentials!", color="red")

        ui.button("Login", on_click=login).props("color=blue")

        # Admin actions (only visible after login)
        with admin_actions_container:
            ui.label("Admin Actions:").classes("text-h5")

            def view_users():
                ui.notify(f"Registered users: {', '.join(users.keys()) or 'No users yet'}")

            def send_announcement():
                ui.notify("Announcement sent to all users!")  # Replace with email logic if needed

            ui.button("View Users", on_click=view_users).props("color=orange")
            ui.button("Send Announcement", on_click=send_announcement).props("color=purple")

# ------------------ FOOTER ------------------
with ui.footer().classes("bg-gray-200"):
    ui.label("Made with NiceGUI • Free Hosting • No Watermark • By Aidan Hallett")

# ------------------ WATERMARK ------------------
ui.label("Aidan Hallett™").classes("absolute bottom-2 right-2 text-gray-400 opacity-50 text-xs")

# ------------------ RUN ------------------
port = int(os.environ.get("PORT", 8080))
ui.run(host="0.0.0.0", port=port)