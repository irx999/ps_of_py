# merge_images.py
import os

from loguru import logger
from PIL import Image

logger.add("./logs/Merge_images.log", rotation="1 MB")


def merge_images(
    input_folder,
    merge_image_list,
    output_path,
    width=750,
):
    """合并图片

    param input_folder: 输入文件夹路径
    param merge_image_list: 合并图片列表
    param width: 合并图片宽度
    """
    assert os.path.isdir(input_folder), f"❌ 错误：路径不存在 - {input_folder}"

    image_files = merge_image_list

    assert image_files, "没有找到图片文件。"

    logger.info(f"✅ 找到 {len(image_files)} 张图片，正在拼接...")

    image_width, image_height = width, width
    total_height = image_height * len(image_files)
    long_image = Image.new("RGB", (image_width, total_height), color="white")

    for i, filename in enumerate(image_files):
        img_path = os.path.join(input_folder, filename)
        try:
            img = Image.open(img_path).convert("RGB")
            if img.size != (image_width, image_height):
                logger.info(
                    f"⚠️ 警告：{filename} 尺寸不是 {image_width}x{image_width}，已自动调整。"
                )
                img = img.resize((image_width, image_height), Image.LANCZOS)  # type: ignore
            long_image.paste(img, (0, i * image_height))
        except Exception as e:
            logger.info(f"❌ 跳过无效图片 {filename}: {e}")

    if output_path is None:
        output_path = os.path.join(input_folder, "output_long_image.jpg")
    else:
        output_path = os.path.join(input_folder, output_path)

    long_image.save(output_path, quality=95)
    logger.info(f"\n🎉 拼接完成！长图已保存为: {output_path}")

    # # 如果指定了归档文件夹，则移动原始图片和拼接后的图片到该文件夹
    # if archive_folder:
    #     if not os.path.exists(archive_folder):
    #         os.makedirs(archive_folder)

    #     # 移动原始图片
    #     for filename in image_files:
    #         source_path = os.path.join(input_folder, filename)
    #         dest_path = os.path.join(archive_folder, filename)
    #         shutil.move(source_path, dest_path)
    #         logger.info(f"📁 原始图片已移动到: {dest_path}")

    #     # 移动拼接后的图片
    #     output_filename = os.path.basename(output_path)
    #     final_output_path = os.path.join(archive_folder, output_filename)
    #     shutil.move(output_path, final_output_path)
    #     logger.info(f"📁 拼接图片已移动到: {final_output_path}")

    #     return final_output_path

    # return True


if __name__ == "__main__":
    pass
