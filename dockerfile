FROM ros:iron
SHELL ["/bin/bash", "-c"]


# WORKDIR /app

RUN apt-get update &&  apt-get install -y  \
    python3-smbus \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p ros2_ws/src

WORKDIR /ros2_ws
RUN colcon build

WORKDIR /ros2_ws/src
RUN . /opt/ros/iron/setup.sh && \
    ros2 pkg create --build-type ament_python py_pubsub && \
    ros2 pkg create --build-type ament_python gy_521

COPY py_pubsub/py_pubsub py_pubsub/py_pubsub
COPY py_pubsub/setup.py py_pubsub/setup.py

COPY gy_521/gy_521 gy_521/gy_521
COPY gy_521/setup.py gy_521/setup.py

WORKDIR /ros2_ws
RUN . /opt/ros/iron/setup.sh && \
    rosdep install -i --from-path src --rosdistro iron -y && \
    colcon build --packages-select py_pubsub gy_521
    

COPY ros_entrypoint.sh .

ENTRYPOINT ["/ros2_ws/ros_entrypoint.sh"]
CMD ["bash"]