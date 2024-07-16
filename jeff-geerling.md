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
      service: name=ntpd state=started enabled=yes
```

> Idempotency

Nothing changes if done once.

> How ansible modules makes things easier
```
---
- hosts: all
  become: yes
  tasks:
    - name: Ensure NTP is installed
    - shell: |
        if ! rpm -qa | grew -qw ntp; then
         yum install -y ntp
        fi
    - name: Ensure NTP is running
      service: name=ntpd state=started enabled=yes
```

> Good to name the plays as well if there are multiple in the playbook

```
---

- name: Setup NTP on all servers
  hosts: all
  become: yes
  tasks:
    - name: Ensure NTP is installed
    - shell: |
        if ! rpm -qa | grew -qw ntp; then
         yum install -y ntp
        fi
    - name: Ensure NTP is running
      service: name=ntpd state=started enabled=yes
```



Chapter 3 (missed to commit chapter2)

> Multi-host adhoc orchestration

ansible -i inventory multi -b -B 3600 -P 0 "yum update -y"

ansible -i inventory db -b -m async_status -a "jid=999996518999.17"


> check logs
```
ansible -i inventory multi -b -a "tail /var/log/messages"

ansible -i inventory multi -b -m shell -a "tail /var/log/messages | grep ansible-command | wc -l"   
# need to use shell as | is not allowed by ansible command module

ansible -i inventory multi -b -m cron -a "name=abc hour=3 job=/path//script.sh"
```

> cloning a Git repository onto multiple hosts 
```
ansible -i inventory multi -b -m git "repo=github_url dest=/opt/app update=yes version=1.2.4"
```

> With pipelining enabled (pipelining = True), Ansible sends multiple tasks over the same SSH connection, which can significantly reduce the connection setup time and overall execution time, especially for large playbooks or configurations involving many tasks.
ansible.cfg

[ssh_connection]
pipelining = True


> Intro to playbooks

inventory
```
[ec2]
35.175.148.144

[ec2:vars]
ansible_user=centos
ansible_ssh_private_key_file=~/.ssh/bhanu_malhotra_aws.pem

```

shell-script.sh
```
# Install Apache
yum install --quiet -y httpd httpd-devel
# Copy configuration files.
cp httpd.conf /etc/httpd/conf/httpd.conf
cp httpd-vhosts /etc/httpd/conf/httpd-vhosts.conf
# Start Apache and configure it to run at boot
service httpd start
chkconfig httpd on
```

playbook.yml

```
---
- name: Install Apache
  hosts: all

  tasks:
    - name: Install Apache
      command: yum install --quiet -y httpd httpd-devel

    - name: Copy configuration files
      command: >
        cp httpd.conf /etc/httpd/conf/httpd.conf
    - command: >
        cp httpd-vhosts /etc/httpd/conf/httpd-vhosts.conf

    - name: Start Apache and configure it to run at boot.
      command: service httpd start
    - command: chkconfig httpd on
        


```

```
---
- name: Install Apache
  hosts: all

  tasks:
    - name: Install Apache
      shell: |
        yum install --quiet -y httpd httpd-devel
        cp httpd.conf /etc/httpd/conf/httpd.conf
        cp httpd-vhosts /etc/httpd/conf/httpd-vhosts.conf
        
```

```


---

- name: Install Apache
  hosts: all
  become: true                             # root user needed

  tasks:
    - name: Install Apache
      yum:
        name:
          - httpd
          - httpd-devel
        state: present


    - name: Copy configuration files
      copy:
        src: "{{ item.src }}"            # In both Ansible and Helm, "mustaches" typically refer to template placeholders used for variable substitution.
        dest: "{{ item.dest }}"
        owner: root
        group: root
        mode: 0644
      with_items:
        - src: httpd.conf
          dest: /etc/httpd/conf/httpd.conf
        - src: httpd-vhosts
          dest: /etc/httpd/conf/httpd-vhosts.conf
     - name: Make sure Apache is started now at boot
       service:
         name: httpd
         state: started
         enabled: yes
        
```

```
ansible-playbook -i inventory playbook.yml
```

```
ansible-playbook -i inventory multi --limit=
```

```
ansible-inventory --list -i inventory
```


Chapter 4
