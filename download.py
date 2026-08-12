import sys
import os
import json
import yt_dlp

def detect_platform(extractor_key):
    ext = (extractor_key or '').lower()
    if 'instagram' in ext:
        return 'instagram'
    elif 'youtube' in ext:
        return 'youtube'
    elif 'tiktok' in ext:
        return 'tiktok'
    elif 'twitter' in ext or 'x' in ext:
        return 'twitter'
    return 'outros'

def download_media(url, base_dir="media"):
    try:
        # 1. Identifica a plataforma sem realizar o download ainda
        with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl_info:
            info_dict = ydl_info.extract_info(url, download=False)
            platform = detect_platform(info_dict.get('extractor_key'))

        # 2. Cria a subpasta específica da plataforma
        target_dir = os.path.join(base_dir, platform)
        os.makedirs(target_dir, exist_ok=True)

        ydl_opts = {
            'outtmpl': os.path.join(target_dir, '%(title).40s_%(id)s.%(ext)s'),
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True,
            'noprogress': True,
        }

        # 3. Faz o download do arquivo
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            # Trata extensão em caso de conversão mp4
            base, ext = os.path.splitext(filename)
            possible_file = base + ".mp4"
            if os.path.exists(possible_file):
                filename = possible_file

            file_ext = os.path.splitext(filename)[1].lower()
            media_type = 'foto' if file_ext in ['.jpg', '.jpeg', '.png', '.webp'] else 'video'

            result = {
                "status": "success",
                "platform": platform,
                "media_type": media_type,
                "filename": os.path.basename(filename),
                "relative_path": f"{platform}/{os.path.basename(filename)}",
                "title": info.get('title', 'Mídia Salva')
            }
            print(f"JSON_RESULT:{json.dumps(result)}")

    except Exception as e:
        result = {"status": "error", "message": str(e)}
        print(f"JSON_RESULT:{json.dumps(result)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        download_media(sys.argv[1])
    else:
        print(f"JSON_RESULT:{json.dumps({'status': 'error', 'message': 'Nenhuma URL fornecida.'})}")
