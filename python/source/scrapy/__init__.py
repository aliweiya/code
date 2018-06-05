"""
Scrapy - a web crawling and web scraping framework written for Python
"""
# __all__指定的是指此包被import * 的时候, 哪些模块会被import进来
__all__ = ['__version__', 'version_info', 'twisted_version',
           'Spider', 'Request', 'FormRequest', 'Selector', 'Item', 'Field']

# __path__指定了包的搜索路径
# 默认情况下只有一个元素, 就是当前包的路径, 修改__path__, 可以修改此包内的搜索路径.
# __path__.insert(0,os.path.join(dirname,'Linux'))

# Scrapy version
# https://docs.python.org/2/library/pkgutil.html
# Get a resource from a package
import pkgutil
__version__ = pkgutil.get_data(__package__, 'VERSION').decode('ascii').strip()
version_info = tuple(int(v) if v.isdigit() else v
                     for v in __version__.split('.'))
del pkgutil

# Check minimum required Python version
import sys
if sys.version_info < (2, 7):
    print("Scrapy %s requires Python 2.7" % __version__)
    sys.exit(1)

# Ignore noisy twisted deprecation warnings
# https://docs.python.org/2/library/warnings.html
# Insert an entry into the list of warnings filters (at the front).
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning, module='twisted')
del warnings

# Apply monkey patches to fix issues in external libraries
from . import _monkeypatches
del _monkeypatches

from twisted import version as _txv
twisted_version = (_txv.major, _txv.minor, _txv.micro)

# Declare top-level shortcuts
from scrapy.spiders import Spider
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from scrapy.item import Item, Field

del sys
