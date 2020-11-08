# PEAK CAN USB 설치

작성자 : djjin

Ubuntu 16.04 LTS에서 peak can usb driver 설치하기

https://www.peak-system.com/fileadmin/media/linux/index.htm

[TOC]

## 1. Installing PCAN Driver Package

1. 파일 다운받은 뒤 압출 풀기

   gcc-multilib package 설치

   ```
    $ sudo apt-get update -y
    $ sudo apt-get install -y gcc-multilib
   ```

2. 패키지 설치 후

   압축해제된 파일 폴더로 이동

   ~~~
   $ sudo apt-get install libelf-dev
   $ sudo apt-get install libpopt-dev
   $ cd peak-linux-driver-8.10.1
   $ make
   ~~~

3. 빌드 후 인스톨

   ~~~
   $ make -C lib 
   $ make -C test 
   $ sudo make install 
   ~~~

4. 설치가 제대로 되었는지 확인

   ~~~
   $ sudo modprobe pcan
   $ pcaninfo
   ~~~

   

## 2. PCAN-View 설치

~~~
$ wget -q http://www.peak-system.com/debian/dists/`lsb_release -cs`/peak-system.list -O- | sudo tee /etc/apt/sources.list.d/peak-system.list

$ wget -q http://www.peak-system.com/debian/dists/wheezy/peak-system.list -O- | sudo tee /etc/apt/sources.list.d/peak-system.list

$ wget -q http://www.peak-system.com/debian/peak-system-public-key.asc -O- | sudo apt-key add -

$ sudo apt-get update
$ sudo apt-get install pcanview-ncurses
$ pcanview
~~~





# PCAN-TEST

https://github.com/jdj2261/PCAN-TEST.git

테스트 영상 : https://www.youtube.com/watch?v=ibM16Gtvp-s

## 1. Description

This is a test that turns on/off the RELAY2CAN LED by receiving SAS can data.

- pcan_cpp        (c++언어로 작성)
- pcan_python  (python언어로 작성)

## 2. Install and Excute

- git 저장소에서 PCAN-TEST 소스 clone

~~~
$ git clone https://github.com/jdj2261/PCAN-TEST.git
~~~

- pcan_cpp와 pcan_python 2개로 나누어져 있음

  - pcan_cpp

    ~~~
    $ cd pcan_cpp/libcanbasic/examples/c++
    $ ./umd_pcan
    ~~~

    각도 입력하면 프로그램 실행

    @ 실행 파일을 추가하거나 수정할 일이 있을 때

    -  Makefile을 수정 후

      ~~~
      $ make clean
      $ make
      ~~~

  - pcan_python

    ~~~
    $ cd pcan_python/scripts
    $ ./sas2relay
    ~~~

    각도 입력하면 프로그램 실행

    

## 3. Can Python Package

### 1) can

https://github.com/hardbyte/python-can.git 

위의 주소에서 can 라이브러리 가져옵니다.

### 2) mycan

- logger.py
  - 이벤트가 일어나거나, 에러발생 시 logger 
- read.py
  - can read
- write.py
  - can write

### 3) Main

- umd_can.py

  can read SAS -> compare -> can write to relay board

- initialize.py

  sas error 시 초기화



