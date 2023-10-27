from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT='-e .'
def get_requirements(file_path:str) -> List[str]:
    '''This functions return the list of requirements'''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [requirement.replace("\n","") for requirement in requirements]
        
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
            
    return requirements
setup(
    name='grocery_store_pipeline',
    version='0.0.1',
    author='Fausto Pucheta Fortin',
    email='faustopuchetafortin@gmail.com',
    packages=find_packages(),
    install_reqiures=get_requirements('requirements.txt')
)