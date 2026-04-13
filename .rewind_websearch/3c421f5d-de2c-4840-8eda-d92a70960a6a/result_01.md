# Web函数-<em>阿里云</em>

URL: https://help.aliyun.com/document_detail/2513511.html

Query: 阿里云函数计算 FC 部署 Python Flask 教程 2025 2026

---

本文介绍自定义运行时中函数调用的方式、使用限制及代码示例。
背景信息
自定义运行时支持托管用户的 HTTP Server，并将函数调用的请求转换为 HTTP 请求发送到 HTTP Server，将 HTTP Server 的响应转换为函数调用的响应返回给 Client。过程示意如下：
函数调用的方式有两种，分别为：
HTTP 调用（推荐）：使用 HTTP 方式调用，例如使用 HTTP 触发器或者自定义域名来调用。
API 调用：通过 InvokeFunction API 进行调用，例如使用 SDK 调用函数或者通过事件源触发函数。
调用方式的不同，用户的 HTTP Server 的请求和响应的格式也会不同。
使用限制
一个函数的一个版本或别名，最多只能创建一个 HTTP 触发器。详细信息，请参见 版本管理 和 别名管理 。
HTTP Request 限制
Request Headers 不支持以 x-fc- 开头的自定义字段和以下自定义字段：
connection
keep-alive
如果 Request 超过以下限制，会返回 400 状态码和 InvalidArgument 错误码。
Headers 大小：Headers 中的所有 Key 和 Value 的总大小不得超过 8 KB。
Path 大小：包括所有的 Query Params，Path 的总大小不得超过 4 KB。
Body 大小：同步调用请求的 Body 的总大小不得超过 32 MB，异步调用请求的 Body 的总大小不得超过 128 KB。
HTTP Response 限制 
Response Headers 不支持以 x-fc- 开头的自定义字段和以下自定义字段：
connection
content-length
date
keep-alive
server
content-disposition:attachment
说明 
从安全角度考虑，使用 函数计算 默认的 aliyuncs.com 域名，服务端会在 Response Headers 中强制添加 content-disposition: attachment 字段，此字段会使得返回结果在浏览器中以附件的方式下载。如果需要解除该限制，需 配置自定义域名 。
如果 Response 超过以下限制，会返回 502 状态码和 BadResponse 错误码。
Headers 大小：Headers 中的所有 Key 和 Value 的总大小不得超过 8 KB。
其他使用说明
您可以通过绑定自定义域名，为函数映射不同的 HTTP 访问路径。详细信息，请参见 配置自定义域名 。
HTTP 调用（推荐）
对于 HTTP 方式的调用，函数计算采用透传模式，即将 Client 的 HTTP 请求透传到用户的 HTTP Server，并且将 HTTP Server 的响应透传给 Client。一些系统保留的字段将不会透传，具体请参考 使用限制 。
请求头（HTTP Request Header）
使用 HTTP 触发器或者自定义域名调用函数时，函数计算支持使用配置请求头控制请求的行为，具体如下表所示。
名称
类型
是否必选
示例
描述
名称
类型
是否必选
示例
描述
X-Fc-Invocation-Type
String
否
Sync
调用方式，具体信息请参见 调用方式 。取值说明如下：
Sync：同步调用。
Async：异步调用。
X-Fc-Log-Type
String
否
Tail
请求返回日志。取值说明如下：
Tail：返回当前请求产生的最后 4 KB 日志。
None：默认值，不返回请求日志。
响应头（HTTP Response Header）
使用 HTTP 触发器或自定义域名调用函数时，响应中会包含函数计算默认添加的一些响应头，具体如下表所示。
名称
描述
示例值
名称
描述
示例值
X-Fc-Request-Id
函数调用的请求 ID。
dab25e58-9356-4e3f-97d6-f044c4****
API 调用
对于使用 InvokeFunction API 的调用，函数计算会将 InvokeFunction 请求转换成 HTTP 请求，传递给用户的 HTTP Server，转换的规则如下：
InvokeFunction 的 event 参数被转换成 HTTP 请求的消息体。
path 为 /invoke 。
method 为 POST 。
Content-Type 消息头为 application/octe-stream 。
函数计算会将用户 HTTP Server 的响应转换为 InvokeFunction 的响应返回给客户端，转换的规则如下：
HTTP 响应体转换成 InvokeFunction 的响应体。
在转换过程中会丢失 HTTP 响应头和状态码信息。
Invoke API 请求的转换示例
Invoke 请求
HTTP Request (HTTP Server 收到的请求）
Invoke 请求
HTTP Request (HTTP Server 收到的请求）
Invoke API 请求内容：
"hello world"
> POST /invoke HTTP/1.1 > Host: 21.0.X.X > Content-Length: 11 > Content-Type: application/octet-stream  hello world
Invoke API 响应的输出示例
HTTP Response
Invoke 响应
HTTP Response
Invoke 响应
< HTTP/1.1 200 OK < Date: Mon, 10 Jul 2025 10:37:15 GMT < Content-Type: application/octet-stream < Content-Length: 11 < Connection: keep-alive  hello world
hello world
< HTTP/1.1 400 Bad Request < Date: Mon, 10 Jul 2025 10:37:15 GMT < Content-Type: application/octet-stream < Content-Length: 28 < Connection: keep-alive  {"errorMessage":"exception"}
{ "errorMessage" : "exception" }
函数计算响应码和响应头
Custom Runtime 本质是您实现的 HTTP Server，因此每一次函数调用都是一次 HTTP 请求，即每次响应都有响应码和响应头。
响应码 StatusCode
200 ：成功状态。
404 ：失败状态。
响应头 x-fc-status
200 ：成功状态。
404 ：失败状态。
通过 Headers 中的 x-fc-status 响应，向函数计算汇报本地函数是否执行成功。
不设置 x-fc-status ：函数计算默认本次调用是成功执行的，但是您的函数可能有异常，没有向函数计...
