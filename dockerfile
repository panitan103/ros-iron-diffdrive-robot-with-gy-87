FROM ros:iron
SHELL ["/bin/bash", "-c"]


# WORKDIR /app

# RUN apt-get update &&  apt-get install -y  \
#     apt-get install ros-{ros-version}-demo-nodes-cpp 

RUN mkdir -p ros2_ws/src

WORKDIR /ros2_ws
RUN colcon build

WORKDIR /ros2_ws/src
RUN . /opt/ros/iron/setup.sh && \
    ros2 pkg create --build-type ament_python py_pubsub
COPY pub_sub/script/* py_pubsub/py_pubsub
COPY pub_sub/setup.py py_pubsub

WORKDIR /ros2_ws
RUN . /opt/ros/iron/setup.sh && \
    rosdep install -i --from-path src --rosdistro iron -y && \
    colcon build --packages-select py_pubsub
    

COPY ros_entrypoint.sh .

ENTRYPOINT ["/ros2_ws/ros_entrypoint.sh"]
CMD ["bash"]