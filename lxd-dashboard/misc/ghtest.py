import requests
import sourcemanager

# sourcemanager.fetch_and_extractall_github_release_tag_name('lxdware', 'lxd-dashboard', tag_name='latest', dst='/tmp/')

f = sourcemanager.fetchGithub('lxdware', 'lxd-dashboard', tag_name='latest', dst='/tmp/')

print(f[0])
print(f[1])

print( sourcemanager.extract(f) )
