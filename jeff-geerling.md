Chapter 1

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

> inventory
```
[solr]
54.210.120.211 ansible_user=ubuntu

```

> main.yml
```
---
- hosts: solr
  become: true
  vars_files:
    - vars.yml
  pre_tasks:
    - name: Update apt cache if needed
      apt:
        update_cache: true
        cache_valid_time: 3600
  handlers:
    - name: restart solr
      service: name=solr state=restarted
  tasks:
     - name: Install java
       package: name=openjdk-8-jdk state=present
     - name: Install solr
       get_url:
         url: "https://mirrors.ocf.berkeley.edu/apache/lucene/solr/{{ solr_version }}/{{ solr_version }}.tgz"
         dest: "{{ download_dir }}/solr-{{ solr_version }}.tgz "
         checksum: "{{ solr_checksum }}"
     - name: Expand Solr
       unarchive:
         src: "{{ download_dir }}"/solr-{{ solr-version }}.tgz
         dest: "{{ download_dir }}"
         remote_src: true            # by default unarchive copies from local to remote and then unarchive. If your file is already at remote, set this to true so that it doesn't copy.
         creates: " {{ download_dir/solr-{{ solr_version }}/README.txt}}"   # Ansible will check if this file exists. If it does, Ansible will consider the task successful and will not run the unarchive task again unless the file (readme.txt) is removed or the task is forced to run.
     - name: Run Solr installation script
       command: >
         {{ download_dir }}/solr-{{ solr_version }}/bin/install_solr
         {{ download_dir }}/solr-{{ solr_version }}.tgz
         -i /opt
         -d /var/solr
         -u solr
         -s solr
         -p 8983
         creates={{ solr_dir }}/bin/solr
     - name: Ensure solr is started and enabled at boot
       service:
         name: solr
         state: started
         enabled: yes     
```

> vars.yml
```
---
download_dir: /dir
solr_dir: /opt/solr
solr_version: 8.5.0
solr_checksum: sha512:7e16aa71fc01f9d9b05e5514e35798104a18253a211426aa669aa3b91225d110a4fa1c78c9ec86b7e1909e2aae63696deffd877536790303cd0638eb7f1a8c63
https://www.apache.org/dyn/closer.lua/solr/solr/9.6.1/solr-9.6.1.tgz?action=download
```


> To check if yml is valid or not
```
ansible-playbook main.yml --syntax-check
```

> Run the playbook
```
ansible-playbook -i inventory main.yml

```


Chapter 5

apache.yml
```
---
- name: Install Apache
  hosts: centos
  become: true

  handlers:
    - name: restart apache
      service:
        name: httpd
        state: restarted

  tasks:
    - name: Ensure Apache is installed.
      yum:
        name: httpd
        state: present
    - name: Copy test config file
      copy:
        src: files/test.conf
        dest: /etc/httpd/conf.d/test.conf        # whenever this result in change it calls the handler
        notify: restart apache
    - name: Make sure handlers are flushed immediately.
      meta: flush_handlers                                    # if you don't use this handlers will be executed at the end of the playbook so flush_handlers are used for setting when to run the handlers

    - name: Ensure Apache is running and starts at boot.
      service:
        name: httpd
        state: started
        enabled: true

    - fail:  
```



```
---
- name: Install Apache
  hosts: centos
  become: true

  handlers:
    - name: restart apache
      service:
        name: httpd
        state: restarted

  tasks:
    - name: Ensure Apache is installed.
      yum:
        name: httpd
        state: present
    - name: Copy test config file
      copy:
        src: files/test.conf
        dest: /etc/httpd/conf.d/test.conf        # whenever this result in change it calls the handler
        notify: restart apache

    - name: Ensure Apache is running and starts at boot.
      service:
        name: httpd
        state: started
        enabled: true

    - fail:                                    # this will fail the playbook after the tasks above it, so no handler will run.
```


- Handlers run end of playbook if flush_handlers isn't used.


```
---
- name: Install Apache
  hosts: centos
  become: true

  handlers:
    - name: restart apache
      service:
        name: httpd
        state: restarted
    - name: restart memcached
      service:
        name: memcached
        state: restarted

  tasks:
    - name: Ensure Apache is installed.
      yum:
        name: httpd
        state: present
    - name: Copy test config file
      copy:
        src: files/test.conf
        dest: /etc/httpd/conf.d/test.conf        # whenever this result in change it calls the handler
        notify:
          - restart apache
          - restart memcached                  # one more handler
    - name: Ensure Apache is running and starts at boot.
      service:
        name: httpd
        state: started
        enabled: true
```



```
---
- name: Install Apache
  hosts: centos
  become: true

  handlers:
    - name: restart apache
      service:
        name: httpd
        state: restarted
      notify: restart memcached                  # one handler starts the other handler (so handlers are nothing but tasks in ansible which can be called.)
    - name: restart memcached
      service:
        name: memcached
        state: restarted

  tasks:
    - name: Ensure Apache is installed.
      yum:
        name: httpd
        state: present
    - name: Copy test config file
      copy:
        src: files/test.conf
        dest: /etc/httpd/conf.d/test.conf        # whenever this result in change it calls the handler
        notify:
          - restart apache

    - name: Ensure Apache is running and starts at boot.
      service:
        name: httpd
        state: started
        enabled: true
```


> Environment variables

```
---
- name: Install Apache
  hosts: centos
  become: true

  handlers:
    - name: restart apache
      service:
        name: httpd
        state: restarted
  tasks:
    - name: Add an environment variable to the remote user's shell.
      lineinfile:
        dest:"~/.bash_profile"
        regexp: '^ENV_VAR='
        line: 'ENV_VAR=value'
        become: false        # switches off sudo
   - name: Get the value of an environment variable.
     shell: 'source ~/.bash_profile && echo $ENV_VAR'
```
