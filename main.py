import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from pydub import AudioSegment

from commands import *
from keyboards import keyboards
from messages import *
from model import our_tts as model
from secret import API

# Configure logging
# This sets the root logger to write to stdout (your console).
# Your script/app needs to call this somewhere at least once.
logging.basicConfig()

# By default the root logger is set to WARNING and all loggers you define
# inherit that value. Here we set the root logger to NOTSET. This logging
# level is automatically inherited by all existing and new sub-loggers
# that do not set a less verbose level.
logging.root.setLevel(logging.NOTSET)

# The following line sets the root logger level as well.
# It's equivalent to both previous statements combined:
logging.basicConfig(level=logging.NOTSET)

logger = logging.getLogger('MovieNotifier')

#
# class StatMiddleware(BaseMiddleware):
#
#     def __init__(self):
#         super(StatMiddleware, self).__init__()
#
#     async def on_process_message(self, message: types.Message, data: dict):
#         await logger.write_logs(self._manager.bot.id, message, parse_text=True)


# Initialize bot and dispatcher
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())


# dp.middleware.setup(StatMiddleware())


class ReqState(StatesGroup):
    get_text = State()
    get_audio = State()


@dp.message_handler(commands=command_start)
async def start(message: types.Message):
    logger.info(f'Request: command_start from {message.chat.id}')
    await message.answer(message_start)
    await ReqState.get_text.set()


@dp.message_handler(state=ReqState.get_text)
async def get_text(message: types.Message, state: FSMContext):
    with open(f'texts/text_{message.chat.id}.txt', 'w') as file:
        file.write(message.text)
        file.close()
    await message.answer(message_load_audio, reply_markup=keyboards[command_start])
    await ReqState.get_audio.set()


@dp.message_handler(state=ReqState.get_audio, content_types=['photo', 'audio', 'document', 'text'])
async def get_audio(message: types.Message, state: FSMContext):
    filename = f'audios/audio_{message.chat.id}'
    if message.content_type == 'audio':
        audio_format = message.audio.file_name
        audio_format = audio_format[audio_format.rfind('.') + 1:]
        await message.audio.download(destination_file=f'{filename}.{audio_format}')
    elif message.content_type == 'document' and message.document.mime_type.find('audio') != -1:
        audio_format = message.document.file_name
        audio_format = audio_format[audio_format.rfind('.') + 1:]
        await message.document.download(destination_file=f'audios/audio_{message.chat.id}.{audio_format}')
    else:
        await message.answer(message_error_file_type, reply_markup=keyboards[command_start])
        return

    await message.answer(message_wait)

    sound = AudioSegment.from_file(f'{filename}.{audio_format}', f"{audio_format}")
    sound.export(f'{filename}.wav', format="wav")

    out_path = model.fit([f'{filename}.wav'], open(f'texts/text_{message.chat.id}.txt').read(),
                         out_path=f'results/result_{message.chat.id}.wav')
    await message.answer_audio(open(out_path, "rb"), title="hero_speaker", reply_markup=keyboards[command_start])
    # await message.answer(message_result, reply_markup=keyboards[command_start])
    await state.finish()


# @dp.callback_query_handler(lambda query: query.data.split(' ')[0] == command_track_item)
# async def track_item(call: types.CallbackQuery):
#     movie_id = call.data.split(' ')[1]
#     logger.info(f'Command track item {movie_id}')
#     db.add_track(call.message.chat.id, movie_id)
#     await call.message.answer(message_track_item, reply_markup=keyboards[command_track_item])
#
#
# @dp.callback_query_handler(lambda query: query.data.split(' ')[0] == command_save_item)
# async def save_item(call: types.CallbackQuery):
#     movie_id = call.data.split(' ')[1]
#     db.add_saved_item(call.message.chat.id, movie_id)
#     await call.message.answer(message_save_item, reply_markup=keyboards[command_track_item])
#

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
