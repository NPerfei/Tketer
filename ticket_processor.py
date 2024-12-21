from PIL import Image, ImageDraw, ImageFont, ImageTk
import database_manager as dbm

def create_ticket_image(database: dbm.DatabaseManager, event_name, event_venue, event_date, event_time, file_path, mode: int, id = None):
    def draw_event_title(draw, name):
        x1, y1, x2, y2 = (200, 200, 2300, 1000)
        font = ImageFont.truetype("arialbd.ttf", 150)

        # draw.rectangle([x1, y1, x2, y2], width=2, outline="red")

        bbox = draw.textbbox((0, 0), name, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        text_x = x1 + (x2 - x1 - text_width) // 2
        text_y = y1 + (y2 - y1 - text_height) // 2

        draw.text((text_x, text_y), name, fill="black", font=font)

    def draw_event_venue(draw, venue):
        x1, y1, x2, y2 = (100, 1130, 2325, 1250)
        font= ImageFont.truetype("arial.ttf", 80)

        # draw.rectangle([x1, y1, x2, y2], width=2, outline="blue")

        bbox = draw.textbbox((0, 0), venue, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        text_x = x1 + (x2 - x1 - text_width) // 2
        text_y = y1 + (y2 - y1 - text_height) // 2

        draw.text((text_x, text_y), venue, fill="black", font=font)

    
    def draw_event_date(draw, date):
        x1, y1, x2, y2 = (100, 1230, 2325, 1350)
        font = ImageFont.truetype("arial.ttf", 60)

        # draw.rectangle([x1, y1, x2, y2], width=2, outline="blue")

        bbox = draw.textbbox((0, 0), date, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        text_x = x1 + (x2 - x1 - text_width) // 2
        text_y = y1 + (y2 - y1 - text_height) // 2

        draw.text((text_x, text_y), date, fill="black", font=font)


    def draw_event_time(draw, start, end):
        x1, y1, x2, y2 = (100, 1300, 2325, 1420)
        font = ImageFont.truetype("arial.ttf", 50)
        time = f"{start} to {end}"

        # draw.rectangle([x1, y1, x2, y2], width=2, outline="blue")

        bbox = draw.textbbox((0, 0), time, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        text_x = x1 + (x2 - x1 - text_width) // 2
        text_y = y1 + (y2 - y1 - text_height) // 2

        draw.text((text_x, text_y), time, fill="black", font=font)


    def draw_name(image, name):
        x1, y1, x2, y2 = (2520, 60, 2600, 1310)

        font = ImageFont.truetype("arial.ttf", 50)

        box_width = x2 - x1
        box_height = y2 - y1

        temp_image = Image.new("RGBA", (box_width + 1000, box_height), (255, 255, 255, 0))
        temp_draw = ImageDraw.Draw(temp_image)

        text_bbox = temp_draw.textbbox((0, 0), name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        text_x = (box_width - text_width) // 2 + 500
        text_y = (box_height - text_height) // 2

        temp_draw.text((text_x, text_y), name, font=font, fill="black")

        rotated_image = temp_image.rotate(90, expand=True)

        # draw.rectangle([x1, y1, x2, y2], outline="red", width=3)

        new_x1 = x1 + (box_width - rotated_image.width) // 2
        new_y1 = y1 + (box_height - rotated_image.height) // 2

        image.paste(rotated_image, (new_x1, new_y1), rotated_image)


    def draw_course_section(image, course_section):
        x1, y1, x2, y2 = (2650, 60, 2750, 990)

        font = ImageFont.truetype("arial.ttf", 50)

        box_width = x2 - x1
        box_height = y2 - y1

        temp_image = Image.new("RGBA", (box_width + 1500, box_height), (255, 255, 255, 0))
        temp_draw = ImageDraw.Draw(temp_image)

        text_bbox = temp_draw.textbbox((0, 0), course_section, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        text_x = (box_width - text_width) // 2 + 500
        text_y = (box_height - text_height) // 2

        temp_draw.text((text_x, text_y), course_section, font=font, fill="black")

        rotated_image = temp_image.rotate(90, expand=True)

        # draw.rectangle([x1, y1, x2, y2], outline="red", width=3)

        new_x1 = x1 + (box_width - rotated_image.width) // 2
        new_y1 = y1 + (box_height - rotated_image.height) // 2

        image.paste(rotated_image, (new_x1, new_y1), rotated_image)


    def draw_ticket_no(image, ticket_no):
        x1, y1, x2, y2 = (2950, 60, 3000, 990)

        font = ImageFont.truetype("cour.ttf", 100)

        box_width = x2 - x1
        box_height = y2 - y1

        temp_image = Image.new("RGBA", (box_width + 1400, box_height), (255, 255, 255, 0))
        temp_draw = ImageDraw.Draw(temp_image)

        text_bbox = temp_draw.textbbox((0, 0), ticket_no, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        text_x = (box_width - text_width) // 2 + 500
        text_y = (box_height - text_height) // 2

        temp_draw.text((text_x, text_y), ticket_no, font=font, fill="red")

        rotated_image = temp_image.rotate(90, expand=True)

        # draw.rectangle([x1, y1, x2, y2], outline="red", width=3)

        new_x1 = x1 + (box_width - rotated_image.width) // 2
        new_y1 = y1 + (box_height - rotated_image.height) // 2

        image.paste(rotated_image, (new_x1, new_y1), rotated_image)


    name = event_name
    venue = event_venue
    date = event_date
    start = event_time[0]
    end = event_time[1]

    image_path = "images/ticket_template.png"

    if mode == 1:
        all_data = database.get_data()

        for row in all_data:
            ticket_number = f"{row[0]:06d}"
            entry_name = row[1]
            entry_course_section = row[2]

            image = Image.open(image_path)
            draw = ImageDraw.Draw(image)

            draw_event_title(draw, name)
            draw_event_venue(draw, venue)
            draw_event_date(draw, date)
            draw_event_time(draw, start, end)

            draw_name(image, entry_name)
            draw_course_section(image, entry_course_section)
            draw_ticket_no(image, ticket_number)

            output_path = f"{file_path}/{entry_name.split()[-1]}_{entry_course_section}_{ticket_number}.png"
            
            image.save(output_path)
    
    if mode == 2:
        data = database.get_datum(id)

        ticket_number = f"{data[0]:06d}"
        entry_name = data[1]
        entry_course_section = data[2]

        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        draw_event_title(draw, name)
        draw_event_venue(draw, venue)
        draw_event_date(draw, date)
        draw_event_time(draw, start, end)

        draw_name(image, entry_name)
        draw_course_section(image, entry_course_section)
        draw_ticket_no(image, ticket_number)

        return ImageTk.PhotoImage(image.resize((500, 250)))

    if mode == 3:
        data = database.get_datum(id)

        ticket_number = f"{data[0]:06d}"
        entry_name = data[1]
        entry_course_section = data[2]

        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        draw_event_title(draw, name)
        draw_event_venue(draw, venue)
        draw_event_date(draw, date)
        draw_event_time(draw, start, end)

        draw_name(image, entry_name)
        draw_course_section(image, entry_course_section)
        draw_ticket_no(image, ticket_number)

        output_path = f"{file_path}/{entry_name.split()[-1]}_{entry_course_section}_{ticket_number}.png" 
        image.save(output_path)
