from setuptools import setup
import os
import glob

package_name = 'ksr_robot20'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        (os.path.join('share', package_name), ['package.xml']),
        (os.path.join('share', package_name), glob.glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools', 'pygame'],
    zip_safe=True,
    maintainer='yuki',
    maintainer_email='jared.butcher1219@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'driver = ksr_robot20.driver:main',
            'teleop_keyboard = ksr_robot20.teleop_keyboard:main',
        ],
    },
)
