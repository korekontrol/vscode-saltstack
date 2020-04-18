'''
generate_snippets uses salt-call equivalent to list existing states and their functions.
Basic autocomplete snippets are then configured for each state.
If the snippet has been further edited, the script will not touch them. Thus,
the resulting workflow is to run generate_snippets on new salt releases to
capture any added states or functions. Then hand edit for the defaults which
make sense.
'''
import salt.client

import os
import json

def _gen_snippet(state_name, state_functions):
    '''
    Builds up and returns basic snippet definition for a given state
    '''
    snippets = {}
    for function in state_functions:
        snippets['{}.{}'.format(state_name, function)] = {}
        snippets['{}.{}'.format(state_name, function)]['prefix'] = '{}.{}:'.format(state_name, function)
        snippets['{}.{}'.format(state_name, function)]['body'] = ['{}.{}:'.format(state_name, function), "$0"]
        snippets['{}.{}'.format(state_name, function)]['description'] = '{}.{}:'.format(state_name, function)
    return snippets

def _get_state_name(json_path):
    '''
    Returns just the state name from a string like ./snippets/test.json
    Used for sorting the snippet list in package.json
    '''
    state_name = json_path['path'][11:-5]
    return state_name

def _add_all_snippets(states):
    '''
    Ensures package.json is updated with all generated state snippet paths
    '''
    state_paths = list(map(lambda x : "./snippets/{}.json".format(x), states))
    with open('package.json', 'r') as json_file:
        data = json.load(json_file)
    configured_snippets = []
    snippet_data = data['contributes']['snippets']
    for current_snippet in snippet_data:
        current_path = current_snippet['path']
        configured_snippets.append(current_path)
    needed_snippets = list(set(state_paths).difference(set(configured_snippets)))
    if needed_snippets:
        for new_snippet_path in needed_snippets:
            print('Adding support for {} completion'.format(new_snippet_path))
            new_snippet = {}
            new_snippet['language'] = 'sls'
            new_snippet['path'] = new_snippet_path
            data['contributes']['snippets'].append(new_snippet)
        # Sort snippet data
        snippet_data = data['contributes']['snippets']
        snippet_data.sort(key=_get_state_name)
        data['contributes']['snippets'] = snippet_data
        with open('package.json', 'w') as json_file:
            json.dump(data, json_file, indent='\t')
    else:
        print("All states present in package.json")

local = salt.client.Caller()
state_info = local.cmd('baredoc.list_states', names_only=True)
function_blacklist = ['mod_watch']

any_updates = False

for state in state_info:

    # Build list of functions for state
    current_functions = []
    state_path = os.path.join('snippets', state + '.json')
    # Don't include mod_watch functions as these aren't used in state files
    current_functions = list(set(state_info[state]) - set(function_blacklist))
    snippets = _gen_snippet(state, current_functions)

    if not os.path.exists(state_path):
        print("Generating basic {}".format(state_path))
        with open(state_path, 'w') as json_file:
            json.dump(snippets, json_file, indent='\t')
    else:
        data_updated = False
        with open(state_path, 'r') as json_file:
            data = json.load(json_file)

        for key in snippets:
            if key not in data:
                any_updates = True
                data_updated = True
                data[key] = snippets[key]
                print('Updated {} for {}'.format(key, state))
        if data_updated:
            with open(state_path, 'w') as json_file:
                json.dump(data, json_file, indent='\t')

if not any_updates:
    print('No changes made to snippet files')
_add_all_snippets(sorted(state_info.keys()))
