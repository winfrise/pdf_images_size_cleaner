import fitz  # PyMuPDF
import os

def remove_small_images_from_pdf(input_pdf, output_pdf, min_width=50, min_height=50, max_width=60, max_height=50):
    """
    批量删除PDF中尺寸较小的图片
    :param input_pdf: 输入PDF文件路径
    :param output_pdf: 输出PDF文件路径
    :param min_width: 图片的最小宽度（像素）
    :param min_height: 图片的最小高度（像素）
    :param max_width: 图片的最大宽度（像素）
    :param max_height: 图片的最大高度（像素）
    """
    try:
        # 1. 打开PDF文档
        doc = fitz.open(input_pdf)
        print(f"📄 正在处理文件: {input_pdf}")
        
        total_removed = 0

        # 2. 遍历每一页
        for page_index in range(len(doc)):
            page = doc[page_index]
            # 获取当前页面的图片列表 (full=True 获取详细信息)
            image_list = page.get_images(full=True)
            
            # 注意：必须倒序遍历，因为删除图片会改变索引位置
            # 但 PyMuPDF 的删除机制是基于 XREF 的，所以正序遍历也可以，只要标记正确
            # 为了稳妥，我们直接操作底层 xref
            
            if not image_list:
                continue

            print(f"   - 第 {page_index + 1} 页发现 {len(image_list)} 张图片，正在扫描...")

            for img in image_list:
                xref = img[0]  # 图片的 xref ID
                
                # 获取图片在页面中的矩形区域 (bbox)
                # PyMuPDF 1.19.0+ 版本推荐使用 get_image_bbox
                try:
                    rect = page.get_image_bbox(img)
                except:
                    # 兼容旧版本或特殊情况
                    rect = fitz.Rect() 
                
                # --- 核心修复逻辑 ---
                # rect 包含 (x0, y0, x1, y1)
                # 我们需要计算宽和高
                width = rect.width
                height = rect.height

                #打印图片宽高
                print(f"[图片信息] (宽:{rect.width:.1f}, 高:{rect.height:.1f}, x: {round(rect.x0)}, y: {round(rect.y0)}, x1: {round(rect.x1)}, y1: {round(rect.y1)})")


                if width < max_width and height < max_height and width > min_width and height > min_height:
                    # 从页面中删除该图片
                    page.delete_image(xref)
                    total_removed += 1
                    print(f"      [删除] 发现小图 (宽:{width:.1f}, 高:{height:.1f})，已移除。")

        # 3. 保存新文件
        doc.save(output_pdf)
        doc.close()
        print(f"✅ 处理完成！共删除 {total_removed} 张图片。")
        print(f"💾 文件已保存至: {output_pdf}")

    except Exception as e:
        print(f"❌ 发生错误: {e}")

# ================== 主程序入口 ==================
if __name__ == "__main__":
    # 设置输入输出路径
    # 请确保路径正确，或者将 pdf 文件放在与脚本同级目录下
    # input_file = "one.pdf"  # 你的输入文件名
    # output_file = "one_cleaned.pdf" # 输出文件名

    input_file = "/Users/teacher/Desktop/example_edit/split/one.pdf"       
    output_file = "/Users/teacher/Desktop/example_edit/split/cleaned_example.pdf"
    min_width=300
    min_height=40
    max_width=420
    max_height=70
    
    
    # 检查文件是否存在
    if not os.path.exists(input_file):
        print(f"❌ 找不到文件: {input_file}")
        print("请将你的 PDF 文件重命名为 'one.pdf' 并放在脚本同级目录下。")
    else:
        # 运行函数
        # 参数说明：min_width=60 表示宽度小于 60 像素的图都会被删掉
        remove_small_images_from_pdf(input_file, output_file, min_width, min_height, max_width, max_height)


