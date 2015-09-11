import sys
sys.path.append("../")

from rule_console import settings
from rule_console.api import app
from rule_console.middleware import TestMiddleware
import rule_console.api.rule
import rule_console.api.refer_info
import rule_console.api.common


if __name__ == "__main__":
    app.run(host="0.0.0.0", processes=4, debug=settings.DEBUG)
