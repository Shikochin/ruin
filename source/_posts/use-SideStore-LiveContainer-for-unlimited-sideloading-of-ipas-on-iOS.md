---
title: 使用 SideStore + LiveContainer 在 iOS 上无限侧载 .ipa
date: 2025-11-02 14:50:35
tags:
 - SideStore
 - LiveContainer
 - 侧载
 - iOS
 - .ipa
categories:
 - 技术
---

## 前言

大家都有在 iOS 设备上侧载 App 的需求，一般的 AltStore 或者 Sideloadly! 是通过假装你正在开发这个 App 给你一个七天就会过期的签名，且一个 Apple Account 最多只能签 3 个 App，**which is sort of 菜**。

SideStore 解决了续签需要连接电脑的问题，但是这样一来你只能签 2 个 App 在 iOS 上了。

LiveContainer 就是来解决这个问题的，它是一个“可重签名的应用容器 (App Bundle Shell)”，它自身的结构被设计成允许 iOS 在不卸载 App 的前提下重新写入 / 替换其中的二进制和签名文件，以实现安装其它 .ipa 的能力。

所以，SideStore + LiveContainer = 无限侧载 + 自动续签。

# 配置无限侧载

## 安装 SideStore

这一步我就不赘述了，[SideStore 官网](https://sidestore.io/#get-started)是有教程的，注意**保存好你的 pairing file(.plist)**。

## 安装 StosVPN

这是 SideStore 官方的用来续签 App 的工具，在**环大陆**的 App Store 都可以搜索到，安装好后启用。

## 在 SideStore 侧载 SideStore+LiveContainer

神奇的是 LiveContainer 为了方便把本体和 SideStore 结合在了一起，你可以在这里找到 [SideStore+LiveContainer](https://github.com/LiveContainer/LiveContainer/releases/)

1. 在 SideStore 中侧载这个 App，无脑下一步（记得选 **Refresh Now**）
2. SideStore 会自行退出重装一次，我们再次重复操作 1（选 **Keep App Extensions(Use Main Profile)**）
3. 侧载完成后你就可以在桌面看到 LiveContainer 了

## 配置 LiveContainer 中内置的 SideStore

确保刚才侧载的 LiveContainer 可以正常打开后，把 SideStore 直接卸载。

打开 LiveContainer，左上角第二个图标就是进入内置 SideStore 的入口，点击后会闪退一次，重新打开就变成了 SideStore 的界面，我们给它提供 **pairing file**。

点击 My Apps，点击 Refresh All，这一步是为了重新登录你的 Apple Account（记得还要选 **Refresh Now** 和 **Keep App Extensions(Use Main Profile)**）。

之后 App 会退出并重装，再次进入就回到了 LiveContainer。

## 导入 SideStore 的证书

在 LiveContainer 里，点击设置 > 从 SideStore 导入证书，直到显示为**可以刷新证书**即为导入成功。

至此，你的 LiveContainer 已经可以无限导入 .ipa 并运行了。

# 配置自动续签

已知 SideStore 续签需要 StosVPN 开启且当前连接了 Wi-Fi，且 iOS 有快捷指令，于是我们有：

![IMG_0521.png](https://s2.loli.net/2025/11/02/2FQBis5InWRouYX.png)

这是成品，你也可以直接导入，注意修改掉最后一行的重新连接其他 VPN，如果你没有连接需求改为断开连接即可：https://www.icloud.com/shortcuts/d24a504578d34dcebb4cb8b3e9a3a70b

配置好运行一次，确保可以正常续签。

然后我们设置快捷指令里的自动化，让它每周运行几次即可保证续签，这里不再赘述。

