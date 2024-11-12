class build:
    IMAGE_SIZE = 217 #px from albion online data
    
    #weapon, off hand,helmet,armor,boots,cape,food
    def __init__(self, weapon = str, off_hand = str, helmet = str, armor = str, boots = str, cape = str, food = str) -> None:
        self.weapon = weapon
        self.off_hand = off_hand
        self.helmet = helmet
        self.armor = armor
        self.boots = boots
        self.cape = cape
        self.food = food

    def load_images(self):
        #get images from albion online data
        self.images = {
            'weapon': open_image_from_url("https://render.albiononline.com/v1/item/" + self.weapon),
            'off_hand': open_image_from_url("https://render.albiononline.com/v1/item/" + self.off_hand),
            'helmet': open_image_from_url("https://render.albiononline.com/v1/item/" + self.helmet),
            'armor': open_image_from_url("https://render.albiononline.com/v1/item/" + self.armor),
            'boots': open_image_from_url("https://render.albiononline.com/v1/item/" + self.boots),
            'cape': open_image_from_url("https://render.albiononline.com/v1/item/" + self.cape),
            'food': open_image_from_url("https://render.albiononline.com/v1/item/" + self.food)
        }
        if self.images['off_hand'] is not None:
            self.images['off_hand'] = self.images['off_hand'].resize((int(self.IMAGE_SIZE * 0.65), int(self.IMAGE_SIZE*0.65)))
        
    
    def get_image(self, padding = 0):
        #show images
        total_width = self.IMAGE_SIZE * 6 + padding * 5
        max_height = self.IMAGE_SIZE + 10
        new_image = Image.new('RGBA', (total_width, max_height) , (50,50,50,0))
        x_offset = 0
        y_offset = 5
        for key in self.images.keys():
            image = self.images[key] 
            if image is None or key == 'off_hand':
                continue
            new_image.paste(image, (x_offset, y_offset), mask=image)
            x_offset += image.width + padding
        if self.images['off_hand'] is not None:
            new_image.paste(self.images['off_hand'], (self.IMAGE_SIZE//2 - 20, self.IMAGE_SIZE//2 - 20 + y_offset), mask=self.images['off_hand'])
        return new_image
    


from PIL import Image
from PIL import ImageEnhance
import requests
from io import BytesIO
import csv
from collections import Counter

def open_image_from_url(url):
    if url == "https://render.albiononline.com/v1/item/":
        return None
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Open the image using Pillow from the byte stream
        img = Image.open(BytesIO(response.content)).convert("RGBA")
        return img
    else:
        print(f"Failed to fetch image from {url}. Status code: {response.status_code}")
        return None


def remove_background_with_margin(image, margin):
    # Convertir la imagen a modo RGB
    image = image.convert("RGB")

    # Obtener los colores de píxeles de la imagen
    pixels = list(image.getdata())

    # Contar la ocurrencia de cada color
    color_counts = Counter(pixels)

    # Obtener el color más común
    most_common_color = color_counts.most_common(1)[0][0]

    # Crear una nueva imagen con fondo transparente
    new_image = Image.new("RGBA", image.size, (0, 0, 0, 0))

    # Iterar sobre los píxeles de la imagen original
    for i, pixel in enumerate(pixels):
        # Si el color del píxel no es el color más común ni está dentro del margen, copiarlo a la nueva imagen
        if pixel != most_common_color and not is_color_similar(pixel, most_common_color, margin):
            new_image.putpixel((i % image.width, i // image.width), pixel)

    return new_image

def is_color_similar(color1, color2, margin):
    # Comprobar si los componentes de color están dentro del margen
    for c1, c2 in zip(color1, color2):
        if abs(c1 - c2) > margin:
            return False
    return True



#PROPIEDADES FINALES
WIDTH = 1920
HEIGHT = 1080
LOGO_HEIGHT = 250
LOGO_WIDTH = 250
BUILD_X_OFFSET = 80
BUILD_PADDING = -15
BUILD_IMG_SIZE = 150

GROUP = 0

def main(group, name):
    #Builds
    builds = []
    
    with open('builds.csv', newline='') as csvfile:
        builds_csv = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(builds_csv)
        builds_csv = list(builds_csv)
        for row in builds_csv:
            if row[1] != str(group):
                continue
            build1 = build(row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            #load images
            build1.load_images()
            #show images
            builds.append(build1.get_image(BUILD_PADDING))

    #load bg, logo
    bg = Image.open("src/bgs/bg3.jpg")
    logo = Image.open("src/logo.png")
    logo = remove_background_with_margin(logo, 70)

    final = Image.new('RGBA', (WIDTH, HEIGHT), (0,0,0,255))

    #paste bg
    bg = bg.point(lambda p: p * 0.6)
    bg = bg.resize((WIDTH, HEIGHT))
    final.paste(bg, (0,0))

    #paste logo
    logo = logo.resize((LOGO_WIDTH, LOGO_HEIGHT))
    final.paste(logo, (WIDTH - LOGO_WIDTH - 10, HEIGHT - LOGO_HEIGHT - 10),mask=logo)

    #paste builds
    y_offset = 150
    for i in range(len(builds)//2):
        build_img = builds[i]
        print(build_img.width, BUILD_IMG_SIZE * build_img.width /build_img.height)
        build_img = build_img.resize((int(BUILD_IMG_SIZE * build_img.width /build_img.height), BUILD_IMG_SIZE))
        final.paste(build_img, (BUILD_X_OFFSET, y_offset), mask=build_img)
        y_offset += build_img.height + 20

    y_offset = 156
    for i in range(len(builds)//2, len(builds) - (1&len(builds))):
        build_img = builds[i]
        build_img = build_img.resize((int(BUILD_IMG_SIZE * build_img.width /build_img.height), BUILD_IMG_SIZE))
        final.paste(build_img, (WIDTH - BUILD_X_OFFSET - build_img.width, y_offset), mask=build_img)
        y_offset += build_img.height + 20

    if(1&len(builds)):
        build_img = builds[len(builds) - 1]
        build_img = build_img.resize((int(BUILD_IMG_SIZE * build_img.width /build_img.height), BUILD_IMG_SIZE))
        final.paste(build_img, (WIDTH//2 - build_img.width//2, y_offset), mask=build_img)

    enhancer = ImageEnhance.Color(final)
    final = enhancer.enhance(1.5)
    final.save(name + ".png")

if __name__ == "__main__":
    main(1, "dps")

