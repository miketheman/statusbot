import importlib

from tldextract import TLDExtract


def check_site(site):
    site_name = normalize_site_name(site)

    try:
        module_name = "statusbot.sites." + site_name + "_site"
        imported_module = importlib.import_module(module_name)
    except ImportError:
        raise NotImplementedError

    print(f"Checking site: {site}")
    status = imported_module.status()

    return site_name, status


def normalize_site_name(site_name):
    """Receive a string and compare against known sites and convert to internal name
    Return site domain without any other elements.
    """
    # Prevent the default behavior of TLDExtract making an outbound request to cache TLDs
    tldextractor = TLDExtract(suffix_list_urls=False)
    return tldextractor(site_name).domain.lower()
