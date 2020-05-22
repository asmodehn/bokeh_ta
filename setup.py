import runpy
import subprocess
import sys

import setuptools

# Ref : https://packaging.python.org/single_source_version/#single-sourcing-the-version
# runpy is safer and a better habit than exec
version = runpy.run_path('bokeh_ta/_version.py')
__version__ = version.get('__version__')


# Best Flow :
# Clean previous build & dist
# $ gitchangelog >CHANGELOG.rst
# change version in code and changelog
# $ python setup.py prepare_release
# WAIT FOR TRAVIS CHECKS
# $ python setup.py publish
# => TODO : try to do a simpler "release" command


# Clean way to add a custom "python setup.py <command>"
# Ref setup.py command extension : https://blog.niteoweb.com/setuptools-run-custom-code-in-setup-py/
class PrepareReleaseCommand(setuptools.Command):
    """Command to release this package to Pypi"""
    description = "prepare a release of timecontrol"
    user_options = []

    def initialize_options(self):
        """init options"""
        pass

    def finalize_options(self):
        """finalize options"""
        pass

    def run(self):
        """runner"""

        # TODO :
        # $ gitchangelog >CHANGELOG.rst
        # change version in code and changelog
        subprocess.check_call(
            "git commit CHANGELOG.rst timecontrol/_version.py -m 'v{0}'".format(__version__), shell=True)
        subprocess.check_call("git push", shell=True)

        print("You should verify travis checks, and you can publish this release with :")
        print("  python setup.py publish")
        sys.exit()


# Clean way to add a custom "python setup.py <command>"
# Ref setup.py command extension : https://blog.niteoweb.com/setuptools-run-custom-code-in-setup-py/
class PublishCommand(setuptools.Command):
    """Command to release this package to Pypi"""
    description = "releases timecontrol to Pypi"
    user_options = []

    def initialize_options(self):
        """init options"""
        # TODO : register option
        pass

    def finalize_options(self):
        """finalize options"""
        pass

    def run(self):
        """runner"""
        # TODO : clean build/ and dist/ before building...
        subprocess.check_call("python setup.py sdist", shell=True)
        subprocess.check_call("python setup.py bdist_wheel", shell=True)
        # OLD way:
        # os.system("python setup.py sdist bdist_wheel upload")
        # NEW way:
        # Ref: https://packaging.python.org/distributing/
        subprocess.check_call("twine upload dist/*", shell=True)  # TODO : handle authentication... (keyring...)

        subprocess.check_call("git tag -a {0} -m 'version {0}'".format(__version__), shell=True)
        subprocess.check_call("git push --tags", shell=True)
        # TODO : gitflow option of merging develop into master ?
        sys.exit()


setuptools.setup(
    name='bokeh_ta',
    version=__version__,
    description='Technical Analysis Indicators Plots',
    author='AlexV',
    author_email='asmodehn@gmail.com',
    url='https://github.com/asmodehn/bokeh_ta',
    packages=['bokeh_ta'],
    install_requires=[
        "pandas==1.0.3",
        "bokeh==2.0.2",
    ],
    cmdclass={
        'prepare_release': PrepareReleaseCommand,
        'publish': PublishCommand,
    },
    setup_requires=['wheel', 'twine']
)

