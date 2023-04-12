import os
import csv

from PIL import Image


# Set the path to the parent directory containing the subfolders
parent_dir = "/mnt/d/giveaway/src_images"

# Set the path to the output CSV file
output_file = "./catalog.csv"

# Define a list to hold the tags
tags = []

# Define a function to get the tag from a file path
def get_tag(path):
    # Split the path into its components
    components = path.split("/")
    # The tag is the name of the subfolder that contains the file
    return components[-2]

# Define a function to get the list of SVG files
def get_svg_files():
    # Define a list to hold the file paths
    files = {}
    # Walk through the subfolders
    for dirpath, dirnames, filenames in os.walk(parent_dir):
        # Check each file in the folder
        folder_name = dirpath.split('/')[-1]
        for filename in sorted(filenames):
            # If the file is an SVG, add its path to the list
            if filename.endswith(".png"):
                if folder_name not in files:
                    files[folder_name] = []
                files[folder_name].append([os.path.join(dirpath, filename), filename])
    # Return the list of file paths
    return files

# Get the list of SVG files
svg_files = get_svg_files()

horizontal_wood_image = Image.open('/mnt/d/giveaway/wood_sign.png')
vertical_wood_image = Image.open('/mnt/d/giveaway/wood_sign.png')
vertical_wood_image = vertical_wood_image.rotate(90, expand=True)

'''
handleId = folder name
first entry's fieldType is Product, all others are Variant
first entry name is the folder name, others are blank
first entry description is the description, others are blank
first entry productImageUrl is a semi-colon delimited list of all the images in the folder, others are blank
first entry collection is "laser engraved signs", otehrs are blank
sku and ribbon are blank
first entry price is 3.99, others are blank
surcharge is blank
first entry visible is TRUE, others are blank
first entry inventory is blank, others are "InStock"
first entry 
first entry weight is 0.25, others are blank


'''




