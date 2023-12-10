#meta developer: @POMA_TERABAITbI
import os
import shutil
from BingImageCreator import ImageGen
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from .. import loader
@loader.tds
class Bingimage(loader.Module):
    """Генерирует Картиночки"""

    strings_ru = {
        "name": "BingIMage",
        "config_warning": "Bing cookie. Хранить в недоступном для детей месте.",
        "config_set_cookie": "Сначала установите ваш Bing cookie через конфиг, команда:  cfg BingIMage\n <a href='https://t.me/TerabyteModules'>[ТУТОРИАЛ ПО ПОЛУЧЕНИЮ BING COOKIE ЗДЕСЬ]</a>",
        "generate_message": "🔄 <b>Генерирую!</b>",
        "generate_prompt": "🚫 А что генерировать собственно?",
        "image_caption": "📸 <b>Изображения по запросу:</b> {}",
    }

    strings = {
        "name": "BingIMage",
        "config_warning": "Bing cookie. Keep out of reach of children.",
        "config_set_cookie": "First set your Bing cookie through the config, command: cfg BingIMage\n <a href='https://t.me/TerabyteModules'>[TUTORIAL ON GETTING BING COOKIE HERE]</a>",
        "generate_message": "🔄 <b>Generating!</b>",
        "generate_prompt": "🚫  What's to generate, exactly?",
        "image_caption": "📸 <b>Images on request:</b> {}",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "bing_cookie",
                None,
                self.strings["config_warning"],
                validator=loader.validators.Hidden(),
            )
        )
    @loader.command(ru_doc="<Запрос> - Получить Картиночки 🖼️")
    async def creator(self, message):
        """<Request> - Get Pictures 🖼️"""
        await message.edit(self.strings["generate_message"])
        if not self.config["bing_cookie"]:
            await message.edit(self.strings["config_set_cookie"])
            return

        args = message.text.split(" ", 1)
        if len(args) < 2:
            await message.edit(self.strings["generate_prompt"])
            return

        text = args[1]

        tmp_dir = "tmp"
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

        auth_cookie = self.config["bing_cookie"]
        image_gen = ImageGen(auth_cookie=auth_cookie, auth_cookie_SRCHHPGUSR=auth_cookie)
        image_links = image_gen.get_images(text)
        file_name = "landscape_images"
        image_gen.save_images(image_links, tmp_dir, file_name)

        output_files = []
        for f in os.listdir(tmp_dir):
            if f.endswith(".jpeg"):
                try:
                    image = Image.open(os.path.join(tmp_dir, f))
                    output = BytesIO()
                    image.save(output, "jpeg")
                    output.seek(0)
                    output_files.append(output)
                except UnidentifiedImageError:
                    print(f"Ignoring unreadable image: {f}")

        if output_files:
            caption = self.strings["image_caption"].format(text)
            await message.client.send_file(message.chat_id, file=output_files, caption=caption, force_document=False, reply_to=message.id)
            await message.delete()
            
        shutil.rmtree(tmp_dir)
