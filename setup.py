from setuptools import setup, find_packages

setup(
    name="CongiFlow",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pyperclip>=1.8.2',
        'ttkbootstrap>=1.10.1',
        'pystray>=0.19.3',
        'Pillow>=9.5.0'
    ],
    entry_points={
        'gui_scripts': [
            'congiflow = congi.app:main'
        ]
    },
    package_data={
        'congi': ['resources/*']
    }
)
