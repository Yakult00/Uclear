# Uclear - 火炬职院洗衣机抢占程序

## 项目概述

Uclear 是一个专为火炬职院设计的洗衣机抢占程序，旨在帮助用户高效地使用宿舍楼内的洗衣机资源。该程序支持8、9、10楼的洗衣机抢占，并允许用户进行洗衣机卡订单操作。

## 功能特点

- **楼层支持**：程序覆盖8、9、10楼的洗衣机，确保用户能够快速找到可用的洗衣机。
- **手机验证码登录**：首次运行时，用户需要通过手机验证码进行登录，保障账户安全。
- **洗衣机卡订单**：支持洗衣机卡下单，简化使用流程。

## 使用说明

### 首次运行

在首次运行程序之前，请确保文件所在文件夹下存在一个名为 `token.json` 的文件。该文件用于存储用户的登录凭证。

### token.json 文件内容

```json
{
    "token": ""
}
```
## 还在开发的功能

通过图片二维码获取洗衣机id来实现不同区域洗衣机抢占功能

## 贡献与反馈

我们欢迎任何形式的贡献和反馈。如果您在使用过程中遇到任何问题，或者有任何改进建议，请通过GitHub Issues与我们联系。
