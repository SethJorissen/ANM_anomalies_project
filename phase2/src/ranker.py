import pandas as pd
import numpy as np
from tqdm import tqdm
from typing import Dict, List
from loguru import logger
import os


class DataManager:
    def __init__(self, 
                 data_path: str, 
                 ignore_columns: List[str] = [
                    'timestamp',
                    'container_start_time_seconds',
                    'container_last_seen']):
        self.data_path = data_path
        self.ignore_columns = ignore_columns

        # Load from file
        self.data: Dict[str, np.ndarray] = {}
        self.columns: List[str] = []
        self.__load()

    def __fill_na(self, df: pd.DataFrame):
        df.interpolate(method='linear', inplace=True)
        df.fillna(0.0, inplace=True)

    def __load(self):
        for file in os.listdir(self.data_path):
            if not file.endswith('.csv'):
                continue

            cur_df = pd.read_csv(os.path.join(self.data_path, file), engine='c')
            self.__fill_na(cur_df)
            self.columns = sorted([i for i in cur_df.columns.values if i not in self.ignore_columns])
            self.data[file[:-4]] = cur_df[self.columns].values

    def get(self, s: str) -> np.ndarray:
        return self.data[s]


class KSigmaDetecor:
    def __init__(self):
        pass

    def fit(self, data: np.ndarray):
        self.mu = np.mean(data, axis=0, keepdims=True)
        self.sigma = np.std(data, axis=0, keepdims=True)

    def decision_function(self, data: np.ndarray, eps: float=1e-3):
        # Data: [timesteps x features]
        detect_result = []
        
        for i in range(data.shape[1]):
            # Check if data is constant
            if np.all(self.sigma[0, i] == 0) and np.all(data[:, i] == data[0, i]):
                detect_result.append(np.zeros_like(data[:, i], dtype=np.float32))
            else:
                detect_result.append(np.abs(data[:, i] - self.mu[:, i]) / (self.sigma[:, i] + eps))

        return np.stack(detect_result, axis=1)


class AnomalyDetector:
    def __init__(self, hyper_params):
        self.hyper_params = hyper_params
        self.detector_dict: Dict[str, KSigmaDetecor] = {}

    def fit(self, data: DataManager):
        for s in tqdm(list(data.data.keys()), desc='Fitting detector(s)'):
            detector = KSigmaDetecor()
            detector.fit(data.get(s))
            self.detector_dict[s] = detector

    def detect(self, data: DataManager):
        # Simply return the max anomaly degree of all metrics
        result: Dict[str, float] = {}

        for k, v in data.data.items():
            detect_result = self.detector_dict[k].decision_function(v)

            assert type(detect_result) == np.ndarray
            result[k] = np.max(detect_result)

        return result


class Ranker:
    """
        This is a naive ranking algorithm, which simply rank according to the anomaly scores.
    """
    def __init__(self, hyper_params):
        self.hyper_params = hyper_params

        logger.info("[Ranker] Fitting the ranker with training data...")
        self.train_data = DataManager(hyper_params['train_dir'])
        self.anomaly_detector = AnomalyDetector(hyper_params)
        self._init_ranker()
    
    def _init_ranker(self):
        self.anomaly_detector.fit(self.train_data)

    def rank(self, case_dir: str):     
        # Load test data
        test_data = DataManager(case_dir)

        # Detect anomaly
        anomaly_score = self.anomaly_detector.detect(test_data)

        # TODO: You need to modify the ranking algorithm to achieve better results!   
        # This is a naive ranking algorithm, which simply rank according to the anomaly scores.
        rank_result = sorted(list(anomaly_score.keys()), key=lambda x: anomaly_score[x], reverse=True)

        return rank_result
