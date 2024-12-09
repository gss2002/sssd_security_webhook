 docker build . -t sssd_security_webhook:latest
 docker tag  sssd_security_webhook:latest registry.devops.senia.org/k8s/images/sssd_security_webhook:latest
 docker push registry.devops.senia.org/k8s/images/sssd_security_webhook:latest
