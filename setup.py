from setuptools import setup, find_packages
import hsettings


static_setup_params = dict(
    name=hsettings.__prog__,
    version=hsettings.__version__,
    description=hsettings.__descr__,
    long_description=hsettings.__doc__,
    author=hsettings.__author__,
    author_email=hsettings.__author_email__,
    url='https://github.com/wwtg99/hsettings',
    license='MIT',
    keywords='settings',
    python_requires='>=3.5',
    package_dir={'': 'hsettings'},
    packages=find_packages('hsettings'),
    install_requires=[
        'pyyaml>=3.13'
    ],
    classifiers=[
        "Operating System :: OS Independent",
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        ],
    # Installing as zip files would break due to references to __file__
    zip_safe=False
)


def main():
    """Invoke installation process using setuptools."""
    setup(**static_setup_params)


if __name__ == '__main__':
    main()
