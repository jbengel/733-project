Use command:
yt-dlp -ciwxk --download-archive downloaded.txt --no-post-overwrites  --format bestaudio --audio-format mp3 --audio-quality 160K --output "%(channel)s____%(id)s____%(upload_date>%Y-%m-%d)s____%(view_count)d____%(title)s.%(ext)s" --yes-playlist 'https://www.youtube.com/playlist?list=PLiqHKzmCCitFWQIOeKINPkk2WCC-vaJmo'

downloaded.txt is used to skip duplicates

Remove extra webm files:
rm *.webm