with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    tag_counts = {}
    header_row = "handleId,fieldType,name,description,productImageUrl,collection,sku,ribbon,price,surcharge,visible,discountMode,discountValue,inventory,weight,cost,productOptionName1,productOptionType1,productOptionDescription1,productOptionName2,productOptionType2,productOptionDescription2,productOptionName3,productOptionType3,productOptionDescription3,productOptionName4,productOptionType4,productOptionDescription4,productOptionName5,productOptionType5,productOptionDescription5,productOptionName6,productOptionType6,productOptionDescription6,additionalInfoTitle1,additionalInfoDescription1,additionalInfoTitle2,additionalInfoDescription2,additionalInfoTitle3,additionalInfoDescription3,additionalInfoTitle4,additionalInfoDescription4,additionalInfoTitle5,additionalInfoDescription5,additionalInfoTitle6,additionalInfoDescription6,customTextField1,customTextCharLimit1,customTextMandatory1,customTextField2,customTextCharLimit2,customTextMandatory2,brand".split(',')
    writer.writerow(header_row)

    print(len(header_row))
    for path in svg_files:
        print(path)
        handle_id = path.replace(' ','_').lower()

        image_list = []
        image_names = []

        variant_rows = []
        image_count = 0
        for file in svg_files[path]:
            image_count += 1
            path_file = file[0]
            filename = file[1]

            output_filename = f'{handle_id}_{image_count}.jpg'
            image_url = f'https://iandouglasllc-engraver.herokuapp.com/img/{handle_id}/{output_filename}'

            image_list.append(image_url)
            variant_name = filename.replace('.png','').replace('_',' ').title()
            image_names.append(variant_name)

            
            base_img = Image.new('RGB', (1500, 1500), (255, 255, 255))
            text_image = Image.open(path_file)
            width, height = text_image.size
            sign_image = horizontal_wood_image
            # 1500 x 1000
            pad_left_right = 0
            pad_top_bottom = 250

            # print("path file", path_file)
            # print("before width", width)
            # print("before height", height)

            if height > width:
                sign_image = vertical_wood_image
                # 1000 x 1500
                pad_left_right = 250
                pad_top_bottom = 0
                # scale width to 900 pixels and keep aspect ratio of height the same
                scale = 900 / width
                width = 900
                height = int(height * scale)

                if height > 1500:
                    scale = 1400 / height
                    height = 1400
                    width = int(width * scale)

            else: # horizontal
                scale = 900 / height
                height = 900
                width = int(width * scale)

                if width > 1500:
                    scale = 1400 / width
                    width = 1400
                    height = int(height * scale)

            # print("scale", scale)
            # print("after width", width)
            # print("after height", height)

            # tell PIL to scale the image to the new width and height
            text_image = text_image.resize((width, height))

            # overlay wood sign on top of base image
            base_img.paste(sign_image, (pad_left_right, pad_top_bottom), sign_image)

            left_right_offset = int((1500 - width) / 2)
            top_bottom_offset = int((1500 - height) / 2)

            # print("left_right_offset", left_right_offset)
            # print("top_bottom_offset", top_bottom_offset)

            #overlay text on top of base image
            base_img.paste(text_image, (left_right_offset, top_bottom_offset), text_image)

            # write base image to disk
            # new_path = path.replace('/src_images/','/img/')



            try:
                os.mkdir(f'/mnt/d/giveaway/img/{handle_id}')
            except:
                pass
            base_img.save(f'/mnt/d/giveaway/img/{handle_id}/{output_filename}', optimize=True, quality=75)

            variant_row = ['']*53
            variant_row[0] = handle_id
            variant_row[1] = 'Variant'
            variant_row[10] = True
            variant_row[13] = 'InStock'
            variant_row[18] = variant_name
            variant_rows.append(variant_row)

        product_row = ['']*53
        product_row[0] = handle_id
        product_row[1] = 'Product'
        product_row[2] = path
        product_row[3] = 'Laser engraving on a 10cm x 15cm (4" x 6") piece of wood. Final product may have rounded corners and colors may vary slightly from the image shown. Wood will also have natural variations in color and grain.'
        product_row[4] = ';'.join(image_list)
        product_row[5] = 'Laser Engraved Signs'
        product_row[6] = ''
        product_row[7] = ''
        product_row[8] = 3.99
        product_row[9] = ''
        product_row[10] = True
        product_row[11] = 'PERCENT'
        product_row[12] = '0.0'
        product_row[13] = 'InStock'
        product_row[14] = 0.25
        product_row[15] = ''
        product_row[16] = 'Quotation'
        product_row[17] = 'DROP_DOWN'
        product_row[18] = ';'.join(image_names)


        writer.writerow(product_row)
        for variant_row in variant_rows:
            writer.writerow(variant_row)
        # import sys; sys.exit()
        # writer.writerow([product_id, 'Product', product_name, 'Laser engraving on a 10cm x 15cm (4" x 6") piece of wood.', url, tag, product_id, 3.99, "InStock", "0.25", 'TRUE', "", "", "", "", "", "", "", "", "", "", "", ""])


        # for file in svg_files[path]:

    # import sys; sys.exit()

    # for file in svg_files:
    #     path = file[0]
    #     path_file = file[1]
    #     filename = file[2]

    #     tag = path.replace('/mnt/d/giveaway/src_images/','')

    #     if tag not in tag_counts:
    #         tag_counts[tag] = 0
    #     tag_counts[tag] += 1
    #     product_id = f'{tag}_{tag_counts[tag]}'

    #     product_name = filename.replace('.png','').replace('_',' ')

    #     # make a new 1500x1500 PNG graphic with PIL
    #     # set the background color to white

    #     base_img = Image.new('RGB', (1500, 1500), (255, 255, 255))
    #     text_image = Image.open(path_file)
    #     width, height = text_image.size
    #     sign_image = horizontal_wood_image
    #     # 1500 x 1000
    #     pad_left_right = 0
    #     pad_top_bottom = 250

    #     # print("path file", path_file)
    #     # print("before width", width)
    #     # print("before height", height)

    #     if height > width:
    #         sign_image = vertical_wood_image
    #         # 1000 x 1500
    #         pad_left_right = 250
    #         pad_top_bottom = 0
    #         # scale width to 900 pixels and keep aspect ratio of height the same
    #         scale = 900 / width
    #         width = 900
    #         height = int(height * scale)

    #         if height > 1500:
    #             scale = 1400 / height
    #             height = 1400
    #             width = int(width * scale)

    #     else: # horizontal
    #         scale = 900 / height
    #         height = 900
    #         width = int(width * scale)

    #         if width > 1500:
    #             scale = 1400 / width
    #             width = 1400
    #             height = int(height * scale)

    #     # print("scale", scale)
    #     # print("after width", width)
    #     # print("after height", height)

    #     # tell PIL to scale the image to the new width and height
    #     text_image = text_image.resize((width, height))

    #     # overlay wood sign on top of base image
    #     base_img.paste(sign_image, (pad_left_right, pad_top_bottom), sign_image)

    #     left_right_offset = int((1500 - width) / 2)
    #     top_bottom_offset = int((1500 - height) / 2)

    #     # print("left_right_offset", left_right_offset)
    #     # print("top_bottom_offset", top_bottom_offset)

    #     #overlay text on top of base image
    #     base_img.paste(text_image, (left_right_offset, top_bottom_offset), text_image)

    #     # write base image to disk
    #     new_path = path.replace('/src_images/','/img/')

    #     base_img.save(f'{new_path}/{product_id}.jpg', optimize=True, quality=75)

    #     url = f'https://iandouglasllc-engraver.herokuapp.com/img/{tag}/{product_id}.jpg'
    #     writer.writerow([product_id, 'Product', product_name, 'Laser engraving on a 10cm x 15cm (4" x 6") piece of wood.', url, tag, product_id, 3.99, "InStock", "0.25", 'TRUE', "", "", "", "", "", "", "", "", "", "", "", ""])

    #     # import sys; sys.exit()