import json

def convert_devcontainer_to_dockerfile(devcontainer_path):
    with open(devcontainer_path, 'r') as file:
        devcontainer = json.load(file)
    
    dockerfile_lines = []
    
    # Base image
    base_image = devcontainer.get('image', '')
    if base_image:
        dockerfile_lines.append(f'FROM {base_image}')
    
    # Customizations: VS Code extensions are not applicable in Dockerfile, so we skip those.
    
    # Update content command
    update_command = devcontainer.get('updateContentCommand', '')
    if update_command:
        dockerfile_lines.append('RUN ' + update_command.replace('&&', '\\\n    &&'))
    
    # Post attach command: This is typically not directly translatable to a Dockerfile command,
    # but we can add it as a comment for reference or adapt if feasible.
    post_attach_command = devcontainer.get('postAttachCommand', '')
    if post_attach_command:
        dockerfile_lines.append('# Post Attach Command (for reference, adjust as needed):')
        dockerfile_lines.append('# ' + str(post_attach_command))
    
    # Write the Dockerfile
    with open('Dockerfile', 'w') as dockerfile:
        dockerfile.write('\n'.join(dockerfile_lines))
    
    print('Dockerfile generated successfully.')

# Example usage
convert_devcontainer_to_dockerfile('path/to/your/.devcontainer.json')