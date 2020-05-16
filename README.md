# quicksync
A data synchronization tool designed for remote desktop work.  

### Useage

Once properly configured, you can push files to the server using
```
forward_sync <project_name>
```
and pull files to local using
```
backward_sync <project_name>
```

### Configuration

There are two configuration files, both in yaml format:

#### Computer config

The computer config is where you place information about the remote computer. It looks like this:

```
username: weepingwillowben  # <unix username>
ip: 67.124.212.159          # <server ip address>
port: 22                    # <server ssh port (should be 22)>
ssh_key_path: ~/.ssh/desktop_key/id_desk # path to ssh key that allows passwordless login
```

#### Project config

The project config specifies what files you want to sync for each project, and where to sync them (both the machine and the path on the machine).

```
robo_proj:
    machine: "example_computer_config"            # name of computer config yaml file (looks in same directory as the project file)
    source: "~/code/main_projs/robotics_project/"  # path to sync on local
    dest: "~/class_projs/robotics_project/"       # path to sync on remote
    delete: True                                  # Whether to enable delete files when syncing
    exclude:
      - _img_dir                             # excludes files from sync.
chess_proj:
    machine: "example_computer_config"
    source: "/mnt/c/Users/weepi/code/main_projs/chess_proj"
    dest: "~/class_projs/chess_proj/"
    # delete defaults to false
    # exclude defaults to no exclusions
```


### Manual installation

There is no install script, but you can manually install this tool by the following steps.

#### Install dependencies

1. pyyaml python package `pip install pyyaml`
1. rsync client on local `sudo apt-get install rsync`
1. rsync server on server
1. Start rsync server on server (on ubuntu `sudo systemctl start rsync`)

#### Install quicksync

1. Move all files in `quicksync/scripts` directory to `~/.local/bin` (creating the folder if it is not there)
1. Add `~/.local/bin` to path permanently by appending `export PATH="$HOME/.local/bin/:$PATH"` to .bashrc
1. Create computer config and put it in `~/.loval/var/<machine_name>.yaml`
1. Create project config and put it in `~/.loval/var/projects.yaml` (this specific path is important! Script only looks here!)
