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
    print(args)

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


def add_known_hosts (jenkins_container_name, workdir, host_container_ip):
    cmd = "ssh-keyscan " + host_container_ip
    out = exec_cmd (jenkins_container_name, workdir, cmd)
    print (out)

    cmd = "ls .ssh"
    ret = sys_cmd (jenkins_container_name, workdir, cmd)
    if 0 == ret:
        pass
    else:
        cmd="mkdir .ssh"
        sys_cmd (jenkins_container_name, workdir, cmd)

    cmd = "ls .ssh/known_hosts"
    ret = sys_cmd (jenkins_container_name, workdir, cmd)
    if 0 == ret:
        pass
    else:
        cmd="touch .ssh/known_hosts"
        sys_cmd (jenkins_container_name, workdir, cmd)

    #ret = sys_cmd (jenkins_container_name, workdir, "find / -name scan-host-key.sh")

    cmd = "/scan-host-key.sh " + host_container_ip
    out = exec_cmd (jenkins_container_name, workdir, cmd)
    print (out)

    #cmd = "cat .ssh/known_hosts"
    #ret = sys_cmd (jenkins_container_name, workdir, cmd)

def ssh_keygen_R (jenkins_container_name, workdir, host_container_ip):
    cmd = "ls -la .ssh"
    out = exec_cmd (jenkins_container_name, workdir, cmd)
    print (jenkins_container_name, workdir, cmd, " -->" ,out)

    cmd = 'ssh-keygen -f "' + workdir + '/.ssh/known_hosts" -R ' + host_container_ip
    out = sys_cmd (jenkins_container_name, workdir, cmd)
    print (out)

def view_pub_key (jenkins_container_name, workdir):
    cmd = "pwd"
    cmd = "ls -la .ssh"
    out = exec_cmd (jenkins_container_name, workdir, cmd)
    print (jenkins_container_name, workdir, cmd, " -->" ,out)

    cmd = "cat .ssh/authorized_keys"
    out = exec_cmd (jenkins_container_name, workdir, cmd)
    print (jenkins_container_name, workdir, cmd, " -->" ,out)

    #cmd = "ls -la agent"
    #cmd = "ls -la"
    #ret = sys_cmd (jenkins_container_name, workdir, cmd)
    #print(ret)

def add_jenkins_agent_known_host (host_container):
    host_container_ip = get_container_ip (host_container)
    if host_container_ip is not None:
        print(host_container + " IP is " + host_container_ip)

        #add_known_hosts ("jenkins-blueocean", "/var/jenkins_home", host_container_ip)
        ssh_keygen_R    ("jenkins_sandbox", "/var/jenkins_home", host_container_ip)
        add_known_hosts ("jenkins_sandbox", "/var/jenkins_home", host_container_ip)

def add_git_server_known_host (host_container):
    host_container_ip = get_container_ip (host_container)
    if host_container_ip is not None:
        print(host_container + " IP is " + host_container_ip)
        #return

        ssh_keygen_R    ("jenkins_sandbox",       "/var/jenkins_home", host_container_ip)
        add_known_hosts ("jenkins_sandbox",       "/var/jenkins_home", host_container_ip)
        ssh_keygen_R    ("jenkins_agent",         "/home/jenkins",     host_container_ip)
        add_known_hosts ("jenkins_agent",         "/home/jenkins",     host_container_ip)
        ssh_keygen_R    ("jenkins_agent_android", "/home/jenkins",     host_container_ip)
        add_known_hosts ("jenkins_agent_android", "/home/jenkins",     host_container_ip)

#view_pub_key("jenkins_agent", "/home/jenkins")

add_jenkins_agent_known_host ("jenkins_agent")
add_jenkins_agent_known_host ("jenkins_agent_android")

add_git_server_known_host ("git_server_jkarlos")
add_git_server_known_host ("git_server_ubivisgmbh")
add_git_server_known_host ("git_server_rockstorm")
# view_pub_key("git_server_rockstorm", "/home/git")
#view_pub_key("rockstorm_git_server", "/home/git")
#add_git_server_known_host ("rockstorm_git_server")