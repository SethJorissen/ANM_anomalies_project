import pandas as pd
import numpy as np
from tqdm import tqdm
from loguru import logger
from ranker import Ranker
import os
import json


# Hyper Parameters
hyper_params = {
    'train_dir': '../dataset/train/processed',
    'test_dir': '../dataset/test/processed',
    'label_path': '../dataset/test/label.json'
}


if __name__ == '__main__':
    # Initialize ranker
    logger.info("[main] Loading data and ranking...")
    ranker = Ranker(hyper_params)

    # Load test cases
    result_list = []
    case_idx: int = 0
    with tqdm(total=len(os.listdir(hyper_params['test_dir']))) as t:
        while True:
            case_dir = os.path.join(hyper_params['test_dir'], str(case_idx))
            if not os.path.exists(case_dir):
                break
            t.set_description(f"Ranking {case_dir}")

            cur_rank = ranker.rank(case_dir)
            result_list.append(cur_rank)

            # Update tqdm
            t.update()
            case_idx += 1

    # Dump Result
    os.makedirs('result', exist_ok=True)
    with open('result/result.json', 'wt') as f:
        json.dump(result_list, f)
