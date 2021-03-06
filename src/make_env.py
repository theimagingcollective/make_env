﻿#! /usr/bin/env python3
import collections as coll
import os
import shutil

# from archived_code.moved_frm_make_env import setup_paths, copy_direnv, make_exec, check_direnv


def identify_shell(param_shell='bash', force=False):  # default parameter added here for unittests
    # userconfig file locations for various shells & the instructions to be inserted into them:
    ShellHook = coll.namedtuple('ShellHook', 'name command files')
    shell_hooks = {'bash': ShellHook(name='bash', command='eval "$(direnv hook bash)"\n',
                                     files=("~/.profile", "~/.bash_profile", "~/.bashrc")),
                   'zsh': ShellHook(name='zsh', command='eval "$(direnv hook zsh)"\n',
                                    files=("~/.zprofile", "~/.zshrc")),
                   'fish': ShellHook(name='fish', command='eval (direnv hook fish)\n',
                                     files=("~/.config/fish/config.fish",)),
                   'tcsh': ShellHook(name='tcsh', command='eval `direnv hook tcsh`\n',
                                     files=("~/.cshrc",))
        }

    if force == 'force' or True:
        shell_name = param_shell
        possible_shell_files = tuple(os.path.realpath(os.path.expanduser(file_))
                                     for file_ in shell_hooks[shell_name].files)
        shell = {'name': shell_name,
                 'command': shell_hooks[shell_name].command,
                 'files': possible_shell_files}
        return shell

    shell_name = os.environ.get('SHELL', 'bash').split(os.sep)[-1]
    possible_shell_files = tuple(os.path.realpath(os.path.expanduser(file_))
                               for file_ in shell_hooks[shell_name].files)
    found_shell_files = tuple(file_ for file_ in possible_shell_files if os.path.exists(file_))
    
    shell = {'name': shell_name,
             'command': shell_hooks[shell_name].command,
             'files': found_shell_files
             }
    return shell

if __name__ == '__main__':
    print(identify_shell())
#TODO: direnv is a good candidate for a Class. maybe backup+restore in one too. Shell?