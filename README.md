# dummy_https

The code is based on https://gist.github.com/Alexufo/2303bff77f0a16ba83568f0260b8cf47

To generate certificate and key files:

~~~~~
$ openssl req -new -newkey rsa:4096 -nodes -keyout dummy.key -out dummy.csr
$ openssl x509 -req -sha256 -days 365 -in dummy.csr -signkey dummy.key -out dummy.pem
~~~~~




