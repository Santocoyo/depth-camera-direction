# Cómo usar la cámara de profundidad Intel Realsense D435 en una NVIDIA Jetson Nano

Para usar la cámara de profundidad Intel Realsense D435 en una NVIDIA Jetson Nano es necesario tener el sistema operativo Ubuntu 16.04, 18.04 o 20.04, el SO recomendado es Ubuntu 20.04 LTS.

Con la cámara desconectada se empezará a configurar las librerías, paquetes y actualizaciones necesarias en la NVIDIA Jetson Nano.

1. Asegurar que la Herramienta Avanzada de Paquetería está actualizada:

    ```
    sudo apt-get update && sudp apt-get upgrade
    ```

2. Instalar Python 3 y sus archivos de desarrollo

    ```
    sudo apt-get install python3 python3-dev python3-pip
    ```

3. Instalar `Numpy` y `OpenCV` por medio de PIP

    ```
    pip3 install numpy  
    pip3 install opencv-python
    ```

4. Registrar las llaves públicas del servidor de la librería `librealsense`

    ```
    sudo apt-key adv --keyserver keyserver.ubuntu.com  --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key
    ```

5. Añadir el server a la list de repositorios

    ```
    sudo add-apt-repository "deb https://librealsense.intel.com/Debian/apt-repo $(lsb_release -cs) main" -u
    ```

6. Instalar el SDK

    ```
    sudo apt-get install apt-utils -y  
    sudo apt-get install librealsense2-utils librealsense2-dev -y
    ```








