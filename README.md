# Cómo usar la cámara de profundidad Intel Realsense D435 en una NVIDIA Jetson Nano.

Para usar la cámara de profundidad Intel Realsense D435 en una NVIDIA Jetson Nano es necesario tener el sistema operativo Ubuntu 16.04, 18.04 o 20.04, el SO recomendado es Ubuntu 20.04 LTS.

Con la cámara desconectada se empezará a configurar las librerías, paquetes y actualizaciones necesarias en la NVIDIA Jetson Nano.

1. Asegurar que la Herramienta Avanzada de Paquetería está actualizada:

    ```
    sudo apt-get update && sudp apt-get upgrade
    ```

2. Instalar Python 3 y sus archivos de desarrollo.

    ```
    sudo apt-get install python3 python3-dev python3-pip
    ```

3. Instalar `Numpy` y `OpenCV` por medio de PIP.

    ```
    pip3 install numpy  
    pip3 install opencv-python
    ```

4. Registrar las llaves públicas del servidor de la librería `librealsense`.

    ```
    sudo apt-key adv --keyserver keyserver.ubuntu.com  --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key
    ```

5. Añadir el server a la list de repositorios.

    ```
    sudo add-apt-repository "deb https://librealsense.intel.com/Debian/apt-repo $(lsb_release -cs) main" -u
    ```

6. Instalar el SDK.

    ```
    sudo apt-get install apt-utils -y  
    sudo apt-get install librealsense2-utils librealsense2-dev -y
    ```

## Utilizar Python para leer la cámara de profundidad Intel RealSense D435.

1. Se instalan las herramientas de Python necesarias para la utilización.

    ```
    sudo apt-get update && sudo apt-get -y upgrade
    sudo apt-get install -y --no-install-recommends \
        python3 \
        python3-setuptools \
        python3-pip \
        python3-dev
    ```
   
2. Instalar los paquetes core necesarios para acceder a la información de la cámara desde Python.

    ```
    sudo apt-get install -y git libssl-dev libusb-1.0-0-dev pkg-config libgtk-3-dev
    sudo apt-get install -y libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev
    ```
    
3. Clonar el repositorio de librealsense.

    ```
    git clone https://github.com/IntelRealSense/librealsense.git
    cd ./librealsense
    ```
    
4. Ejecutar el archivo que habilita los permisos de utilización de la cámara.

    ```
    ./scripts/setup_udev_rules.sh
    ```
    
5. Preparar la compilación de paquetes.

    ```
    mkdir build && cd build
    ```
    
    Compilar los paquetes de Python.
    
    ```
    cmake ../ -DBUILD_PYTHON_BINDINGS:bool=true
    ```
    
    Recompilar los archivos binarios de configuración.
    
    ```
    sudo make uninstall && sudo make clean && sudo make -j4 && sudo make install
    ```
    
6. Exportar variable de entorno para reconocer el paquete desde Python.

    ```
    export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.6/pyrealsense2
    ```
    
    Para que la variable de entorno no se reinicie cada vez que se apague la máquina se puede añadir el comando de exportación dentro del archivo `~/.bashrc`.
    
    Ahora Python es capaz de acceder a la información de la cámara de profundidad D435.
    
## Habilitando los pines GPIO de la Jetson Nano.

Para habilitar con Python el uso de los pines digitales de salida de la Jetson Nano, también llamados GPIO, son necesarias unas configuraciones.

1. Instalar las librerías de `Jetson.GPIO`.

    ```
    sudo pip install Jetson.GPIO
    sudo pip3 install Jetson.GPIO
    ```
    
2. Configurar los permisos del usuario.

    ```
    sudo groupadd -f -r gpio
    sudo usermod -a -G gpio your_user_name
    ```
    
    La variable `your_user_name` debe cambiarse por el nombre de usuario de la máquina.
    
3. Copiar el archivo `99-gpio.rules` en el directorio `rules.d`

    ```
    sudo cp etc/99-gpio.rules /etc/udev/rules.d/
    ```
    
4. Volver a cargar las reglas para que el archivo entre en vigor.

    ```
    sudo udevadm control --reload-rules && sudo udevadm trigger
    ```
    
    Ahora Python es capaz de controlar la salida de voltaje de los pines GPIO de la Jetson Nano.
    
## Configurar un servidor VNC en la Jetson Nano.

1. Habilitar el servidor VNC cada vez que se acceda a la Jetson Nano.

    ```
    mkdir -p ~/.config/autostart
    cp /usr/share/applications/vino-server.desktop ~/.config/autostart/.
    ```
    
2. Configurar el servidor VNC

    ```
    gsettings set org.gnome.Vino prompt-enabled false
    gsettings set org.gnome.Vino require-encryption false
    ```
    
3. Configurar una contraseña de acceso al servidor VNC

    ```
    gsettings set org.gnome.Vino authentication-methods "['vnc']"
    gsettings set org.gnome.Vino vnc-password $(echo -n 'thepassword'|base64)
    ```
    
    La cadena `thepassword` se sustituye por la contraseña deseada
    
4. Reiniciar el sistema para aplicar los cambios

    ```
    sudo reboot
    ```
    
    Ahora la Jetson Nano cuenta con un servidor VNC cada vez que se accede a ella.
    
    Para poder acceder por medio de VNC desde otra computadora se puede utilizar un software como VNC Viewer especificando la red, el usuario y la contraseña del servidor VNC de la Jetson Nano.
    
## Habilitar el acceso automático a la Jetson Nano.

Para poder acceder a la Jetson Nano sin necesidad de que se pida un usuario y una contraseña al inicio, es necesario habilitar el inicio de sesión automático, para esto se realiza lo siguiente:

Abrir "Unity launcher" de la pantalla principal, ejecutar la aplicación "User Accounts", dar click en "Unlock" del botón de la esquina superior derecha de la ventana, escribir la contraseña requerida y habilitar la opción "Enable/Disable Automatic Login for your Account".

Con esto ahora cada vez que se encienda la Jetson Nano se accederá directamente a la pantalla principal sin requerir usuario y contraseña.

## Configurar la ejecución automática de un archivo de Python

Para que el programa principal se ejecute con tan solo encender la Jetson Nano es necesaria la siguiente configuración:

1. Crear un archivo llamado `/usr/local/bin/python.sh` donde adentro de este archivo se tengan los comandos necesarios para ejecutar el archivo de Python, por ejemplo:

    ```
    #!/bin/bash
    python3 ~/project/opencv_pyrealsense2.py
    ```
    
2. Cambiar sus permisos de ejecución.

    ```
    sudo chmod +x /usr/local/bin/python.sh
    ```
    
3. Crear un archivo llamado `/etc/systemd/system/python.service`.

4. En este archivo poner le siguiente texto:

    ```
    [Unit]
    Description=python: initialize my python script
    After=multi-user.target

    [Service]
    ExecStart=/usr/local/bin/python.sh
    Restart=always
    StartLimitInterval=10
    RestartSec=10

    [Install]
    WantedBy=multi-user.target
    ```
    
5. Correr los siguiente comando en la terminal para habilitar e iniciar el servicio.

    ```
    sudo systemctl enable mything.service
    sudo systemctl start mything.service
    ```
    
Ahora el programa de Python se ejecutará cada vez que inicie la máquina.
