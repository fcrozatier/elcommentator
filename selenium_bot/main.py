import os

from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options

from bot import Bot

load_dotenv()
year = 2021
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

expected_download = os.path.dirname(os.getcwd()) + f"/Bulletins/{year}"
opt = Options()
opt.add_experimental_option(
    "prefs",
    {
        "download.default_directory": expected_download,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
    },
)


bot = Bot(options=opt, close_on_exit=False)
bot.connect_ent(USERNAME, PASSWORD)
bot.open_pronote()
bot.download(start=94)
