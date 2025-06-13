#!/usr/bin/python3
#
# stderr: No ED25519 host key is known for 172.18.0.7 and you have requested strict checking.
# Host key verification failed.

def proc_out(args):
    import subprocess

    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    output =  stdout.decode()

    return output

host_container="ubivisgmbh_git_server"

def get_container_ip (host_container_name):
    import re

    args = ["docker", "exec", "-it",  host_container_name, "ifconfig"]
    ifconfig_output =  proc_out(args)

    pattern = "inet addr:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})  Bcast:"
    a = re.findall(pattern, ifconfig_output)
    if len(a):
        return a[0]

host_container_ip = get_container_ip (host_container)
print(host_container_ip)

def sys_cmd (jenkins_container_name, workdir, cmd):
    import os
    command = "docker exec -it --workdir=" + workdir + " " + jenkins_container_name
    # print(command)

    args = command.split(" ")
    args += cmd.split(" ")
    # print(args)

    ret = os.system(command + " " + cmd)

    return ret

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


def ls_known_hosts (jenkins_container_name, workdir):
    cmd="ssh-keyscan " + host_container_ip
    out = exec_cmd (jenkins_container_name, workdir, cmd)
    print (out)

    cmd="ls .ssh/known_hosts"

    ret = sys_cmd (jenkins_container_name, workdir, cmd)
    print (ret)

    
    if 0 == ret:
        pass
    else:
        cmd="touch .ssh/known_hosts"
        sys_cmd (jenkins_container_name, workdir, cmd)
        
    cmd="ssh-keyscan " + host_container_ip + " > .ssh/known_hosts"
    out = exec_cmd (jenkins_container_name, workdir, cmd)
    print (out)


#all_ls_ssh()
#ls_known_hosts ("jenkins-blueocean", "/var/jenkins_home")
ls_known_hosts ("agent",             "/home/jenkins")
#ls_known_hosts ("agent_android",     "/home/jenkins")
