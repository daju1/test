#/bin/bash
#
# stderr: No ED25519 host key is known for 172.18.0.7 and you have requested strict checking.
# Host key verification failed.


get_container_ip ()
{
	host_container_name=$1
	docker exec -it $host_container_name ifconfig | grep inet | grep Bcast | awk -F " " '{print $2}'| awk -F ":" '{print $2}'
}

exec_cmd ()
{
   jenkins_container_name=$1
	workdir=$2
	cmd=$3
	docker exec -it --workdir=${workdir} ${jenkins_container_name} ${cmd}
}

all_ls_ssh_ ()
{
	exec_cmd jenkins-blueocean /var/jenkins_home "ls .ssh"
	exec_cmd agent             /home/jenkins     "ls .ssh"
	exec_cmd agent_android     /home/jenkins     "ls .ssh"
}

all_ls_ssh ()
{
	cmd="ls .ssh"
	exec_cmd jenkins-blueocean /var/jenkins_home ${cmd}
	exec_cmd agent             /home/jenkins     ${cmd}
	exec_cmd agent_android     /home/jenkins     ${cmd}
}


#all_ls_ssh


ls_ssh ()
{
	docker exec -it --workdir=/var/jenkins_home jenkins-blueocean  ls .ssh
	docker exec -it --workdir=/home/jenkins     agent              ls .ssh
	docker exec -it --workdir=/home/jenkins     agent_android      ls .ssh
}

ls_known_hosts ()
{
	docker exec -it --workdir=/var/jenkins_home jenkins-blueocean  ls .ssh/known_hosts
	docker exec -it --workdir=/home/jenkins     agent              ls .ssh/known_hosts
	docker exec -it --workdir=/home/jenkins     agent_android      ls .ssh/known_hosts
}

cat_known_hosts ()
{
	docker exec -it --workdir=/var/jenkins_home jenkins-blueocean  cat .ssh/known_hosts
	#docker exec -it --workdir=/home/jenkins     agent              cat .ssh/known_hosts
	#docker exec -it --workdir=/home/jenkins     agent_android      cat .ssh/known_hosts
}

host_container=ubivisgmbh_git_server

key_scan ()
{
	docker exec -it --workdir=/var/jenkins_home jenkins-blueocean  ssh-keyscan $(get_container_ip ${host_container})
	#docker exec -it --workdir=/home/jenkins     agent              `ssh-keyscan $(get_container_ip ${host_container})`
	#docker exec -it --workdir=/home/jenkins     agent_android      `ssh-keyscan $(get_container_ip ${host_container})`
}

key_add ()
{
	docker exec -it --workdir=/var/jenkins_home jenkins-blueocean  ssh-keyscan "$(get_container_ip ${host_container}) >> /var/jenkins_home/.ssh/known_hosts"
	#docker exec -it --workdir=/home/jenkins     agent              "ssh-keyscan $(get_container_ip ${host_container}) >> .ssh/known_hosts"
	#docker exec -it --workdir=/home/jenkins     agent_android      `ssh-keyscan $(get_container_ip ${host_container}) >> .ssh/known_hosts`
}

#pwd_workdir
#ls_ssh
#ls_known_hosts
# 
key_scan
key_add
cat_known_hosts





