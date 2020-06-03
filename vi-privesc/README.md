Privilege escalation challenge.

Credentials to the SSH server is user:haaukins
Solution: The attacker is expected to use vi (which is allowed to run as super user) to access bash.
Once the attacker accessed the bash, the script can be run and flag will be printed.

Reference here to build and run the container: https://docs.docker.com/engine/examples/running_ssh_service/