https://docs.ansible.com/

https://groups.google.com/g/ansible-project

https://www.ansible.com/blog/

Installation -  
pip3 install ansible
ansible --version

ssh user@hostname


> inventory

[example]  
ip

> module
  
ansible -i inventory example -m ping -u centos
  
> ansible.cfg

INVENTORY = inventory

https://docs.ansible.com/ansible/latest/reference_appendices/config.html#ansible-configuration-settings-locations



> adhoc

ansible example -a "free -h" -u centos

ansible example(all servers in ansible group)  (cmd is the bydefault module) -a(adhoc) "free -h" -u(user) centos


> playbook
```
---
- hosts: all
  become: yes
  tasks:
    - name: Ensure NTP is installed
      yum: name=ntp state=present
    - name: Ensure NTP is running
      service: name=ntpd state=started enable=yes
    
      
