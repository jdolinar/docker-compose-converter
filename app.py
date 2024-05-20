from flask import Flask, request, jsonify, send_from_directory
import yaml
import os
import re

app = Flask(__name__, static_folder='.')

def preprocess_command(command):
    """
    Combines multiline bash commands into a single line.
    """
    command = re.sub(r'\\\s*\n', ' ', command)
    return command

def parse_docker_run(command):
    parts = command.split()
    service = {}
    ports = []
    volumes = []
    environment = []
    command_parts = []
    entrypoint = None
    container_name = None
    hostname = None
    restart_policy = None

    i = 2
    while i < len(parts):
        if parts[i] == '-p' or parts[i] == '--publish':
            ports.append(parts[i + 1])
            i += 2
        elif parts[i] == '-v' or parts[i] == '--volume':
            volumes.append(parts[i + 1])
            i += 2
        elif parts[i] == '-e' or parts[i] == '--env':
            environment.append(parts[i + 1])
            i += 2
        elif parts[i] == '--name':
            container_name = parts[i + 1]
            i += 2
        elif parts[i] == '--hostname':
            hostname = parts[i + 1]
            i += 2
        elif parts[i] == '--entrypoint':
            entrypoint = parts[i + 1]
            i += 2
        elif parts[i] == '--restart':
            restart_policy = parts[i + 1]
            i += 2
        elif parts[i] == '--detach':
            i += 1
        elif parts[i].startswith('-'):
            i += 1
        else:
            if 'image' not in service:
                service['image'] = parts[i]
            else:
                command_parts.append(parts[i])
            i += 1

    if ports:
        service['ports'] = ports
    if volumes:
        service['volumes'] = volumes
    if environment:
        service['environment'] = environment
    if container_name:
        service['container_name'] = container_name
    if hostname:
        service['hostname'] = hostname
    if entrypoint:
        service['entrypoint'] = entrypoint
    if restart_policy:
        service['restart'] = restart_policy
    if command_parts:
        service['command'] = ' '.join(command_parts)

    return service

def generate_docker_compose(services):
    compose = {
        'version': '3',
        'services': {}
    }
    for index, service in enumerate(services):
        service_name = f'app{index + 1}'
        compose['services'][service_name] = service
    return yaml.dump(compose, default_flow_style=False)

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    docker_run_commands = data.get('commands')
    if not docker_run_commands:
        return jsonify({'error': 'No commands provided'}), 400

    try:
        preprocessed_commands = [preprocess_command(cmd) for cmd in docker_run_commands]
        services = [parse_docker_run(cmd) for cmd in preprocessed_commands]
        docker_compose_content = generate_docker_compose(services)
        return jsonify({'docker_compose': docker_compose_content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
