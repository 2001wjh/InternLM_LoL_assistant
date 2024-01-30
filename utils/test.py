import requests
from pyquery import PyQuery as pq
import csv
import re
from bs4 import BeautifulSoup
import pandas as pd

# ----------------------------------------------------------------------------------------------------------------------

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

html = requests.get("http://www.op.gg/champion/statistics", headers=headers).text
# print(html)

soup = BeautifulSoup(html, 'html.parser')
# print(soup)

tag_1 = soup.find('div', class_="css-67h8o1 esk32cx0")

tag_2 = tag_1.find('tbody')

tag_3 = tag_2.find_all('tr')

# ----------------------------------------------------------------------------------------------------------------------

Rank = []
Champion = []
Tier = []
Position = []
WinRate = []
PickRate = []
BanRate = []
WeakAgainst = []
hero_url = []
innate = []
sumskills = []
sum = 0

# ----------------------------------------------------------------------------------------------------------------------

def innate_skill(html_content):
    inborn = html_content.find('div', class_='css-18v97ez e2gxw6z3')
    if inborn:
        flairs = inborn.find_all('div', class_='css-1l6y0w9 e1y8mv8s0')
        # print(flairs)
        for flair in flairs:
            # print(flair)
            senses = flair.find_all('div', class_='row')
            for sense in senses:
                image_container = sense.find_all('div', style='position:relative')
                # .find('div', style_='position:relative')
                for i in image_container:
                    image = i.find('img')
                    if 'e_grayscale' not in image['src']:
                        print(image['alt'])
                        innate.append(image['alt'])
    global sum
    sum += 1
    print(sum)


# ----------------------------------------------------------------------------------------------------------------------

def summoner_skills(html_content):
    inborn = html_content.find('ul', class_='css-eh1etn e1qbmy400')

    image_container = inborn.find_all('div', style='position:relative')
    print(image_container)
    for image in image_container:
        skill = image.find('img')
        print(skill['alt'])
        sumskills.append(skill['alt'])


# ----------------------------------------------------------------------------------------------------------------------

for content in tag_3:
    data_0 = content.find('td', class_='css-v6xa4a e186jz34')
    # print(data_0)
    # # 检查data_0是否为None
    if data_0 is not None:
        rank_tag = data_0.find('span')
        # 再次检查rank_tag是否为None
        if rank_tag is not None:
            Rank.append(rank_tag.text)
        else:
            print("没有找到<span>标签")
    else:
        print("没有找到匹配的<td>标签")

# ----------------------------------------------------------------------------------------------------------------------

    data_1 = content.find('td', class_="css-4ee3gn e186jz32")
    if data_1:  # 检查 data 是否为 None
        img_tag = data_1.find('img')
        if img_tag and 'alt' in img_tag.attrs:  # 检查 img_tag 是否存在且是否有 alt 属性
            Champion.append(img_tag['alt'])
        else:
            print("img 标签不存在或没有 alt 属性")
    else:
        print("未找到指定的标签")

# ----------------------------------------------------------------------------------------------------------------------

    data_2 = content.find('td', class_="css-1qly9n1 e186jz35")
    if data_2:
        if data_2.text == '0':
            Tier.append('OP')
        else:
            Tier.append(data_2.text)
    else:
        print("未找到指定的标签")

# ----------------------------------------------------------------------------------------------------------------------

    data_3 = content.find('td', class_="css-1amolq6 edsne5b1")
    if data_3:  # 检查 data 是否为 None
        position_tag = data_3.find('img')
        if position_tag and 'alt' in position_tag.attrs:  # 检查 img_tag 是否存在且是否有 alt 属性
            pos = position_tag['alt']
            if pos == 'ROLE-TOP':
                Position.append('上单')
            elif pos == 'ROLE-JUNGLE':
                Position.append('打野')
            elif pos == 'ROLE-MID':
                Position.append('中单')
            elif pos == 'ROLE-ADC':
                Position.append('射手')
            else:
                Position.append('辅助')
        else:
            print("img 标签不存在或没有 alt 属性")
    else:
        print("未找到指定的标签")

# ----------------------------------------------------------------------------------------------------------------------

    data_4 = content.find_all('td', class_="css-1amolq6 edsne5b1")
    # print(data_4[1].text)
    if data_4:
        WinRate.append(data_4[1].text)
    else:
        print("未找到指定的标签")

# ----------------------------------------------------------------------------------------------------------------------

    data_5 = content.find_all('td', class_="css-1amolq6 edsne5b1")
    # print(data_5[2].text)
    if data_5:
        PickRate.append(data_5[2].text)
    else:
        print("未找到指定的标签")

# ----------------------------------------------------------------------------------------------------------------------

    data_6 = content.find_all('td', class_="css-1amolq6 edsne5b1")
    # print(data_5[2].text)
    if data_6:
        BanRate.append(data_6[3].text)
    else:
        print("未找到指定的标签")

# ----------------------------------------------------------------------------------------------------------------------

    data_7 = content.find('td', class_="css-1gnhxc7 e186jz36")
    num3 = data_7.find_all('a')
    wkag_hero = []
    for num in num3:
        if num:
            text = num.find('div').find('img')
            wkag_hero.append(text['alt'])
        else:
            print("未找到指定的标签")
    WeakAgainst.append(wkag_hero)

# ----------------------------------------------------------------------------------------------------------------------

    data_8 = content.find('td', class_="css-4ee3gn e186jz32")
    hero_u = ' https://op.gg' + str(data_8.a['href'])
    hero_url.append(hero_u)

# ----------------------------------------------------------------------------------------------------------------------


    for url in hero_url:
        html_detail = requests.get(url, headers=headers).text
        html_con = BeautifulSoup(html_detail, 'html.parser')
        innate_skill(html_con)
        # summoner_skills(html_con)


# if __name__ == '__main__':
#     print(Rank)
#     print(Champion)
#     print(Tier)
#     print(Position)
#     print(WinRate)
#     print(PickRate)
#     print(BanRate)
#     print(WeakAgainst)
#     print(hero_url)

    # df = pd.DataFrame({
    #     'Tier': Tier,
    #     'Position': Position,
    #     'WinRate': WinRate,
    #     'PickRate': PickRate,
    #     'BanRate': BanRate,
    #     'WeakAgainst': WeakAgainst,
    #     'hero_url': hero_url
    # }, index=Champion)
    #
    # df.to_csv('./champions_data.csv', encoding='utf_8_sig')
    #
    # print("数据已保存到 'champions_data.csv'")
    # # print(innate)

