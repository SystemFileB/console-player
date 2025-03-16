import sys, os, time, shutil, py7zr, json
from colorama import Fore, Style, Cursor, init
from concurrent.futures import ThreadPoolExecutor
from . import process_frame,pic2terminal,version

__version__=version

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tsize=shutil.get_terminal_size()
init(autoreset=True)

def clear_screen():
    print("\033c", end="")

def main():
    from tqdm import tqdm
    if len(sys.argv) < 2:
        versionstr=pic2terminal(os.path.join(path,"consoleplay","icon.png"),th=19,try_rgba=True).split("\n")
        versionstr[0]+=f"  ConsolePlay {version}"
        versionstr[1]+="  By: SystemFileB和其他贡献者们"
        versionstr[2]+="  赞助: https://afdian.com/a/systemfileb"
        versionstr[3]+="  Github: https://github.com/SystemFileB/console-player"
        versionstr[4]+="  用法: python -m consoleplay <视频路径> [-mw=<最大工作线程数>]"
        print("\n".join(versionstr))
        sys.exit(0)
    if not os.path.exists(sys.argv[1]):
        print(f"{Fore.RED}E{Style.RESET_ALL}: 视频不存在")
        sys.exit(2)
    from pygame import mixer
    mixer.init()
    max_workers = os.cpu_count()
    if len(sys.argv) > 2:
        if sys.argv[2].startswith("-mw="):
            max_workers = int(sys.argv[2][4:])
        
    cpvid=py7zr.SevenZipFile(sys.argv[1], 'r')
    print("读取所有文件...")
    files=cpvid.readall()
    manifest=json.load(files["manifest.json"])
    del files["manifest.json"]
    framesCount=manifest["frames"]
    fps=manifest["fps"]
    print(f"视频信息: 长度: {framesCount} FPS: {fps}")
    print("加载音频文件...")
    try:
        audio=os.path.join(os.path.dirname(os.path.abspath(__file__)),"audio.mp3")
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"audio.mp3"),"wb") as f:
            f.write(files["audio.mp3"].read())
            f.close()
    except:
        audio=os.path.join(os.path.expanduser("~"),"console_player.mp3")
        with open(os.path.join(os.path.expanduser("~"),"console_player.mp3"),"wb") as f:
            f.write(files["audio.mp3"].read())
            f.close()
    mixer.music.load(audio)
    del files["audio.mp3"]
    
    frames = []
    cpvid.close()
    cpvid=None
    def processor(a):
        fa=files[a]
        del files[a]
        return process_frame(fa,manifest["type"]=="cpvt",xz=manifest["xz"])
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        with tqdm(total=framesCount, unit='frame', desc="预处理所有帧", colour="green") as pbar:
            if manifest["type"]=="cpvt":
                if manifest["xz"]:
                    frame_paths = [f"frames/{i}.txt.xz" for i in range(1, framesCount + 1)]
                else:
                    frame_paths = [f"frames/{i}.txt" for i in range(1, framesCount + 1)]
            elif manifest["type"]=="cpv":
                frame_paths = [files[f"frames/{i}.jpg"] for i in range(1, framesCount + 1)]
            for result in executor.map(processor, frame_paths):
                frames.append(result)
                pbar.update(1)
    files=None
    clear_screen()
    mixer.music.play()
    
    i=0
    old_i=0
    while True:
        try:
            pos=mixer.music.get_pos()
            i=pos//(1000//fps)
            if i!=old_i:
                if pos==-1 or i>=framesCount:
                    break
                print(f"帧: {i}/{framesCount}\n"+frames[i],end="")
                if i>=3:
                    frames[i-3]=None
            old_i=i
            time.sleep(0.00001)
        except KeyboardInterrupt:
            print(Cursor.UP(tsize.lines)+Cursor.BACK(tsize.columns),end="")
            mixer.music.pause()
            if input("已暂停，回车继续，'q'退出: ")=="q":
                break
            else:
                print(Cursor.UP(tsize.lines),end="")
                mixer.music.unpause()
    frames=None
    clear_screen()
    print("清理音频文件...\n如果你在这里等待时间太久，你可以直接Ctrl+C")
    mixer.music.stop()
    mixer.quit()
    while True:
        try:
            os.remove(audio)
        except:
            time.sleep(0.1)
        else:
            break
    input("播放完毕，按下回车键退出")

if __name__ == "__main__":
    main()