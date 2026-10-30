# 下载与解压说明（综合技术离线资料库，2026-10-30）

## 发布包

| 文件 | 字节数 | 内容 | 是否必需 |
| --- | --- | --- | --- |
| `engineering_offline_library_20261030_batch001_cn_en.tar` | 543,162,368（0.51 GiB） | 中文总入口、10 个领域的导读和书目、20 个实战项目、登记表、脚本、可再分发的 PDF/规范（_public/）、许可允许的源码归档（vendor/）、离线首页 index_cn.html、本地公式库 _offline_libs/ | 必需 |
| `engineering_offline_library_20261030_vendor_large_wikis_cn_en.tar` | 1,179,648,000（1.10 GiB） | ArduPilot wiki、PX4 user guide、树莓派 documentation 三个大型文档源码归档（vendor/） | 可选 |
| `engineering_offline_library_20261030_restricted_cn_en.tar` | 1,005,584,384（0.94 GiB） | 资料库标为“仅个人阅读、不进公开 Release”的部分：_local_only/ 的 PDF（作者站公开的 CUP、Springer、MIT Press 等书，以及 CC BY-NC 材料）、docs_html/ 的 18 个网页镜像、5 个 NC 或个人用途的源码归档。仓库所有者决定随包提供，并单独打成这个包，清单见 release_restricted_cn.csv | 可选（首页里标“受限资料包”的链接需要它） |

SHA-256：

```
0c03ab0efe3f3b04ef543129716502f80767938a4d4d300a6ec78f95590c4f76  engineering_offline_library_20261030_batch001_cn_en.tar
312cbdcc9f99c96bc625e3a906218ce36a36733e5753a6a97ad34ec09fbb88ed  engineering_offline_library_20261030_vendor_large_wikis_cn_en.tar
c369e031ee4262c43fa7647c8a9d3f7bf9a4a532dcf009672c40a823c3e99e49  engineering_offline_library_20261030_restricted_cn_en.tar
```

Windows 校验：PowerShell `Get-FileHash 文件名 -Algorithm SHA256`，或者 `certutil -hashfile 文件名 SHA256`。

## 解压（Windows）

1. 先建一个**路径短**的空目录，例如 `D:\eol\`。包内最长相对路径为 194 个字符，目录越短越不容易超过 Windows 资源管理器 260 字符的限制。
2. 把下载的 tar 包**全部解压到这同一个目录**。tar 包里没有外层文件夹，`README.md`、`00_portal\` 等会直接出现在 `D:\eol\` 下。
   - 命令行（Windows 10/11 自带 tar）：`tar -xf engineering_offline_library_20261030_batch001_cn_en.tar -C D:\eol`，其他包同样处理。
   - 7-Zip：选中全部 tar 包，“解压到…”，填写 `D:\eol\`。**不要**用“解压到 <包名>\”，否则会分成几个文件夹，包之间的链接就失效了。
3. 用浏览器（Edge、Chrome、Firefox 均可）打开 `D:\eol\index_cn.html`，这是离线首页。也可以从 `00_portal\总入口.html` 开始读。

## 离线阅读说明

- 全部中文导读（`*.md`）旁边都生成了同名的 `.html`，浏览器可以直接打开，导读之间以及导读到本地文件的链接都能离线跳转。`.md` 原文保留，可用 VS Code、Typora 等编辑器阅读。
- 离线首页列出了 `inventories/download_log.csv` 的全部 161 条登记：已下载的 63 条链接到本地文件；下载失败或只登记链接的条目给出“在线”原址。
- 网页镜像（`docs_html/`）都是“入口页加一层”的有限镜像，资料库原本就是这样保存的。页面所需的样式、脚本、图片、字体以及 MathJax 公式库（2.7.9 和 3.2.2）都已改为包内本地副本，放在 `_offline_libs/` 和各镜像目录内。链接到未保存页面的地方改成了原站网址，联网时可以打开，断网时不会出现“找不到文件”。以下内容仍保持在线：统计脚本、评论组件、Adobe Typekit 字体（其许可不允许再分发；断网时浏览器改用系统字体，正文不受影响）。
- 链接指向目录时（如 `_public/`、`vendor/`），浏览器显示该目录的文件列表。
- `vendor/`、`_public/` 和 `_local_only/` 里的 `.tar.gz` 和 `.zip` 是资料原样的源码或文档归档，需要时再用 7-Zip 解压。其中 4 个已重新打包，以便在 Windows 下顺利解压：
  - `vendor/d2l-zh-master.tar.gz` 和 `_local_only/ai/prince_udl_github_src.tar.gz` 里有只差大小写的文件名，已加 `_caseN` 后缀；
  - `vendor/python-control-0.10.2.tar.gz` 和 `vendor/ThinkDSP-master.tar.gz` 里的符号链接已换成文件副本。
- 为兼容 Windows 改过名或改过内容的文件（如含 `?` 的网页资源名、离线化改写的网页），逐条记录在 `windows_rename_map_cn.csv`。这些文件的 SHA-256 与 `inventories/` 登记表中的值不同，以发布包为准。`archive_index_cn.csv` 列出了每个文件属于哪个 tar 包。
- 资料库本身的边界没有变：项目均为“已整理，未运行验证”。文中提到的 `/root/linux_python_offline_resources/` 等路径指作者机器上的其他资料库（各有自己的 GitHub 仓库），不在本发布包内。
