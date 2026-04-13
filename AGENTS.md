盼之平台 (pzds.com) 商品列表页顶部“商品类型”筛选栏包含固定选项：成品号、昵称 (hot)、代肝 (hot)、充值 (new)、捏脸。抓取时需识别这些特定文本以确认页面加载正确性。

## 盼之平台反爬应对策略
盼之代售 (pzds.com) 具有严格的 WAF 验证机制。若 Selenium 自动化脚本触发“请进行如下验证”拦截，建议：1. 切换网络环境（如使用手机热点）以更换 IP；2. 清除浏览器 Cookie 后重试；3. 优先使用 `undetected-chromedriver` 库替代标准 Selenium 以绕过指纹检测；4. 采用“人工接管”模式，即脚本启动浏览器后暂停，由用户手动完成验证/登录，随后在终端确认继续执行。

## Python 3.14 环境依赖修复
在 macOS Python 3.14 环境下运行 `undetected-chromedriver` 时，需安装 `setuptools` 以补全缺失的 `distutils` 模块，并处理 SSL 证书验证问题（可通过 `Install Certificates.command` 或代码层临时禁用验证）。

## Python 3.14 环境依赖与路径配置
在 macOS Python 3.14 环境下运行 `undetected-chromedriver` 时：
1. 需安装 `setuptools` 以补全缺失的 `distutils` 模块。
2. 若遇 SSL 验证错误，可临时在代码中设置 `ssl._create_default_https_context = ssl._create_unverified_context`。
3. 必须显式指定 Chrome 二进制路径（如 `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`），否则可能报 `TypeError: Binary Location Must be a String`。

## macOS Python 3.14 ChromeDriver 环境配置
在 macOS Python 3.14 环境下运行 `undetected-chromedriver` 时：
1. 需安装 `setuptools` 以补全缺失的 `distutils` 模块。
2. 若遇 SSL 验证错误，可临时在代码中设置 `ssl._create_default_https_context = ssl._create_unverified_context`。
3. 必须显式指定 Chrome 二进制路径（如 `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`），否则可能报 `TypeError: Binary Location Must be a String`。若标准路径不存在，需通过 `mdfind` 查找实际安装位置并更新脚本。

## macOS Python 3.14 ChromeDriver 环境配置与路径探测
在 macOS Python 3.14 环境下运行 `undetected-chromedriver` 时：
1. 需安装 `setuptools` 以补全缺失的 `distutils` 模块。
2. 若遇 SSL 验证错误，可临时在代码中设置 `ssl._create_default_https_context = ssl._create_unverified_context`。
3. 必须显式指定 Chrome 二进制路径，否则可能报 `TypeError: Binary Location Must be a String`。若标准路径 `/Applications/Google Chrome.app` 不存在，需通过 `mdfind "kMDItemCFBundleIdentifier == 'com.google.Chrome'"` 查找实际安装位置（如桌面目录）并更新脚本。

## 盼之爬虫 DNS 解析失败应对
盼之爬虫脚本在 macOS 上若出现 `ERR_NAME_NOT_RESOLVED` 但系统 ping 正常，通常因 Chrome 实例未继承系统 DNS/代理设置。应在启动参数中添加 `--dns-prefetch-disable` 和 `--no-proxy-server` 以排除干扰。

## 盼之爬虫 Chrome 路径动态探测
在 macOS 环境下，若标准路径 `/Applications/Google Chrome.app` 不存在，必须通过 `mdfind "kMDItemCFBundleIdentifier == 'com.google.Chrome'"` 动态获取 Chrome 实际安装路径（如桌面目录），并显式传入 `undetected_chromedriver` 的 `options.binary_location` 参数，否则将报 `TypeError: Binary Location Must be a String`。
