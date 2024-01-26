import os
import paramiko
import seaborn as sns
import matplotlib.pyplot as plt
from paramiko import Ed25519Key
from datetime import datetime
import shutil


def download_most_recent(
    server_ip,
    username,
    private_key_path,
    base_folder,
    pathology,
    agent,
    model,
    addendum,
    destination_folder,
    folder_position=0,
):
    if server_ip:
        private_key = Ed25519Key.from_private_key_file(private_key_path)
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)
        client.connect(server_ip, username=username, pkey=private_key)
        sftp = client.open_sftp()
        listdir = sftp.listdir
        copy = sftp.get
    else:
        listdir = os.listdir
        copy = shutil.copy

    all_folder_files = listdir(base_folder)

    base_folder = base_folder.rstrip("/")

    folder_date_mapping = {}
    if not addendum:
        addendum = tuple(str(i) for i in range(10))
    for item in all_folder_files:
        if item.startswith(f"{pathology}_{agent}_{model}_") and item.endswith(addendum):
            n_underscore = addendum.count("_")
            if n_underscore == 0:
                date_time_str = "_".join(item.split("_")[-2:])
            else:
                date_time_str = "_".join(
                    item.split("_")[-(2 + n_underscore) : -n_underscore]
                )
            date_time_obj = datetime.strptime(date_time_str, "%d-%m-%Y_%H:%M:%S")
            folder_date_mapping[item] = date_time_obj

    latest_folder = sorted(
        folder_date_mapping, key=folder_date_mapping.get, reverse=True
    )[folder_position]

    files = listdir(os.path.join(base_folder, latest_folder))
    for file in files:
        if "_results" in file:
            remote_file_path = os.path.join(base_folder, latest_folder, file)
            local_file_path = os.path.join(destination_folder, file)
            copy(remote_file_path, local_file_path)

    if server_ip:
        client.close()


def download_most_recent_FI(
    server_ip,
    username,
    private_key_path,
    base_folder,
    pathology,
    model,
    addendum,
    destination_folder,
    folder_position=0,
):
    if server_ip:
        private_key = Ed25519Key.from_private_key_file(private_key_path)
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)
        client.connect(server_ip, username=username, pkey=private_key)
        sftp = client.open_sftp()
        listdir = sftp.listdir
        copy = sftp.get
    else:
        listdir = os.listdir
        copy = shutil.copy

    base_folder = base_folder.rstrip("/")

    all_folder_files = listdir(base_folder)
    folder_date_mapping = {}
    for item in all_folder_files:
        if item.startswith(f"{pathology}_{model}_") and item.endswith(
            f"_FULL_INFO{addendum}"
        ):
            n_underscore = addendum.count("_")
            date_time_str = "_".join(
                item.split("_")[-(4 + n_underscore) : -(2 + n_underscore)]
            )
            date_time_obj = datetime.strptime(date_time_str, "%d-%m-%Y_%H:%M:%S")
            folder_date_mapping[item] = date_time_obj

    latest_folder = sorted(
        folder_date_mapping, key=folder_date_mapping.get, reverse=True
    )[folder_position]

    files = listdir(os.path.join(base_folder, latest_folder))
    for file in files:
        if "_results" in file or ".log" in file:
            remote_file_path = os.path.join(base_folder, latest_folder, file)
            local_file_path = os.path.join(destination_folder, file)
            copy(remote_file_path, local_file_path)

    if server_ip:
        client.close()


server_ip = ""  # IP of your server or cluster (if you are using one). Leave blank if you have direct access
username = ""  # Relevant if you are using a server or cluster
private_key_path = ""  # Relevant if you are using a server or cluster
base_folder = ""  # Base folder of where the runs are saved
destination_folder = ""  # Base folder where you want to download the runs

agent = "ZeroShot"

full_info = True  # Change between True and False depending on if you are download CDM-FI or normal CDM runs
folder_position = 0  # This specifies only the most recent run should be downloaded

for addendum in ["_PLI_N"]:
    for model in [
        "WizardLM-70B-V1.0-GPTQ",
        "Llama2-70B-OASST-SFT-v10-GPTQ",
        "Llama-2-70B-chat-GPTQ",
    ]:
        # for model in ['ClinicalCamel-70B-GPTQ', 'Meditron-70B-GPTQ']:
        for pathology in [
            "appendicitis",
            "cholecystitis",
            "pancreatitis",
            "diverticulitis",
        ]:
            if full_info:
                download_most_recent_FI(
                    server_ip,
                    username,
                    private_key_path,
                    base_folder,
                    pathology,
                    model,
                    addendum,
                    destination_folder,
                    folder_position,
                )
            else:
                download_most_recent(
                    server_ip,
                    username,
                    private_key_path,
                    base_folder,
                    pathology,
                    agent,
                    model,
                    addendum,
                    destination_folder,
                    folder_position,
                )
