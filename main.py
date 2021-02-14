import pandas as pd
import numpy as np
import csv

column_names = ['name', 2, 'bid_price', 'ask_price', 'trade_price', 'bid_vol', 'ask_vol', 'trade_vol', 'update_type',
                10, 'date', 'time', 'opening_price', 14, 'code', 16]

df = pd.read_csv("scandi.csv", names=column_names)
df = df.drop([2, 10, 14, 16], axis=1)
df = df.loc[~(df.code.str.contains('UT', na=False))]
df = df.loc[((df.update_type == 1) | (df.update_type == 2) | (df.update_type == 3))]

stocks = df.name.unique()
# codes = df.code.unique()
# update = df.update_type.unique()
# print(codes)
# print(update)
# print(stocks)
# print(len(stocks))
# crosslist=list()
with open('results.csv', 'w', newline='') as result_file:
    wr = csv.writer(result_file, quoting=csv.QUOTE_NONE)
    wr.writerow(['Stock Identifier', 'Mean Time Between Trades', 'Median Time Between Trades',
                 'Longest Time Between Trades', 'Mean Time Between Ticks', 'Median Time Between Ticks',
                 'Longest Time Between Ticks', 'Mean Bid-Ask Spread', 'Median Bid-Ask Spread',
                 'Round Number Price Probability', 'Round Number Volume Probability', 'Trade Price Growth'])
    for x in stocks:
        time_trades = list()
        time_ticks = list()
        bid_ask_spread = list()
        current_stock = df.loc[(df['name'] == x)]
        first_loop = True
        longest_time_trade = 0
        longest_time_tick = 0
        cross_count = 0
        round_price_count = 0
        round_volume_count = 0
        current_trades = current_stock.loc[(current_stock['update_type'] == 1)]
        no_of_trades = len(current_trades)

        prev_bid_ask_spread = 0.0

        for i in current_stock.itertuples(index=False):
            if i.update_type == 1:
                if first_loop is True:
                    first_loop = False

                elif i.date == temp.date:
                    time_diff = i.time - temp.time
                    tick_diff = i.trade_price - temp.trade_price
                    # if time_diff != 0:
                    # if i.bid_price > i.ask_price:
                    # crosslist.append(i)
                    # cross_count = cross_count+1
                    time_trades.append(time_diff)
                    if time_diff > longest_time_trade:
                        longest_time_trade = time_diff
                    if tick_diff != 0:
                        time_ticks.append(time_diff)
                        if time_diff > longest_time_tick:
                            longest_time_tick = time_diff
                # else: print("skipped")
                if str(i.trade_price).endswith('0'):
                    round_price_count = round_price_count + 1
                if str(i.trade_vol).endswith('0'):
                    round_volume_count = round_volume_count + 1
                temp = i

            current_bid_ask_spread = i.ask_price - i.bid_price
            if (current_bid_ask_spread > 0) & (current_bid_ask_spread != prev_bid_ask_spread):
                bid_ask_spread.append(current_bid_ask_spread)
                prev_bid_ask_spread = current_bid_ask_spread

        # print(cross_count)
        # f=open('listfile1.txt', "w")
        # for listitem in crosslist:
        #    f.write('%s\n' % str(listitem))
        time_trades.sort()
        mean_time_trade = np.mean(time_trades)
        print(repr(x) + ' Mean Time Between Trades = ' + repr(mean_time_trade))
        median_time_trade = np.median(time_trades)
        print(repr(x) + ' Median Time Between Trades = ' + repr(median_time_trade))
        print(repr(x) + ' Longest Time Between Trades = ' + repr(longest_time_trade) + '\n')
        time_ticks.sort()
        mean_time_tick = np.mean(time_ticks)
        print(repr(x) + ' Mean Time Between Ticks = ' + repr(mean_time_tick))
        median_time_tick = np.median(time_ticks)
        print(repr(x) + ' Median Time Between Ticks = ' + repr(median_time_tick))
        print(repr(x) + ' Longest Time Between Ticks = ' + repr(longest_time_tick) + '\n')
        if round_price_count == 0:
            round_price = 0
            print(repr(x) + ' Round Number Effect Price = 0%')
        else:
            round_price = (round_price_count / no_of_trades) * 100
            print(repr(x) + ' Round Number Effect Price = ' + repr(round_price) + '%')
        if round_volume_count == 0:
            round_volume = 0
            print(repr(x) + ' Round Number Effect Volume = 0%\n')
        else:
            round_volume = (round_volume_count / no_of_trades) * 100
            print(repr(x) + ' Round Number Effect Volume = ' + repr(round_volume) + '%\n')
        if len(current_trades) != 0:
            first_trade_price = current_trades['trade_price'][current_trades.index[0]]
            last_trade_price = current_trades['trade_price'][current_trades.index[-1]]
            trade_growth = ((last_trade_price - first_trade_price) / first_trade_price) * 100
            print(repr(x) + ' Value Growth Percentage = ' + repr(trade_growth) + '%\n')
        else:
            trade_growth = 0
            print(repr(x) + ' Value Growth Percentage = 0%\n')

        bid_ask_spread.sort()
        mean_bid_ask_spread = np.mean(bid_ask_spread)
        print(repr(x) + ' Mean Bid Ask Spread = ' + repr(mean_bid_ask_spread))
        median_bid_ask_spread = np.median(bid_ask_spread)
        print(repr(x) + ' Median Bid Ask Spread = ' + repr(median_bid_ask_spread) + '\n')
        wr.writerow([i.name, mean_time_trade, median_time_trade, longest_time_trade,
                     mean_time_tick, median_time_tick, longest_time_tick, mean_bid_ask_spread,
                     median_bid_ask_spread, round_price, round_volume, trade_growth])
