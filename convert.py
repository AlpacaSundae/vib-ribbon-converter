from pathlib import Path
import ffmpeg
import time
import sys

def convert_files(files: list[Path], out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)

    cue_output = []

    for file in files:
        file_name = file.with_suffix(".wav").name
        out_file = out_dir / file_name

        ffmpeg \
            .input(file.as_posix()) \
            .output(out_file.as_posix(), format="wav", loglevel="quiet") \
            .run(overwrite_output=True)
        cue_output.append(out_file)
    
    cue_file = out_dir / Path("this.cue")
    with open(cue_file, "w") as f:
        for ii, file in enumerate(cue_output):
            f.writelines([
                f"FILE \"{file.name}\" BINARY\n",
                f"  TRACK {(1+ii):0>{2}} AUDIO\n",
                "    INDEX 01 00:00:00\n"
                ])

def is_audio_file(file_path):
    try:
        probe = ffmpeg.probe(file_path, loglevel="quiet")
        
        for stream in probe.get('streams', []):
            if stream.get('codec_type') == 'audio':
                return True
        return False
    except ffmpeg.Error as e:
        return False


def convert_dir(search_dir: Path):
    time_str = time.strftime("%Y%m%d-%H%M%S")
    out_dir = Path("out") / Path(f"{time_str}-{search_dir.name}")
    
    audio_files = []

    for x in search_dir.iterdir():
        if x.is_file():
            if is_audio_file(x):
                audio_files.append(x)

    convert_files(audio_files, out_dir)

def main():
    search_dir = None
    if len(sys.argv) > 2:
        print(f"too many args given. {sys.argv[1:]}")
        exit(1)
    elif len(sys.argv) == 2:
        search_dir = Path(sys.argv[1])
    else:
        search_dir = Path(input("enter a directory of music: "))
    
    if search_dir is None or not search_dir.is_dir():
        print(f"search_dir was not a directory: {search_dir}")
        exit(2)

    convert_dir(search_dir)

if __name__ == "__main__":
    main()
