openssl req -x509 -days 365 -sha256 -key key.pem -out certificate.pem -extensions v3_self_signed -config openssl.cnf

openssl x509 -outform der -in certificate.pem -out certificate.der