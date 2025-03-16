import consoleplay as cp,sys,os
__version__=cp.version
def main():
    if len(sys.argv)>1:
        print(cp.pic2terminal(sys.argv[1]),try_rgba=True)
    else:
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        versionstr=cp.pic2terminal(os.path.join(path,"consoleplay","icon.png"),th=19,try_rgba=True).split("\n")
        versionstr[0]+=f"  ConsolePlay {cp.version}"
        versionstr[1]+="  By: SystemFileB和其他贡献者们"
        versionstr[2]+="  赞助: https://afdian.com/a/systemfileb"
        versionstr[3]+="  Github: https://github.com/SystemFileB/console-player"
        versionstr[4]+="  用法: python -m consolepic <图片路径>"
        print("\n".join(versionstr))
if __name__=="__main__":
    main()