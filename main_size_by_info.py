import fitz  # PyMuPDF
import os
from typing import Dict, Tuple

# ==========================================
# ⚙️ 配置区域 (Configuration)
# ==========================================
# 目标图片的尺寸（像素）
TARGET_WIDTH = 1182
TARGET_HEIGHT = 175

# 容差范围（像素），用于处理尺寸微小偏差
TOLERANCE = 1

SKIP_DELETE = False

# 输入输出路径配置
INPUT_PDF_PATH = "/Users/teacher/Desktop/demo/001.pdf"
OUTPUT_PDF_PATH = "/Users/teacher/Desktop/demo/000-1.pdf"


# 判断图片是否满足删除条件。
def should_remove_image(
    img_info: Dict, 
    target_width: float,
    target_height: float, 
    tolerance: int,
) -> bool:
    width, height = img_info['width'], img_info['height']
    # width = img_info.get("width", 0)
    # height = img_info.get("height", 0)
    
    # 计算边界
    min_w, max_w = target_width - tolerance, target_width + tolerance
    min_h, max_h = target_height - tolerance, target_height + tolerance
    
    # 判断是否落在指定范围内
    is_width_match = min_w < width < max_w
    is_height_match = min_h < height < max_h
    
    return is_width_match and is_height_match

# 打开PDF，遍历页面，移除符合特定尺寸的图片。
def process_pdf_images(input_path: str, output_path: str, ) -> None:
    try:
        # 1. 打开文档
        doc = fitz.open(input_path)
        print(f"📄 正在处理文件: {input_path}")
        
        total_scanned = 0
        total_removed = 0
        total_matched = 0

        # 2. 遍历每一页
        for page_index in range(len(doc)):
            page = doc[page_index]
            # 获取页面所有图片信息
            image_list = page.get_image_info(xrefs=True)
            
            print(f"--- 正在扫描第 {page_index + 1} 页，发现 {len(image_list)} 个图像对象 ---")

            for img_index in range(len(image_list)):
                img = image_list[img_index]

                total_scanned += 1

                # 打印图片信息
                print(f"    |- {page_index}-{img_index} [图片真实宽高] ((宽:{img['width']:.1f}, 高:{img['height']:.1f}))")

                # 显示的宽高信息
                # rect = img['bbox'] 
                # display_width = rect[2] - rect[0]
                # display_height = rect[3] - rect[1]
                # print(f"    |- {page_index}-{img_index} [图片显示宽高] ((宽:{display_width:.1f}, 高:{display_height:.1f}))")


                # 调用函数式逻辑判断是否需要删除
                if should_remove_image(img, TARGET_WIDTH, TARGET_HEIGHT, TOLERANCE):
                    total_matched += 1
                    print(f"   [匹配图片] (宽:{img['width']:.1f}, 高:{img['height']:.1f})")
                    if not SKIP_DELETE:
                        # 执行删除操作
                        page.delete_image(img["xref"])
                        total_removed += 1
                    
                    print(f"✅ [移除] 发现目标图片 (宽:{img['width']}, 高:{img['height']})")

        # 3. 保存结果
        if not SKIP_DELETE:
            doc.save(output_path)
            print(f"💾 文件已保存至: {output_path}")

        doc.close()
        
        print("-" * 30)
        print(f"🎉 共扫描图片{total_scanned}")
        print(f"🔍 共匹配到: {total_matched} 张")
        print(f"🗑️  共成功删除: {total_removed} 张")

    except Exception as e:
        print(f"❌ 发生严重错误: {e}")


# ==========================================
# 🏁 程序入口
# ==========================================
if __name__ == "__main__":
    # 检查文件是否存在
    if not os.path.exists(INPUT_PDF_PATH):
        print(f"❌ 错误: 找不到文件 -> {INPUT_PDF_PATH}")
        print("请检查路径配置是否正确。")
    else:
        process_pdf_images(INPUT_PDF_PATH, OUTPUT_PDF_PATH)