import os
import openai
from nicegui import ui

# ---------------- CONFIG ----------------
ui.page_title("My Public App!")
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")  # Set this in Render
openai.api_key = OPENAI_KEY

ADMIN_USERNAME = "aidan"
ADMIN_PASSWORD = "TTellahnadia"

users = {}  # For demonstration of user accounts

# ---------------- HEADER ----------------
with ui.header().classes("bg-blue-600 text-white"):
    ui.label("My Website").classes("text-h5")
    ui.label("Free No Watermark").classes("text-subtitle2")

# ---------------- TABS ----------------
with ui.tabs() as tabs:
    home_tab = ui.tab("Home")
    tools_tab = ui.tab("Tools")
    about_tab = ui.tab("About")
    contact_tab = ui.tab("Contact")
    admin_tab = ui.tab("Admin")

# ---------------- TAB PANELS ----------------
with ui.tab_panels(tabs, value=home_tab):

    # --- HOME ---
    with ui.tab_panel(home_tab):
        ui.label("🏠 Home").classes("text-h4")
        ui.label("Welcome to my NiceGUI app made by Aidan Hallett! 😄")

        def hello():
            ui.notify("Hello! Thanks for visiting my app 😄")

        def surprise():
            ui.notify("🎉 Surprise! You found the secret button!")

        ui.button("Say Hello", on_click=hello)
        ui.button("Surprise Me", on_click=surprise).props("color=purple")

    # --- TOOLS ---
    with ui.tab_panel(tools_tab):
        ui.label("🛠 Tools").classes("text-h4")

        user_input = ui.input("Type something")

        def show_text():
            ui.notify(f"You typed: {user_input.value}")

        ui.button("Show my text", on_click=show_text)

        count = {"value": 0}

        def increase():
            count["value"] += 1
            counter_label.set_text(f"Counter: {count['value']}")

        counter_label = ui.label("Counter: 0")
        ui.button("Increase Counter", on_click=increase)

    # --- ABOUT ---
    with ui.tab_panel(about_tab):
        ui.label("ℹ️ About").classes("text-h4")
        ui.markdown(
            """
This website is built using **NiceGUI** and Python.

Features:
- Multiple sections
- Buttons
- Inputs
- Fully free hosting
- No watermark
- Shareable public URL
"""
        )

    # --- CONTACT ---
    with ui.tab_panel(contact_tab):
        ui.label("📬 Contact").classes("text-h4")
        name = ui.input("Your name")
        message = ui.textarea("Your message")

        def send():
            ui.notify(f"Thanks {name.value}! Message sent to aidanhallett@gmail.com")
            name.value = ""
            message.value = ""

        ui.button("Send Message", on_click=send).props("color=green")

    # --- ADMIN ---
    with ui.tab_panel(admin_tab):
        ui.label("🔑 Admin Login").classes("text-h4")
        admin_user = ui.input("Username")
        admin_pass = ui.input("Password").props("password=True")
        admin_status = ui.label("")

        # Admin actions container (hidden until login)
        admin_actions = ui.column()
        admin_actions.set_visibility(False)

        # AI Chat
        ui.label("🤖 AI Chatbot").classes("text-h5")
        question_input = ui.input("Ask the AI a question")
        ai_response_label = ui.label("")

        def ask_ai():
            prompt = question_input.value
            if not prompt:
                ui.notify("Please type a question")
                return
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )
                answer = response.choices[0].message.content
                ai_response_label.set_text(answer)
            except Exception as e:
                ai_response_label.set_text(f"Error: {e}")

        ui.button("Ask AI", on_click=ask_ai).props("color=indigo")

        # Admin privileges
        def login():
            if admin_user.value == ADMIN_USERNAME and admin_pass.value == ADMIN_PASSWORD:
                ui.notify("Admin logged in!")
                admin_status.set_text("✅ Logged in as Admin")
                admin_actions.set_visibility(True)
            else:
                ui.notify("Invalid credentials")
                admin_status.set_text("❌ Login failed")
                admin_actions.set_visibility(False)

        ui.button("Login", on_click=login).props("color=red")

        # Example admin actions
        with admin_actions:
            ui.label("🛡 Admin Privileges").classes("text-h5")
            def show_users():
                ui.notify(f"Users: {', '.join(users.keys()) or 'No users yet'}")

            ui.button("Show Users", on_click=show_users)
            def clear_users():
                users.clear()
                ui.notify("All users cleared!")

            ui.button("Clear Users", on_click=clear_users).props("color=orange")

# ---------------- FOOTER ----------------
with ui.footer().classes("bg-gray-200"):
    ui.label("Made with NiceGUI • Free Hosting • No Watermark • By Aidan Hallett™")

# ---------------- WATERMARK ----------------
ui.label("Aidan Hallett™").classes("absolute bottom-2 right-2 text-gray-400 opacity-50 text-xs")

# ---------------- RUN ----------------
port = int(os.environ.get("PORT", 8080))
ui.run(host="0.0.0.0", port=port)