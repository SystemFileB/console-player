import ffmpeg
import sys, os, asyncio, shutil
from PIL import Image
from colorama import Fore, Style, init, Cursor

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
init(autoreset=True)

def RGB(r, g, b):
    return f"\033[48;2;{r};{g};{b}m"

async def vid_show(frame):
    frame=frame.replace(b"\x00", b"")
    # 使用 Pillow 打开字节数组作为图像
    img = Image.open(frame)
    
    # 将图像转换为 RGB 模式
    img = img.convert('RGB')
    
    # 获取图像的宽度和高度
    width, height = img.size
    tw, th = shutil.get_terminal_size()
    if width>height:
        ratio = tw/width
    else:
        ratio = th/height
    width = int(width*ratio)
    height = int(height*ratio)
    img = img.resize((width, height))
    
    print_str = ""
    # 遍历图像的每一个像素
    for y in range(height):
        for x in range(width):
            # 获取像素的 RGB 值
            r, g, b = img.getpixel((x, y))
            # 输出带有背景颜色的空格
            print_str+=RGB(r, g, b) + "  "+Style.RESET_ALL
        print_str+="\n"
    print(print_str+Cursor.UP(height)+Cursor.BACK(width))
    await asyncio.sleep(0.1)

async def main():
    if len(sys.argv) < 2:
        print("用法: python __main__.py <视频路径>")
        sys.exit(1)
    if not os.path.exists(sys.argv[1]):
        print(f"{Fore.RED}E{Style.RESET_ALL}: 视频不存在")
        sys.exit(2)

    # 获取视频的帧率
    probe = ffmpeg.probe(sys.argv[1])
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    if video_stream is None:
        print(f"{Fore.RED}E{Style.RESET_ALL}: 无法获取视频流信息")
        sys.exit(3)
    fps = video_stream['avg_frame_rate']

    # 使用FFmpeg处理视频，输出每一帧到管道
    video = (
        ffmpeg
        .input(sys.argv[1])
        .output('pipe:', format='rawvideo', pix_fmt='rgb24', vf=f'fps={fps}')
        .run_async(pipe_stdout=True)
    )

    # 异步读取每一帧并传递给vid_show函数
    while True:
        in_bytes = video.stdout.read(1024 * 1024)
        if not in_bytes:
            break
        await vid_show(in_bytes)

def run():
    asyncio.run(main())

if __name__ == "__main__":
    run()