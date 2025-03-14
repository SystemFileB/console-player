import subprocess as sp, os, shutil, py7zr, asyncio, json
from colorama import Cursor,init
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from consoleplay import process_frame

async def rm(temp):
    files = [os.path.join(temp, filename) for filename in os.listdir(temp)]
    if files:
        with tqdm(total=len(files), unit='file', desc="删除文件", colour="green") as pbar:
            for file_path in files:
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                    pbar.update(1)
                except Exception as e:
                    print(f'无法删除{file_path} {e}')

async def compress_directory(directory_path, output_path):
    total_files = sum([len(files) for _, _, files in os.walk(directory_path)])
    with py7zr.SevenZipFile(output_path, 'w', mp=True) as archive:
        with tqdm(total=total_files, unit='file', desc="压缩文件",colour="green") as pbar:
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    archive.write(file_path, os.path.relpath(file_path, directory_path))
                    pbar.update(1)
async def gen(input,output,mode,height,fps,temp,max_workers=None,xz=False):
    ffmpeg=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/console_player_tools/ffmpeg.exe"
    if not os.path.exists(ffmpeg):
        ffmpeg="ffmpeg"
    await rm(temp)

    os.makedirs(os.path.join(temp,"frames"),exist_ok=True)
    ffmpeg_frame = [
        ffmpeg,
        '-i', input,
        '-vf', f'scale=-1:{height},fps={fps}',
        '-hide_banner',
        f'{temp}/frames/%d.jpg'
    ]
    if mode=="dp":
        ffmpeg_audio = [
            ffmpeg,
            '-i', input,
            '-vn',
            '-hide_banner',
            f'{temp}/audio.ogg'
        ]
    else:
        ffmpeg_audio = [
            ffmpeg,
            '-i', input,
            '-vn',
            '-hide_banner',
            f'{temp}/audio.mp3' 
        ]
    audio_runner=sp.run(ffmpeg_audio) # 如果你在这里报错，请安装ffmpeg并放在path里
    if audio_runner.returncode!=0:
        return
    frame_runner=sp.run(ffmpeg_frame)
    if frame_runner.returncode!=0:
        return
    
    
    print("写信息文件...")
    with open(os.path.join(temp,"manifest.json"),"w") as f:
        manifest={
            "frames":len(os.listdir(os.path.join(temp,"frames"))),
            "fps":fps, 
            "type":mode,
            "xz":xz
        }
        if mode=="cpvt":
            manifest["height"]=height
        json.dump(manifest,f)
        f.close()

    if mode=="dp":
        pass
        #os.makedirs(os.path.join(temp,"datapack","data"),exist_ok=True)
    elif mode=="cpvt":
        frames = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            with tqdm(total=manifest["frames"], unit='frame', desc="预处理所有帧", colour="green") as pbar:
                # 修改路径生成方式，使用os.path处理路径
                frame_paths = [os.path.join(temp, "frames", f"{i}.jpg") for i in range(1, manifest["frames"] + 1)]
                
                # 分批处理帧数据，每批50个任务
                chunk_size = 50
                futures = []
                for i, path in enumerate(frame_paths):
                    futures.append(executor.submit(process_frame, path, th=height, xz=xz))
                    # 每积累一定数量的任务就等待完成
                    if (i + 1) % chunk_size == 0:
                        for future, frame_path in zip(futures, frame_paths[i-chunk_size+1:i+1]):
                            result = future.result()
                            if xz:
                                txt_path = os.path.splitext(frame_path)[0] + ".txt.xz"
                                with open(txt_path, "wb") as f:
                                    f.write(result)
                                    f.close()
                            else:
                                txt_path = os.path.splitext(frame_path)[0] + ".txt"
                                with open(txt_path, "w", encoding="utf-8") as f:
                                    f.write(result)
                                    f.close()
                            os.unlink(frame_path)
                            pbar.update(1)
                        futures = []
                        await asyncio.sleep(0)  # 释放事件循环
                
                # 处理剩余任务
                for future, frame_path in zip(futures, frame_paths[-len(futures):]):
                    result = future.result()
                    txt_path = os.path.splitext(frame_path)[0] + ".txt"
                    with open(txt_path, "w", encoding="utf-8") as f:
                        f.write(result)
                    os.unlink(frame_path)
                    pbar.update(1)
    await asyncio.sleep(0.5)
    await compress_directory(temp,output)

    print("再次清空目录...")
    await rm(temp)
    await asyncio.sleep(0.5)