"""Model classes for Two-Stage Model - must be importable for pickle loading."""
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted

try:
    import xgboost as xgb
except ImportError:
    xgb = None

try:
    import lightgbm as lgb
except ImportError:
    lgb = None

try:
    from catboost import CatBoostRegressor, CatBoostClassifier
except ImportError:
    CatBoostRegressor = None
    CatBoostClassifier = None

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingRegressor, HistGradientBoostingClassifier
from sklearn.base import BaseEstimator, RegressorMixin, ClassifierMixin


class ZeroNonZeroClassifier:
    def __init__(self, model_type="xgb"):
        self.model_type = model_type
        
    def fit(self, X, y):
        y_binary = (y > 0).astype(int)
        if self.model_type == "xgb":
            import xgboost as xgb
            self.model_ = xgb.XGBClassifier(
                n_estimators=200, learning_rate=0.1, max_depth=4,
                subsample=0.8, colsample_bytree=0.8, random_state=42, n_jobs=-1,
                eval_metric="logloss")
        elif self.model_type == "lgb":
            import lightgbm as lgb
            self.model_ = lgb.LGBMClassifier(
                n_estimators=200, learning_rate=0.1, num_leaves=31,
                subsample=0.8, colsample_bytree=0.8, random_state=42, 
                n_jobs=-1, verbose=-1)
        elif self.model_type == "cat":
            from catboost import CatBoostClassifier
            self.model_ = CatBoostClassifier(
                iterations=200, learning_rate=0.1, depth=4,
                random_state=42, verbose=False)
        else:
            from sklearn.linear_model import LogisticRegression
            self.model_ = LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1)
        self.model_.fit(X, y_binary)
        return self
    
    def predict_proba(self, X):
        return self.model_.predict_proba(X)
    
    def predict(self, X):
        return self.model_.predict(X)


class LogTargetRegressor:
    def __init__(self, model_type="xgb"):
        self.model_type = model_type
        
    def fit(self, X, y):
        mask = y > 0
        if mask.sum() < 10:
            self.model_ = None
            return self
            
        y_log = np.log1p(y[mask])
        X_pos = X[mask]
        
        if self.model_type == "xgb":
            import xgboost as xgb
            self.model_ = xgb.XGBRegressor(
                n_estimators=300, learning_rate=0.05, max_depth=4,
                subsample=0.8, colsample_bytree=0.8, reg_lambda=1,
                random_state=42, n_jobs=-1)
        elif self.model_type == "lgb":
            import lightgbm as lgb
            self.model_ = lgb.LGBMRegressor(
                n_estimators=300, learning_rate=0.05, num_leaves=31,
                subsample=0.8, colsample_bytree=0.8, reg_lambda=1,
                random_state=42, n_jobs=-1, verbose=-1)
        elif self.model_type == "cat":
            from catboost import CatBoostRegressor
            self.model_ = CatBoostRegressor(
                iterations=300, learning_rate=0.05, depth=4,
                random_state=42, verbose=False)
        else:
            from sklearn.ensemble import HistGradientBoostingRegressor
            self.model_ = HistGradientBoostingRegressor(
                max_iter=300, learning_rate=0.05, max_depth=4,
                min_samples_leaf=20, l2_regularization=0.1, random_state=42)
        
        self.model_.fit(X_pos, y_log)
        return self
    
    def predict(self, X):
        if self.model_ is None:
            return np.zeros(len(X))
        pred_log = self.model_.predict(X)
        return np.expm1(pred_log)


class TwoStageModel:
    def __init__(self, clf_type="xgb", reg_type="xgb", threshold=0.5):
        self.clf_type = clf_type
        self.reg_type = reg_type
        self.threshold = threshold
        
    def fit(self, X, y):
        from model_classes import ZeroNonZeroClassifier, LogTargetRegressor
        self.clf_ = ZeroNonZeroClassifier(self.clf_type)
        self.clf_.fit(X, y)
        
        from model_classes import LogTargetRegressor
        self.reg_ = LogTargetRegressor(self.reg_type)
        self.reg_.fit(X, y)
        return self
    
    def predict(self, X):
        proba = self.clf_.predict_proba(X)[:, 1]
        y_reg = self.reg_.predict(X)
        return proba * y_reg
    
    def predict_proba(self, X):
        return self.clf_.predict_proba(X)
