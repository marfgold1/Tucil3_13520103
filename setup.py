from setuptools import find_packages, setup

setup(
    name='FifteenPuzzleSolver',
    version='1.0.0',
    author='Amar Fadil',
    author_email='13520103@std.stei.itb.ac.id',
    description=' '.join([
        'A solver for the famous 15-puzzle',
        'using Branch and Bound strategy.',
    ]),
    url='https://github.com/marfgold1/Puzzle15Solver',
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.7',
)