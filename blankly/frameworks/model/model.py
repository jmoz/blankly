"""
    An improved strategy simulation layer built for spot and futures trading
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
import typing

from blankly.exchanges.interfaces.paper_trade.backtest_controller import BackTestController, BacktestResult
from blankly.exchanges.interfaces.paper_trade.backtest_headers import ABCBacktestController
from blankly.exchanges.interfaces.paper_trade.paper_trade import PaperTrade
from blankly.exchanges.exchange import Exchange
import time
import blankly


class Model:
    def __init__(self, exchange: Exchange):
        self.__exchange = exchange
        self.__exchange_cache = self.__exchange
        self.is_backtesting = False

        self.interface = exchange.interface

        self.has_data = True

        self.backtester: ABCBacktestController = BackTestController(self)
        # Type these internal calls to the specific backtester
        self.__backtester: BackTestController = self.backtester

    def backtest(self, args, initial_values: dict = None) -> BacktestResult:
        # Construct the backtest controller
        if not isinstance(self.__exchange, Exchange):
            raise NotImplementedError

        # Toggle backtesting
        self.is_backtesting = True
        self.__exchange = PaperTrade(self.__exchange)
        self.interface = self.__exchange.interface
        backtest = self.__backtester.run(args,
                                         initial_account_values=initial_values,
                                         exchange=self.__exchange)
        self.is_backtesting = False
        self.__exchange = self.__exchange_cache
        self.has_data = True

        blankly.reporter.export_backtest_result(backtest)
        return backtest

    def run(self, args: typing.Any = None):
        self.main(args)

    def main(self, args):
        raise NotImplementedError("Add a main function to your strategy to run the model.")

    @property
    def time(self):
        if not self.is_backtesting:
            return time.time()
        else:
            return self.__backtester.time

    def sleep(self, seconds: [int, float]):
        if not self.is_backtesting:
            time.sleep(seconds)
        else:
            self.__backtester.sleep(seconds)