#!/usr/bin/env python3
import json, time, os, sys, subprocess, shlex, platform, argparse
from shutil import copyfile
from subprocess import PIPE, Popen

from prekinto import *


log = print


def cmd(command):
    # subprocess.Popen takes a list of arguments:

    # from subprocess import Popen, PIPE
    # process = Popen(['swfdump', '/tmp/filename.swf', '-d'], stdout=PIPE, stderr=PIPE)
    # stdout, stderr = process.communicate()
    # There's even a section of the documentation devoted to helping users migrate from os.popen to subprocess.
    process = Popen(
        args=command,
        stdout=PIPE,
        universal_newlines=True,
        shell=True
    )
    stdout, stderr = process.communicate()
    # log('check_x11 stdout', stdout)
    # log('check_x11 stderr', stderr)
    return stdout.strip()


def parsed_args():
    # 解析传入的参数
    parser = argparse.ArgumentParser()
    # 如果有 -r 或者 --remove 就表示 uninstall
    # action='store_true' 会自动把 args.uninstall 设置为 true
    # dest - The name of the attribute to be added to the object returned by parse_args().
    parser.add_argument('-r', dest='uninstall', action='store_true', help="uninstall kinto")
    parser.add_argument('--remove', dest='uninstall', action='store_true', help="uninstall kinto")

    # 拿到解析后的 args
    args = parser.parse_args()
    # log('args', args)
    return args


def create_config_dir():
    # 拿到 home path
    homedir = os.path.expanduser("~")
    log('homedir', homedir)
    # 在 home 目录下建 kinto config 文件夹
    if not os.path.isdir(homedir + "/.config/kinto"):
        os.mkdir(homedir + "/.config/kinto")
        # time.sleep(0.5)


def check_x11():
    x11_info = cmd("(env | grep -i x11 || loginctl show-session \"$XDG_SESSION_ID\" -p Type) | awk -F= '{print $2}'")
    # log('len(check_x11) == 0', len(check_x11) == 0, os.name)
    if len(x11_info) == 0:
        if os.name != 'nt':
            print("You are not using x11, please logout and back in using x11/Xorg")
            sys.exit()


def run_something():
    # TODO: 搞懂这个 awk 是干啥的
    distro = cmd("awk -F= '$1==\"NAME\" { print $2 ;}' /etc/os-release").replace('"','').strip().split(" ")[0]
    dename = cmd("./linux/system-config/dename.sh").replace('"','').strip().split(" ")[0].lower()
    # log('distro', distro)
    # log('dename', dename)
    cmd("git fetch")

    # 艹, 这是要干嘛
    kintover = cmd('echo "$(git describe --tag --abbrev=0 | head -n 1)" "build" "$(git rev-parse --short HEAD)"')

    print("\nKinto " + kintover + "Type in Linux like it's a Mac.\n")


def uninstall():
    # check_call 
    # Run command with arguments. Wait for command to complete. If the return code was zero then return, otherwise raise CalledProcessError.

    # shlex.split
    # Split the string s using shell-like syntax.
    # 和 string split 区别不大...
    subprocess.check_call(shlex.split("./xkeysnail_service.sh uninstall"))
    exit()


def run():
    subprocess.check_call(shlex.split("./xkeysnail_service.sh"))


def main():
    args = parsed_args()
    create_config_dir()

    # log('platform.system()', platform.system())
    check_x11()

    run_something()

    if args.uninstall:
        uninstall()

    run()


if __name__ == "__main__":
    main()