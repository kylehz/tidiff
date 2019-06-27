## tidbdiff

```
usage: tidbdiff [-h] [-c CONFIG] [-p PKEY] remote_host_A remote_host_B

tidbdiff is a command line tool to show the difference of tidb config between tow host.
usage example: tidbdiff "user@example.com"  "example.com:50022"
user and remote ssh port are optional in remote_host


positional arguments:
  remote_host_A         remote host, example: user@example.com:22
  remote_host_B         another remote host, example: user@example.com:22

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        tidb config file path on remote host. default value is /etc/tidb/tidb.toml
  -p PKEY, --pkey PKEY  ssh pkey path. default value is ~/.ssh/id_rsa
```

### install & build
use python3

install dependence:

```
pip3 install -r requirements.txt
```

build binary file

```
pyinstaller -Fw tidbdiff.py
```

### binary file
you can download binary file and use it immediately

[centos7](https://github.com/kylehz/tidiff/releases/download/0.1/tidiff_centos7)

[macosx10.12](https://github.com/kylehz/tidiff/releases/download/0.1/tidiff_macosx_10_12)
