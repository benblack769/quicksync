import subprocess
import yaml
import os
import sys

def generate_ssh_command(ssh_key,port):
    str = "ssh "
    str += " -o StrictHostKeyChecking=no "
    if ssh_key:
        str += " -i '{}' ".format(ssh_key)
    if port:
        str += " -p {} ".format(port)
    return str

def generate_rsync_command(username,ssh_key,ip,port,source,dest,is_forward,exclude,delete):
    command = [
        "rsync",
        "-a",# archive mode
        "-e",generate_ssh_command(ssh_key,port),# specify port
    ]
    if delete:
        command.append("--delete")
    if exclude:
        if isinstance(exclude,list):
            for e in exclude:
                command.append("--exclude")
                command.append(e)
        else:
            command.append("--exclude")
            command.append('{}'.format(exclude))

    dest_str = "{}@{}:{}".format(username,ip,dest)
    forward_end = [source,dest_str]
    backward_end = [dest_str,source]
    command += forward_end if is_forward else backward_end
    return command


def load_data_from_yaml(yaml_path,proj_name,computer_override):
    project_yaml = yaml_path + "projects.yaml"
    all_project_data = yaml.safe_load(open(project_yaml))

    project_data = all_project_data[proj_name]
    machine_path = os.path.join(yaml_path,"{}.yaml".format(project_data['machine'] if computer_override is None else computer_override))
    machine_data = yaml.safe_load(open(machine_path))
    return machine_data,project_data


def defaulted(config,name,default_val):
    return config[name] if name in config else default_val

def gen_rsync_on_data(computer_data,project_data,is_forward):
    command = generate_rsync_command(
        username=computer_data['username'],
        ssh_key=computer_data['ssh_key_path'],
        ip=computer_data['ip'],
        port=defaulted(computer_data,'port',22),
        source=project_data['source'],
        dest=project_data['dest'],
        is_forward=is_forward,
        exclude=defaulted(project_data,'exclude',None),
        delete=defaulted(project_data,'delete',False)
    )
    return command

def exec_command(command):
    joined_cmd = " ".join(command)
    subprocess.check_call(command)#joined_cmd,shell=True)

def exec_input(yaml_path,proj_name,is_forward,computer_override):
    computer_data,project_data = load_data_from_yaml(yaml_path,proj_name,computer_override)
    command = gen_rsync_on_data(computer_data,project_data,is_forward)
    print(" ".join(command))
    exec_command(command)

def test():
    yaml_path = "my_configs/"
    proj_name = "robo_proj"
    computer_data,project_data = load_data_from_yaml(yaml_path,proj_name)
    print(project_data)
    print(computer_data)
    is_forward = True
    print(computer_data['username'])
    command = gen_rsync_on_data(computer_data,project_data,is_forward)
    print(" ".join(command))

if __name__ == "__main__":
    assert 3 <= len(sys.argv) <= 4, "needs 2 arguments, the project name and the direction (true for forward)"
    projname = sys.argv[1]
    is_forward = True if "true" in sys.argv[2].lower()  else False
    yaml_path = os.path.expanduser("~/.local/var/")
    yaml_override = None if len(sys.argv) < 4 else sys.argv[3]
    exec_input(yaml_path,projname,is_forward,yaml_override)
