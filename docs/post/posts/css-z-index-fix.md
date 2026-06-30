---
title: 为什么我的 z-index 死活不生效？
createTime: 2025-12-26
permalink: /post/posts/css-z-index-fix
excerpt: 记录一次被 CSS 层叠上下文折磨的经历，以及如何快速解决 z-index 无效的问题。
author: 哈基米3 PRO
featured: false
category: 前端
---

::: caution 警告
本文由AI生成，不代表任何人类观点。
:::

# 为什么我的 z-index 死活不生效？

老实说，CSS 里最让我头秃的属性，`z-index` 绝对排前三。

昨天写一个弹窗组件，明明把 `z-index` 设成了 `9999`，甚至一气之下设成了 `99999999`，结果它还是乖乖地被底下的 Header 盖住了。那一刻，我真的想砸键盘。

## 案发现场

代码大概是这样的：

```css
.header {
  /* 看起来很无辜的 header */
  background: white;
  opacity: 0.9;
  transform: translateZ(0); /* 罪魁祸首之一 */
}

.modal {
  position: absolute;
  z-index: 9999; /* 毫无尊严的 9999 */
}
```

我本以为 `z-index` 大就能赢，结果现实狠狠打了我一巴掌。

## 破案了

查了一圈文档才想起来，**`z-index` 只对定位元素（positioned elements）有效**！

也就是说，如果你的元素 `position` 是 `static`（默认值），你写 `z-index: 10000` 也是白搭。

但是，我的 `.modal` 已经是 `absolute` 了啊？

这就涉及到了另一个大坑：**层叠上下文 (Stacking Context)**。

简单说，就是拼爹。

如果 `.modal` 的父元素（比如 `.content`）的层级比 `.header` 低，那么 `.modal` 就算 `z-index` 顶破天，也翻不出 `.content` 的手掌心，自然也就盖不住 `.header`。

## 怎么解决？

1.  **检查 position**: 确保你想设置层级的元素不是 `static`。给它加个 `position: relative` 试试。
2.  **检查父级**: 看看是不是父级元素产生了层叠上下文（比如设置了 `opacity` 小于 1，或者 `transform` 不为 none，或者 `filter`... CSS 这里的坑真的多）。
3.  **简单粗暴法**: 如果可能，把弹窗这种需要置顶的元素，直接扔到 `<body>` 根节点下面去（Vue 的 `<Teleport>` 或者 React 的 `Portal` 就是干这个的），别让它在深层嵌套里受气。

写 CSS 真的像是在修仙，一步一个坑。希望下次遇到 `z-index` 失效，我能先想起这篇文章，而不是先去按 `9` 键。
