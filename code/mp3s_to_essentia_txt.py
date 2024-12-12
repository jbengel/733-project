import os
import subprocess

# Source directory of mp3 files
source_directory = "../music"

# Path to essentia music extractor binary
extractor_path = "../essentia/streaming_extractor_music"

# Output directory for generated essentia txt files
output_directory = "../data/essentia_txt_files"
os.makedirs(output_directory, exist_ok=True)

# For each mp3 file in the source dir
count = 0
for filename in os.listdir(source_directory):
    if filename.endswith(".mp3"):
        count = 1 + count
        print(f"\n__[{count:04d}]__\n") # can assume no more than 9999 entries

        mp3_path = os.path.join(source_directory, filename)
        
        # Expect mp3 files in specific format:
        # artistName____youtubeID____year-month-day____viewcount____full video title.mp3
        # Want to use ID as unique key for output txt
        parts = filename.split("____")
        if len(parts) != 5:
            print(f"[Warning] Skipped file with unexpected format: {filename}")
            continue
        yt_id = parts[1]
        # output_filename = f"{yt_id}.txt"
        output_filename = filename.split(".mp3")[0] # avoiding need to match files back later

        output_path = os.path.join(output_directory, output_filename)
        
        # Invoke shell to run binary
        # Use source mp3 from source dir
        # Output txt file in output dir
        command = [extractor_path, mp3_path, output_path]
        try:
            subprocess.run(command, check=True)
            print(f"Processed: {mp3_path} -> {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"[Warning] Could not process mp3 {mp3_path}: {e}")
