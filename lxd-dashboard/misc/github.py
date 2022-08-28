import requests

tag_name='latest'
owner='lxdware'
repo='lxd-dashboard'

headers = {
    'Accept': 'application/vnd.github+json',
}

if tag_name == 'latest':
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/releases/latest", headers=headers)
else:
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{tag_name}", headers=headers)

tuple = (response.json()['name'], response.json()['tarball_url'])

print(tuple)
