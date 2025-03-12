import shutil
from colorama import Style,Cursor,init
from PIL import Image
tsize=shutil.get_terminal_size()
init()
def RGB(r, g, b):
    return f"\033[48;2;{r};{g};{b}m"
def pic2terminal(frame, lore=False,cursor_move=False,th=None):
    """将图片转化为终端可显示的字符串，只支持RGB而不支持带透明度的图片
    ### 参数
    - frame: 图片路径，可以是Pillow支持的任何格式
    - lore: 是否在移动光标的时候往上多移动一行
    - cursor_move: 是否移动光标
    - th: 生成的图片高度，如果没有指定就按照终端高度生成
    ### 用法
    ```python
    import consoleplay as cp
    cp.pic2terminal("test.jpg")
    ```
    这里仅包含了一般图片的转化，理论上io.BytesIO和bytes格式也可以"""
    img = Image.open(frame)
    
    # 将图像转换为 RGB 模式
    img = img.convert('RGB')
    
    # 获取图像的宽度和高度
    width, height = img.size
    if not th:
        tw, th = tsize
    else:
        tw=tsize.columns
    tw/=2
    th-=3
    if tw<th:
        ratio = tw/width
    else:
        ratio = th/height
    width = int(width*ratio)
    height = int(height*ratio)
    img = img.resize((width, height),Image.Resampling.NEAREST)
    print_str = ""
    # 遍历图像的每一个像素
    for y in range(height):
        for x in range(width):
            # 获取像素的 RGB 值
            r, g, b = img.getpixel((x, y))
            # 输出带有背景颜色的空格
            print_str+=RGB(r, g, b) + "  "+Style.RESET_ALL
        print_str+="\n"
    if not cursor_move:
        return print_str
    if lore:
        return print_str+Cursor.UP(height+1)+Cursor.BACK(width*2)
    else:
        return print_str+Cursor.UP(height)+Cursor.BACK(width*2)

def process_frame(frame_path,text=False,th=None):
    if text:
        return frame_path.read().decode("utf-8")
    else:
        return pic2terminal(frame_path, True, True,th)