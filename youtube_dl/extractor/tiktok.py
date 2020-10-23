# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor


class TikTokIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?tiktok.com/@([a-zA-Z0-9\._]+)/video/(?P<id>[0-9]+)'
#    _VALID_URL = r'https?://(?:www\.)?yourextractor\.com/watch/(?P<id>[0-9]+)'
    _TEST = {
        'url': 'https://www.tiktok.com/@nyannyancosplay/video/6808321472864537861',
        'md5': '9bfc1b0cf582a8f2743051bc00f67eaf',
        'info_dict': {
            'id': '6808321472864537861',
            'ext': 'unknown_video',
            'title': 'Kat',
            'thumbnail': r're:^https?://.*',
            'description': 'Kat(@nyannyancosplay) has created a short video on TikTok with music Still Into You. Draft clean out time during this quarantine 🤣 | #cosplay #foryou #kannakamui #kannakamuicosplay #draft #paramore',
            'uploader': 'Kat',
            'uploader_id': 'nyannyancosplay',
            'uploader_url': 'https://www.tiktok.com/@nyannyancosplay',
            'upload_date': '20200326',
            'release_date': '20200326',

        }
    }

    def _real_extract(self, url):
        webpage = self._download_webpage(url, '')
        video_id = self._match_id(url)
        jsonString = self._html_search_regex(r'<script id="__NEXT_DATA__" type="application\/json" crossorigin="anonymous">(.+?)<\/script><script crossorigin="anonymous" nomodule=', webpage, '', group=1)
        json = self._parse_json(jsonString, '')
        videoProps = json['props']['pageProps']['videoObjectPageProps']['videoProps']
        watermarkedURL = videoProps['contentUrl']
        width = videoProps['width']
        height = videoProps['height']
        duration = 0
        durationDigits = ''
        for char in videoProps['duration']:
            if char.isdigit():
                durationDigits += char
        duration = int(duration)
        formats = [{
            'url': watermarkedURL,
            'format': 'mp4',
            'format_id': '0',
            'width': width,
            'height': height,
            'format_note': 'watermarked'
        }]
        thumbnails = []
        for thumbnailImg in videoProps['thumbnailUrl']:
            thumbnails.append({'url': thumbnailImg})

        watermarkedVideo = self._download_webpage(watermarkedURL, '')

        idPosition = watermarkedVideo.index('vid:')
        try:
            secretVideoID = watermarkedVideo[idPosition + 4: idPosition + 36]
        except ValueError:
            url = watermarkedURL
        else:
            url = 'https://api2.musical.ly/aweme/v1/playwm/?video_id=' + str(secretVideoID)
            formats.append({
                'url': 'https://api2.musical.ly/aweme/v1/playwm/?video_id=' + str(secretVideoID),
                'format': 'mp4',
                'format_id': '1',
                'width': width,
                'height': height,
                'format_note': 'no watermark'
            })

        return {
            'id': video_id,
            'title': videoProps['creator']['name'],
            'formats': formats,
            'ext': 'mp4',
            # 'thumbnail': videoProps['thumbnailUrl'][0],
            'thumbnails': thumbnails,
            'description': videoProps['description'],
            'uploader': videoProps['creator']['name'],
            'uploader_id': videoProps['creator']['url'].split('@')[1],
            'uploader_url': videoProps['creator']['url'],
            'upload_date': videoProps['uploadDate'].replace('-','')[0:8],
            'release_date': videoProps['uploadDate'].replace('-','')[0:8],
            'duration': duration

        }
