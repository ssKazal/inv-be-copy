from hashids import Hashids
from datetime import datetime
import random
import base64, io
from PIL import Image
from django.core.files.base import ContentFile
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def generate_uids():
    """
    Generating random uids
    """
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    n1 = random.randint(10000, 1000000)
    hashids = Hashids(salt="{}{}".format(n1, timestamp))
    n2 = random.randint(1, 9999)
    ids = hashids.encode(5, 5, 5, n2)
    return ids


def get_image_from_data_url(file_name, data_url, resize=False, base_width=60):
    """
    Convering image string to file
    """
    format, dataurl = data_url.split(";base64,")
    filename, extension = file_name.lower(), format.split("/")[-1]
    file = ContentFile(
        base64.b64decode(dataurl), name=f"{filename}-{generate_uids()}.{extension}"
    )

    if resize:
        image = Image.open(file)
        image_io = io.BytesIO()
        w_percent = base_width / float(image.size[0])
        h_size = int((float(image.size[1]) * float(w_percent)))
        image = image.resize((base_width, h_size), Image.ANTIALIAS)
        image.save(image_io, format=extension)
        file = ContentFile(image_io.getvalue(), name=f"{filename}.{extension}")

    return file


def send_notification(user):
    # To send real-time notification to user
    async_to_sync(get_channel_layer().group_send)(
        f"notification_room_{user.id}",
        {
            "type": "message_notification",
            "response_type": "latest_msg_notification",
            "status":"test"
        }
    )
