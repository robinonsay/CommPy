import dearpygui.dearpygui as dpg


def main():
    dpg.create_context()
    with dpg.window(tag="Primary Window"):
        dpg.add_text("Hello, world")

    dpg.create_viewport(title='Custom Title', width=1080, height=720)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()
