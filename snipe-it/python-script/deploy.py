import os
from subprocess import check_output
from dotenv import load_dotenv
from jinja2 import Template

# Load all environmental variables
load_dotenv(dotenv_path=".env")
load_dotenv(dotenv_path=".env.secret")
load_dotenv(dotenv_path=".env.configmap")

# Run script in debug mode
# If set to true, no changes are applied to cluster
# and the rendered files are created under /.local
DEBUG = True
if os.environ['DEBUG'].lower() == "false":
    DEBUG = False

# Directory for manifest templates
directory = 'manifests'  # set directory path

K8S_NAMESPACE = os.environ['K8S_NAMESPACE']

# Create secret from .env file
def create_secret(env_path):
    # Create command
    create_cmd   = \
        f"kubectl --namespace={K8S_NAMESPACE} create secret generic snipe-it --from-env-file={env_path} \
            -o=yaml --dry-run=client \
            > ./.local/secret.yaml"
    if not DEBUG:
        create_cmd   = f"kubectl --namespace={K8S_NAMESPACE} create secret generic snipe-it --from-env-file={env_path}"
    
    # Run command
    apply_cmd = check_output(args=create_cmd, text=True, shell=True)
    return apply_cmd


# Create configmap from .env-configmap
def create_configmap(env_path):
    # Create command
    create_cmd   = \
        f"kubectl --namespace={K8S_NAMESPACE} create configmap snipe-it --from-env-file={env_path} \
            -o=yaml --dry-run=client \
            > ./.local/configmap.yaml"
    if not DEBUG:
        create_cmd   = f"kubectl  --namespace={K8S_NAMESPACE} create configmap snipe-it --from-env-file={env_path}"
    
    # Run command
    apply_cmd = check_output(args=create_cmd, text=True, shell=True)
    return apply_cmd


# Render templates
def render_templates():
    rendered_files = ""
    for entry in os.scandir(directory):  

        # check if it's a file
        if entry.is_file():
            with open(entry.path, "r") as f:
                text = f.read()
            template = Template(text)

            # Add rendered files to variables
            rendered_files += template.render(env=os.environ)
            # Seperate manifests
            rendered_files += "\n\n---\n"

    return rendered_files


# Apply rendered_files k8s manifests
def apply_mainfests(rendered_files):
   
    # Create command
    apply_manifests_cmd   = f"kubectl apply -o=yaml --dry-run=client -f -"
    if not DEBUG:
        apply_manifests_cmd   = f"kubectl apply -f -"
   
    # Run command
    apply_manifests_value = \
        check_output(args=apply_manifests_cmd, input=rendered_files, text=True, shell=True)
    
    # Return command value
    return apply_manifests_value


if __name__ == '__main__':

    create_configmap(".env-configmap")
    create_secret(".env-secret")

    rendered_files = render_templates()

    if DEBUG:
        with open(".local/rendered.yaml", "w") as f:
            f.write(rendered_files)

    return_val = apply_mainfests(rendered_files)
    print(return_val)

    exit(0)