from setuptools import find_packages, setup

package_name = 'sim_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='shvass',
    maintainer_email='akshayb@gmx.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'launch_controller = sim_controller.launch_controller:main',
            'ball_spawner = sim_controller.ball_spawner:main',
            'dist_basket=sim_controller.basket_tf:main',
            'relative_dist_bot=sim_controller.bot_relative:main'
        ],
    },
)
