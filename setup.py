from distutils.core import setup


def read(file_relative):
    file = file_relative
    with open(str(file)) as f:
        return f.read()


setup(
    name='esp32_net_config',
    packages=[''],
    version='0.1.13',
    license='MIT',
    description='module to allow configuration of netword ssid and password through local access point',
    long_description=read('README.rst'),
    author='Todd Flanders',
    author_email='toddfbass@gmail.com',
    url='https://github.com/tflander/esp32-machine-emulator',
    download_url='https://github.com/tflander/esp32-machine-emulator/archive/v_01.tar.gz',  # I explain this later on
    keywords=['ESP32', "MicroPython"],
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: MicroPython'
    ],
)
