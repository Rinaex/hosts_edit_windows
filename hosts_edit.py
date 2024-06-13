import os
import shutil
import chardet
import configparser

config = configparser.ConfigParser()
config.read('conf.ini',encoding="utf-8")

hosts_path = 'C:/Windows/System32/drivers/etc/hosts'
backup_path = "hosts.bak"
result_ip = ""
threads = config.get('setting','threads')
menu =  '''
(o)打开HOSTS文件
(m)开始测速并修改HOSTS文件
(b)备份当前HOSTS文件
(r)还原备份的HOSTS文件
(c)清空控制台内容
(q)退出程序
(h)查看本菜单
输入括号中内容执行对应操作,conf.ini中可以修改部分配置
QQ交流群:730798667
'''



def open_hosts():
    os.popen(f'notepad {hosts_path}')
    input('按任意键继续')
# 测速
def speedtest():
    global result_ip
    if result_ip == "":
        # 获取当前工作目录
        current_dir = os.getcwd()
        # 切换工作目录到被运行程序所在目录
        os.chdir('CloudflareST')

        # 启动cmd程序并获取输出
        process = os.popen(f'echo.|CloudflareST.exe -n {threads} -o "result_hosts.txt"')
        process.close()

        # 打开txt文件
        with open('result_hosts.txt', 'r' ,encoding="utf-8") as file:
            # 读取第二行
            lines = file.readlines()
            if len(lines) >= 2:
                second_line = lines[1].strip()
            else:
                print("测速结果文件读取错误!")

        # 关闭文件
        file.close()
        # 切换回原工作目录
        os.chdir(current_dir)
        result_ip = second_line.split(",")[0]
        print('测速成功,使用IP: %s' % result_ip)

# 修改HOSTS
def modify_hosts():

    if os.path.exists(backup_path)==False:
        response = input("备份hosts文件,当前没有备份hosts文件，是否备份?(y/n)\n")
        if response == 'y':
            backup_hosts()
        elif response == 'n':
            pass
        else:
            print("无效输入，请重新输入\n")
    #   测速
    speedtest()

    if result_ip =="":
        print('没有获取到测速结果 请检查测速文件夹中的 result_hosts.txt 是否存在')
        return
    
    # 读取配置文件中的网址
    websites = config.options('websites')
    encoding = get_encoding(hosts_path)
    with open(hosts_path,'r', encoding=encoding) as file:
        lines = file.readlines()
    print("开始修改hosts文件")

    for website in websites:
        site_not_in_line = True
        site = config.get('websites',website)
        website_found = False
        for i, line in enumerate(lines):
                if site in line:
                    # 如果site已经存在 覆写该行
                    site_not_in_line = False
                    print(f'{site} 数据已存在 使用当前ip进行覆写')
                    lines[i] = f'\n{result_ip} {site}'
                        
        if site_not_in_line:
            # 如果不存在site 添加一行
            print(f'添加数据 {site}')
            lines.append(f'\n{result_ip} {site}')

    with open(hosts_path, 'w', encoding=encoding) as file:
        file.writelines(lines)

    os.popen("ipconfig /flushdns")
    print("修改结束")
    input('按任意键继续')
# 备份HOSTS
def backup_hosts():
    if os.path.exists(backup_path):
        response = input("备份文件已经存在,是否覆盖备份文件?(y/n)\n")
        if response == 'y':
            shutil.copyfile(hosts_path, backup_path)
            print('备份成功,备份文件在程序目录下hosts.bak')
        elif response == 'n':
            return
        else:
            print("无效输入，请重新输入\n")
    else:
        shutil.copyfile(hosts_path, backup_path)
        print('备份成功,备份文件在程序目录下hosts.bak')
    input('按任意键继续')
# 还原备份的hosts文件
def restore_hosts(): 
    if os.path.exists(backup_path):
        shutil.copyfile(backup_path, hosts_path)
        print("恢复成功","成功恢复Hosts文件！")
    else:
        response = input("没有找到备份文件,是否还原为Windows默认Hosts文件?(y/n)\n")
        if response == 'y':
            # 还原为Windows默认hosts文件
            default_hosts_path = "hosts.default"
            shutil.copyfile(default_hosts_path, hosts_path)
        elif response == 'n':
            return
        else:
            print("无效输入，请重新输入\n")
    input('按任意键继续')

# 检测文件编码
def get_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    return encoding

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def help():
    print(menu)

# 创建函数映射字典
function_map = {
    'o': open_hosts,
    'm': modify_hosts,
    'b':backup_hosts,
    'r':restore_hosts,
    'c' : clear,
    'h': help
}


def main():
    help()
    while True:
        user_input = input('请输入命令:')

        if user_input.lower() == 'q':
            print("程序退出")
            break
        
        if user_input in function_map:
            function_map[user_input]()
        else:
            print("无效的输入，请重新输入")
        
        
if __name__ == "__main__":
    main()