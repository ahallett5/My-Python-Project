import os
from nicegui import ui

ui.page_title('My Public App!')

with ui.header().classes('bg-blue-600 text=white'):
    ui.label('My Website').classes('text-h5')
    ui.label('Free No Watermark').classes('text-subtitle2')

# ---------- MAIN SECTIONS ----------

with ui.tabs().classes('w-full') as tabs:

    home = ui.tab('Home')

    tools = ui.tab('Tools')

    about = ui.tab('About')

    contact = ui.tab('Contact')



with ui.tab_panels(tabs, value=home).classes('w-full'):

    

    # ----- HOME -----

    with ui.tab_panel(home):

        ui.label('🏠 Home').classes('text-h4')

        ui.label('Welcome to my NiceGUI app made by Aian Hallett! Click the buttons below:')

        

        def hello():

            ui.notify('Hello! Thanks for visiting my app 😄')

        

        def surprise():

            ui.notify('🎉 Surprise! You found the secret button!')

        

        ui.button('Say Hello', on_click=hello)

        ui.button('Surprise Me', on_click=surprise).props('color=purple')



    # ----- TOOLS -----

    with ui.tab_panel(tools):

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



    # ----- ABOUT -----

    with ui.tab_panel(about):

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

        """)



    # ----- CONTACT -----

    with ui.tab_panel(contact):

        ui.label('📬 Contact').classes('text-h4')



        name = ui.input('Your name')

        message = ui.textarea('Your message')



        def send():

            ui.notify(f'Thanks {name.value}! Message sent.')

            name.value = ''

            message.value = ''



        ui.button('Send Message', on_click=send).props('color=green')



# ---------- FOOTER ----------

with ui.footer().classes('bg-gray-200'):

    ui.label('Made with NiceGUI • Free Hosting • No Watermark')


# ---------- WATERMARK --------
ui.label('Aidan Hallett™').classes('absolute bottom-2 right-2 text-gray-400 opacity-50 text-xs')



# Cloud hosting compatibility

port = int(os.environ.get("PORT", 8080))

ui.run(host='0.0.0.0', port=port)