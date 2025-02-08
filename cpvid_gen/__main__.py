import sys, os, stat, curses, asyncio, tqdm
cli=False
try:
    import easygui
except:
    cli=True
if os.environ.get("CP_CLI"):
    cli=True

async def main():
    # 定义变量
    if len(sys.argv) == 3:
        inputVideo = sys.argv[1]
        outputCPVid = sys.argv[2]
    else:
        inputVideo = ""
        outputCPVid = ""
    path = os.path.dirname(os.path.abspath(__file__))
    mode=False
    h=480
    fps=20
    try:
        temp = os.path.join(path, "temp")
        if not os.path.exists(temp):
            os.makedirs(temp, exist_ok=True)
    except:
        if os.name == "nt":
            temp = os.path.join(os.path.expanduser("~"), "AppData", "Local", "SystemFileB", "cpvid_generator")
            if not os.path.exists(temp):
                os.makedirs(temp, exist_ok=True)
        else:
            temp = os.path.join(os.path.expanduser("~"), ".SystemFileB", "cpvid_generator")
            if not os.path.exists(temp):
                os.makedirs(temp, exist_ok=True)

    if inputVideo == "" or outputCPVid == "":
        if cli:
            inputVideo = input("输入视频路径：")
            outputCPVid = input("输入cpvid文件保存路径：")
            if not (inputVideo and outputCPVid):
                print("输入不能为空")
                return 1
            

        else:
            inputVideo = easygui.fileopenbox("请选择视频文件", "选择视频文件", filetypes=["*.mp4", "*.avi", "*.mkv", "*.flv", "*.mov", "*.wmv", "*.webm", "*.ts", "*.m3u8", "*.m3u", "*.*"],default="*.mp4")
            if not inputVideo:
                return 0
            outputCPVid = easygui.filesavebox("请选择cpvid文件保存路径", "选择cpvid文件保存路径", filetypes=["*.cpvid","*.zip","*.*"], default="output.cpvid")
            if not outputCPVid:
                return 0
    if cli:
        if input("是否生成Minecraft数据包文件? (y/N):")=="y":
                mode=True
                h=64
        inp=input("视频高度({})".format(h))
        if inp:
            try:
                h=int(inp)
            except:
                print("输入错误")
                return 1
        inp=input("视频帧率({})".format(fps))
        if inp:
            try:
                fps=int(inp)
            except:
                print("输入错误")
                return 1
    else:
        if easygui.ynbox("是否生成Minecraft数据包文件?"):
                mode=True
                h=64
        inp=easygui.enterbox("视频高度({})".format(h))
        if inp:
            try:
                h=int(inp)
            except:
                easygui.msgbox("输入错误")
                return 1
        inp=easygui.enterbox("视频帧率({})".format(fps))
        if inp:
            try:
                fps=int(inp)
            except:
                easygui.msgbox("输入错误")
                return 1
    if os.path.exists(outputCPVid):
        if cli:
            if input("文件已存在，是否覆盖并继续? (y/N):")=="y":
                os.remove(outputCPVid)
            else:
                return 0
        else:
            if easygui.ynbox("文件已存在，是否覆盖并继续?"):
                os.remove(outputCPVid)
            else:
                return 0
    from .gen import gen
    await gen(inputVideo, outputCPVid, mode, h, fps, temp)
    easygui.msgbox("完成","cpvid生成器")
    return 0

sys.exit(asyncio.run(main()))