import os
import uuid

from PIL import Image, ImageOps

from pillow_heif import register_heif_opener

register_heif_opener()


def optimize_image(file, upload_folder, quality=85, max_width=1600):
    """
    يحفظ نسخة WebP محسنة من الصورة.
    - يحافظ على نسبة العرض للطول.
    - لا يكبر الصور الصغيرة.
    - يصحح اتجاه صور الهاتف.
    - يحولها إلى WebP.
    """

    image = Image.open(file)

    # تصحيح اتجاه صور الهاتف
    image = ImageOps.exif_transpose(image)

    # تحويل إلى RGB إذا لزم
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    width, height = image.size

    # تصغير فقط إذا كانت الصورة أكبر من الحد
    if width > max_width:
        ratio = max_width / width
        new_height = int(height * ratio)

        image = image.resize(
            (max_width, new_height),
            Image.LANCZOS
        )

    filename = f"{uuid.uuid4().hex}.webp"

    save_path = os.path.join(upload_folder, filename)

    image.save(
        save_path,
        "WEBP",
        quality=quality,
        optimize=True,
        method=6
    )

    return filename