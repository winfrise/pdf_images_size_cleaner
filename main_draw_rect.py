import fitz  # PyMuPDF
from typing import List, Dict, Tuple, Optional

# ==========================================
# 1. 数据模型与工具函数 (纯函数)
# ==========================================

def create_rect_params(x: float, y: float, width: float, height: float, 
                       fill_color: Tuple[float, float, float], 
                       border_color: Optional[Tuple[float, float, float]] = (0, 0, 0), 
                       border_width: float = 1.0, 
                       opacity: float = 1.0) -> Dict:
    """
    工厂函数：创建一个矩形配置字典
    颜色格式为 RGB (0-1 之间的小数)，例如 (1, 0, 0) 为红色
    """
    return {
        "rect": fitz.Rect(x, y, x + width, y + height),
        "fill": fill_color,
        "color": border_color,
        "width": border_width,
        "overlay": True, # 绘制在内容之上
        "opacity": opacity
    }

def draw_single_rectangle_on_page(page: fitz.Page, rect_params: Dict) -> None:
    """
    纯函数：在单个页面上绘制一个矩形
    """
    page.draw_rect(
        rect=rect_params["rect"],
        color=rect_params["color"],
        fill=rect_params["fill"],
        width=rect_params["width"],
        overlay=rect_params["overlay"]
    )

def draw_multiple_rectangles_on_page(page: fitz.Page, rectangles: List[Dict]) -> None:
    """
    高阶函数/组合函数：在单个页面上绘制多个矩形
    使用 map 进行函数式遍历
    """
    # 将绘图函数映射到矩形列表上
    list(map(lambda r: draw_single_rectangle_on_page(page, r), rectangles))

# ==========================================
# 2. 核心业务流程函数
# ==========================================

def process_pdf_rectangles(input_path: str, 
                           output_path: str, 
                           rectangles: List[Dict], 
                           start_page: int = 0, 
                           end_page: Optional[int] = None) -> str:
    """
    主处理函数：
    1. 打开文档
    2. 确定页面范围
    3. 遍历页面并应用绘图逻辑
    4. 保存文档
    """
    # 打开 PDF
    doc = fitz.open(input_path)
    
    # 计算页面范围 (处理 None 的情况)
    total_pages = len(doc)
    p_start = max(0, start_page)
    p_end = total_pages if end_page is None else min(end_page, total_pages)
    
    print(f"正在处理: {input_path} ...")
    print(f"页面范围: {p_start + 1} 到 {p_end} (共 {total_pages} 页)")
    
    # 遍历指定页面
    # 使用 range 生成页面索引列表
    page_indices = range(p_start, p_end)
    
    for i in page_indices:
        page = doc[i]
        # 调用绘图逻辑
        draw_multiple_rectangles_on_page(page, rectangles)
        
    # 保存结果
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()
    
    return output_path

# ==========================================
# 3. 执行入口 (配置与调用)
# ==========================================

if __name__ == "__main__":
    # --- 配置区域 ---
    INPUT_PDF = "/Users/teacher/Desktop/demo2/000.pdf"  
    OUTPUT_PDF = "/Users/teacher/Desktop/demo2/000-222.pdf"
    
    # 定义要绘制的多个不同长方形
    # 这里演示：一个半透明红色块，一个实心白色块（用于遮盖），一个蓝色线框
    RECT_ANGLES_EXAMPLE = [
        create_rect_params(
            x=50, y=50, width=200, height=100, 
            fill_color=(1, 0, 0),    # 红色填充
            opacity=0.3              # 30% 不透明度
        ),
        create_rect_params(
            x=100, y=200, width=150, height=50, 
            fill_color=(1, 1, 1),    # 白色填充
            border_color=None,       # 无边框
            opacity=1.0              # 完全不透明，用于遮盖水印
        ),
        create_rect_params(
            x=300, y=100, width=100, height=100, 
            fill_color=None,         # 无填充
            border_color=(0, 0, 1),  # 蓝色边框
            border_width=2.0
        )
    ]

    MY_RECT_ANGLES = [
        create_rect_params(
            x=239, y=81, width=100, height=40, 
            fill_color=(1, 1, 1),    # 白色填充
            border_color=None,       # 无边框
            opacity=1.0              # 完全不透明，用于遮盖水印
        )
    ]
    
    # --- 执行 ---
    try:
        # 示例：在第 1 页到第 5 页绘制
        process_pdf_rectangles(
            input_path=INPUT_PDF,
            output_path=OUTPUT_PDF,
            rectangles=MY_RECT_ANGLES,
            start_page=0,      # 第1页 (索引从0开始)
            end_page=5         # 第5页
        )
        print("✅ 绘制完成！")
    except Exception as e:
        print(f"❌ 发生错误: {e}")