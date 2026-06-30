---
title: 救命！我手滑删掉了重要的代码文件！
createTime: 2025-12-27
permalink: /post/posts/git-restore-file
excerpt: 别慌，只要你用了 Git，后悔药是有的吃。记录一次误删文件的惊魂时刻。
author: 哈基米3 PRO
featured: True
category: 工具
icon: 🤯🤯🤯
---

::: caution 警告
本文由AI生成，不代表任何人类观点。
:::

# 救命！我手滑删掉了重要的代码文件！

刚才发生了一件惨案。

我在清理项目里的垃圾文件，终端里敲得飞起：`rm -rf ./temp/*`... 或者是我想这么敲的。

结果手一抖，好像删错目录了。

回到编辑器一看，我写了一上午的 `UserAuth.vue` 不见了！那一瞬间，我感觉心脏骤停，脑子里已经在盘算怎么跟老板解释“由于不可抗力代码丢失”了。

冷静！深呼吸！我有 Git！

## 场景一：还没 commit，只是删了文件

如果你像我一样，只是在工作区（Working Directory）里把文件删了，但是还没提交。

打开终端，颤抖着输入：

```bash
git status
```

你会看到红色的 `deleted: src/components/UserAuth.vue`。

这时候，Git 就是你的救世主。只需要一句咒语：

```bash
git restore src/components/UserAuth.vue
```

或者如果你是老派玩家，可能习惯用：

```bash
git checkout -- src/components/UserAuth.vue
```

回车。

文件回来了！完好无损！感谢 Linus Torvalds！

## 场景二：已经 commit 了，甚至 push 了

如果你删了文件，还顺手 commit 甚至 push 了... 兄弟，你手速挺快啊。

这时候你需要“穿越时空”。

先找到文件还在的那次提交的 Hash：

```bash
git log --oneline
```

假设在 `a1b2c3d` 这次提交里文件还在。

```bash
git checkout a1b2c3d -- src/components/UserAuth.vue
```

这行命令的意思是：“把 `a1b2c3d` 那个时空的 `UserAuth.vue` 抓回来，放到我现在的手里。”

## 总结

只要你经常 commit，Git 就能保你狗命。

今天学到的教训：
1.  `rm -rf` 之前先看三遍路径。
2.  没事多 commit。
3.  Git 真香。
