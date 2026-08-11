from setuptools import find_packages, setup

package_name = 'python_service'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name+"/resource", ['resource/default.webp']),
        ('share/' + package_name+"/resource", ['resource/new.jpg']),

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
            "face_detect = python_service.face_detect:main",
            "face_node = python_service.face_node:main",
            "face_client = python_service.face_client:main",
        ],
    },
)
