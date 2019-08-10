from fabric.api import env
from fabric.api import local
from fabric.api import run
from fabric.api import task
# from fabric.api import prompt
# from fabric.api import execute
from fabric.context_managers import cd

import os

env.forward_agent = True
env.user = 'root'
env.hosts = ['your production host']

project_dst = 'project-name'

compose_cmd = [
    'docker-compose',
    '-f', 'docker-compose.yml',
    '-f',
]

# service to run commands against
service_name = None
renv = 'dev'  # dev by default
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(CURRENT_DIR, 'app')


def create_compose_cmd() -> list:
    return compose_cmd + ['docker-compose-%s.yml' % renv]


def call(arg, *args, **kwargs) -> str:
    """
    Returns the correct function call for the environment.
    """
    fn = run if renv == 'prd' else local
    return fn(' '.join(arg) if type(arg) in (tuple, list) else arg)


def test_cmd_exists(cmd: str) -> bool:
    """
    Tests whether `cmd` executable is in the path.
    """
    msg = '"%s" not found in path. Please, install it to continue.'

    if 'not found' in local('which %s' % cmd, capture=True):
        raise Exception(msg % cmd)


def insert_line_after(lines: list, line: str, after: str) -> None:
    """
    Inserts `line` after the line in `lines` that has
    `after` as a substring.
    """
    for i in range(len(lines)):
        if after in lines[i]:
            lines.insert(i+1, line)
            break


def replace_line(lines: list, line: str, condition: str) -> None:
    """
    Replaces the line in `lines` that has `condition` as a substring
    with `line`.
    """
    for i in range(len(lines)):
        if condition in lines[i]:
            lines[i] = line
            break


@task(alias='setup')
def do_setup():
    """
    Helps you setup your environment. Call it once per project.
    """

    test_cmd_exists('docker')
    test_cmd_exists('docker-compose')

    local(' '.join(["cookiecutter", "https://github.com/italomaia/flask-empty"]))

    print(
        "IMPORTANT:"
        "\n" "\t"
        "Use the following command to add 'dv' as a alias in your hosts file:"
        "\n" "\t"
        "sudo echo \"127.0.0.1  dv\" >> /etc/hosts"
    )

    print(
        "IMPORTANT: "
        "\n" "\t"
        "be sure to update your 'envfile' files;"
    )
    print(
        "IMPORTANT: "
        "\n" "\t"
        "update fabfile.py with your environment information;"
    )

    print(
        "\n"
        "Now you're ready to go:"
        "\n" "\t"
        "fab env:dev up  # for development mode"
        "\n" "\t"
        "fab env:tst up  # for test mode"
        "\n" "\t"
        "fab env:prd up  # for production mode"

        "\n" "\n"
        "Locally, your project will be available at http://dv:8080"
    )


@task(alias='env')
def set_renv(local_renv):
    "Sets docker-compose environment"
    global renv

    renv = local_renv


@task(alias='up')
def compose_up(name: str = None) -> None:
    """
    Calls docker compose up using the correct environment.
    """
    opt = ['-d'] if renv == 'prd' else []

    with cd(project_dst):
        local_cmd = create_compose_cmd() + ['up']
        local_cmd += opt
        local_cmd += [name] if name else []
        call(local_cmd)


@task(alias='build')
def compose_build(name: str = None) -> None:
    """
    Calls docker compose build using the correct environment.
    """
    with cd(project_dst):
        local_cmd = create_compose_cmd() + ['build']
        local_cmd += [name] if name else []

        call(local_cmd)


@task(alias='on')
def on_service(name: str) -> None:
    """
    Define service where command should run
    """
    global service_name

    service_name = name


@task(alias='run')
def compose_run(cmd: str) -> None:
    """
    Calls docker compose run using the correct environment.

    :param cmd: run command, including container name.
    """
    opt = ['--rm']

    if service_name is None:
        print("please, provide service name")
        exit()

    with cd(project_dst):
        local_cmd = create_compose_cmd() + ['run']
        local_cmd += opt
        local_cmd += [service_name]
        local_cmd += cmd.split()
        call(local_cmd)


@task(alias='logs')
def docker_logs(name: None) -> None:
    """
    Get docker container logs.
    """
    call('docker logs %s' % name)
