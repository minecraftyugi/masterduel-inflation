import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

class BarChart:
    def __init__(self, deck_stats) -> None:
        self.deck_stat = deck_stats

    def draw(self):
        rates = self.deck_stat.get_monthly_inflation_rates()[:12]
        start_dates = self.deck_stat.get_start_dates()[:12]
        perc_rates = [percent_format(rate) for rate in rates]

        # reverse start dates and percentage rates so the graph is in chronological order
        start_dates = start_dates[::-1]
        perc_rates = perc_rates[::-1]

        fig, ax = plt.subplots(figsize =(16, 9))

        x = np.arange(len(rates))
        ax.set_title('Monthly Inflation Rate for the 10 Most Popular Decks Over One Year')
        ax.set_ylabel('Inflation Rate (% Change)')
        ax.set_xticks(x)
        ax.set_xticklabels(start_dates)
        ax.set_xlabel('Month')

        bars = ax.bar(x, perc_rates)
        ax.bar_label(bars)
 
        plt.show()


        
class LineChart:
    def __init__(self, deck_stats) -> None:
        self.deck_stats = deck_stats

    def draw(self):
        rates = self.deck_stats.get_yearly_inflation_rates()[:12]
        ur_rates = self.deck_stats.get_yearly_ur_inflation_rates()[:12]
        sr_rates = self.deck_stats.get_yearly_sr_inflation_rates()[:12]
        other_rates = self.deck_stats.get_yearly_other_inflation_rates()[:12]
        start_dates = self.deck_stats.get_start_dates()[:12]
        perc_rates = [percent_format(rate) for rate in rates]
        ur_perc_rates = [percent_format(rate) for rate in ur_rates]
        sr_perc_rates = [percent_format(rate) for rate in sr_rates]
        other_perc_rates = [percent_format(rate) for rate in other_rates]

        # reverse start dates and percentage rates so the graph is in chronological order
        start_dates = start_dates[::-1]
        perc_rates = perc_rates[::-1]
        ur_perc_rates = ur_perc_rates[::-1]
        sr_perc_rates = sr_perc_rates[::-1]
        other_perc_rates = other_perc_rates[::-1]

        fig, ax = plt.subplots(figsize =(16, 9))

        x = np.arange(len(rates))
        ax.set_title('Yearly Percent Changes for the 10 Most Popular Decks')
        ax.set_ylabel('% Change')
        ax.set_xticks(x)
        ax.set_xticklabels(start_dates)
        ax.set_xlabel('Month')
        ax.yaxis.set_major_locator(ticker.MultipleLocator(5))

        ax.plot(start_dates, perc_rates, label="total deck cost")
        ax.plot(start_dates, ur_perc_rates, label="total URs")
        ax.plot(start_dates, sr_perc_rates, label="total SRs")
        ax.plot(start_dates, other_perc_rates, label="total N/Rs")
        ax.legend()
        plt.grid(axis="y")
        plt.show()

def percent_format(n):
    return round((n - 1) * 100, 2)