import pypandoc
long_description = open('README.md').read()
long_description = pypandoc.convert_file('README.md', 'rst')
with open('README.rst') as f: print(long_description, file=f)
