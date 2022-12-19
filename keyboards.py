from aiogram.types import InlineKeyboardMarkup

from commands import *

# button_menu = InlineKeyboardButton(text=message_menu, callback_data=command_menu)
# button_search = InlineKeyboardButton(text=button_name_search, callback_data=command_search)
# button_tracked_list = InlineKeyboardButton(text=button_name_tracked_list, callback_data=command_show_tracked_items)
# button_saved_list = InlineKeyboardButton(text=button_name_saved_list, callback_data=command_show_saved_items)
# button_search_more = InlineKeyboardButton(text=button_name_search_more, callback_data=command_search_more)
#
#
# def get_button_track_item(movie_id):
#     return InlineKeyboardButton(text=button_name_track, callback_data=command_track_item + ' ' + str(movie_id))
#
#
# def get_button_save_item(movie_id):
#     return InlineKeyboardButton(text=button_name_save, callback_data=command_save_item + ' ' + str(movie_id))
#
#
keyboard_command_start = InlineKeyboardMarkup(row_width=2)
# keyboard_command_start.add(button_search)
# keyboard_command_start.add(button_tracked_list, button_saved_list)
#
#
# def keyboard_command_find(movie_id):
#     keyboard = InlineKeyboardMarkup(row_width=2)
#     keyboard.add(get_button_track_item(movie_id), get_button_save_item(movie_id))
#     keyboard.add(button_menu, button_search_more)
#     return keyboard
#
#
# keyboard_command_find_failed = InlineKeyboardMarkup()
# keyboard_command_find_failed.add(button_search_more)
# keyboard_command_find_failed.add(button_menu)
#
# keyboard_command_track_item = InlineKeyboardMarkup(row_width=2)
# keyboard_command_track_item.add(button_menu, button_search_more)
#
# keyboard_menu = InlineKeyboardMarkup()
# keyboard_menu.add(button_search)
# keyboard_menu.add(button_tracked_list, button_saved_list)

keyboards = {
    command_start: keyboard_command_start,
    # command_find: [keyboard_command_find, keyboard_command_find_failed],
    # command_track_item: keyboard_command_track_item,
    # command_menu: keyboard_menu,
    # command_show_saved_items: InlineKeyboardMarkup().add(button_menu),
    # command_show_tracked_items: InlineKeyboardMarkup().add(button_menu)
}
