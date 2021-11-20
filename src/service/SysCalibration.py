import pandas as pd
from scipy import interpolate
import numpy as np
from store.mongoStore import MongoStore


class Calibrate_System:
    def __init__(self, cycles=3):
        self.cycles = cycles
        self.dt_intervals = 100
        self.target_mass = 2000
        self.max_per_diff = 100
        self.start_time = 10
        self.clip_mass = 3500
        self.a_cal = 189
        self.b_cal = -26
        self.store = MongoStore.getInstance()

    def compile_data(self, times):
        self.df_cycles = []
        for t in times:
            cycle_data = self.store.getMass(t[0], t[1], 0, 2048)
            df = pd.DataFrame.from_dict(cycle_data, orient='columns')
            df.set_index('time', inplace=True)
            df_mass = df['mass'].dropna().to_frame()
            df_mass.reset_index(inplace=True)

            f_mass = interpolate.interp1d(list(df_mass.time), list(df_mass.mass), fill_value='extrapolate')
            tnew = np.linspace(np.min([list(df_mass.time) ]),np.max([list(df_mass.time) ]),self.dt_intervals)
            df_cycle = pd.DataFrame({'time': tnew,'mass': f_mass(tnew)})

            df_cycle.loc[:, "time"] = df_cycle["time"].apply(lambda x: x - np.min(tnew))

            # extract only info related to filling operation,
            idx = df_cycle.query('mass >'+str(self.clip_mass)+'or time <' +str(str(self.start_time))+ 'or time > 30').index
            df_cycle.drop(idx, inplace=True)

            # drop cycles with less than 3 datapoints
            if len(df_cycle) < 3:
                pass
            else:
                self.df_cycles.append(df_cycle)

        # get estimates based on fits to indivdual cycles
        cycle_predictions = []
        for df in self.df_cycles:
            a, b = np.polyfit(df.time, df.mass, 1)
            estimate_t = (self.target_mass - b)/a
            cycle_predictions.append(estimate_t)
        mean_predictions = np.mean(cycle_predictions)

        # remove cycles that have a prediction to far from the mean prediction of all cycles
        bad_cycles = []
        for i,cycle_pred in enumerate(cycle_predictions):
            per_diff = (cycle_pred/mean_predictions)*100
            if per_diff > self.max_per_diff:
                #print('outlier',per_diff)
                bad_cycles.append(i)
        self.df_cycles = [i for j, i in enumerate(self.df_cycles) if j not in bad_cycles]
        return self.df_cycles



    def calibrate_constants(self):


        a_cal= []
        b_cal = []
        for cycle,df in enumerate(self.df_cycles):
            a, b = np.polyfit(df.time, df.mass, 1)
            a_cal.append(a)
            b_cal.append(b)
        self.a_cal = np.mean(a_cal)
        self.b_cal = np.mean(b_cal)
        return { 'a': self.a_cal, 'b': self.b_cal }

    def predict(self,delta_mass):
        delta_t = (delta_mass - self.b_cal)/self.a_cal
        return delta_t

