import requests
import xml.etree.ElementTree as ET

HOST = "china-hjz.github.io"  # 替换为你的实际域名
KEY = "d153551697ef4d63ad84b35fbf0c3d44"  # 替换为你的 API Key

def get_latest_posts(sitemap_path, n=10):
    # 解析 XML sitemap
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    
    # 使用命名空间
    namespaces = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    # 获取所有 URL
    urls = [(url.find('s:loc', namespaces).text, url.find('s:lastmod', namespaces).text)
            for url in root.findall('s:url', namespaces)]
    
    # 根据最后修改时间排序
    urls.sort(key=lambda x: x[1], reverse=True)

    # 返回最近的 n 个 URL
    return [url[0] for url in urls[:n]]

def ping_bing(url_list):
    # url = 'https://www.bing.com/indexnow'
    url = 'https://api.indexnow.org/IndexNow'
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
    }

    # 准备数据
    data = {
        "host": HOST,
        "key": KEY,
        "keyLocation": f"https://{HOST}/{KEY}.txt",
        "urlList": url_list
    }

    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=data)
    return response

if __name__ == "__main__":
    sitemap_path = "sitemap.xml"  # 替换为你的 sitemap 文件路径
    url_list = get_latest_posts(sitemap_path, 20)  # 获取最近 10 篇文章的 URL
    print("最近更新的文章 URL 列表：")
    print(url_list)  # 打印获取的 URL 列表

    response = ping_bing(url_list)  # 向 IndexNow 发送请求
    print("响应状态码：", response.status_code)  # 打印响应状态
    print("响应内容：", response.text)  # 打印响应内容
