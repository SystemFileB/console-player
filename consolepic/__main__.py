import consoleplay as cp,sys
def main():
    if len(sys.argv)>1:
        print(cp.pic2terminal(sys.argv[1]))
    else:
        print("用法：consolepic <图片路径>")
if __name__=="__main__":
    main()