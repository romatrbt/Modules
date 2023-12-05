import os
import shutil
from BingImageCreator import ImageGen
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from .. import loader
#meta developer: @POMA_TERABAITbI
@loader.tds
class Bingimage(loader.Module):
    strings = {"name": "BingIMage"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "bing_cookie",
                None,
                lambda: "Bing cookie. Хранить в недостпуном для детей месте",
                validator=loader.validators.Hidden(),
            )
        )

    async def creatorcmd(self, message):
        """<Запрос> Получить Картиночки 🖼️"""
        await message.edit("🔄 <b>Генерирую!</b>")
        if not self.config["bing_cookie"]:
            await message.edit("🚫 Сначала установите ваш Bing cookie через конфиг, команда:  cfg BingIMage\n <a href='https://t.me/TerabyteModules'>[ТУТОРИАЛ ПО ПОЛУЧЕНИЮ BING COOKIE ЗДЕСЬ]</a>")
            return

        args = message.text.split(" ", 1)
        if len(args) < 2:
            await message.edit("🚫 А что генерировать собственно?")
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
            caption = f"📸 <b>Изображения по запросу:</b> {text}"
            await message.client.send_file(message.chat_id, file=output_files, caption=caption, force_document=False, reply_to=message.id)
            await message.delete()
            
        shutil.rmtree(tmp_dir)
