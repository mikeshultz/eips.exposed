# Ansible Deployment

These playbooks will stand up a CentOS system, install docker, and build and
run the containers for eips.exposed.

## Quickstart

    ansible-playbook ops/ansible/main.yaml

## Prerequesites

- Install ansible locally
- Configure SSH with keys for direct access to the machine(s)
- Configure sudo on remote systems to be available to the user without a password
