from io import BytesIO
from matplotlib.figure import Figure
from base64 import b64encode


class Show():

    def __init__(self, coins, daily):
        self.coins = coins
        self.bins = []
        self.values = []
        self.daily = daily
        self.coin_saved_week = []

    def get_coin_saved_week(self):
        """
        The get_coin_saved_week function is a method of the Coin class. It takes no arguments and returns
        a list of Daily objects that have the same name as the coin attribute

        :param self: Allow the function to refer to itself
        :return: A list of all the coins that have the same name that were saved in a week

        """
        [self.coin_saved_week.append(i) for i in self.daily if i.name == self.coins.name]
        return self.coin_saved_week

    def figure_gain_value(self):
        """
        The figure_gain_value function is used to create a graph that shows the evolution of the value of coins saved over time.
        It takes as input a list of CoinSavedWeek objects and returns an image url.

        :param self: Access variables that belongs to the class
        :return: A figure that represents the evolution of the value of coins saved during a week
        """
        """"""

        self.get_coin_saved_week()
        for d in self.coin_saved_week:
            self.bins.append(d.date_add.strftime('%m-%d'))
            print(d.date_add.strftime('%m-%d'))
            self.values.append(d.value - self.coins.value)
        self.bins[0] = ''
        ## The figure style is set here
        fig = Figure()
        ax = fig.subplots()
        ax.spines['bottom'].set_color('#dddddd')
        ax.spines['top'].set_color('#100f0f')
        ax.spines['left'].set_color('#dddddd')
        ax.spines['right'].set_color('#100f0f')
        ax.yaxis.label.set_color('#1fc36c')
        ax.xaxis.label.set_color('#1fc36c')
        ax.set_facecolor('#100f0f')
        fig.patch.set_facecolor('#100f0f')
        ax.tick_params(axis='x', colors='#1fc36c')
        ax.tick_params(axis='y', colors='#1fc36c')
        ax.spines['bottom'].set_position('center')
        fig.suptitle("semaine", fontsize=10, color='#1fc36c',y=0.1)

        ## The figure is plotted here

        ax.plot(self.bins, self.values, color='#1fc36c')
        if len(self.bins) > 1:
            maxi = max(self.values)
            mini = min(self.values)
            if abs(maxi) > abs(mini):
                ax.set(xlabel='', ylabel='valeur des gains en euros', xlim=(0, 8), ylim=(((maxi * 1.3) * -1), maxi*1.3))
            else:
                ax.set(xlabel='', ylabel='valeur des gains en euros', xlim=(0, 8), ylim=(mini*1.3, ((mini*1.3) * -1)))
        else:
            ax.set(xlabel='', ylabel='valeur des gains en euros', xlim=(0, 8), ylim=(self.values[0]*1.3, ((self.values[0] * 1.3) * -1)))
        b = BytesIO()
        fig.savefig(b, format="png")
        dataurl = 'data:image/png;base64,' + b64encode(b.getvalue()).decode('ascii')
        return dataurl
