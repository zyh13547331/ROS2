from setuptools import find_packages, setup
import glob

package_name = 'python_tf'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name+"/launch", glob.glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yuhao9',
    maintainer_email='zyh19136073552@163.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'static_tf = python_tf.static_tf:main',
            'dynamic_tf = python_tf.dynamic_tf:main',
            'tf_lisenter = python_tf.tf_listener:main'
        ],
    },
)
