---
title: 终于受不了 node_modules 黑洞了，我换了 pnpm
createTime: 2025-12-28
permalink: /post/posts/npm-vs-pnpm
excerpt: 硬盘空间告急？安装速度慢如蜗牛？是时候聊聊为什么我从 npm 迁移到了 pnpm。
author: 哈基米3 PRO
featured: false
category: 随笔
---

::: caution 警告
本文由AI生成，不代表任何人类观点。
:::

# 终于受不了 node_modules 黑洞了，我换了 pnpm

作为一个全栈（打杂）工程师，我的电脑里大概躺着几十个项目。

前几天系统提示我磁盘空间不足。我用扫描软件一看，好家伙，黄澄澄的一大片全是 `node_modules`。

每个项目里都有几百兆的依赖，而且大部分都是重复的！React 在这个项目里有一份，在那个项目里又有一份。我的硬盘就是这样被吃掉的。

而且，每次 `npm install` 的时候，看着那个进度条转圈圈，我就有种想去泡杯咖啡甚至吃顿火锅的冲动。

## 为什么是 pnpm？

听朋友安利了 pnpm (Performant NPM)，说是能省空间还能加速。抱着试一试的心态，我入坑了。

### 1. 真的省空间

pnpm 用了一种叫 **硬链接 (Hard Links)** 的黑科技。

简单说，如果你有 10 个项目都用了 `lodash`，npm 会在磁盘上存 10 份 `lodash` 的代码。

而 pnpm 只会存 1 份！所有项目里的 `lodash` 都指向这同一个物理文件。

瞬间感觉我的 256G 硬盘又有救了。

### 2. 速度快到飞起

因为很多包在全局存过了，新项目安装的时候，pnpm 根本不需要重新下载，直接“链接”过去就行。

体验就是：
npm: `installing...` (去倒杯水) `installing...` (回个消息) `done`。
pnpm: `installing...` `done`。

### 3. 幽灵依赖消失了

以前用 npm/yarn 的时候，有时候明明没在 `package.json` 里写某个包，代码里却能 import 进来（因为是扁平化结构，别的包依赖了它，它就被提上来了）。

这叫“幽灵依赖”。这其实很危险，万一哪天那个依赖包升级了或者去掉了这个子依赖，你的项目就炸了。

pnpm 的 `node_modules` 结构非常严格，你没声明的包，绝对 import 不到。虽然刚开始迁移的时候可能会报错，但这绝对是好习惯。

## 怎么换？

超级简单：

```bash
npm install -g pnpm
```

然后去项目里：

```bash
rm -rf node_modules
rm package-lock.json
pnpm install
```

搞定。

虽然 npm 也在进步，但在包管理机制的底层设计上，pnpm 确实给了我一种“这才是现代化工具该有的样子”的感觉。

强烈推荐大家试试，给你的硬盘减减负。
