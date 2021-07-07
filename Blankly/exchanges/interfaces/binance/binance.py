"""
    binance exchange definitions and setup
    Copyright (C) 2021  Emerson Dove

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


from Blankly.exchanges.exchange import Exchange
from Blankly.utils import utils
import Blankly.exchanges.auth.auth_constructor

from binance.client import Client


class Binance(Exchange):
    def __init__(self, portfolio_name=None, keys_path="keys.json", settings_path=None):
        Exchange.__init__(self, "binance", portfolio_name, keys_path, settings_path)

    """
    Builds information about the symbol on this exchange by making particular API calls
    """
    def get_asset_state(self, symbol):
        """
        Portfolio state is the internal properties for the exchange block.
        """
        # TODO Populate this with useful information
        symbol = utils.get_base_asset(symbol)
        account = self.Interface.get_account(symbol=symbol)
        return account

    def get_exchange_state(self):
        """
        Exchange state is the external properties for the exchange block
        """
        # TODO Populate this with useful information
        return self.Interface.get_fees()

    def get_direct_calls(self) -> Client:
        return self.calls