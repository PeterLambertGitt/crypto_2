from setuptools import setup
from setuptools import find_packages

with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

if __name__ == "__main__":
    setup(name='crypto_2',
      description="package description",
      packages=find_packages(), # NEW: find packages automatically
      install_requires=requirements)
