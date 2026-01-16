import pandas as pd
import numpy as np

class DynamicWeightBuilder:
    def __init__(self, data, id_col, year_col):
        self.data = data.copy()
        self.id_col = id_col
        self.year_col = year_col
        self.years = sorted(data[year_col].unique())
        self.ids = sorted(data[id_col].unique())
        self.n = len(self.ids)
        self._validate_alignment()

    def _validate_alignment(self):
        for year in self.years:
            year_ids = sorted(self.data[self.data[self.year_col] == year][self.id_col].tolist())
            if year_ids != self.ids:
                raise ValueError(f"mhmy-dynaspat Error: Year {year} is missing some IDs or not aligned.")

    def build(self, rule_func, standardize=True):
        dynamic_weights = {}
        for year in self.years:
            year_df = self.data[self.data[self.year_col] == year].sort_values(self.id_col).reset_index(drop=True)
            matrix = np.zeros((self.n, self.n))
            for i in range(self.n):
                for j in range(self.n):
                    if i == j:
                        matrix[i, j] = 0
                        continue
                    matrix[i, j] = rule_func(year_df.iloc[i], year_df.iloc[j])
            
            if standardize:
                row_sums = matrix.sum(axis=1)
                row_sums[row_sums == 0] = 1
                matrix = matrix / row_sums[:, np.newaxis]
            
            dynamic_weights[year] = matrix
        return dynamic_weights