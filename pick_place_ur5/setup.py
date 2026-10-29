from setuptools import find_packages, setup

package_name = 'pick_place_ur5'

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
    maintainer='julss',
    maintainer_email='julss@example.com',
    description='Nodo ROS 2 para una rutina Pick and Place simulada',
    license='TODO',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pick_place_node = pick_place_ur5.pick_place_node:main',
        ],
    },
)
