# Init in Windows
安裝 [ffmpeg](https://ffmpeg.org/download.html) 並加入環境變數


## with Nvidia GPU (建議)
```
    virtualenv vvr
    .\vvr\Scripts\activate
    python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    python -m pip install -r requirements.txt
```

## without Nvidia GPU
```
    virtualenv vvr
    .\vvr\Scripts\activate
    python -m pip install torch torchvision torchaudio
    python -m pip install -r requirements.txt
```

# Start in Windows
```
    .\vvr\Scripts\activate
    python download.py https://www.youtube.com/watch?v=XXXXXXXX
```

# 關於版權
此程式僅適用於開放授權之影片，請勿用於侵權行為。