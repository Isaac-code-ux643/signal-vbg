def detect_file_type(file):
    ext = file.name.split('.')[-1].lower()
    image_exts = ['jpg', 'jpeg', 'png', 'gif', 'webp']
    audio_exts = ['mp3', 'wav', 'ogg', 'm4a']
    video_exts = ['mp4', 'avi', 'mov', 'webm']
    if ext in image_exts:
        return 'image'
    elif ext in audio_exts:
        return 'audio'
    elif ext in video_exts:
        return 'video'
    return 'document'


def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0]
    return request.META.get('REMOTE_ADDR')
