from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import requests
import csv

# 用于修复matplotlib中文显示问题
plt.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei', 'FangSong']  # 用来正常显示中文
plt.rcParams['font.size'] = 10  # 设置字体大小
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# 原网页网址,注意修改为自己所对应的手机品牌
url = "https://search.jd.com/search?keyword=%E6%89%8B%E6%9C%BA&suggest=1.his.0.0&wq=%E6%89%8B%E6%9C%BA&ev=exbrand_%E9%BB%91%E9%B2%A8%5E"

# 获取网页源码，headers用于绕过京东无法直接爬取的限制
soup = BeautifulSoup(requests.get(url, headers={'user-agent': 'Mozilla/5.0'}).content.decode("utf-8"), "html.parser")
phonePrice, phoneName, shopName = [], [], []  # 手机价格，手机型号，店铺名称
sumPrice, avgPrice = {}, {}  # 每个店铺的合计价格字典{店铺名：[合计价格，手机数量]}，每个店铺的平均价格字典{店铺名：平均价格}
name_c, price_c = [], []  # 对店铺平均价格字典的拆分，店铺名，平均价格，用于生成图表

# 查找网页中的div标签，返回列表
price_div = soup.findAll('div', class_='p-price')
# 查找div标签中的i标签，将价格添加到phonePrice中
for i in price_div:
    phonePrice.append(i.findAll('i')[0].text)
# 同上解释，获取手机型号
name_div = soup.findAll('div', class_='p-name p-name-type-2')
for i in name_div:
    phoneName.append(i.findAll('em')[0].text)
# 同上解释，获取店铺名称
shop_div = soup.findAll('div', class_='p-shop')
for i in shop_div:
    shopName.append(i.findAll('a')[0].text)
print(shopName)  # debug

for i in range(0, len(shopName)):
    # 如果字典已经存在此店铺名，则加上新遍历到的手机价格，并把手机数量+1
    if shopName[i] in sumPrice:
        sumPrice[shopName[i]] = [sumPrice[shopName[i]][0] + float(phonePrice[i]), sumPrice[shopName[i]][1] + 1]
        print(sumPrice)
    # 如果字典不存在此店铺名，则添加此店铺名
    else:
        sumPrice[shopName[i]] = [float(phonePrice[i]), 1]
print(sumPrice)  # debug
# 计算均价，并存入字典
for i, j in sumPrice.items():
    avgPrice[i] = j[0] / j[1]
# 字典拆分
for i, j in avgPrice.items():
    name_c.append(i)
    price_c.append(j)

# 生成csv文件，文件在.py源文件目录
with open('alldata.csv', 'w', newline='') as f:
    allData = csv.writer(f, dialect='excel')
    # 添加第一行
    allData.writerow(['型号', '店铺名称', '价格'])
    # 添加混合后数据
    allData.writerows(zip(phoneName,shopName,phonePrice))
with open('data2.csv', 'w', newline='') as s:
    avg = csv.writer(s, dialect='excel')
    avg.writerow(['店铺名称', '评均价格'])
    avg.writerows(zip(name_c, price_c))

# 绘图部分
plt.figure(1)  # 绘制图一
plt.bar(name_c, price_c)  # 绘制直方图
plt.figure(2)  # 绘制图二
plt.pie(price_c, labels=name_c)  # 绘制饼状图
plt.show()  # 显示绘图
