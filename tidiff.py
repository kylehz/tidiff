import remote
import argparse
import ticonfig
import linuxconfig

fetch_remote_file = remote.fetch_with_url
gather_facts = remote.gather_facts

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='''
tidbdiff is a command line tool to show the difference of tidb config between tow host.
usage example: tidbdiff "user@example.com"  "example.com:50022"
user and remote ssh port are optional in remote_host
		''', formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('remote_host_A', action='store', help='remote host, example: user@example.com:22')
	parser.add_argument('remote_host_B', action='store', help='another remote host, example: user@example.com:22')
	parser.add_argument('-c', '--config', dest='config', action='store',
	                    help='tidb config file path on remote host. default value is /etc/tidb/tidb.toml', default='/etc/tidb/tidb.toml')
	parser.add_argument('-p', '--pkey', dest='pkey', action='store',
	                    help='ssh pkey path. default value is ~/.ssh/id_rsa', default='~/.ssh/id_rsa')
	args = parser.parse_args()

	try:
		ticonfig.print_diff(
			fetch_remote_file(args.remote_host_A, args.pkey, args.config),
			fetch_remote_file(args.remote_host_B, args.pkey, args.config))
		linuxconfig.print_diff(
			gather_facts(args.remote_host_A, args.pkey),
			gather_facts(args.remote_host_B, args.pkey))
	except Exception as e:
		print(e)
	