import yt_dlp
import requests
import csv

CORTIS
SEARCH_WORD = "social media marketing"

def get_youtube_data(keyword):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch20:{keyword}", download=False)
    video_data = []
    all_text_data = ""
    for video in result['entries']:
        title = video.get("title","无标题")
        channel = video.get("uploader","未知频道")
        date = video.get("upload_date","未知时间")
        views = video.get("view_count",0)
        likes = video.get("like_count",0)
        desc = video.get("description","无简介")[:400]
        video_data.append([title,channel,date,views,likes,desc])
        all_text_data = all_text_data + f"标题：{title}，简介：{desc}\n"
    return video_data, all_text_data

def gemini_analyse(text_content):
    url = "https://free-gemini-api.vercel.app/api/gemini"
    prompt = f"下面是YouTube搜索出来的全部视频内容，请你总结内容趋势、高频话题、主流观点，字数控制在300字以内，只输出总结文字：{text_content}"
    post_data = {"prompt":prompt}
    res = requests.post(url,json=post_data,timeout=60)
    return res.json()["reply"]

# 主程序运行流程
if __name__ == "__main__":
    videos, total_text = get_youtube_data(SEARCH_WORD)
    summary_result = gemini_analyse(total_text)
    # 写入Excel表格
    with open("youtube_result.csv","w",encoding="utf-8-sig",newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["视频标题","发布频道","发布日期","播放量","点赞数","视频简介","AI整体数据分析"])
        for item in videos:
            writer.writerow(item+[summary_result])
    print("数据采集完毕，表格已生成，可以下载上交")
