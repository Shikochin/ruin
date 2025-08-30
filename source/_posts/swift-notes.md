---
title: Swift 笔记
date: 2025-08-30 20:27:19
tags:
- Swift
- 笔记
- 技术
summary: none
---

## 前言

简单说明一下，很多编程语言通用的东西就不写了，这里记录一些 Swift 的特色（或者是我学到的新东西）。

## Optional 值的 unwrap

### ?? 操作符

可以用 `??` 操作符给一个默认值：

```swift
let maybeExist: String? = nil
print(maybeExist ?? "It doesn't exist.")
```

### if-let 语句

```swift
let maybeExist: String? = nil
if let itDoesExist = maybeExist {
    print("Wow!")
}else{
    print("Damn.")
}
```

### guard-let 语句

```swift
let maybeExist: String? = nil
// 确保 maybeExist != nil 否则
guard let maybeExist else {
    return "Damn."
} 
return "Wow!"
```