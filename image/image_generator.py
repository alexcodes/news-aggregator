import textwrap
from io import BytesIO

import requests
from PIL import Image, ImageFilter, ImageFont, ImageDraw

# TODO add watermark

GAUSSIAN_BLUR_RADIUS = 6
MAX_IMAGE_WIDTH = 600


def resize_image(image):
    if image.width <= MAX_IMAGE_WIDTH:
        return image

    new_width = MAX_IMAGE_WIDTH
    new_height = int(image.height / (image.width / new_width))
    return image.resize((new_width, new_height))


def get_max_word_length(text):
    if not text:
        return 0

    max_length = 0
    for word in text.split(" "):
        length = len(word)
        if length > max_length:
            max_length = length

    return max_length


def get_padding(img_size):
    return int(min(img_size) * 0.1)


def get_text_padding(img_size):
    return 1.5 * get_padding(img_size)


def get_text_padding_top(img_size, lines_count, font_size):
    text_padding = get_text_padding(img_size)
    free_height = img_size[1] - 2 * text_padding
    lines_height = lines_count * font_size
    return text_padding + (free_height - lines_height) / 2


def load_image(img_filename):
    if img_filename.startswith("http"):
        data = requests.get(img_filename).content
        file = BytesIO(data)
        return file

    return img_filename


class ImageGenerator:

    def __init__(self, font_filename, default_image):
        self.font_filename = font_filename
        self.default_image = default_image

    def generate(self, text, img_filename=None):
        background = self._get_background(img_filename)
        foreground = self._get_text_layer(background, text)
        return Image.alpha_composite(background, foreground)

    def _get_background(self, img_filename):
        if not img_filename:
            img_filename = self.default_image

        file = load_image(img_filename)

        background = Image.open(file).convert('RGBA')
        background = resize_image(background)

        padding = get_padding(background.size)

        blurred = background.filter(ImageFilter.GaussianBlur(radius=GAUSSIAN_BLUR_RADIUS))

        cropped = blurred.crop(
            (
                padding,
                padding,
                blurred.width - padding,
                blurred.height - padding
            )
        )
        darken = Image.new('RGBA', cropped.size, (0, 0, 0, 64))
        darken = Image.alpha_composite(cropped, darken)

        background.paste(darken, (padding, padding), darken)
        return background

    def _get_text_layer(self, background, text):
        txt_img = Image.new('RGBA', background.size, (255, 255, 255, 0))

        draw = ImageDraw.Draw(txt_img)

        font_size, line_length = self._get_font_size_and_line_length(txt_img.size, text, draw)
        # print(font_size, line_length)

        font = ImageFont.truetype(self.font_filename, font_size)

        lines = textwrap.wrap(text, line_length)
        padding_top = get_text_padding_top(txt_img.size, len(lines), font_size)
        for line in lines:
            padding_left = (background.width - draw.textsize(line, font=font)[0]) / 2
            draw.text((padding_left, padding_top), line, font=font, fill=(255, 255, 255, 232))
            padding_top += font_size

        return txt_img

    def _get_font_size_and_line_length(self, img_size, text, draw):
        text_padding = get_text_padding(img_size)
        max_line_width = img_size[0] - 2 * text_padding
        max_word_length = get_max_word_length(text)

        max_space = 0
        pair = (0, 0)

        for font_size in range(10, 72, 2):
            max_lines = (img_size[1] - 2 * text_padding) / font_size
            font = ImageFont.truetype(self.font_filename, font_size)
            for chars_in_line in range(max_word_length, 80, 5):
                lines = textwrap.wrap(text, chars_in_line)
                if len(lines) > max_lines:
                    continue

                space = 0
                violated = False
                for line in lines:
                    line_size = draw.textsize(line, font=font)
                    if line_size[0] > max_line_width:
                        violated = True
                        break
                    space += line_size[0] * line_size[1]

                if violated:
                    break

                if space > max_space:
                    max_space = space
                    pair = (font_size, chars_in_line)

        return pair[0], pair[1]

# timestamp = time.time()
# img = generate(image_file, title)
# timestamp = time.time() - timestamp
# print("Generated for {0:.3f} sec".format(timestamp))
