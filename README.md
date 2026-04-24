# 基于Python+pynupdf实现的批量删除图片

> 可结合WondersharePdfElement查看图片的大小

1. 创建虚拟环境：

```python3 -m venv venv```

2. 激活虚拟环境：

```source venv/bin/activate```

3. 安装依赖库

```pip install pymupdf```

4. 运行脚本

```python main_size_by_box.py```

```python main_size_by_info.py```

```python main_draw_rect.py```

```python main_img_watermark.py```


1. 需要改进的地方
```python
TARGET_SIZES = [
    (1182, 175), # 第一种目标尺寸
    (189, 66),   # 第二种目标尺寸
]

def is_target_size(width, height, targets, tolerance):
    """
    判断给定的宽高是否匹配目标尺寸列表中的任意一个（包含容差）
    """
    for t_w, t_h in targets:
        # 计算宽高的差值绝对值
        w_diff = abs(width - t_w)
        h_diff = abs(height - t_h)
        
        # 如果宽高差值都在容差范围内，则视为匹配
        if w_diff <= tolerance and h_diff <= tolerance:
            return True
    return False
```

2. 白色遮挡的实现
```page.draw_rect()```或```page.add_rect_annot()```