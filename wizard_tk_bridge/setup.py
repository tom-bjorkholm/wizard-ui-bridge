#! /usr/local/bin/python3
"""Setup file specifying build of .whl."""

from setuptools import setup  # type: ignore[import-untyped]

setup(
  name='wizard-tk-bridge', version='1.4',
  description='User interface Tk bridge for wizards asking a user questions.',
  author='Tom Björkholm', author_email='klausuler_linnet0q@icloud.com',
  python_requires='>=3.12', packages=['wizard_tk_bridge'],
  package_dir={'wizard_tk_bridge': 'src/wizard_tk_bridge'},
  package_data={'wizard_tk_bridge': ['py.typed']},
  install_requires=[
    'wizard-ui-bridge >= 1.4',
  ])
