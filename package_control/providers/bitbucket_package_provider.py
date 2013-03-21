import re

from ..clients.bitbucket_client import BitBucketClient


class BitBucketPackageProvider():
    """
    Allows using a public BitBucket repository as the source for a single package.
    For legacy purposes, this can also be treated as the source for a Package
    Control "repository".

    :param repo:
        The public web URL to the BitBucket repository. Should be in the format
        `https://bitbucket.org/user/package`.

    :param settings:
        A dict containing at least the following fields:
          `cache_length`,
          `debug`,
          `timeout`,
          `user_agent`,
          `http_proxy`,
          `https_proxy`,
          `proxy_username`,
          `proxy_password`
    """

    def __init__(self, repo, settings):
        self.repo = repo
        self.settings = settings

    def match_url(self):
        """Indicates if this provider can handle the provided repo"""

        return re.search('^https?://bitbucket.org', self.repo) != None

    def get_packages(self):
        """
        Uses the BitBucket API to construct necessary info for a package

        :return:
            A list with a single dict containing the keys: "name",
            "description", "url", "author", "last_modified", "download"
        """

        client = BitBucketClient(self.settings)

        repo_info = client.repo_info(self.repo)
        if repo_info == False:
            return False

        download = client.download_info(self.repo)
        if download == False:
            return False

        return [{
            'name': repo_info['name'],
            'description': repo_info['description'],
            'url': repo_info['url'],
            'author': repo_info['author'],
            'last_modified': download.get('date'),
            'download': download
        }]

    def get_renamed_packages(self):
        """For API-compatibility with :class:`PackageProvider`"""

        return {}

    def get_unavailable_packages(self):
        """
        Method for compatibility with PackageProvider class. These providers
        are based on API calls, and thus do not support different platform
        downloads, making it impossible for there to be unavailable packages.

        :return: An empty list
        """
        return []
