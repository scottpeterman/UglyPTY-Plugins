import click
import pandas as pd
import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import datetime
from itertools import islice
from unittest.mock import MagicMock
import sqlite3
from uglyclick_widget.Library.util import cryptonomicon
from yaml.representer import SafeRepresenter

# Create a subclass of str that will be represented as a literal block
class literal_str(str):
    pass

# Add a representational function to use with the new literal_str
def literal_str_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

# Add the representational function to the safe dumper
SafeRepresenter.add_representer(literal_str, literal_str_representer)

def fetch_devices(yaml_file, include=None, exclude=None):
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
    flat_data = []
    for item in data:

        for session in item['sessions']:
            if include in session['display_name']:
                # print(f"Excluding: `{exclude}`")
                if exclude not in session['display_name'] or exclude == "":

                    flat_data.append({
                        'folder_name': item['folder_name'],
                        'credsid': session['credsid'],
                        'display_name': session['display_name'],
                        'host': session['host']
                    })
                else:
                    print(f"Applying exclude: `{exclude}`")
    df = pd.DataFrame(flat_data)

    devices = df.to_dict('records')
    print(f"Devices fetched: {devices}")
    return devices


def get_creds(user_id):
    conn = sqlite3.connect("settings.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM creds WHERE id = ?", (user_id,))
    record = cursor.fetchone()
    encrypted_password = record[1]
    username = record[0]
    conn.close()

    # Decrypt the password
    decrypted_password = cryptonomicon(encrypted_password)
    print(f"Credentials for user {user_id}: {username}, {decrypted_password}")

    return username, decrypted_password

from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException

def ssh_to_device(device):
    print(f"Connecting to device {device['display_name']} ({device['host']}) with username {device['username']}...")

    try:
        connection = ConnectHandler(
            device_type=device['device_type'],
            ip=device['host'],
            username=device['username'],
            password=device['password']
        )

        print("Connected successfully.")
        print(f"Executing command '{device['command']}'...")
        output = connection.send_command(device['command'])
        print(f"Command output: {output}")
        print("Command executed successfully.")
        print("Disconnecting from device...")
        connection.disconnect()

    except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
        print(f"Netmiko Error: {e}")
        output = str(e)
    except Exception as e:
        print(f"General Error: {e}")
        output = str(e)

    output_text_dir = os.path.join(device['output_dir'], 'output_text')
    os.makedirs(output_text_dir, exist_ok=True)
    output_text_file_path = os.path.join(output_text_dir, f"{device['display_name']}.txt")
    print(f"Writing raw output to file: {output_text_file_path}")
    with open(output_text_file_path, 'w') as f:
        f.write(output)

    print(f"Raw output written to file: {output_text_file_path}")

    output_yaml = {
        'device': {
            'credsid': device['credsid'],
            'display_name': device['display_name'],
            'folder_name': device['folder_name'],
            'host': device['host'],
        },
        'output': literal_str(output),
        'status': 'success' if output else 'failure'
    }
    output_yaml_file_path = os.path.join(device['output_dir'], f"{device['display_name']}.yaml")
    print(f"Writing output and meta data to file: {output_yaml_file_path}")
    with open(output_yaml_file_path, 'w') as f:
        yaml.safe_dump(output_yaml, f, default_flow_style=False)

    print(f"Output and meta data written to file: {output_yaml_file_path}")
    return output


def chunks(data, SIZE=10000):
    """Yield successive SIZE-sized chunks from data."""
    for i in range(0, len(data), SIZE):
        yield data[i:i + SIZE]


@click.command()
@click.option('--max-job-size', default=10, help='Maximum job size')
@click.option('--yaml-file', default='./sessions/sessions.yaml', help='Path to the sessions YAML file')
@click.option('--include', multiple=False, help='Strings to include')
@click.option('--exclude', multiple=False, help='Strings to exclude')
@click.option('--netmiko-type', default='cisco_ios', help='Netmiko device type: cisco_xe, arista_eos, junos')
@click.option('--output-dir', default='./Capture', help='Output directory')
@click.option('--command', default='show run', help='Command to run')
@click.option('--user', default=1, help='User ID from settings.sqlite creds table')
def main(max_job_size, yaml_file, include, exclude, netmiko_type, output_dir, command, user):
    max_job_size = int(max_job_size)
    devices = fetch_devices(yaml_file, include, exclude)
    print(f"Total devices fetched: {len(devices)}")
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    for chunk in chunks(devices, max_job_size):
        print(f"Processing chunk of size {len(chunk)}")
        with ThreadPoolExecutor() as executor:
            job_devices = []
            for device in chunk:
                username, password = get_creds(device['credsid'])  # Fetch credentials for each device
                device['device_type'] = netmiko_type
                device['username'] = username
                device['password'] = password
                device['timestamp'] = timestamp
                device['command'] = command
                device['output_dir'] = output_dir
                job_devices.append(device)
            print(f"Devices in the job: {job_devices}")

            futures = {executor.submit(ssh_to_device, device): device for device in job_devices}
            for future in as_completed(futures):
                device = futures[future]
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (device, exc))


if __name__ == '__main__':
    main()
