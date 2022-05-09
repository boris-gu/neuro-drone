# neuro-drone
Передача команд на БВС под управлением PX4+ROS через UDP сокеты.
```bash
git clone --recurse-submodules https://github.com/boris-gu/neuro-drone.git
```

## Описание скриптов
### server-drone.py
Скрипт запускается на бортовом компьютере БВС.

**Зависимости**  
Зависимости, необходимые для работы **drone_api**, а именно:
* ROS Noetic
* Python3
* MavROS
* OpenCV-Python
* GeographicLib
* PyGeodesy


При запуске можно указать параметр **`-l`**, **`--logfile`**, тогда основная информация о работе скрипта и все поступающие на сервер данные будут сохранены в файл с названием **`neuroLog_<TIME>.txt`**, например, **`neuroLog_2022.05.08 22:19:44.txt`**. Запись ведется от момента старта БВС (**не старта скрипта!**) и до окончания полета.

Сервер дожидается данных на порте **50202**, после чего проверяет их на корректность и, если они корректны, выполняет полученную команду.


### client-human.py
Скрипт запускается на компьютере пользователя. Компьютер пользователя и бортовой компьютер БВС должны быть подключены к одной сети. На данный момент команды для БВС вводятся через терминал, но скрипт написан с расчетом на то, что его легко возможно отредактировать на получение данных с нейроинтерфейса.

**Зависимости**
* Python3

По умолчанию клиент отправляет данные на хост **localhost** (работает для тестирования в симуляторе), порт **50202**. Но хост можно поменять при запуске, указав параметр --host и записав после него IP-адрес БВС. Например:
```bash
./client-human.py --host 192.168.255.121
```
После запуска клиент выведет хост, на который будет отправлять данные, и приглашение на ввод команд. 

## Команды 
Предполагается, что нейроинтерфейс может подавать команды в диапазоне 0-100, где 0 - это максимальное расслабление, 100 - максимальное напряжение. Соответственно, 0 - остановка БВС, 100 - движение с максимально заданной скоростью в одном из направлений.

Команда, отправляемая клиентом, строится следующим образом: **первая буква направления движения+сила команды [0-100]**  
**Направления:**
* Up
* Down
* Forward
* Back
* Left
* Right

**Также существует ряд особых команд:**
* start - БВС заводит моторы и поднимается на высоту 3 метра. После подъема сервер готов принимать данные от клиента. Если задано, сервер начинает писать лог в файл.
* stop - БВС медленно садится и после посадки останавливает моторы. Если задано, файл с логами сохраняется.
* Пустая строка - БВС прекращает какое либо движение, зависает в одной точке

### Примеры команд:
```bash
start
u100
    # Примечание: это пустая строка, тоже команда
l77
r33

d50
stop
```

## Запуск
### В Gazebo
1. Запустите симулятор
    ```bash
    DONT_RUN=1 make px4_sitl_default gazebo
    source Tools/setup_gazebo.bash $(pwd) $(pwd)/build/px4_sitl_default && \
    export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd) && \
    export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd)/Tools/sitl_gazebo
    roslaunch px4 mavros_posix_sitl.launch
    ```
2. Запустите скрипт `server-drone.py`.
3. Запустите скрипт `client-human.py` и начните вводить команды.

### Запуск на БВС
Проводятся тесты