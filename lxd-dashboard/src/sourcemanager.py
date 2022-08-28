# sourcemanager
import io
import sys
import tarfile
from subprocess import CalledProcessError
import requests
from pathlib import Path
import os
import re
import logging

logger = logging.getLogger(__name__)


def fetch_and_extractall(tarfile_url, dst="/tmp/", tarfilemode="r:gz"):
    """
    Fetch and extract a remote URL as a file to a destination path on the filesystem.
    Extracts it.
    Tarfilemode is from tarfile (defaults as r:gz)
    E.g. "r:bz2", "r:gz" etc.

    Returns the absolute Path(filename) if successful. None if not.
    """
    try:
        response = requests.get(tarfile_url, allow_redirects=True, stream=True)
        with tarfile.open(fileobj=io.BytesIO(response.content), mode=tarfilemode) as tfile:
            tfile.extractall(path=Path(dst))
        d = response.headers['content-disposition']
        fname = re.findall("filename=(.+)", d)[0]
        logging.debug("Downloaded FILE: %s", fname)
        if response.status_code == 200:
            return Path(dst).joinpath(fname)
        else:
            return None
    except Exception as e:
        print(e)
        sys.exit(-1)



def fetchGithub(owner, repo, tag_name='latest', dst='/tmp/'):
    """
    Downloads a release file to dst path give the owner, repo name, tag_name.

    Returns a tuple of (str,Path): <name>.<path to downloaded github release file>.

    """
    headers = {
    'Accept': 'application/vnd.github+json',
    }

    if tag_name == 'latest':
        response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/releases/latest", headers=headers)
    else:
        response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{tag_name}", headers=headers)

    tarball_url = response.json()['tarball_url']
    
    r = requests.get(tarball_url, allow_redirects=True, stream=True)

    tarball_filename = r.headers['content-disposition']
    
    fname = re.findall("filename=(.+)", tarball_filename)[0]
    
    logging.debug("Downloaded FILE: %s", fname)

    logging.debug("Saving downloaded file to: " + str(Path(dst).joinpath(fname)) )

    open(Path(dst).joinpath(fname), 'wb').write(r.content)

    # Return the name + Path
    return (response.json()['name'], Path(dst).joinpath(fname))


def extractReleaseFile(filename, dst='/tmp', tarfilemode='r:gz'):
    """
    Extracts a tarfile

    Returns the Path(top-dir) of the extracted tarfile.
    """
    with tarfile.open(filename, mode=tarfilemode) as tfile:
        logging.debug(f"Extracting {filename} to:" + str(dst) + os.path.commonprefix(tfile.getnames())) 
        tfile.extractall(path=Path(dst))
        return Path(dst).joinpath(os.path.commonprefix(tfile.getnames()))


def fetch_and_extractall_github_release_tag_name(owner, repo, tag_name='latest', dst='/tmp/', tarfilemode='r:gz'):
    """
    Fetches a given tag_name (release) from github.com
    """
    headers = {
    'Accept': 'application/vnd.github+json',
    }

    try:
        if tag_name == 'latest':
            response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/releases/latest", headers=headers)
        else:
            response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{tag_name}", headers=headers)

        tarball_url = response.json()['tarball_url']

        print(tarball_url)

        response = requests.get(tarball_url, allow_redirects=True, stream=True)

        d = response.headers['content-disposition']
        fname = re.findall("filename=(.+)", d)[0]
        logging.debug("Downloaded FILE: %s", fname)

        with tarfile.open(fileobj=io.BytesIO(response.content), mode=tarfilemode) as tfile:
            print(f"Extracting {fname} to:", dst + os.path.commonprefix(tfile.getnames()))
            logging.debug(f"Extracting {fname} to:", dst, os.path.commonprefix(tfile.getnames())) 
            tfile.extractall(path=Path(dst))
        
        if response.status_code == 200:
            return Path(dst).joinpath(fname)
        else:
            return None

    except tarfile.ExtractError as e:
        print("Failed extracting: ", str(e))
        sys.exit(-1)

    except Exception as e:
        print("Failed downloading release:", str(e))
        sys.exit(-1)
    
    
def getGitHubTarByTagName(owner, repo, tag_name='latest', dst='/tmp/', tarfilemode='r:gz'):
    headers = {
    'Accept': 'application/vnd.github+json',
    }

    try:
        if tag_name == 'latest':
            response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/releases/latest", headers=headers)
        else:
            response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{tag_name}", headers=headers)

        tarball_url = response.json()['tarball_url']

        response = requests.get(tarball_url, allow_redirects=True, stream=True)

        d = response.headers['content-disposition']
        fname = re.findall("filename=(.+)", d)[0]
    except Exception as e:
        print("Failed downloading release:", str(e))
        sys.exit(-1)
