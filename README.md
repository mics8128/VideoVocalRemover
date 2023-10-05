Init in Windows with Nvidia GPU
```
    virtualenv vvr
    .\vvr\Scripts\activate
    python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    python -m pip install demucs pytube
```
額外安裝 [ffmpeg](https://ffmpeg.org/download.html) 並加入環境變數

Start in Windows
```
    .\vvr\Scripts\activate
```