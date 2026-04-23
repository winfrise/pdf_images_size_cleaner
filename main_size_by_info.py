import fitz  # PyMuPDF
import os

def remove_small_images_from_pdf(input_pdf, output_pdf):
    try:
        # 1. 打开PDF文档
        doc = fitz.open(input_pdf)
        print(f"📄 正在处理文件: {input_pdf}")
        
        total_removed = 0
        total_found = 0

        # 2. 遍历每一页
        for page_index in range(len(doc)):
            page = doc[page_index]


            #图片宽度（像素）
            pic_width = 1182
            #图片高度（像素）
            pic_height = 175
            #宽度容差
            width_delta = 1
            #高度容差
            height_delta = 1
            #是否跳过删除图片
            skip = False 

            
            min_width= pic_width - width_delta #图片的最小宽度（像素）
            min_height= pic_height - height_delta #图片的最小高度（像素）
            max_width= pic_width + width_delta #图片的最大宽度（像素）
            max_height= pic_height + height_delta #图片的最大高度（像素）



            print(f"【第{page_index}页】")
            # 获取页面所有图片信息
            image_list = page.get_image_info(xrefs=True)

            for img in image_list:
                width = img['width']
                height = img['height']
                # 图片的原始像素宽高
                print(f"图片原始像素宽: {img['width']}, 图片原始像素高: {img['height']}")
                
                if width < max_width and height < max_height and width > min_width and height > min_height:
                    total_found += 1
                    print(f"[发现图片] (宽:{width:.1f}, 高:{height:.1f})，已移除。")
                    if not skip:
                        # 从页面中删除该图片
                        page.delete_image(img)
                        total_removed += 1
                        print(f"      [删除图片] (宽:{width:.1f}, 高:{height:.1f})，已移除。")

        # 3. 保存新文件
        doc.save(output_pdf)
        doc.close()
        print(f"✅ 共匹配到 {total_removed} 张图片。")
        print(f"✅ 共删除了 {total_removed} 张图片。")
        print(f"💾 文件已保存至: {output_pdf}")

    except Exception as e:
        print(f"❌ 发生错误: {e}")

# ================== 主程序入口 ==================
if __name__ == "__main__":
    # 设置输入输出路径
    # 请确保路径正确，或者将 pdf 文件放在与脚本同级目录下
    # input_file = "one.pdf"  # 你的输入文件名
    # output_file = "one_cleaned.pdf" # 输出文件名

    input_file = "/Users/teacher/Desktop/demo/000-2.pdf"       
    output_file = "/Users/teacher/Desktop/demo/000-3.pdf"
    
    
    # 检查文件是否存在
    if not os.path.exists(input_file):
        print(f"❌ 找不到文件: {input_file}")
        print("请将你的 PDF 文件重命名为 'one.pdf' 并放在脚本同级目录下。")
    else:
        # 运行函数
        # 参数说明：min_width=60 表示宽度小于 60 像素的图都会被删掉
        remove_small_images_from_pdf(input_file, output_file)


