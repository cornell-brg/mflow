#=========================================================================
# subgraph.py
#=========================================================================
# Author : Alex Carsello
# Date   : July 18, 2023
#

import copy
import importlib
import os
import sys
import yaml

from mflowgen.utils import get_top_dir, read_yaml, write_yaml
from mflowgen.components.step import Step
from mflowgen.core.run import RunHandler as rh

class Subgraph(Step):

  def __init__( s, graph_path, design_name ):
    
    # Get the construct.py file path

    construct_path = rh.find_construct_path( graph_path, False )

    # Import the graph for this design (copied from RunHandler)

    c_dirname  = os.path.dirname( construct_path )
    c_basename = os.path.splitext( os.path.basename( construct_path ) )[0]

    mod_spec = importlib.util.spec_from_file_location(c_basename, construct_path)
    subgraph_construct_mod = importlib.util.module_from_spec(mod_spec)
    try:
      mod_spec.loader.exec_module(subgraph_construct_mod)
    except ModuleNotFoundError:
      print()
      print( bold( 'Error:' ), 'Could not open construct script at',
                                      '"{}"'.format( construct_path ) )
      print()
      sys.exit( 1 )

    try:
      subgraph_construct_mod.construct
    except AttributeError:
      print()
      print( bold( 'Error:' ), 'No module named "construct" in',
                                      '"{}"'.format( construct_path ) )
      print()
      sys.exit( 1 )

    # Construct the graph
    s._graph = subgraph_construct_mod.construct()

    # Generate step data

    data = {}
    data['name'] = design_name
    data['outputs'] = s._graph.all_outputs()
    data['commands'] = [ \
      f"mflowgen run --design {construct_path}",
      'make outputs',
      'mkdir -p outputs',
      'cd outputs',
      'output_dir=$(find ../ -type d -regex "^../[0-9]+-outputs/outputs")'
    ]

    data['postconditions'] = []
    for output in s._graph.all_outputs():
      data['commands'].append(f"ln -sf $output_dir/{output} .")
      data['postconditions'].append(f"assert File( outputs/{output} )")
    
    super().__init__(data)
  
  #-----------------------------------------------------------------------
  # get_graph
  #-----------------------------------------------------------------------

  # Returns underlying graph object used to create Subgraph Step.
  def get_graph( s ):
    return s._graph

  #-----------------------------------------------------------------------
  # Clone
  #-----------------------------------------------------------------------

  def clone( s ):
    new_step = Step.__new__( Step )
    new_step._config = copy.deepcopy( s._config )
    new_step.step_dir  = s.step_dir
    return new_step

  #-----------------------------------------------------------------------
  # API to help build graphs interactively
  #-----------------------------------------------------------------------

  # Get handles (that can be connected with Graph .connect)

  def get_input_handle( s, f ):

    assert s._config['inputs'], \
      'get_input_handle -- This step has no inputs'
    assert f in s._config['inputs'], \
      'get_input_handle -- No input "%s" found in the step' % f

    handle = ( s._config['name'], 'inputs', f )

    return handle

  def get_output_handle( s, f ):

    assert s._config['outputs'], \
      'get_output_handle -- This step has no outputs'

    outputs = s.all_outputs()

    assert f in outputs, \
      'get_output_handle -- No output "%s" found in the step' % f

    handle = ( s._config['name'], 'outputs', f )

    return handle

  # Syntactic sugar for getting input and output handles

  def i( s, name ):
    return s.get_input_handle( name )

  def o( s, name ):
    return s.get_output_handle( name )

  # All handles at once to make it easy to connect between steps by name

  def all_input_handles( s ):
    if 'inputs' not in s._config.keys():
      return []
    input_handles = \
      [ s.get_input_handle( name ) for name in s._config['inputs'] ]
    return input_handles

  def all_output_handles( s ):
    if 'outputs' not in s._config.keys():
      return []
    outputs = s.all_outputs()
    output_handles = \
      [ s.get_output_handle( name ) for name in outputs ]
    return output_handles

  # API to extend inputs and outputs

  def extend_inputs( s, new_list ):
    try:
      s._config['inputs']
    except KeyError:
      s._config['inputs'] = []
    s._config['inputs'].extend( new_list )

  def extend_outputs( s, new_list ):
    try:
      s._config['outputs']
    except KeyError:
      s._config['outputs'] = []
    s._config['outputs'].extend( new_list )

  # API to pre/post extend commands

  def pre_extend_commands( s, new_list ):
    try:
      s._config['commands']
    except KeyError:
      s._config['commands'] = []
    s._config['commands'][:0] = new_list

  def extend_commands( s, new_list ):
    try:
      s._config['commands']
    except KeyError:
      s._config['commands'] = []
    s._config['commands'].extend( new_list )

  # API to extend preconditions and postconditions

  def extend_preconditions( s, new_list ):
    try:
      s._config['preconditions']
    except KeyError:
      s._config['preconditions'] = []
    s._config['preconditions'].extend( new_list )

  def extend_postconditions( s, new_list ):
    try:
      s._config['postconditions']
    except KeyError:
      s._config['postconditions'] = []
    s._config['postconditions'].extend( new_list )

  def set_preconditions( s, new_list ):
    s._config['preconditions'] = new_list

  def set_postconditions( s, new_list ):
    s._config['postconditions'] = new_list

  def get_preconditions( s ):
    return s._config['preconditions']

  def get_postconditions( s ):
    return s._config['postconditions']

  #-----------------------------------------------------------------------
  # Parameter system
  #-----------------------------------------------------------------------

  def set_name( s, name ):
    s._config['name'] = name

  def get_name( s ):
    return s._config['name']

  def set_param( s, param, value ):
    try:
      step_params = s._config['parameters']
    except KeyError:
      raise KeyError( 'set_param -- ' \
        'No parameter "%s" in step "%s"' % ( param, s.get_name() ) )
    try:
      step_params[param]
      step_params[param] = value
    except KeyError:
      raise KeyError( 'set_param -- ' \
        'No parameter "%s" in step "%s" (available parameters: %s)' % \
          ( param, s.get_name(), step_params.keys() ) )

  def get_param( s, param ):
    assert 'parameters' in s._config.keys(), \
      'get_param -- ' \
      'No parameter "%s" in step "%s"' % ( param, s.get_name() )
    assert param in s._config['parameters'].keys(), \
      'get_param -- ' \
      'No parameter "%s" in step "%s" (options: %s)' % \
        ( param, s.get_name(), s._config['parameters'].keys() )
    return s._config['parameters'][param]

  # update_params
  #
  # Take the {params} dict and update the params of this step. If
  # {allow_new} is true, then params that are not yet defined are also
  # added to this step, otherwise only params that are already defined are
  # updated.
  #

  def update_params( s, params, allow_new=False ):
    assert type(params) == dict, \
      'update_param -- ' \
      'Expecting argument of type dictionary to update parameters'

    # Update all parameters and add new parameters

    if allow_new:
      try:
        s._config['parameters']
      except KeyError:
        s._config['parameters'] = {}
      s._config['parameters'].update( params )

    # Only update parameters that were defined in the configuration YAML

    else:
      try:
        for p in params.keys():
          if p in s._config['parameters'].keys():
            s._config['parameters'][p] = params[p]
      except KeyError:
        pass

  def params( s ):
    if 'parameters' not in s._config.keys():
      return {}
    return s._config['parameters']

  # expand_params
  #
  # Populate all parameters in outputs and commands

  def expand_params( s ):

    # Expand outputs

    if 'outputs' in s._config.keys():
      for idx, o in enumerate( s._config['outputs'] ):
        if type(o) == dict:
          key   = o.keys()[0].format( **s.params() )
          value = o.values()[0].format( **s.params() )
          s._config['outputs'][idx] = { key : value }
        elif type(o) == str:
          output = o.format( **s.params() )
          s._config['outputs'][idx] = output
        else:
          assert False, \
            'expand_params -- ' \
            'Unrecognized type %s in output "%s"' % ( type(o), o )

    # Expand commands

    if 'commands' in s._config.keys():
      for idx, c in enumerate( s._config['commands'] ):
        try:
          s._config['commands'][idx] = c.format( **s.params() )
        except KeyError as e:
          cause = e.args[0]
          raise KeyError( 'Error: Unrecognized parameter "' + cause + '"'
            ' in commands for step "' + s.get_name() + '"!' +
            ' Please escape literal curly braces with double braces' )
        except AttributeError as e:
          print( '\nError: Perhaps a command was interpreted as a dict\n')
          raise

    # Expand debug

    if 'debug' in s._config.keys():
      for idx, c in enumerate( s._config['debug'] ):
        s._config['debug'][idx] = c.format( **s.params() )

  #-----------------------------------------------------------------------
  # Metadata
  #-----------------------------------------------------------------------

  # update_metadata
  #
  # Updates the internal "s._config" dictionary with all contents of the
  # input dictionary.

  def update_metadata( s, data ):
    s._config.update( data )

  #-----------------------------------------------------------------------
  # Ninja helpers
  #-----------------------------------------------------------------------

  # escape_dollars
  #
  # Ninja expects dollar signs to be escaped

  def escape_dollars( s ):

    # Escape outputs

    if 'outputs' in s._config.keys():
      for idx, o in enumerate( s._config['outputs'] ):
        if type(o) == dict:
          key   = o.keys()[0].replace( '$', '$$' )
          value = o.values()[0].replace( '$', '$$' )
          s._config['outputs'][idx] = { key : value }
        elif type(o) == str:
          output = o.replace( '$', '$$' )
          s._config['outputs'][idx] = output
        else:
          assert False, \
            'escape_dollars -- ' \
            'Unrecognized type %s in output "%s"' % ( type(o), o )

    # Escape commands

    if 'commands' in s._config.keys():
      for idx, c in enumerate( s._config['commands'] ):
        s._config['commands'][idx] = c.replace( '$', '$$' )

    # Escape debug

    if 'debug' in s._config.keys():
      for idx, c in enumerate( s._config['debug'] ):
        s._config['debug'][idx] = c.replace( '$', '$$' )

  #-----------------------------------------------------------------------
  # Observability methods
  #-----------------------------------------------------------------------

  # List all inputs

  def all_inputs( s ):
    if 'inputs' not in s._config.keys():
      return []
    return s._config['inputs']

  # all_outputs -- normal version
  #
  # This is the list of all outputs that appear in the 'outputs/' dir
  #
  # Unpack tagged outputs such that this configuration YAML:
  #
  #     outputs:
  #     - foo1.txt
  #     - foo2.txt
  #     - foo3.txt: results/1/2/3/data.txt
  #
  # Turns into this:
  #
  #     outputs = [
  #       'foo1.txt',
  #       'foo2.txt',
  #       'foo3.txt',
  #     ]
  #

  def all_outputs( s ):
    if 'outputs' not in s._config.keys():
      return []
    outputs = list( s._config['outputs'] )
    for idx, o in enumerate( outputs ):
      if type(o) == dict:
        outputs[idx] = o.keys()[0]
    return outputs

  # all_outputs_execute -- execute version
  #
  # This is the list of all outputs that 'execute' will generate.
  #
  # Unpack tagged outputs such that this configuration YAML:
  #
  #     outputs:
  #     - foo1.txt
  #     - foo2.txt
  #     - foo3.txt: results/1/2/3/data.txt
  #
  # Turns into this:
  #
  #     outputs = [
  #       'foo1.txt',
  #       'foo2.txt',
  #       '../results/1/2/3/data.txt',  <-- relative to 'outputs/' dir
  #     ]
  #

  def all_outputs_execute( s ):
    if 'outputs' not in s._config.keys():
      return []
    outputs = list( s._config['outputs'] )
    for idx, o in enumerate( outputs ):
      if type(o) == dict:
        outputs[idx] = '../' + o.values()[0]
    return outputs

  # all_outputs_tagged -- version with only the tagged subset
  #
  # These are the outputs that need to be linked to the 'outputs/' dir.
  #
  # Return only tagged outputs so that this configuration YAML:
  #
  #     outputs:
  #     - foo1.txt
  #     - foo2.txt
  #     - foo3.txt: results/1/2/3/data.txt
  #
  # Returns this:
  #
  #     outputs = [
  #       { foo3.txt: results/1/2/3/data.txt }
  #     ]
  #

  def all_outputs_tagged( s ):
    if 'outputs' not in s._config.keys():
      return []
    return [ o for o in s._config['outputs'] if type(o) == dict ]

  # all_outputs_untagged -- version with only the untagged subset
  #
  # These are the outputs that need to be stamped in the 'outputs/' dir.
  #
  # Return only untagged outputs so that this configuration YAML:
  #
  #     outputs:
  #     - foo1.txt
  #     - foo2.txt
  #     - foo3.txt: results/1/2/3/data.txt
  #
  # Returns this:
  #
  #     outputs = [
  #       'foo1.txt',
  #       'foo2.txt',
  #     ]
  #

  def all_outputs_untagged( s ):
    if 'outputs' not in s._config.keys():
      return []
    return [ o for o in s._config['outputs'] if type(o) != dict ]

  #-----------------------------------------------------------------------
  # Used in backends
  #-----------------------------------------------------------------------

  def get_dir( s ):
    return s.step_dir

  def get_commands( s ):
    return s._config['commands']

  def get_debug_commands( s ):
    if 'debug' in s._config.keys():
      return s._config['debug']
    else:
      return []

  def dump_yaml( s, build_dir ):

    # Enable dumping multiline strings as block literals
    #
    # Block literals look like this:
    #
    #     foo: |
    #       line 1
    #       line 2
    #       line 3
    #
    # The indentation of the first line is used as the common indentation
    # for the entire block, so when read as a string it looks like this:
    #
    #     >>> line 1
    #     >>> line 2
    #     >>> line 3
    #

    def str_representer( dumper, data ):
      tmp = { 'tag' : 'tag:yaml.org,2002:str', 'value' : data }
      if len( data.splitlines() ) > 1:
        tmp.update( { 'style' : '|' } )
      return dumper.represent_scalar( **tmp )
    yaml.add_representer( str, str_representer )

    # Dump the content

    write_yaml(
      data = s._config,
      path = build_dir + '/configure.yml',
    )

  # The sandbox flag will copy the source step directory if true (default)
  # or symlink the source files into the build directory if false

  def set_sandbox( s, val ):
    s._config['sandbox'] = val

  def get_sandbox( s ):
    try:
      return s._config['sandbox']
    except KeyError:
      return True


