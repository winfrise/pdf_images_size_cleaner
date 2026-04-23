import os
import fitz  # PyMuPDF

def is_target_image(rect: fitz.Rect, target_w: float, target_h: float, tolerance: float) -> bool:
    """
    纯函数：判断图片尺寸是否符合删除标准。
    不修改任何外部状态，仅根据输入返回布尔值。
    """
    width = rect.width
    height = rect.height
    
    # 计算范围
    min_w, max_w = target_w - tolerance, target_w + tolerance
    min_h, max_h = target_h - tolerance, target_h + tolerance
    
    # 返回判断结果
    return (min_w <= width <= max_w) and (min_h <= height <= max_h)

def remove_images_by_size(
    input_path: str, 
    output_path: str, 
    target_width: float, 
    target_height: float, 
    tolerance: float,
    skip_delete: bool
):
    """
    主处理函数：根据指定尺寸删除 PDF 中的图片。
    
    参数:
        input_path: 输入 PDF 路径
        output_path: 输出 PDF 路径
        target_width: 目标图片宽度
        target_height: 目标图片高度
        tolerance: 容差范围
        skip_delete: 是否跳过删除
    """
    # 1. 基础检查
    if not os.path.exists(input_path):
        print(f"❌ 错误：找不到文件 -> {input_path}")
        return

    try:
        doc = fitz.open(input_path)
        print(f"📄 正在处理: {input_path}")
        
        stats = {"scanned": 0, "removed": 0, "matched": 0}

        # 2. 遍历页面
        for page_index in range(len(doc)):
            page = doc[page_index]
            image_list = page.get_images(full=True)
            
            if not image_list:
                continue

            print(f" - 扫描第 {page_index + 1} 页，发现 {len(image_list)} 张图片...")

            # 3. 遍历图片
            for img_index in range(len(image_list)):
                img = image_list[img_index]
                xref = img[0]
                stats["scanned"] += 1
                
                try:
                    rect = page.get_image_bbox(img)
                except Exception:
                    continue

                # 打印图片信息
                print(f"    |- {page_index}-{img_index} [图片信息] ((宽:{rect.width:.1f}, 高:{rect.height:.1f}))")

                # 4. 函数式判断逻辑
                # 调用纯函数进行判断，保持主流程清晰
                if is_target_image(rect, target_width, target_height, tolerance):
                    stats["matched"] += 1
                    print(f"   [匹配图片] (宽:{rect.width:.1f}, 高:{rect.height:.1f})")
                    
                    if not skip_delete:
                        page.delete_image(xref)
                        stats["removed"] += 1
                        print(f"    [删除图片] (宽:{rect.width:.1f}, 高:{rect.height:.1f})")

        # 5. 保存
        doc.save(output_path)
        doc.close()
        
        print("-" * 30)
        print(f"✅ 完成！扫描: {stats['scanned']},匹配:{stats['matched']},删除: {stats['removed']}")
        print(f"💾 保存至: {output_path}")

    except Exception as e:
        print(f"❌ 发生错误: {e}")

# ================== 主程序入口 ==================
if __name__ == "__main__":
    # 配置参数 (直接定义变量，而非类)
    INPUT_FILE = "/Users/teacher/Desktop/demo2/000.pdf"
    OUTPUT_FILE = "/Users/teacher/Desktop/demo2/000-1.pdf"
    TARGET_WIDTH = 75
    TARGET_HEIGHT = 36
    TOLERANCE = 4
    SKIP_DELETE = False
    
    # 调用函数并传入参数
    remove_images_by_size(
        input_path=INPUT_FILE,
        output_path=OUTPUT_FILE,
        target_width=TARGET_WIDTH,
        target_height=TARGET_HEIGHT,
        tolerance=TOLERANCE,
        skip_delete = SKIP_DELETE
    )