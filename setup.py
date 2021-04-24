from distutils.core import setup

setup(
  name = 'pmtw',
  packages = ['pmtw'],
  version = '0.1.4',
  license='GPL-3',
  description = 'Python Moderator Toolbox Wrapper for reddit',
  long_description = open('README').read(),
  author = 'AdhesiveCheese',
  author_email = 'adhesiveCheese@gmail.com',
  url = 'https://github.com/adhesivecheese/pmtw',
  download_url = 'https://github.com/adhesivecheese/pmtw/archive/refs/tags/V0_1.tar.gz',
  keywords = ['Reddit', 'Moderator_Toolbox', 'Web Wrapper'],
  install_requires=[
          'praw >=6.0',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Utilities',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Programming Language :: Python :: 3.6',
  ],
)
