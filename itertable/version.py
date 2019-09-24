from pkg_resources import get_distribution, DistributionNotFound
try:
    VERSION = get_distribution("itertable").version
except DistributionNotFound:
    VERSION = "0.0.0"
