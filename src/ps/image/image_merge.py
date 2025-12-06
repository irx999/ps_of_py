# merge_images.py
import os
import shutil

from PIL import Image


def merge_images(input_folder, output_path=None, archive_folder=None, width=800):
    assert os.path.isdir(input_folder), f"❌ 错误：路径不存在 - {input_folder}"

    extensions = (".png", ".jpg", ".jpeg")
    image_files = [
        f for f in sorted(os.listdir(input_folder)) if f.lower().endswith(extensions)
    ]

    assert image_files, "没有找到图片文件。"

    print(f"✅ 找到 {len(image_files)} 张图片，正在拼接...")

    image_width, image_height = width, width
    total_height = image_height * len(image_files)
    long_image = Image.new("RGB", (image_width, total_height), color="white")

    for i, filename in enumerate(image_files):
        img_path = os.path.join(input_folder, filename)
        try:
            img = Image.open(img_path).convert("RGB")
            if img.size != (image_width, image_height):
                print(
                    f"⚠️ 警告：{filename} 尺寸不是 {image_width}x{image_width}，已自动调整。"
                )
                img = img.resize((image_width, image_height), Image.LANCZOS)  # type: ignore
            long_image.paste(img, (0, i * image_height))
        except Exception as e:
            print(f"❌ 跳过无效图片 {filename}: {e}")

    if output_path is None:
        output_path = os.path.join(input_folder, "output_long_image.jpg")

    long_image.save(output_path, quality=95)
    print(f"\n🎉 拼接完成！长图已保存为: {output_path}")

    # 如果指定了归档文件夹，则移动原始图片和拼接后的图片到该文件夹
    if archive_folder:
        if not os.path.exists(archive_folder):
            os.makedirs(archive_folder)

        # 移动原始图片
        for filename in image_files:
            source_path = os.path.join(input_folder, filename)
            dest_path = os.path.join(archive_folder, filename)
            shutil.move(source_path, dest_path)
            print(f"📁 原始图片已移动到: {dest_path}")

        # 移动拼接后的图片
        output_filename = os.path.basename(output_path)
        final_output_path = os.path.join(archive_folder, output_filename)
        shutil.move(output_path, final_output_path)
        print(f"📁 拼接图片已移动到: {final_output_path}")

        return final_output_path

    return True


if __name__ == "__main__":
    input_folder = "./test/test_export"
    output_path = "./test/merge.png"
    archive_folder = "./test/测试用"
    merge_images(input_folder, output_path, archive_folder, width=750)
