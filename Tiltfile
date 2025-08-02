# print("""
# -----------------------------------------------------------------
# ✨ Hello Tilt! This appears in the (Tiltfile) pane whenever Tilt
#    evaluates this file.
# -----------------------------------------------------------------
# """.strip())
# warn('ℹ️ Open {tiltfile_path} in your favorite editor to get started.'.format(
#     tiltfile_path=config.main_path))
# Run local commands

update_settings(
    k8s_upsert_timeout_secs=300,
)


local_resource('install-helm',
               cmd='which helm > /dev/null || brew install helm',
)

settings = {
    'profile': 'dev',
}
# cli_args = config.parse()
settings.update(read_json(
    "tilt_config.json",
    default = {},
))

# k8s_yaml('cluster-config/k8s/ingress-nginx/01-namespace.yaml')

load('ext://helm_resource', 'helm_resource', 'helm_repo')

k8s_yaml('helm-charts/backend/templates/01-namespace.yaml')


docker_build(
    'backend',
    context='.',
    dockerfile='Dockerfile',
    live_update=[
        sync('./backend', '/app'),
        run('pip install --no-cache-dir -r requirements.txt', trigger=['requirements.txt']),
    ],
    build_args={
        'ENV': 'bob',
    }
    )


# Load Kubernetes YAML
k8s_yaml(['helm-charts/backend/templates/deployment.yaml', 'helm-charts/backend/templates/service.yaml'])
k8s_resource('backend',
             # map one or more local ports to ports on your Pod
             port_forwards=['8000:8000', "5678:5678"],
             # change whether the resource is started by default
             auto_init=False,
             # control whether the resource automatically updates
             trigger_mode=TRIGGER_MODE_AUTO,
             # alter envs
            #  resource_deps=['ingress-nginx-controller', 'cert-manager'],
            
)

k8s_yaml(['helm-charts/database/templates/deployment.yaml', 'helm-charts/database/templates/service.yaml'])
k8s_resource('database',
             # map one or more local ports to ports on your Pod
             port_forwards=['5432:5432'],
             # change whether the resource is started by default
             auto_init=False,
             # control whether the resource automatically updates
             trigger_mode=TRIGGER_MODE_AUTO,
)
