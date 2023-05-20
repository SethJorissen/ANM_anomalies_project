# ANM 2023 Project (Phase 2)
This is the project document for ANM 2023 Project (Phase 2).

## Dataset
- `train`: Exactly the same as phase 1.
- `test/processed/[failure_id]/[service]-[container_id].csv`: The data format is exactly the same as phase1. But the content of the data is different.
- `label.json`: Only timestamps are provided.

## Task
We will provide an online judge platform and use additional data to evaluate each team's code. This online judge platform has a limit on the number of submissions (5 per day per team).In the final class (Week 16), each team will be required to give a presentation on your algorithm design and improvement. The score for Phase 2 will consist of the leaderboard score and the presentation score. You will be provided with specific requirements and a detailed scoring method at the beginning of Phase 2. This part will account for 45% of your total score.

In phase 2, you need to write a program that can localize the root cause of each failure case in phase 2 data and output the __ranking__ results in `json` format for each failure case. __The output format should be consistent with the example output `src/result/result.json`.__ You can use all the data that has been provided. (Including the data and labels already provided in phase 1.)

## Online Judge
The Online Judge platform will be open on the first day of phase 2.

- **Website**: http://anm.xz2000.cn
- **Username** & Password: ANM2, anm865855
- Submission: The output in `json` format.
- **Rate Limit**: 5 successful submissions / Group / Day. (If your submission is not in the correct format, it will not count towards your submission count. Refreshed at 00:00 (UTC+8) every day.)
- **Leaderboard**: MRR (Mean Reciprocal Rank). MRR is calculated by averaging the multiplicative inverse of the rank in each failure case.

## Scoring
- **Leaderboard**: 25%. (25 % * `MRR of your group` / `Max MRR of all groups`).
- **Presentation**: 20%.

## Requirements
- You should save the code corresponding to your best submission and submit the code to TA at the end of phase 2.
- Each group's presentation should be no longer than 20 minutes, and everyone must participate. You should detail the algorithms you explored in phase 1 and the improvements you made in phase 2. You should also conclude with a presentation on the lessons you have learned from this experience.
- Please do not try to submit fake answers (i.e., answers that are not output by your program). Otherwise, your group may be penalized.

## Example Program
1. `cd src/`.
2. `python3 main.py`.
3. Upload `src/result/result.json` to the OJ platform.
