from PIL import Image, ImageDraw, ImageFont
import os
import textwrap


BASE_CARD_DIR = "static/base_cards"
GENERATED_CARD_DIR = "static/generated_cards"


def generate_gratitude_card(
        card_id : int,
        receiver_name : str,
        message : str,
        sender_name : str,
        output_filename : str
):
    # Generate a gratitude card image by embedding text on a base canva card

    base_card_path = os.path.join(BASE_CARD_DIR,f"card_{card_id}.png")
    file_system_path = os.path.join(GENERATED_CARD_DIR,output_filename)
    url_path = f"static/generated_cards/{output_filename}"

    #Load base image

    img = Image.open(base_card_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    #Load the font

    font = ImageFont.truetype(
                    "fonts/PlayfairDisplay-Regular.ttf",
                     size = 55)

    #Text Placement

    text_x = 300    #moves text to right
    text_y = 400     #moves text down
    y_offset = text_y
    max_width = 35  #character per line

    wrapped_text = textwrap.fill(message,width = max_width)

    draw.text(
        (text_x,y_offset),
        f"Dear {receiver_name},",
        #wrapped_text,
        fill = (20,40,80),
        font=font
    )

    y_offset += 70  #space after name

    # Message
    draw.multiline_text(
        (text_x, y_offset),
        wrapped_text,
        fill=(40, 60, 110),
        font=font,
        spacing=16
    )

    #Message height calc
    bbox = draw.multiline_textbbox(
        (text_x,y_offset),
        wrapped_text,
        #fill=(40,60,110),
        font=font,
        spacing=16
    )

    #y_offset += wrapped_text.count("\n") * 40 + 40
    text_height = bbox[3] - bbox[1]
    y_offset += text_height + 50

    #Sender name
    draw.text(
        (text_x+800,y_offset),
        f"-{sender_name}",
        fill=(20,40,80),
        font = font
    )

    img.save(file_system_path)

    return url_path




