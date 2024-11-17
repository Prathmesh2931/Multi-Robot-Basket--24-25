FROM shvass/humble

# copy the source code and install all project dependencies
COPY --chown=1000:1000 . src/
RUN . /entrypoint.sh && sudo rosdep init && rosdep update && rosdep install --from-paths src --ignore-src -r -y \
    && rm src -r && mkdir ws \
    && echo "source ~/ws/install/setup.bash" >> /home/vrc/.bashrc
