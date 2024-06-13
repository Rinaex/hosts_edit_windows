# hosts_edit_windows

由于很多GalGame资源站使用了 Cloudflare CDN 导致有很多同好无法打开  
即便提供了修改hosts的教程也仍然有伙伴搞不懂 于是做了这样一个简单的修改器

##  使用方法
下载并解压本程序 如果GitHub访问慢 您也可以在 [123盘](https://www.123pan.com/s/QyezVv-YpBph.html)下载  
解压完成后 右键点击 ```hosts_edit.exe``` 点击 ```以管理员身份运行```  
然后根据提示输入对应的按键回车即可

## 配置
在程序目录下有一个 ```conf.ini``` 它包含了程序的站点配置,您可以随意增改 但请务必保证您增加的站点使用了Cloudflare CDN  
文件中另一项配置 ```threads = 400``` 是测速程序的线程数 最大为1000 您可以根据您的网络硬件情况进行修改  线程数越高 测速越快

## 感谢项目
- https://github.com/XIU2/CloudflareSpeedTest

> 测速直接使用了西柚哥的程序,我本人只是写了一点修改文件的代码  
> 西柚哥,我滴神!

## License

The GPL-3.0 License.