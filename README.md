# 综合技术离线资料库（轻量分支）

本分支只含中文导读、书目、实战项目说明与代码、登记表、脚本和发布说明。PDF、源码归档、网页镜像等全文在 Release **`engineering-full-20261030`** 的 3 个 tar 包里：

1. 下载 `engineering_offline_library_20261030_batch001_cn_en.tar`（必需），按需下载 `..._vendor_large_wikis_cn_en.tar` 和 `..._restricted_cn_en.tar`；
2. 全部解压到同一个短路径目录（如 `D:\eol\`）；
3. 用浏览器打开 `index_cn.html`，离线阅读，链接可离线跳转。

详见 [download_restore_cn.md](download_restore_cn.md)。每个文件在哪个包里，见 [archive_index_cn.csv](archive_index_cn.csv)；受限资料包的清单见 [release_restricted_cn.csv](release_restricted_cn.csv)；为兼容 Windows 所做的改名和改动，见 [windows_rename_map_cn.csv](windows_rename_map_cn.csv)。

以下是资料库原 README。

---

# 综合技术离线资料库

**中文总入口：[`00_portal/总入口.md`](00_portal/总入口.md)**

本目录是独立资料库，路径：`/root/engineering_offline_library/`。  
与大模型目录 `/root/llm_lifecycle_resources/`、Agent 目录 `/root/ai_agent_resources/`、Python 环境仓库均分开，不混放。

配套实践环境（保留原仓库，不混目录）：

| 用途 | 位置 |
| --- | --- |
| Linux x86-64 Python 环境 | `/root/linux_python_offline_resources/environments/` |
| 运行时 | `/root/linux_python_offline_resources/runtimes/` |
| 系统 deb | `/root/linux_python_offline_resources/system_dependencies/` |
| 开发板/固件/镜像 | `/root/linux_python_offline_resources/embedded/` |
| 使用说明 | `/root/linux_python_offline_resources/guides/` |

本轮状态：**已下载并整理，未在本机安装、未运行实验、未连接硬件、未烧录、未部署。**
