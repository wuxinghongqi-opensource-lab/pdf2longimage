# -*- coding: utf-8 -*-
import sys
from pathlib import Path
import datetime
import random
import shutil
import argparse

import fitz  # PyMuPDF
from PIL import Image
from tqdm import tqdm


def gen_random_tmp_path(path_str_len: int = 16) -> str:
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result_list = ["tmp_"]  # 直接生成列表
    result_list.extend(random.choice(seed) for _ in range(path_str_len))
    return "".join(result_list)


def convert_pdf_to_images(pdf_path: str, images_path: str) -> int:
    try:
        pdf_doc = fitz.open(pdf_path)
        images_amount = pdf_doc.page_count  # 使用 page_count 替代 pageCount
        print("Converting PDF to images...")
        images_dir = Path(images_path)
        images_dir.mkdir(parents=True, exist_ok=True)  # 使用 pathlib 创建目录

        with tqdm(total=images_amount) as pbar:
            for image_id in range(images_amount):
                page = pdf_doc[image_id]
                rotate = 0
                # 使用放大缩放系数生成更高分辨率的图像
                zoom = 4  # 使用统一的 zoom 变量
                mat = fitz.Matrix(zoom, zoom, rotate)  # 直接传递旋转角度
                pix = page.get_pixmap(matrix=mat, alpha=False)  # 使用 get_pixmap 替代 getPixmap
                image_path = images_dir / f"images_{image_id}.png"
                pix.save(image_path)
                pbar.update(1)
        return images_amount
    except Exception as exc:
        print(f"Error while converting PDF to images: {exc}")
        return -1


def merge_images_as_long_image(images_path: str, images_amount: int, long_image_path: str) -> bool:
    try:
        long_image = None
        each_tmp_image_size = None
        print(f"Merging {images_amount} images into one long image...")
        images_dir = Path(images_path)
        with tqdm(total=images_amount) as pbar:
            for image_id in range(images_amount):
                image_path = images_dir / f"images_{image_id}.png"
                tmp_image = Image.open(image_path)
                if long_image is None:
                    each_tmp_image_size = tmp_image.size
                    long_image = Image.new(
                        "RGB", (each_tmp_image_size[0], images_amount * each_tmp_image_size[1]), (250, 250, 250))
                long_image.paste(tmp_image, (0, image_id * each_tmp_image_size[1]))
                pbar.update(1)
        long_image.save(long_image_path, "JPEG")  # 保存为 JPEG
    except Exception as exc:
        print(f"Error while merging images: {exc}")
        return False
    return True


def clean_tmp_images(images_path: str) -> bool:
    try:
        shutil.rmtree(images_path)  # 删除临时图片目录
    except Exception as exc:
        print(f"Error while cleaning up images: {exc}")
        return False
    return True


def convert_pdf_to_long_image(pdf_path: str, long_image_path: str = None, images_path: str = None) -> bool:
    if images_path is None:
        images_path = gen_random_tmp_path()
    if long_image_path is None:
        long_image_path = pdf_path.replace(".PDF", ".jpg").replace(".pdf", ".jpg")

    images_amount = convert_pdf_to_images(pdf_path, images_path)
    if images_amount <= 0:
        return False

    if not merge_images_as_long_image(images_path, images_amount, long_image_path):
        return False

    if not clean_tmp_images(images_path):
        return False

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF to Long Image.")
    parser.add_argument("--pdf_path", help="The path of the PDF to convert", type=str, required=True)
    parser.add_argument("--long_image_path", help="The output path for the long image", type=str, default=None)
    parser.add_argument("--tmp_images_path", help="Temporary images storage path", type=str, default=None)

    args = parser.parse_args()
    success = convert_pdf_to_long_image(args.pdf_path, args.long_image_path, args.tmp_images_path)

    if success:
        print("PDF successfully converted to long image.")
    else:
        print("Failed to convert PDF to long image.")
