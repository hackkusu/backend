import qrcode

class QRCodeBll:
    @staticmethod
    def generate_qr_code(phone_number):
        # For SMS
        sms_uri = 'smsto:' + phone_number

        # # For WhatsApp
        # whatsapp_url = 'https://wa.me/11234567890'

        # Choose the content you want in the QR code
        qr_content = sms_uri  # or sms_uri

        # Generate QR code
        qr = qrcode.make(qr_content)
        qr.save('qr_code_' + phone_number + '.png')
