"""
    Logging system to allow users to view & understand actions done in the strategy
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

import pandas
from typing import Union
from datetime import datetime as dt

import blankly
from blankly.exchanges.interfaces.abc_exchange_interface import ABCExchangeInterface
from blankly.exchanges.orders.market_order import MarketOrder
from blankly.exchanges.orders.limit_order import LimitOrder
from blankly.utils.utils import AttributeDict


class StrategyLogger(ABCExchangeInterface):
    def __init__(self, interface=None, strategy=None):
        self.interface = interface
        self.strategy = strategy

    def get_calls(self):
        return self.interface.get_calls()
    
    def get_exchange_type(self):
        return self.interface.get_exchange_type()
    
    def get_account(self, symbol: str = None) -> AttributeDict:
        out = self.interface.get_account(symbol)

        # Log this with the account info as well as the account it was attached to
        blankly.reporter.log_strategy_event(self.strategy, 'get_account', out, symbol=symbol)
        return out
    
    def get_products(self):
        return self.interface.get_products()

    def get_product_history(self, symbol: str, epoch_start: float,
                            epoch_stop: float, resolution: Union[str, int]) -> pandas.DataFrame:
        return self.interface.get_product_history(symbol, epoch_start, epoch_stop, resolution)
    
    def history(self,
                symbol: str,
                to: Union[str, int] = 200,
                resolution: Union[str, int] = '1d',
                start_date: Union[str, dt, float] = None,
                end_date: Union[str, dt, float] = None,
                return_as: str = 'df') -> pandas.DataFrame:
        if end_date is None:
            end_date = self.strategy.time()
        return self.interface.history(symbol, to=to,
                                      resolution=resolution, start_date=start_date,
                                      end_date=end_date, return_as=return_as)
    
    def market_order(self, symbol: str, side: str, size: float) -> MarketOrder:
        out = self.interface.market_order(symbol, side, size)

        # Record this market order along with the arguments
        blankly.reporter.log_strategy_event(self.strategy, 'market_order', out,
                                            symbol=symbol, side=side,
                                            funds=size)
        return out
    
    def limit_order(self, symbol: str, side: str, price: float, size: float) -> LimitOrder:
        out = self.interface.limit_order(symbol, side, price, size)

        # Record limit order along with the arguments
        blankly.reporter.log_strategy_event(self.strategy, 'limit_order', out,
                                            symbol=symbol, side=side,
                                            price=price, size=size)
        return out
    
    def cancel_order(self, symbol: str, order_id: str) -> dict:
        out = self.interface.cancel_order(symbol, order_id)

        # Record the cancellation along with the arguments
        blankly.reporter.log_strategy_event(self.strategy, 'cancel_order', out,
                                            symbol=symbol, order_id=order_id)
        return out

    def get_open_orders(self, symbol: str = None) -> list:
        return self.interface.get_open_orders(symbol=symbol)

    def get_order(self, symbol: str, order_id: str) -> dict:
        return self.interface.get_order(symbol, order_id)

    def get_fees(self) -> dict:
        return self.interface.get_fees()

    def get_order_filter(self, symbol: str):
        return self.interface.get_order_filter(symbol)
    
    def get_price(self, symbol: str) -> float:
        return self.interface.get_price(symbol)

    @property
    def account(self) -> AttributeDict:
        return self.interface.account
    
    @property
    def orders(self) -> list:
        return self.interface.orders

    @property
    def cash(self) -> float:
        return self.interface.cash
    
