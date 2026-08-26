from setuptools import find_packages, setup

package_name = 'cerbers_app'

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
            'init_pose=cerbers_app.init_pose:main',
            'get_pose=cerbers_app.get_pose:main',
            'nav_to_pose=cerbers_app.nav_to_pose:main',
            'way_point_follow=cerbers_app.way_point_follow:main'
        ],
    },
)
