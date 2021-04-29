#!/bin/bash
if [[ $(id -u) -ne 0 ]] ; then
    echo "É nescessário privilégios de superuser."
    sudo bash setup-ambiente-relatorio.sh
else
    echo "======================================================"
    echo "Instalando dependências do módulo relatório-automático"
    echo "======================================================"
    
    sudo apt update
    sudo apt install python3
    sudo apt install python3-pip
    sudo pip3 install pyModbusTCP
    sudo pip3 install wappdriver
    sudo pip3 install django

    
    #Driver para o MSSQL
    #sudo apt  install curl
    #sudo curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
    #sudo curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
    #sudo apt update
    #sudo ACCEPT_EULA=Y apt-get install msodbcsql17
    #sudo ACCEPT_EULA=Y apt-get install mssql-tools
    #echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
    #echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
    #source ~/.bashrc
    #sudo apt-get install unixodbc-dev 
    #sudo pip3 install pyodbc
    #sudo pip3 install numpy
    #sudo pip3 install pandas
    #sudo pip3 install matplotlib
    #sudo pip3 install reportlab
    
    
fi
