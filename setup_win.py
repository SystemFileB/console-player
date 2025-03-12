import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="console_player",
    version="1.00",
    author="SystemFileB",
    description="让终端可以播放视频！",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="github.com/SystemFileB/console-player",
    packages=["cpvid_gen","consoleplay","console_player_tools"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)", 
    ],
    install_requires=[
        "py7zr",
        "tqdm",
        "Pillow",
        "colorama",
        "pygame"
    ],
    platforms=["Windows"],
    entry_points={
       "cpvid_gen": "cpvid_gen.__main__:run",
       "consoleplay": "consoleplay.__main__:run",
    },
    license="LGPLv3",
    include_package_data=True
)