# 阿里云函数计算部署指南

## 📋 部署前准备

- [ ] 注册阿里云账号并完成实名认证
- [ ] 开通函数计算 FC 服务
- [ ] 开通日志服务 SLS（免费额度够用）
- [ ] 获取 AccessKey ID 和 AccessKey Secret
- [ ] 安装 Funcraft 工具：`npm install @alicloud/fun -g`
- [ ] 配置 credentials：`fun config`

## 🚀 部署步骤

### 1. 本地测试
```bash
cd ui-survey-fc

# 本地运行测试（可选）
python3 index.py
```

### 2. 部署到阿里云
```bash
# 执行部署
fun deploy -y

# 记录返回的函数 URL
# https://<service>.<region>.fc.aliyuncs.com/...
```

### 3. 配置环境变量（可选）
- 访问函数计算控制台
- 找到 `ui-survey-service` → `ui-survey-function`
- 添加环境变量 `DINGTALK_WEBHOOK`

### 4. 测试 API
```bash
# GET 请求测试
curl https://<你的函数 URL>

# POST 请求测试
curl -X POST https://<你的函数 URL> \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### 5. 更新前端配置
编辑 `index.html`：
```javascript
const dataCollectionMethod = 'custom';
const customApiUrl = 'https://<你的函数 URL>';
```

### 6. 部署前端到 GitHub Pages
```bash
cd ../ui-survey

# 替换 API 地址
# 将 index.html 中的 customApiUrl 改为云函数 URL

# 推送更新
git add index.html
git commit -m "Update API to Aliyun FC"
git push
```

## 🔍 监控与调试

### 查看日志
```bash
# 使用 CLI 查看最新日志
fun logs ui-survey-service ui-survey-function
```

### 控制台查看
1. 访问 [日志服务控制台](https://sls.console.aliyun.com/)
2. 找到对应的 Project 和 Logstore
3. 实时查看函数执行日志

## ⚠️ 常见问题

### Q1: 部署失败提示权限错误
**解决**：检查 RAM 用户是否有 FC 相关权限，或改用主账号 AK/SK。

### Q2: 函数调用超时
**解决**：增加 Timeout 值（template.yaml 中调整，最大 60 秒）。

### Q3: Excel 文件丢失
**说明**：`/tmp` 目录是临时的，函数冷启动后会清空。  
**方案**：改用 OSS 存储或钉钉表格。

### Q4: CORS 错误
**解决**：代码已包含 CORS 头，确保前端请求方法正确。

## 💰 费用说明

- 每月前 100 万次调用免费
- CPU 时间按实际使用计费（问卷场景约 ¥2-10 元/月）
- 详见：https://www.aliyun.com/price/product#/fc/detail

## 📞 技术支持

- 官方文档：https://help.aliyun.com/product/50978.html
- 开发者社区：https://developer.aliyun.com/group/
