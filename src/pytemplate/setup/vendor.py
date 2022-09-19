import os
import sys
from typing import Optional

from pytemplate.log import LOG


def setup_vendor(
    current=os.path.dirname(__file__),
) -> Optional[str]:
    """ Setup Python module vendoring if present """
    dev_vendor = os.path.join(
        current,
        '..',
        '..',
        'vendor',
    )
    if os.path.isdir(dev_vendor):
        sys.path.insert(
            0,
            os.path.abspath(dev_vendor),
        )
        LOG.info(f'Using development vendor packages at {dev_vendor}')
        return 'dev'


    for i in range(2, 6):
        vendor = os.path.join(
            current,
            *(['..'] * i),
            'pytemplate',
            'vendor',
        )
        if os.path.isdir(vendor):
            sys.path.insert(
                0,
                os.path.abspath(vendor),
            )
            return 'system'
    LOG.info(
        'No pytemplate/vendor folder found, not loading vendored packages'
    )
    return None

