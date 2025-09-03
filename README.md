


## Project Overview
This project applies **Polynomial Regression** to predict a chess player's **rating strength** based on various game-related features.  
The model is trained to estimate the **black player's rating** using information about the game, the opponent (white), and performance indicators such as ACPL (Average Centipawn Loss).  

Although predicting exact chess ratings is challenging due to the **noisy nature of chess performance data**, the model provides practical insights into estimating the opponent’s skill level.

---

## Features and Target

- **Target (Y):**
  - `black_rating` → the rating of the black player.

- **Features (X):**
  - `white_rating` → rating of the white player.  
  - `game_category_blitz`  
  - `game_category_bullet`  
  - `game_category_classical`  
  - `game_category_rapid`  
  - `white_best` → best move count by white.  
  - `black_best` → best move count by black.  
  - `Black_result` → outcome of the game for black.  
  - `white_ACPL` → average centipawn loss for white.  
  - `performance_vs_rating_ratio` → ratio of black’s ACPL to white’s rating.

---

##  Model Training and Evaluation

The dataset was split into training and testing sets.  
Polynomial regression with degree=2 was applied, and the model performance was evaluated using **10-fold cross-validation**.

**R² Scores per fold:**
[0.6333, 0.6275, 0.6241, 0.6433, 0.6619, 0.6804,
0.6199, 0.5567, 0.6158, 0.6273]

**Average R² Score:**  
`0.629`
## Error Analysis

### Residuals Across Samples
<img width="587" height="268" alt="image" src="https://github.com/user-attachments/assets/87946c22-7cbc-4114-913f-c6168b9dc7a1" />

### Residual Distribution
<img width="581" height="313" alt="image" src="https://github.com/user-attachments/assets/41ba9626-8d72-440b-abd9-38a280703950" />

- The residuals are centered around zero, with no strong bias.  
- The errors roughly follow a **normal distribution**.  
- Most predictions fall within **±200 rating points** of the actual values.

---

## Project Structure

| Path                         | Description                                      | 
|-----------------------------|---------------------------------------------------|
| `chess-rating-prediction/`  | Project root                                      |
| `notebook.ipynb`            | Main Jupyter Notebook with analysis               |
| `utils.py`                  | Utility functions (encoding, preprocessing)       |
| `data/`                     | Dataset files (not included in repo)              |
| `images/`                   | Plots and figures used in the README              |
| `README.md`                 | Project documentation                             |
| `requirements.txt`          | requriments                                       |

---

##  Conclusion

- The **R² score (~0.63)** indicates the model captures a meaningful portion of rating variance but does not fully explain it.  
- This is expected because chess ratings are influenced by many **noisy, unobserved factors** (psychology, opening prep, style matchups, etc.).  
- Still, a prediction within **±200 points** is **completely acceptable in chess**, as it places players in the correct skill tier.  

 **In practice, this model gives a useful estimation of opponent strength**, even if not a perfect rating predictor.
