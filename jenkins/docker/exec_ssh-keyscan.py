#!/usr/bin/python3
#
# stderr: No ED25519 host key is known for 172.18.0.7 and you have requested strict checking.
# Host key verification failed.

def sys_cmd (jenkins_container_name, workdir, cmd):
    import os
    command = "docker exec -it --workdir=" + workdir + " " + jenkins_container_name
    # print(command)

    ret = os.system(command + " " + cmd)
    return ret

def proc_out(args):
    import subprocess

    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    output =  stdout.decode()

    return output

def get_container_ip (host_container_name):
    import re

    args = ["docker", "exec", "-it",  host_container_name, "ifconfig"]
    ifconfig_output =  proc_out(args)

    pattern = "inet addr:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})  Bcast:"
    a = re.findall(pattern, ifconfig_output)
    if len(a):
        return a[0]

    pattern = "inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})  netmask"
    a = re.findall(pattern, ifconfig_output)
    if len(a):
        return a[0]

    print(ifconfig_output)

def exec_cmd (jenkins_container_name, workdir, cmd):
    command = "docker exec -it --workdir=" + workdir + " " + jenkins_container_name
    # print(command)

    args = command.split(" ")
    args += cmd.split(" ")
    # print(args)

    out = proc_out(args)
    return out


def all_ls_ssh ():
    cmd="ls .ssh"

    out = exec_cmd ("jenkins-blueocean", "/var/jenkins_home", cmd)
    print (out)

    out = exec_cmd ("agent",             "/home/jenkins",     cmd)
    print (out)

    out = exec_cmd ("agent_android",     "/home/jenkins",     cmd)
    print (out)


def ls_known_hosts (jenkins_container_name, workdir, host_container_ip):
    cmd="ssh-keyscan " + host_container_ip
    out = exec_cmd (jenkins_container_name, workdir, cmd)
    print (out)

    cmd="ls .ssh"
    ret = sys_cmd (jenkins_container_name, workdir, cmd)
    if 0 == ret:
        pass
    else:
        cmd="mkdir .ssh"
        sys_cmd (jenkins_container_name, workdir, cmd)

    cmd="ls .ssh/known_hosts"
    ret = sys_cmd (jenkins_container_name, workdir, cmd)
    if 0 == ret:
        pass
    else:
        cmd="touch .ssh/known_hosts"
        sys_cmd (jenkins_container_name, workdir, cmd)

    ret = sys_cmd (jenkins_container_name, workdir, "pwd")
    #ret = sys_cmd (jenkins_container_name, workdir, "ls ./scan-host-key.sh")
    ret = sys_cmd (jenkins_container_name, workdir, "find / -name scan-host-key.sh")

    cmd="/scan-host-key.sh " + host_container_ip
    out = exec_cmd (jenkins_container_name, workdir, cmd)
    print (out)

    cmd="cat .ssh/known_hosts"
    ret = sys_cmd (jenkins_container_name, workdir, cmd)


host_container="ubivisgmbh_git_server"
host_container="jenkins_agent"

host_container_ip = get_container_ip (host_container)
print(host_container_ip)

if host_container_ip is not None:
    #all_ls_ssh()
    ls_known_hosts ("jenkins_sandbox", "/var/jenkins_home", host_container_ip)
    #ls_known_hosts ("jenkins-blueocean", "/var/jenkins_home", host_container_ip)
    #ls_known_hosts ("agent",             "/home/jenkins", host_container_ip)
    #ls_known_hosts ("agent_android",     "/home/jenkins", host_container_ip)
