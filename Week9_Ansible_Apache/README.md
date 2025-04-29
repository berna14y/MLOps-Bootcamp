## Apache Configuration with Ansible
This repository contains the files and documentation for the homework assignment focused on containerization, automation, and web server management using Ansible and Apache. The goal was to configure Apache web servers on test and prod environments using Ansible playbooks and display custom content on the web interface.

#### Table of Contents

Overview
Files Included
How to Replicate the Setup
Screenshots
Conclusion

#### Overview

The homework assignment involved the following tasks:

1) Prepare a Jenkins container as an Ansible server.
2) Install and configure Ansible within the Jenkins container.
3) Create an Ansible playbook to install and configure Apache on test and prod containers.
4) Customize the Apache configuration to:
    Listen on different ports (8001 for test and 8000 for prod).
    Display a custom index.html page with your name and server type.
5) Verify the setup by accessing the web interface and confirming the Apache service status.

#### Files Included

The following files are included in this submission:

1) apache_setup.yml:
    The Ansible playbook used to install and configure Apache on the test and prod servers.
    Key tasks:
        Install Apache (httpd).
        Create a custom index.html file.
        Configure Apache to listen on custom ports.
        Start the Apache service manually.
2) inventory:
    The Ansible inventory file defining the test and prod servers.
    Includes connection details such as:
        Hostnames (test_server, prod_server).
        Username (root).
        Password (Ankara_06).
        SSH arguments to disable host key checking.
3) Screenshots:
    Browser Screenshots:
        Test Server: http://<docker-host-ip>:8001 showing My name is Berna Yılmaz on Test Server.
        Prod Server: http://<docker-host-ip>:8000 showing My name is Berna Yılmaz on Prod Server.
    Terminal Screenshots:
        Test Server: Terminal output showing the httpd process running.
        Prod Server: Terminal output showing the httpd process running.

#### How to Replicate the Setup

To replicate the setup, follow these steps:

###### 1. Set Up the Environment

1) Start the Docker Containers:
    Use the provided docker-compose.yml file to start the Jenkins, test_server, and prod_server containers.
    Run:
    docker-compose up -d

2) Access the Jenkins Container:
    Access the Jenkins container as the root user:
    docker exec -u root -it jenkins bash

3) Install Ansible and sshpass:
    Install Ansible and sshpass in the Jenkins container:
    apt update
    apt install -y ansible sshpass

###### 2. Configure SSH on test_server and prod_server

1) Access the test_server Container:
    Start the SSH service:
        /usr/sbin/sshd
    Set a password for the root user:
        passwd root

2) Repeat for the prod_server Container:
    Start the SSH service and set a password for the root user.

###### 3. Run the Ansible Playbook

1) Run the Playbook for the test_server:
    ansible-playbook -i /var/jenkins_home/inventory /var/jenkins_home/apache_setup.yml --extra-vars "server_type='Test Server' httpd_port=8001" -l test_server

2) Run the Playbook for the prod_server:
    ansible-playbook -i /var/jenkins_home/inventory /var/jenkins_home/apache_setup.yml --extra-vars "server_type='Prod Server' httpd_port=8000" -l prod_server

###### 4. Verify the Setup

1) Access the Web Interface:
    Test Server: http://<docker-host-ip>:8001
    Prod Server: http://<docker-host-ip>:8000
2) Check Apache Service Status:
    Access the containers and verify that Apache is running:
    ps aux | grep httpd

#### Screenshots
You can find screenshots in the file

#### Conclusion

This homework assignment demonstrated the use of Ansible for automating the installation and configuration of Apache web servers in a containerized environment.





