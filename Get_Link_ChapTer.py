# session = HTMLSession()
# URL = "http://www.nettruyen.com/truyen-tranh/gia-kim-thuat-2259"
# r = session.get(URL)
# rs = r.html.find("#nt_listchapter .chapter a",first=False)
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import argparse
from progress.bar import IncrementalBar
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor




#kiểm tra thông tin đầu vào từ chapter bao nhiêu
parser = argparse.ArgumentParser()
parser.add_argument("square", help="display a square of a given number",
                    nargs='?',
                    default=1, 
                    type=int)
args = parser.parse_args()
# print(args.square)
# exit()
star_time = time.time()

def Remove_unwanted_string(TempString):
    remove_text = 'Gần nhất phát sách mới quá nhiều người, cái kia đội hình thấy ta tê cả da đầu.<br/><br/>Ta lão Giang Sơn ca « Thái Ất », Nhai thần « Chửng Cứu Toàn Cầu », lão Bắc Hà « thích khách chi vương », còn chứng kiến Thái Miêu « Tửu Điếm Cung Ứng Thương », còn có một đoàn nhận biết gia hỏa. . . Tê cả da đầu.<br/><br/>Sở dĩ, đã nhiều người như vậy phát sách, vậy ta cũng phải đi theo!<br/><br/>Sách mới nhân vật chính tên. . . Mạnh Tề Tịch thế nào? Ta muốn viết một cái kỳ tích nam nhân, tin tưởng kỳ tích người, tổng là cùng kỳ tích một dạng không tầm thường! <p> </p><p>Chúc Nhúy xấu trai sinh nhật vui vẻ, mọi quà tặng gửi bank in 21806 <a href="https://truyencv.com/lao-tang-quet-rac-max-cap-lien-xuong-nui/">Lão Tăng Quét Rác , Max Cấp Liền Xuống Núi</a></p> <div style="margin-bottom: 10px;"><div class="fb-like" data-action="like" data-href="https://www.facebook.com/truyencvcom/" data-layout="standard" data-show-faces="true" data-size="small"></div></div> </div>'
    remove_text1 ='<p>Chúc Nhúy xấu trai sinh nhật vui vẻ, mọi quà tặng gửi bank in 21806 <a href="https://truyencv.com/lao-tang-quet-rac-max-cap-lien-xuong-nui/">Lão Tăng Quét Rác , Max Cấp Liền Xuống Núi</a></p> <div style="margin-bottom: 10px;"><div class="fb-like" data-action="like" data-href="https://www.facebook.com/truyencvcom/" data-layout="standard" data-show-faces="true" data-size="small"></div></div> </div>'
    remove_text2 ='<div style="margin-bottom: 10px;"><div class="fb-like" data-action="like" data-href="https://www.facebook.com/truyencvcom/" data-layout="standard" data-show-faces="true" data-size="small"></div></div> </div>'
    remove_text3 ='<script type="text/javascript">var _avlVar=_avlVar||[];_avlVar.push(["6f8adab64618480bb109e5dcefadecf7","[yo_page_url]","[width]","[height]"]);</script><script id="s-6f8adab64618480bb109e5dcefadecf7" src="//ss.yomedia.vn/js/yomedia-sdk.js?v=3" type="text/javascript"></script>'
    remove_text4 ='<div style="margin-bottom: 10px;"><div class="fb-like" data-action="like" data-href="https://www.facebook.com/truyencvcom/" data-layout="standard" data-show-faces="true" data-size="small"></div></div> <div class="alert alert-success" role="alert"><span aria-hidden="true" class="glyphicon glyphicon-info-sign"></span> Đề cử truyện hot: <br/><br/>Cửu Thiên ✯ Tiền Nhiệm Vô Song<br/><br/>✯✯✯ ✯✯✯ ✯✯✯</div> </div>'
    remove_text5 ='<p> </p><p><a href="https://truyencv.com/toan-the-gioi-chi-co-ta-khong-biet-ta-la-cao-nhan/">Toàn Thế Giới Chỉ Có Ta Không Biết Ta Là Cao Nhân</a> Ta là phàm nhân, nhưng các đại năng cứ nghĩ ta là Đại Tiên, vậy làm sao bây giờ?</p>'
    remove_text6 ='<div style="margin-bottom: 10px;"><div class="fb-like" data-action="like" data-href="https://www.facebook.com/truyencvcom/" data-layout="standard" data-show-faces="true" data-size="small"></div></div> <div class="alert alert-success" role="alert"><span aria-hidden="true" class="glyphicon glyphicon-info-sign"></span> Đề cử truyện hot: <br><br/>Cửu Thiên ✯ Tiền Nhiệm Vô Song<br/><br/>✯✯✯ ✯✯✯ ✯✯✯</br></div> </div>'
    remove_text7 ='div class="fb-like" data-action="like" data-href="https://www.facebook.com/truyencvcom/" data-layout="standard" data-show-faces="true" data-size="small"></div></div> <div class="alert alert-success" role="alert"><span aria-hidden="true" class="glyphicon glyphicon-info-sign"></span> '
    remove_text8 ='<script type="text/javascript">var _avlVar=_avlVar||[];_avlVar.push(["6f8adab64618480bb109e5dcefadecf7","[yo_page_url]","[width]","[height]"]);</script><script id="s-6f8adab64618480bb109e5dcefadecf7" src="//ss.yomedia.vn/js/yomedia-sdk.js?v=3" type="text/javascript">'
    TempString.replace(remove_text,"")
    TempString.replace(remove_text1,"")
    TempString.replace(remove_text2,"")
    TempString.replace(remove_text3,"")
    TempString.replace(remove_text4,"")
    TempString.replace(remove_text5,"")
    TempString.replace(remove_text6,"")
    TempString.replace(remove_text7,"")
    TempString.replace(remove_text8,"")
    return TempString


