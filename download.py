from pytube import YouTube
import os
import demucs.separate
import shlex

# 獲取 YouTube 連結
url = input("請輸入 YouTube 連結: ")
# url = "https://www.youtube.com/watch?v=N9XgnvGaZxk"

# 使用 pytube 下載影片
yt = YouTube(url)
stream = yt.streams.get_highest_resolution()

# 路徑們
current_path = os.path.dirname(__file__)
output_path = os.path.join(current_path, 'output')
temp_path = os.path.join(current_path, 'temp')

# 建立資料夾們
if not os.path.exists(temp_path):
    os.makedirs(temp_path)
if not os.path.exists(output_path):
    os.makedirs(output_path)

# 下載影片
video_file = stream.download(output_path=temp_path)

# 取得影片檔案名稱 (不包含副檔名)
video_name = os.path.splitext(os.path.basename(video_file))[0]

# 人聲檔案名稱
vocals_file = os.path.join(temp_path, f"htdemucs_ft", f"{video_name}", f"vocals.mp3")

# 伴奏檔案名稱
no_vocals_file = os.path.join(temp_path, f"htdemucs_ft", f"{video_name}", f"no_vocals.mp3")

# 分割伴奏 (如果沒有)
if not os.path.exists(no_vocals_file):
    demucs.separate.main(shlex.split(f"--mp3 --two-stems vocals -n htdemucs_ft -d cuda \"{video_file}\" -o \"{temp_path}\""))

# 使用 ffmpeg 合併左右聲道

# 輸出
output_ktv_file = os.path.join(output_path, f"{video_name}_KTV.mp4")
output_no_vocals_file = os.path.join(output_path, f"{video_name}_NoVocals.mp4")

# 左聲道用 no_vocals_file 右聲道用 video_file 影片用 video_file
os.system(f"ffmpeg -y -i \"{video_file}\" -i \"{no_vocals_file}\" -filter_complex \"[0:a][1:a]amerge=inputs=2,pan=stereo|c0<c2+c3|c1<c0+c1\" -map 0:v -c:v copy \"{output_ktv_file}\"")

# 聲音用 no_vocals_file 影片用 video_file
os.system(f"ffmpeg -y -i \"{video_file}\" -i \"{no_vocals_file}\" -map 1:a -map 0:v -c:v copy \"{output_no_vocals_file}\"")