---
title: 关于 Arcaea 的改包和私服
date: 2025-08-18 17:23:25
tags:
- Arcaea
- 改包
- 私服
- 逆向
categories:
- 技术
---
![f65ddd713edfcbcfdf77a9ff3624333e.jpg](https://s2.loli.net/2025/08/18/PnHKIsVzESeaM5X.jpg)
## 前言
本文不提供任何改包和私服的成品供您下载，我不想被 lowiro 告上法庭。

本文仅提供改包和私服的思路以及操作方法，采用本文的方法则默认您已知悉了可能存在的风险，一切后果概不负责。

本文仅记录 Apple 设备（Tested on iPadOS 26 Developer Beta 6）的修改方法，关于 Android 系统，您可以参考 Arcaea Mod Wiki 的教程，那里有 Android 版本的修改方式。

部分思路来自 [Arcaea Mod Wiki](https://github.com/FishiaTee/arcmodwiki)(CC0-1.0 Licensed).

## 获取脱壳后的 .ipa 文件

Apple 对于上架了 App Store 的 App 进行了加密，防止开发人员进行反编译操作。

如果您有 Jailbroken 的设备，可以自行砸壳，我没有 Jailbroken 的设备故不做说明，您有 Jailbreak iPhone / iPad 的能力相信这里不需要我赘述。

如果您没有 Jailbroken 的设备，可以去 [decrypt.day](https://decrypt.day) 这个网站下载。

## 获取 Arcaea Bundle

从 Arcaea 5.4.0 开始，少量游戏内容的更新方式变为了游戏内下载捆绑包的方式，我们需要获取这个所谓 "Bundle" 备用。

由于 iOS 的沙盒机制，这个文件并不好获取，需要 Jailbreak，不过我们可以使用 root 后的 Android 设备来获取（root 可比 Jailbreak 简单多了不是吗）。

下载最新的 Arcaea 的 APK 文件，注意不要是 Chinese 版本，Chinese 版本的游戏内容跟随版本号更新，里面并没有我们想要的东西。

安装后，进入游戏下载 Bundle 并至少进入一次游戏主界面。

然后进入 `/data/data/moe.low.arc/files`，有一个叫做 `dltemp` 的文件夹，里面应当存在两个文件，一个是 `<版本号>.bundle`，一个是 `<版本号>.json`，将这两个文件取出备用。


## Bypass 掉 Arcaea 的 SSL Pinning

在 Arcaea 3.6.0 的安全更新后，逆向和反编译变得困难，并且增加了和服务器连接使用的 SSL 证书，Arcaea 连接时只认 lowiro 自己服务器上的证书，如果你不进行这一步，你将无法连接到自己的服务器。

> Android 设备请参考 Arcaea Mod Wiki，这里的步骤只适用于 iOS 版本。

### 先行知识

在进行逆向之前，你需要安装 IDA Pro（其他工具我不知道是否可用，我没有进行验证），这是一个很常用的逆向工具。

关于 [NOP](https://zh.wikipedia.org/zh-cn/NOP)(from Wikipedia)：计算机科学中，NOP 或 NOOP（No Operation 或 No Operation Performed 的缩写，意为无操作）是汇编语言的一个指令，一系列编程语句，或网络传输协议中的表示不做任何有效操作的命令。

所以，我们需要 NOP 掉 Arcaea 的部分指令调用以 Bypass SSL Pinning，由于 Arcaea 运行在 arm64 的设备上，对于 arm64 架构，等价 NOP 指令的十六进制码是：`1F 20 03 D5`，所以如果你跟我一样使用 arm 设备运行 IDA Pro，由于架构不支持不自带方便的 NOP 操作，你可以手动输入十六进制码，它们是**等价**的操作。

### 开始魔法！

> 以下教程基于 Arcaea 6.7.0，如果您是其他版本（>= 3.6.0），可能会有文字上的不同，不过大体结构是相同的

解压从 decrypt.day 上下载的 .ipa 文件，用 IDA Pro 打开里面的 `Arc-mobile`，不出意外，IDA Pro 应该会自动定位到里面的 `Arc-mobile`（注意这和上面的不是一个东西，上面的本质是一个叫做 Arc-mobile.app 的文件夹，下面这个是 ELF/Mach-O arm64 可执行文件）。

![image.png](https://s2.loli.net/2025/08/18/1MkrimdnVHocUIA.png)

打开后，等待初始的自动分析完成，这个过程需要一段时间，取决于你的电脑性能。初始分析后，按 Shift + F12 等待 Strings 列表生成，这同样需要一些时间。

在字符串子窗口，按 Super（Windows：Windows 徽标键 / macOS: Command 键） + F 搜索 `cookieFiIe.txt`，直到您找到这个：

![image.png](https://s2.loli.net/2025/08/18/IRny7xMGmN3uOao.png)

双击它，之后进入如下界面，选中高亮文字：

![image.png](https://s2.loli.net/2025/08/18/TdDMg7XQxuPZhey.png)

按下 X 来执行 xref（交叉引用）。

选择唯一的一个 xref，按下 Enter：

![image.png](https://s2.loli.net/2025/08/18/YB3pvLhwuiKGlZo.png)

之后按下 F5 进行反编译，直到反编译出伪代码后，你应该能看到如下画面：

![image.png](https://s2.loli.net/2025/08/18/u5FvYJBbjWSE8sk.png)

滑动到最底部，直到看到类似绿色方框内的结构，选中红色方框内的这部分，使它高亮（你的文字可能不是 sub_100B714A8）：

![image.png](https://s2.loli.net/2025/08/18/g6hrYV4BsNHcSIn.png)

现在切换到 Hex View-1，右键空白位置，选择 Synchronize with Pseudocode-A（如果你刚才选中高亮字符的页面叫做 Pseudocode-A 的话），然后选中第一个高亮字符：

![image.png](https://s2.loli.net/2025/08/18/ZcCYNOA8JIrpGDz.png)

按 F2 或右键选择 Edit，输入刚才等价 NOP 指令的十六进制码（如果你忘了，我贴心的告诉你是 `1F 20 03 D5`，拿去用吧不客气），然后再按 F2 或者右键选择 Apply Changes，现在看起来应该像这样：

![image.png](https://s2.loli.net/2025/08/18/MYOIVgcTJRQu3o6.png)

然后切换回 Pseudocode-A 页面让 IDA Pro 重新进行一次反编译，不出意外，刚才你选中的那一行应该消失了。

恭喜你已经进行了一次 NOP，记住刚才的种种操作，接下来就会很快了。

再切换回 Strings 页面，这次我们搜索 `vtvtvt`：

![image.png](https://s2.loli.net/2025/08/18/BMXndDHsbwR43pj.png)

双击进入，xref（按下 X）这段高亮文本：

![image.png](https://s2.loli.net/2025/08/18/RZBu1o8FjeP5Mhr.png)

选择第一个 xref，按 Enter 进入，然后选中高亮文本，按 F5 反编译：

![image.png](https://s2.loli.net/2025/08/18/6FJ9rtfKSVPCx42.png)

之后在打开的这个页面，在初始选中的 `"vtvtvt"` 字符下你应该能找到类似绿色方框的结构，选中红色方框内的文本（同理，你的可能不叫 sub_100B714F4），参考上面的操作，NOP 它：

![image.png](https://s2.loli.net/2025/08/18/RsDPgujHk24OF3L.png)

之后别忘了切换回 Pseudocode-B 页面让 IDA Pro 重新反编译并检查是否 NOP 成功。

接下来，用 Edit > Patch program > Apply patches to input file... 保存你的更改。

![image.png](https://s2.loli.net/2025/08/18/e5oxCqQy1JSv7wd.png)

![image.png](https://s2.loli.net/2025/08/18/RAPpmdHBGLSv2wU.png)

> 主播改完忘记保存更改了而是按下了 Ctrl + S 了，我以为这样就是改完了结果这样只是保存了 IDA Pro 对这个文件静态分析后的数据库，然后主播用一点没修改的官方包体折腾了好几个小时无果，警钟长鸣。

然后我们修改 `/Arc-mobile.app/Info.plist`，里面有一个叫做 `NSAllowsArbitraryLoads` 的属性，把它改为 `true`。

接下来重新压缩回 .ipa，就可以用你喜欢的 Sideload 工具安装到你的设备上了。

至此，最难的客户端的修改我们已经完成了，行百里者半九十。

## 配置 Arcaea 服务器

你需要安装 Python 3.6 及以上版本，一个用来通过代理重定向 HTTP 请求的软件（这里我使用 [Charles](https://www.charlesproxy.com)）。

最重要的当然是服务端，我们使用 Lost-MSth 开发的 [Arcaea-server](https://github.com/Lost-MSth/Arcaea-server) 项目，将它 clone 到本地。

之后，cd 进 `latest version` 目录，运行 `pip install -m requirements.txt` 以安装依赖。然后我们进入 `database` 文件夹，运行 `database_initialize.py` 来初始化数据库，然后你应该看到出现了一个叫做 `arcaea_database.db` 的文件。

### 放入 Bundle

还记得刚才我们准备的两个 Bundle 文件吗？将这两个文件放入 `/database/bundle` 里，并将 `<版本号>.bundle` 重命名为 `<版本号>.cb`

![image.png](https://s2.loli.net/2025/08/18/NRzZLIQdUha371y.png)

### 获取歌曲谱面和音乐文件

由于 Arcaea 的软件包体内只包含几首免费歌曲的谱面和音乐文件，我们需要获取其他歌曲的谱面和音乐，这些文件存放在 lowiro 的服务器，需要你付费购买后在游戏内下载才会出现在你的设备里。

给 lowiro 付费的话，本文就没有意义了，这里，请大家自行搜索 Arcaea 离线版本的 APK（当然要和你修改的版本是一个版本），相信大家的搜索能力，并不难找。

之后在 rooted 的 Android 设备上安装，找到 `/data/data/moe.low.arc/files/cb/active/songs`。

将这个 `songs` 文件夹全部提取出来，这就是我们需要的谱面和音乐，你应该注意到服务端的 `database` 文件夹下也有一个叫做 `songs` 的文件夹，将这两个文件夹合并。

![image.png](https://s2.loli.net/2025/08/18/nxdfvAg3BYwRG58.png)

### 配置 Charles

打开 Charles，打开 Proxy > SSL Proxying Settings：

![image.png](https://s2.loli.net/2025/08/18/WQY9wSZrj2E3Ong.png)

在新窗口，勾选 Enable SSL Proxying，点击加号，Host 和 Port 栏全部填写 `*`，保存，然后将你刚才填写的那一项取消勾选：

![image.png](https://s2.loli.net/2025/08/18/sVH5RPWTS7wOchE.png)

关闭这个窗口，打开 Proxy > Proxy Settings：

![image.png](https://s2.loli.net/2025/08/18/64DZmJWTLPv9XgM.png)

配置成如图所示：

![image.png](https://s2.loli.net/2025/08/18/bJxVk4qMZsXl9S7.png)

这两个端口可以随意配置，但最好不要和常见端口冲突。

先别关闭这个窗口，隔壁有一个 macOS（如果你是 Windows 那么叫做 Windows）标签卡，里面有四个选项，全部勾选。

现在去你的系统设置里查看你电脑的**局域网 IP**，记下来。

回到 Charles，打开 Tools > Map Remote，配置成如图所示（局域网 IP 记得改成自己的）：

![image.png](https://s2.loli.net/2025/08/18/ol7d9rzqIjpkhmG.png)

后面的端口号就是待会要配置的服务端的端口号，可以随便改，只要和服务端上的一样就可以。如果你的 Arcaea 版本较老，可能不需要劫持 auth.lowiro.com，不过劫持也无妨，减少试错成本。

### 配置 config.py

回到服务端，将根目录里面的 `config.example.py` 重命名为 `config.py`，打开，按照下面的示例配置（这里只放几个片段）。

```python
'''
--------------------
主机的地址和端口号
Host and port of your server
'''
HOST = '<自己的局域网 IP>'
PORT = <自己配置的端口号>
'''
--------------------
'''

'''
--------------------
游戏API地址前缀
Game API's URL prefix
'''
GAME_API_PREFIX = ["/coldwind/35","/"] 

# Tip: 这里的 API 前缀是每几个版本 lowiro 就会更改，在 6.7.1 版本 /coldwind/35 仍然起效，之后和之前的版本可能不同，目前我还不知道怎么得知这个前缀，这个也是我上网搜到的，如果之后我找到了固定的获取方法会在这里更新。
'''
--------------------
'''

'''
--------------------
允许使用的游戏版本，若为空，则默认全部允许
Allowed game versions
If it is blank, all are allowed.
'''
ALLOW_APPVERSION = []
'''
--------------------
'''
```

### 启动服务器

配置大功告成了，回到服务端根目录，运行 `main.py`，不出所料你应该看到如图所示的输出：

![image.png](https://s2.loli.net/2025/08/18/RWundpBbMxvzl8f.png)

恭喜你，服务端基本配置完成，现在我们距离游玩之差半步之遥了！

## 连接 Arcaea 服务器

回到你的 iOS 设备，在系统的 WiFi 设置里配置 HTTP Proxy，选择手动，Server 输入刚才的局域网 IP，端口输入刚才在 Charles 里设置的 HTTP Proxy 端口（如果你按照我的操作应该是 8888）。

![Screenshot 2025-08-18 at 19.46.22.png](https://s2.loli.net/2025/08/18/VSOXmfiDPslRY2E.png)

在浏览器里访问 chls.pro/ssl，安装 Charles SSL CA 证书，回到系统设置，在 General > VPN Device Management 里安装 Charles Proxy CA 这个 Profile，然后去 General > About > Certificate Trust Settings 里将 Charles Proxy CA (日期，你的设备名) 勾选。

然后回到电脑上的 Charles，点击 Record（红色箭头指向的按钮），不出意外你应该能看到一些网络请求出现在左边，这就代表连接成功了：

![image.png](https://s2.loli.net/2025/08/18/LSNKWxZ8yrse6ml.png)

现在打开我们刚修改的 Arcaea，你应该能在 Charles 看到被劫持的请求，你的服务端那里应该也会输出一些日志：

![image.png](https://s2.loli.net/2025/08/18/LrSwDYlEdB4jxcf.png)

恭喜你，大功告成了，享受属于自己的 Arcaea 服务器吧！

## 获取谱面定数

你可能会发现，玩了一会新歌，自己的 PTT 却一直没变，还是 0，这是因为在 `arcaea_database.db` 里没有这些谱面的定数，我们现在要做的就是把全部谱面的定数重新写入进去。

首先，找一个合适的数据库管理软件，打开 `arcaea_database.db`（最好先关掉服务端），找到 chart 这个表，你会发现里面可能有一些东西了，这里就是老歌曲的歌曲定数。

![image.png](https://s2.loli.net/2025/08/18/nWmNMYOcfK4CExk.png)

感谢 Arcaea 中文维基定数测算组，我们得以获取所有谱面的定数。在[这个页面](https://arcwiki.mcd.blue/Template:ChartConstant.json)有一份谱面定数的 JSON 文件，把它保存下来。

我们会发现 chart 表和这份 JSON 文件格式相近，只是 JSON 文件不存在歌曲名（不过这并不影响，经过我的测试，chart 表里的 name 属性即便全是空的也不影响 PTT 的计算，不清楚 name 属性有何作用），只有歌曲的内部代号，并且定数在 chart 表中全部乘以 10 了。

于是我问 ChatGPT 帮我写了一个 Python 脚本用来转换为 CSV：

```python
import json
import csv

# 读取 JSON 文件
with open("ChartConstant.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 写入 CSV 文件
with open("ChartConstant.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    # 表头
    writer.writerow(["song_id", "name", "rating_pst", "rating_prs", "rating_ftr", "rating_byn", "rating_etr"])
    
    # 遍历 JSON
    for song_id, charts in data.items():
        ratings = []
        for entry in charts:
            if entry is None:
                ratings.append(-1)
            else:
                constant = entry.get("constant")
                if constant is None:
                    ratings.append(-1)
                else:
                    ratings.append(int(constant * 10))
        
        # 保证长度为5
        while len(ratings) < 5:
            ratings.append(-1)
        
        # 写入一行
        writer.writerow([song_id, ""] + ratings)
```

之后导入进 `arcaea_database.db`，把原来的 chart 表删掉，把新导入的表改名为 chart 就可以了。

注意表的格式一定是下面这样：

```sql
CREATE TABLE "chart" (
	"song_id"	TEXT,
	"name"	TEXT,
	"rating_pst"	INTEGER,
	"rating_prs"	INTEGER,
	"rating_ftr"	INTEGER,
	"rating_byn"	INTEGER,
	"rating_etr"	INTEGER
);
```

> rating_xxx 的类型一定要是 INTEGER 不然结算的时候服务端会报错。

大功告成了，现在启动服务端，PTT 就可以正常计算了，体验玩一局就变成 #1 的爽感吧（什

## 结语

这是对一次 Arcaea 逆向和配置私服的记录，之后如果还有新的内容（比如导入自制谱，编写地图文件等等）会在这里继续更新。