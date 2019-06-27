import re
import paramiko
from scp import SCPClient
import os
import uuid
import util

class ScpConn():
	def __init__(self, user, host, port, pkey_path):
		self.user = user
		self.host = host
		self.port = port
		self.pkey_path = pkey_path
	def __enter__(self):
		ssh_pkey = paramiko.RSAKey.from_private_key_file(os.path.expanduser(os.path.normpath(self.pkey_path)))
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(self.host, 
			port=self.port,
			username=self.user,
			pkey = ssh_pkey,
			)
		scp = SCPClient(ssh.get_transport())
		self.scp = scp
		return scp

	def __exit__(self, type, value, traceback):
		self.scp.close()

def get_file_content(scp, remote_path):
	local_path = "/tmp/tidbdff_%s" % uuid.uuid4()
	scp.get(remote_path, local_path)
	with open(local_path, 'r') as f:
		content = f.read()
		os.remove(local_path)
		return content

def fetch(user, host, port, pkey_path, remote_path):
	with ScpConn(user, host, port, pkey_path) as scp:
		return get_file_content(scp, remote_path)

def parse_remote_host(remote_host):
	g = re.match(r'(\w*@)?(.*)', remote_host)
	if not g or len(g.groups()) != 2:
		raise Exception('remote_host not valid: %s' % remote_host)
	user = g.group(1)
	if user:
		user = user.rstrip('@')
	else:
		user = 'root'
	host_port = g.group(2).split(':')
	host = host_port[0]
	if len(host_port) == 2:
		port = int(host_port[1])
	else:
		port = 22
	return user, host, port

def fetch_with_url(remote_host, pkey_path, remote_path):
	print("fetch %s from %s ..." % (remote_path, remote_host))
	user, host, port = parse_remote_host(remote_host)
	remote_path = remote_path
	return fetch(user, host, port, pkey_path, remote_path)

def prase_security_limits(t):
	result = {}
	def get_by_attr(attr1, attr2):
		g = re.search(r"\*[ \t]*%s[ \t]*%s[ \t]*(\d+)" % (attr1, attr2), t)
		if g and len(g.groups()) == 1:
			result["%s_%s" % (attr1, attr2)] = int(g.group(1))
		else:
			result["%s_%s" % (attr1, attr2)] = None
	get_by_attr("hard", "nofile")
	get_by_attr("soft", "nofile")
	get_by_attr("hard", "nproc")
	get_by_attr("soft", "nproc")
	return result

def prase_os_release(t):
	t = util.prase_kv_file(t)
	result = {
		"os" : t.get("ID", None),
		"version" : t.get("VERSION_ID", None)
	}
	return result

def prase_sys_vm_overcommit_memory(t):
	return t

def gather_facts(remote_host, pkey_path):
	print("gather facts from %s ..." % remote_host)
	user, host, port = parse_remote_host(remote_host)
	facts = {}
	with ScpConn(user, host, port, pkey_path) as scp:
		facts["security_limits"] = prase_security_limits(get_file_content(scp, "/etc/security/limits.conf"))
		facts["os"] = prase_os_release(get_file_content(scp, "/etc/os-release"))
		facts["sys_vm_overcommit_memory"] = prase_sys_vm_overcommit_memory(get_file_content(scp, "/proc/sys/vm/overcommit_memory"))
	return facts

