# T00ls sign
使用 GitHub Actions 每天自动执行 T00ls 签到
参(chao)考(xi)自 https://github.com/xirikm/hostloc-auto-get-points

## 使用说明

Fork 本仓库，然后点击你的仓库右上角的 Settings，找到 Secrets 这一项，添加两个秘密环境变量。



其中 `T00LS_USERNAME` 存放你在 Hostloc 的帐户名，`T00LS_PASSWORD` 存放你的帐户密码， `T00LS_MD5` 在存放的密码是 md5 时设置为 `True`， `T00LS_QID` 存放你的登录问题ID，`T00LS_QANS` 存放你的登录问题答案， `SCKEY` 则存放Server酱申请的skey。

设置好环境变量后点击你的仓库上方的 Actions 选项，会打开一个如下的页面，点击 `I understand...` 按钮确认在 Fork 的仓库上启用 GitHub Actions 。

![VZ5E.png](https://img.xirikm.net/images/VZ5E.png)

最后在你这个 Fork 的仓库内随便改点什么（比如给 README 文件删掉或者增加几个字符）提交一下手动触发一次 GitHub Actions 就可以了 **（重要！！！测试发现在 Fork 的仓库上 GitHub Actions 的定时任务不会自动执行，必须要手动触发一次后才能正常工作）** 。

仓库内包含的 GitHub Actions 配置文件会在每天国际标准时间 17 点（北京时间凌晨 1 点）自动执行获取积分的脚本文件，你也可以通过 `Push` 操作手动触发执行（测试发现定时任务的执行可能有 5 到 10 分钟的延迟，属正常现象，耐心等待即可）。

**注意：** 为了实现某个链接/帐户访问出错时不中断程序继续尝试下一个，GitHub Actions 的状态将永远是“通过”（显示绿色的✔），请自行检查 GitHub Actions 日志 `T00ls Sign` 项的输出确定程序执行情况。