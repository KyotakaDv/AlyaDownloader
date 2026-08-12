import sys
import os
import json
import yt_dlp

def detect_platform(extractor_key, url):
    ext = (extractor_key or '').lower()
    url_lower = url.lower()

    if 'instagram' in ext or 'instagram.com' in url_lower:
        return 'instagram'
    elif 'youtube' in ext or 'youtu.be' in url_lower or 'youtube.com' in url_lower:
        return 'youtube'
    elif 'tiktok' in ext or 'tiktok.com' in url_lower:
        return 'tiktok'
    elif 'twitter' in ext or 'x' in ext or 'twitter.com' in url_lower or 'x.com' in url_lower:
        return 'twitter'
    elif 'pinterest' in ext or 'pin.it' in url_lower or 'pinterest.com' in url_lower:
        return 'pinterest'
    return 'outros'

def download_media(url, base_dir="media"):
    os.makedirs(base_dir, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(base_dir, 'temp_%(id)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': True,
        'no_warnings': True,
        'noprogress': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Baixa e resolve o link em uma única operação
            info = ydl.extract_info(url, download=True)

            if 'entries' in info and info['entries']:
                info = info['entries'][0]

            temp_filename = ydl.prepare_filename(info)

            # Ajusta extensão se foi convertido para mp4
            base, ext = os.path.splitext(temp_filename)
            possible_file = base + ".mp4"
            if os.path.exists(possible_file):
                temp_filename = possible_file

            # Detecta a plataforma após seguir os redirecionamentos do link
            extractor = info.get('extractor_key', '')
            platform = detect_platform(extractor, url)

            # Organiza na subpasta correspondente
            target_dir = os.path.join(base_dir, platform)
            os.makedirs(target_dir, exist_ok=True)

            file_ext = os.path.splitext(temp_filename)[1].lower()
            clean_title = "".join(c for c in (info.get('title') or 'media') if c.isalnum() or c in (' ', '_', '-')).strip()[:30]
            final_filename = f"{clean_title}_{info.get('id', 'item')}{file_ext}"
            final_path = os.path.join(target_dir, final_filename)

            if os.path.exists(temp_filename):
                os.rename(temp_filename, final_path)

            media_type = 'foto' if file_ext in ['.jpg', '.jpeg', '.png', '.webp'] else 'video'

            result = {
                "status": "success",
                "platform": platform,
                "media_type": media_type,
                "filename": final_filename,
                "relative_path": f"{platform}/{final_filename}",
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