url = "https://truyencv.com/index.php"

payload = "showChapter=1&media_id=924&number=1&page=1&type=vu%20luyen%20dien%20phong"

headers = {
    'cookie': "__cfduid=ddfe02caa50eade1b34a5ffdc608bea6b1592748448; PHPSESSID=e172b4bec33dd2dcdbbfec3e1e213b9c; TAM=; reada=9; HstCfa4379013=1592748453464; HstCla4379013=1592748667472; HstCmu4379013=1592748453464; HstPn4379013=5; HstPt4379013=5; HstCnv4379013=1; HstCns4379013=1; _ga=GA1.2.791100113.1592748455; _gid=GA1.2.432818259.1592748455; __yoid__=c31dfa2188a3bd622225576a2d244a49; readingstory=a%3A1%3A%7Bi%3A924%3Bi%3A1%3B%7D; __dtsu=6D001592748466F22D8A2042FD8A429C; _gat_gtag_UA_113932176_22=1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
    'accept': "*/*",
    'accept-language': "en-US,en;q=0.5",
    'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
    'x-requested-with': "XMLHttpRequest",
    'origin': "https://truyencv.com",
    'connection': "keep-alive",
    'referer': "https://truyencv.com/vu-luyen-dien-phong/"
    }
try:
    response = requests.request("POST", url, data=payload, headers=headers)
    response.raise_for_status()
except response.exceptions.HTTPError as err:
    raise SystemExit(err)
soup = BeautifulSoup(response.content, 'html.parser')
all_chapter = soup.select('.item a')
_timeupdate= all_chapter[0]['title']
#_timeupdate= all_chapter[len(all_chapter)-1]
#print(all_chapter)
#exit()
all_chapter.reverse() # đảo ngược list để chapter từ 1---
print("Truyện có số chương là: "+ str(len(all_chapter))+" " +_timeupdate)
print("Số Chương cần tải là : "+ str(len(all_chapter)- int(args.square)))

def Get_Chapter_Content(url):
        try:
            response = requests.request("GET", url, data=payload, headers=headers)
            response.raise_for_status()
        except response.exceptions.HTTPError as err:
            raise SystemExit(err)
        soup_content = BeautifulSoup(response.content, 'html.parser')
        chapter_name = soup_content.find(class_="header")
        #print(chapter_name.get_text())
        chapter_content = soup_content.find(id="js-truyencv-content")
        #print(chapter_content)
        return [chapter_name,chapter_content]

_IncrementalBar = IncrementalBar('Processing', max=len(all_chapter)-int(args.square),suffix='%(percent).1f%% - %(elapsed)ds' )


#filename = "tuchan.html"
Manga_name="VuLuyenDienPhong"
Path(Manga_name).mkdir(parents=True, exist_ok=True)
f = open(Manga_name+"/"+Manga_name+".html",'a+')# Write to only one file

chapter_count=1

for chapter in all_chapter:
    if int(args.square) > 1 and chapter_count < int(args.square):
        chapter_count = chapter_count + 1
        #_IncrementalBar.next()
        continue
    chapter_count = chapter_count + 1
    #print(chapter['href'])
    Content = Get_Chapter_Content(chapter['href'])
    #print(Content)
    #exit()
    _IncrementalBar.next()
    #print(str(Content[0]))
    #xit()
    f.write(str(Content[0]))
    content_final = Remove_unwanted_string(str(Content[1]))
    f.write(content_final)
    f.write("\n")
f.close()
_IncrementalBar.finish()
end_time = time.time()
print(end_time - star_time)


