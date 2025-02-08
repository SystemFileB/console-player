import subprocess as sp, os, shutil, time, py7zr
from tqdm import tqdm
async def rm(temp):
    files = [os.path.join(temp, filename) for filename in os.listdir(temp)]
    with tqdm(total=len(files), unit='file', desc="删除文件", colour="blue") as pbar:
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
    with py7zr.SevenZipFile(output_path, 'w') as archive:
        with tqdm(total=total_files, unit='file', desc="压缩到cpvid文件",colour="blue") as pbar:
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    archive.write(file_path, os.path.relpath(file_path, directory_path))
                    pbar.update(1)

async def gen(input,output,mode,height,fps,temp):
    ffmpeg=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/console_player_tools/ffmpeg"
    print("清空目录...")
    await rm(temp)
    time.sleep(0.5)

    os.makedirs(os.path.join(temp,"frames"),exist_ok=True)
    ffmpeg_frame = [
        ffmpeg,
        '-i', input,
        '-vf', f'scale=-1:{height},fps={fps}',
        f'{temp}/frames/%d.jpg'
    ]
    if mode:
        ffmpeg_audio = [
            ffmpeg,
            '-i', input,
            '-vn',
            f'{temp}/audio.ogg'
        ]
    else:
        ffmpeg_audio = [
            ffmpeg,
            '-i', input,
            '-vn',
            f'{temp}/audio.mp3' 
        ]
    print("提取帧命令行：",ffmpeg_frame,"提取音频命令行：",ffmpeg_audio)
    if sp.call(ffmpeg_audio)!= 0:
        return 1
    if sp.call(ffmpeg_frame) != 0:
        return 1

    if mode:
        pass
    else:
        await compress_directory(temp,output)

    print("再次清空目录...")
    await rm(temp)
    time.sleep(0.5)