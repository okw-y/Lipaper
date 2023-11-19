import subprocess


def getVideoThumbnail(path: str, output: str = "output.png") -> None:
    subprocess.call(
        f"ffmpeg -hide_banner -loglevel error -y -i \"{path}\" -ss 00:00:01.000 -vframes 1 \"{output}\"", shell=True
    )
