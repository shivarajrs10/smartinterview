FROM ubuntu:latest

RUN apt-get update

RUN apt upgrade

# Install OpenCV dependencies

RUN apt-get install -y build-essential cmake unzip pkg-config \
  libjpeg-dev libpng-dev libtiff-dev

RUN apt update && \
      apt install -y software-properties-common && \
      rm -rf /var/lib/apt/lists/*

RUN add-apt-repository "deb http://security.ubuntu.com/ubuntu xenial-security main"
RUN apt update
RUN apt install -y libjasper1 libjasper-dev

RUN apt install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
RUN apt install -y  libxvidcore-dev libx264-dev

RUN apt-get update
RUN apt install -y libgtk-3-dev
RUN apt install -y  libatlas-base-dev gfortran
RUN apt -y autoremove && apt-get -y clean

# Python Set Up

RUN apt-get update \
    && apt-get install -y python3-pip python3-dev \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip

RUN pip3 install numpy

# Download the official OpenCV source
RUN apt install wget


RUN wget -O opencv.zip https://github.com/opencv/opencv/archive/3.4.4.zip
RUN wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/3.4.4.zip


RUN unzip opencv.zip
RUN unzip opencv_contrib.zip

RUN mv /opencv-3.4.4 /opencv
RUN mv /opencv_contrib-3.4.4 /opencv_contrib

# Configure OpenCV with CMake


#RUN cd /opencv
WORKDIR /opencv
RUN mkdir build
#RUN cd build
WORKDIR /opencv/build

RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D WITH_CUDA=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D OPENCV_EXTRA_MODULES_PATH=/opencv_contrib/modules \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D BUILD_EXAMPLES=OFF ..

# Compiling Installing OpenCV
RUN make -j4 && make install && ldconfig



RUN ln -s /usr/local/python/cv2/python-3.6/cv2.cpython-36m-x86_64-linux-gnu.so /usr/local/lib/python3.6/dist-packages/cv2.so
#RUN ls /usr/local/python/cv2/python-3.6 && mv cv2.cpython-36m-x86_64-linux-gnu.so cv2.so

RUN rm /opencv.zip /opencv_contrib.zip
#RUN rm -rf /opencv opencv_contrib.zip
WORKDIR /code
ADD ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
ADD . /code

CMD ["python", "app.py"]
