from io import BytesIO

import qrcode
from PIL import Image, ImageDraw, ImageFont

class QRCodeBll:
    @staticmethod
    def generate_qr_code(phone_number, start_code):
        # The content of the QR code
        qr_content = 'smsto:' + phone_number

        # Create the QR code instance
        qr = qrcode.QRCode(
            version=None,  # Version `None` means the library will auto-determine the size
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,  # The number of pixels per QR code box
            border=4,  # The boxes of the border around the QR code
        )

        # Add the content to the QR code
        qr.add_data(qr_content)
        qr.make(fit=True)

        # Generate the QR code
        img_qr = qr.make_image(fill_color='white', back_color='#2c2e3b')

        # Define the font for the text
        font_path = "FFF_Tusj.ttf"  # Use the correct path to your font file
        font_size = 20
        font = ImageFont.truetype(font_path, font_size)

        # Measure text
        dummy_draw = ImageDraw.Draw(img_qr)
        text_width, text_height = dummy_draw.textsize('text "' + start_code + '" to begin!', font=font)

        # Create a new image with space for the text
        canvas = Image.new(
            'RGB',
            (img_qr.size[0], img_qr.size[1] + text_height + 20),  # New image size
            '#2c2e3b'
        )
        # Place the QR code on the canvas
        canvas.paste(img_qr, (0, 0))

        # Initialize drawing context
        draw = ImageDraw.Draw(canvas)

        # Add text at the bottom
        text_position = ((canvas.size[0] - text_width) // 2, img_qr.size[1] + 10)
        draw.text(text_position, 'text "' + start_code + '" to begin!', font=font, fill='white')

        return canvas

    @staticmethod
    def generate_and_save_qr_code(phone_number, start_code):

        canvas = QRCodeBll.generate_qr_code(phone_number, start_code)
        # Save the final image
        qr_filename = f'qr_code_{phone_number}_{start_code}.png'
        canvas.save(qr_filename)

        return qr_filename

    @staticmethod
    def generate_and_return_bytes_buffer_qr_code(phone_number, start_code):

        canvas = QRCodeBll.generate_qr_code(phone_number, start_code)

        # Instead of saving the file, create an in-memory bytes buffer
        buffer = BytesIO()
        canvas.save(buffer, format='PNG')  # Save the image to the buffer in PNG format
        buffer.seek(0)  # Rewind the buffer's file pointer

        # Return an HTTP response with the image and the correct MIME type
        return buffer
