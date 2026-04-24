import fitz  # PyMuPDF
import os


# ==========================================
# 2. 核心逻辑：函数式编程风格
# ==========================================


def process_page(page, img_bytes, rect):
    """
    纯函数：在指定页面上插入图片
    副作用: 修改 page 对象
    """
    # insert_image 返回一个 xref，如果为 0 则失败，否则成功
    page.insert_image(
        rect, 
        stream=img_bytes, 
        keep_proportion=False  # <--- 关键：强制拉伸，不保持原图比例
    )

def add_watermarks_pipeline(input_path, output_path, img_path, watermark_configs, start_page, end_page):

    try:
        # 1. 打开 PDF
        doc = fitz.open(input_path)
        
        # 如果未指定结束页，默认为最后一页
        if end_page is None:
            end_page = len(doc)

        # 2. 读取图片二进制数据
        if not os.path.exists(img_path):
            print(f"错误：图片文件不存在 -> {img_path}")
            return
            
        with open(img_path, "rb") as f:
            img_bytes = f.read()

        # 3. 遍历所有页面 (函数式映射思想)
        for page_num in range(len(doc)):
            print(f"正在处理第 {page_num} 页")
            page = doc[page_num]
            
            # 对当前页面应用所有配置的水印
            for config in watermark_configs:
                # 检查页面范围 (start <= current <= end)                
                if start_page <= page_num <= end_page:
                    rect = fitz.Rect(
                        config["x"], 
                        config["y"], 
                        config["x"] + config["width"], 
                        config["y"] + config["height"]
                    )
                    # 执行绘制
                    process_page(page, img_bytes, rect)

        # 4. 保存文件
        doc.save(output_path)
        doc.close()
        print(f"✅ 成功：文件已保存至 {output_path}")

    except Exception as e:
        print(f"❌ 发生错误: {e}")

# ==========================================
# 3. 执行配置
# ==========================================

if __name__ == "__main__":
    # --- 用户配置区 ---
    INPUT_PDF = "/Users/teacher/Desktop/demo2/000.pdf"         # 输入PDF路径
    OUTPUT_PDF = "/Users/teacher/Desktop/demo2/000-333.pdf" # 输出PDF路径
    IMAGE_FILE = "/Users/teacher/Downloads/调整图片角度.png"      # 水印图片路径

    # 页面范围
    START_PAGE = 0
    END_PAGE = None # None 代表直到最后

    # 定义多个水印配置 (x, y, width, height 单位像素)
    configs = [
        {
            "x": 244, "y": 127, "width": 65, "height": 37, # 你提供的尺寸
        },
        {
            "x": 343, "y": 85, "width": 97, "height": 20, # 你提供的尺寸
        },
        {
            "x": 259, "y": 775, "width": 67, "height": 25, # 你提供的尺寸
        },
    ]

    # 运行主程序
    add_watermarks_pipeline(INPUT_PDF, OUTPUT_PDF, IMAGE_FILE, configs, START_PAGE, END_PAGE)