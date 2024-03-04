import os
import qrcode
import random
# import categories
import link_generator
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.moduledrawers.pil import CircleModuleDrawer
from qrcode.image.styles.moduledrawers.pil import SquareModuleDrawer
from qrcode.image.styles.moduledrawers.pil import GappedSquareModuleDrawer
from qrcode.image.styles.moduledrawers.pil import VerticalBarsDrawer
from qrcode.image.styles.moduledrawers.pil import HorizontalBarsDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.colormasks import HorizontalGradiantColorMask
from qrcode.image.styles.colormasks import VerticalGradiantColorMask
from PIL import Image, ImageDraw

module_drawers = (CircleModuleDrawer(radius_ratio=1), RoundedModuleDrawer(radius_ratio=1),
                  SquareModuleDrawer(), GappedSquareModuleDrawer(),
                  VerticalBarsDrawer(), HorizontalBarsDrawer())
color_masks = (RadialGradiantColorMask, HorizontalGradiantColorMask, VerticalGradiantColorMask)
bg_images_dirname = "src"
embeded_images_dirname = "embeded_images"
current_dir = os.path.abspath(os.path.curdir)
embeded_images_path = os.path.join(current_dir, embeded_images_dirname)
bg_images_path = os.path.join(current_dir, bg_images_dirname)
destination_folder_name = "dist"
destination_folder_path = os.path.join(current_dir, destination_folder_name)
def txt_tuple_convert(filename):
    tuple = ()
    file = open(filename, "r")
    for str in file:
        if str != '':
            tuple += (str,)
    return tuple

def create_base_tuples():
    categories = txt_tuple_convert("categories.txt")
    usernames = txt_tuple_convert("usernames.txt")
    templates = txt_tuple_convert("templates.txt")
    return(usernames, categories, templates)

def make_regular_qrcode(box_size, link):
    module_drawers = (CircleModuleDrawer(radius_ratio=1),
                      RoundedModuleDrawer(radius_ratio=1),
                      VerticalBarsDrawer(),
                      HorizontalBarsDrawer(),
                      SquareModuleDrawer(),
                      GappedSquareModuleDrawer())
    module_drawer = random.choice(module_drawers)
    eye_drawer = random.choice((module_drawers[1],
                                module_drawers[4]))
    back_color = (255,255,255)
    front_colors = ((0,0,0),(91,77,249),(19,133,246),
                    (92,0,132),(6,37,132),(73,142,74),
                    (179,89,177),(211,102,46),(71,108,240),
                    (229,148,10),(66,30,87))
    edge_color = random.choice(front_colors)
    center_color = random.choice(front_colors)
    color_mask = random.choice(color_masks)
    color_mask = color_mask(back_color, edge_color, center_color)
    chance_of_solid = random.randint(0,100)
    if chance_of_solid > 70:
        color_mask = SolidFillColorMask(back_color, center_color)

    qr = qrcode.QRCode(
        version = None,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = box_size,
        border = 4
    )
    qr.add_data(link)
    qr.make(fit=True)

    qr_img = qr.make_image(
        image_factory = StyledPilImage,
        module_drawer = module_drawer,
        eye_drawer = eye_drawer,
        color_mask = color_mask
    )
    return qr_img

def make_yellow_qrcode(box_size, link):
    module_drawers = (CircleModuleDrawer(radius_ratio=1),
                      RoundedModuleDrawer(radius_ratio=1),
                      VerticalBarsDrawer(),
                      HorizontalBarsDrawer())
    module_drawer = random.choice(module_drawers)
    eye_drawer = module_drawers[1]
    back_color = (255,252,0)
    front_color = (0,0,0)
    qr = qrcode.QRCode(
        version = None,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = box_size,
        border = 4
    )
    qr.add_data(link)
    qr.make(fit=True)

    qr_img = qr.make_image(
        image_factory = StyledPilImage,
        module_drawer = module_drawer,
        eye_drawer = eye_drawer,
        color_mask = SolidFillColorMask(back_color, front_color)
    )
    return qr_img
