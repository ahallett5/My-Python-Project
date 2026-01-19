import os
import openai
from nicegui import ui

# ---------- CONFIG ----------
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_KEY

# ---------- USERS ----------
users = {"aidan": "TTellahnadia"}  # default admin account
logged_in_user = {"name": None}

# ---------- HEADER ----------
ui.page_title("My Public App!")
with ui.header().classes('bg-blue-600 text-white'):
    ui.label("My Website").classes('text-h5')
    ui.label("Free No Watermark").classes('text-subtitle2')

# ---------- TABS ----------
with ui.tabs().classes('w-full') as tabs:
    home_tab = ui.tab("Home")
    tools_tab = ui.tab("Tools")
    ai_tab = ui.tab("Ask AI")
    admin_tab = ui.tab("Admin")
    about_tab = ui.tab("About")
    contact_tab = ui.tab("Contact")

with ui.tab_panels(tabs, value=home_tab).classes('w-full'):

    # ----- HOME -----
    with ui.tab_panel(home_tab):
        ui.label("🏠 Home").classes('text-h4')
        ui.label("Welcome to my NiceGUI app made by Aidan Hallett! Click the buttons below:")

        def hello():
            ui.notify("Hello! Thanks for visiting my app 😄")

        def surprise():
            ui.notify("🎉 Surprise! You found the secret button!")

        ui.button("Say Hello", on_click=hello)
        ui.button("Surprise Me", on_click=surprise).props('color=purple')

    # ----- TOOLS -----
    with ui.tab_panel(tools_tab):
        ui.label("🛠 Tools").classes('text-h4')
        user_input = ui.input("Type something")

        def show_text():
            ui.notify(f"You typed: {user_input.value}")

        ui.button("Show my text", on_click=show_text)

        count = {"value": 0}
        counter_label = ui.label("Counter: 0")

        def increase():
            count["value"] += 1
            counter_label.set_text(f"Counter: {count['value']}")

        ui.button("Increase Counter", on_click=increase)

    # ----- AI CHATBOT -----
    with ui.tab_panel(ai_tab):
        ui.label("🤖 Ask AI").classes('text-h4')
        question_input = ui.input("Ask me anything:")
        ai_answer = ui.markdown("")

        def ask_ai():
            if not OPENAI_KEY:
                ai_answer.set_text("❌ OpenAI API key not set!")
                return

            async def run():
                try:
                    response = await openai.ChatCompletion.acreate(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": question_input.value}],
                        temperature=0.7
                    )
                    ai_answer.set_text(response['choices'][0]['message']['content'])
                except Exception as e:
                    ai_answer.set_text(f"❌ Error: {str(e)}")

            ui.run_async(run())

        ui.button("Ask AI", on_click=ask_ai, color="green")

    # ----- ADMIN -----
    with ui.tab_panel(admin_tab):
        ui.label("🔑 Admin Login").classes('text-h4')
        admin_username = ui.input("Username")
        admin_password = ui.input("Password", password=True)
        login_status = ui.label("")

        admin_options_panel = ui.column(visible=False)

        def login():
            if users.get(admin_username.value) == admin_password.value:
                logged_in_user["name"] = admin_username.value
                login_status.set_text(f"✅ Logged in as {admin_username.value}")
                admin_options_panel.visible = True
                update_user_list()
            else:
                login_status.set_text("❌ Invalid credentials")

        ui.button("Login", on_click=login, color="blue")

        with admin_options_panel:
            ui.label("Admin Options").classes("text-h5")
            # Dynamic user list
            user_list_label = ui.markdown("No users yet")

            def update_user_list():
                user_list_label.set_text(
                    "\n".join(f"- {u}" for u in users.keys()) or "No users yet"
                )

            # Add new user
            new_user_input = ui.input("New username")
            new_pass_input = ui.input("New password", password=True)
            add_status = ui.label("")

            def add_user():
                if new_user_input.value in users:
                    add_status.set_text("❌ User already exists")
                else:
                    users[new_user_input.value] = new_pass_input.value
                    add_status.set_text("✅ User added")
                    update_user_list()

            ui.button("Add User", on_click=add_user, color="green")

            # Remove user
            remove_user_input = ui.input("Remove username")
            remove_status = ui.label("")

            def remove_user():
                if remove_user_input.value in users:
                    if remove_user_input.value == "aidan":
                        remove_status.set_text("❌ Cannot remove admin")
                        return
                    users.pop(remove_user_input.value)
                    remove_status.set_text("✅ User removed")
                    update_user_list()
                else:
                    remove_status.set_text("❌ User not found")

            ui.button("Remove User", on_click=remove_user, color="red")

    # ----- ABOUT -----
    with ui.tab_panel(about_tab):
        ui.label("ℹ️ About").classes("text-h4")
        ui.markdown(
            """
This website is built using **NiceGUI** and Python.
Made by **Aidan Hallett**.

Features:
- Multiple sections
- AI Chatbot
- Admin panel
- Buttons, inputs, and counters
- Fully free hosting
- No watermark
- Shareable public URL
"""
        )

    # ----- CONTACT -----
    with ui.tab_panel(contact_tab):
        ui.label("📬 Contact").classes("text-h4")
        name_input = ui.input("Your name")
        message_input = ui.textarea("Your message")

        def send_message():
            # Optional: replace with real email sending via SMTP
            ui.notify(f"Thanks {name_input.value}! Message sent to aidanhallett@gmail.com")
            name_input.value = ""
            message_input.value = ""

        ui.button("Send Message", on_click=send_message, color="green")

# ---------- FOOTER ----------
with ui.footer().classes("bg-gray-200"):
    ui.label("Made with NiceGUI • Free Hosting • No Watermark • By Aidan Hallett")

ui.label("Aidan Hallett™").classes("absolute bottom-2 right-2 text-gray-400 opacity-50 text-xs")

# ---------- RUN ----------
port = int(os.environ.get("PORT", 8080))
ui.run(host="0.0.0.0", port=port)