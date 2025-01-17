#=========================================================================
# test_0.py
#=========================================================================
# Author : Christopher Torng
# Date   : May 26, 2020

import os
import shutil

from mflowgen.mock import MockHandler

step_path = '../../../steps/mentor-calibre-gdsmerge-child'

def test_0():

  # Prep the build directory

  shutil.rmtree( 'build', ignore_errors=True )
  os.mkdir( 'build' )
  os.chdir( 'build' )

  # Build a mock graph with just the node under test

  mhandler = MockHandler()
  mhandler.launch(
    args  = ['init'],
    help_ = False,
    path  = step_path,
  )

  # Put the test files into the mock push node

  os.system( 'make 0' )
  shutil.copy2( '../files/design.gds', '0-mock-push/outputs' )
  shutil.copy2( '../files/child.gds',  '0-mock-push/outputs' )

  # Run the node under test

  os.system( 'make 1' )

  # Check the node passed the postcondition assertions

  assert os.path.exists( '1-mentor-calibre-gdsmerge-child/.postconditions.stamp' )