def create_qr(config):
    chance = random.randint(0,100)
    link = config["link"]
    deg = config["rotate_degrees"]
    size = config["size"]
    module_drawer = config["module_drawer"]
    eye_drawer = config["eye_drawer"]
    box_size = config["box_size"]
    back_color = config["back_color"]
    front_color = config["front_color"]
    image_path = config["image_path"]
    embeded_image = config["embeded_image"]
    qr_img_bbox = Image.new("RGBA", size=size)
    qr_mask_bbox = Image.new("L", size=size)
    if chance > 50:
        back_color = (255,255,255)
        qr_img = make_regular_qrcode(box_size, link)
    else:
        back_color = (255,252,0)
        qr_img = make_yellow_qrcode(box_size, link)

    if embeded_image:
        qr_img = embed_image(qr_img, image_path, back_color)
    qr_mask = Image.new("L", qr_img.size, color="black")
    draw_mask = ImageDraw.Draw(qr_mask)
    draw_mask.rounded_rectangle((0,0,qr_img.size[0],qr_img.size[1]), fill="white", width=3, radius=24)
    rotated_qr_img = qr_img.rotate(deg, resample=Image.BICUBIC, expand=1)
    rotated_qr_mask = qr_mask.rotate(deg, resample=Image.BICUBIC, expand=1)
    # qr_img_bbox.paste(rotated_qr_img)
    # qr_mask_bbox.paste(rotated_qr_mask)
    bboxes = paste_qr(qr_img_bbox, qr_mask_bbox,
                      rotated_qr_img, rotated_qr_mask)
    # qr_mask_bbox.show()
    return bboxes

def paste_qr(img_bbox, mask_bbox, qr_img, qr_mask):
    min_x = 0
    min_y = 0
    max_x = img_bbox.size[0] - qr_img.size[0]
    max_y = img_bbox.size[1] - qr_img.size[1]
    x = random.randint(min_x, max_x)
    y = random.randint(min_y, max_y)
    img_bbox.paste(qr_img, (x,y))
    mask_bbox.paste(qr_mask, (x,y))
    return (img_bbox, mask_bbox)

def embed_image(img, image_path, back_color):
    emb_img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    center = int(img.size[0] / 2)
    edge = int(img.size[0] / 10)
    coors = (center - edge,
             center - edge,
             center + edge,
             center + edge)
    resized_emb_img = emb_img.resize((coors[2]-coors[0],
                                      coors[3]-coors[1]))
    draw.rounded_rectangle(coors, fill=back_color, width=10, radius=10)
    img.paste(resized_emb_img, (coors[0],coors[1]), resized_emb_img)
    return img

def get_link():
    base_tuples = create_base_tuples()
    link = link_generator.generate(base_tuples)
    return link

def get_module_drawer():
    return random.choice(module_drawers)

def get_eye_drawer():
    return random.choice(module_drawers)

def get_box_size(size):
    divider = random.randint(95, 115)
    main_side = size[0]
    if size[1] < size[0]:
        main_side = size[1]
    box_size = int(main_side / divider)
    print("Box size is ", box_size)
    return box_size

def get_rotate_degrees():
    return random.randint(-45, 45)

def get_bg_color():
    white = (255, 255, 255)
    yellow = (255, 252, 0)
    lightblue = (162, 250, 244)
    pink = (254, 184, 255)
    return random.choice((
        white, #white
        yellow, #yellow
        lightblue, #lightblue
        pink #pink
    ))

def get_fill_color():
    black = (0, 0, 0)
    brown = (38, 14, 14)
    green = (7, 26, 1)
    darkblue = (1, 7, 26)
    grey = (100,100,100)
    return random.choice((
        black, #black
        brown, #brown
        green, #green
        darkblue, #darkblue
        grey
    ))

# def get_color_mask():
#     color_mask = 

def get_image_path():
    filenames = os.listdir(embeded_images_path)
    filename = random.choice(filenames)
    image_path = os.path.join(embeded_images_path, filename)
    return image_path

def get_config(img):
    config = {
        "link": get_link(),
        "module_drawer": get_module_drawer(),
        "eye_drawer": get_eye_drawer(),
        "box_size": get_box_size(img.size),
        "rotate_degrees": get_rotate_degrees(),
        "back_color": get_bg_color(),
        "front_color": get_fill_color(),
        "image_path": get_image_path(),
        "embeded_image": random.randint(0,1)
    }
    return config


for file in os.listdir(bg_images_path):
    final_file_path = os.path.join(destination_folder_path, file)
    filepath = os.path.join(bg_images_path, file)
    bg_img = Image.open(filepath)
    config = get_config(bg_img)
    config["size"] = bg_img.size
    print(config)
    (qr_img_bbox, qr_mask_bbox) = create_qr(config)
    # qr_mask_bbox.show()
    # qr_mask = create_qr_mask(35)
    img = Image.composite(qr_img_bbox, bg_img, qr_mask_bbox)
    # img = Image.composite(bg_img, qr_img, qr_mask)
    # bg_img.paste(qr_img)
    img.save(final_file_path)
# categories.count_lines()
# img.show()