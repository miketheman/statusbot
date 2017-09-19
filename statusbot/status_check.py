from tldextract import TLDExtract

from .sites import github_site
from .sites import twitter_site

KNOWN_SITES = [
    'github',
    'twitter',
]


def check_site(site):
    site_name = normalize_site_name(site)

    if site_name not in KNOWN_SITES:
        raise NotImplementedError

    print("Checking site: {}".format(site))
    # TODO: There must be a better way to call the site checks without a large if/elif
    if site_name == 'github':
        status = github_site.status()
    elif site_name == 'twitter':
        status = twitter_site.status()

    return site_name, status


def normalize_site_name(site_name):
    """Receive a string and compare against known sites and convert to internal name
    Return site domain wihtout any other elements.
    """
    # Prevent the default behavior of TLDExtract making an outbound request to cache TLDs
    tldextractor = TLDExtract(suffix_list_urls=False)
    return tldextractor(site_name).domain
