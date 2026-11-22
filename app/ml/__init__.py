"""ML module with Two-Stage Model classes for pickle compatibility."""
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin, ClassifierMixin
from sklearn.preprocessing import LabelEncoder

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
from sklearn.preprocessing import LabelEncoder


class ZeroNonZeroClassifier:
    def __init__(self, model_type="lgb"):
        self.model_type = model_type
        self.categorical_cols_ = []
        
    def _prepare_categorical(self, X):
        """Convert object columns to pandas category dtype for LightGBM"""
        X_prep = X.copy()
        for col in self.categorical_cols_:
            if col in X_prep.columns:
                X_prep[col] = X_prep[col].astype('category')
        return X_prep
        
    def fit(self, X, y):
        y_binary = (y > 0).astype(int)
        # Identify categorical columns (object or string dtype)
        self.categorical_cols_ = [col for col in X.columns if X[col].dtype == 'object' or pd.api.types.is_string_dtype(X[col])]
        X_prep = self._prepare_categorical(X)
        
        if self.model_type == "lgb":
            import lightgbm as lgb
            self.model_ = lgb.LGBMClassifier(
                n_estimators=200, learning_rate=0.1, num_leaves=31,
                subsample=0.8, colsample_bytree=0.8, random_state=42, 
                n_jobs=-1, verbose=-1)
            # LightGBM handles categorical features natively
            self.model_.fit(X_prep, y_binary, categorical_feature=self.categorical_cols_)
        elif self.model_type == "xgb":
            import xgboost as xgb
            # Need LabelEncoder for XGBoost
            self.label_encoders_ = {}
            X_encoded = X.copy()
            for col in self.categorical_cols_:
                le = LabelEncoder()
                X_encoded[col] = le.fit_transform(X[col].astype(str))
                self.label_encoders_[col] = le
            self.model_ = xgb.XGBClassifier(
                n_estimators=200, learning_rate=0.1, max_depth=4,
                subsample=0.8, colsample_bytree=0.8, random_state=42, n_jobs=-1,
                eval_metric="logloss", enable_categorical=True)
            self.model_.fit(X_encoded, y_binary)
        elif self.model_type == "cat":
            from catboost import CatBoostClassifier
            self.model_ = CatBoostClassifier(
                iterations=200, learning_rate=0.1, depth=4,
                random_state=42, verbose=False)
            self.model_.fit(X, y_binary, cat_features=self.categorical_cols_)
        else:
            from sklearn.linear_model import LogisticRegression
            self.model_ = LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1)
            # Need encoding for sklearn
            self.label_encoders_ = {}
            X_encoded = X.copy()
            for col in self.categorical_cols_:
                le = LabelEncoder()
                X_encoded[col] = le.fit_transform(X[col].astype(str))
                self.label_encoders_[col] = le
            self.model_.fit(X_encoded, y_binary)
        return self
    
    def _encode_categorical(self, X):
        X_encoded = X.copy()
        for col in self.categorical_cols_:
            if col in X_encoded.columns:
                le = self.label_encoders_[col]
                # Handle unseen categories
                X_encoded[col] = X[col].astype(str).map(
                    lambda x: le.transform([x])[0] if x in le.classes_ else -1
                )
        return X_encoded
        
    def predict_proba(self, X):
        if self.model_type == "lgb":
            X_prep = self._prepare_categorical(X)
            return self.model_.predict_proba(X_prep)
        elif self.model_type == "cat":
            return self.model_.predict_proba(X)
        else:
            X_encoded = self._encode_categorical(X)
            return self.model_.predict_proba(X_encoded)
    
    def predict(self, X):
        if self.model_type == "lgb":
            X_prep = self._prepare_categorical(X)
            return self.model_.predict(X_prep)
        elif self.model_type == "cat":
            return self.model_.predict(X)
        else:
            X_encoded = self._encode_categorical(X)
            return self.model_.predict(X_encoded)


class LogTargetRegressor:
    def __init__(self, model_type="lgb"):
        self.model_type = model_type
        self.categorical_cols_ = []
        
    def _prepare_categorical(self, X):
        """Convert object columns to pandas category dtype for LightGBM"""
        X_prep = X.copy()
        for col in self.categorical_cols_:
            if col in X_prep.columns:
                X_prep[col] = X_prep[col].astype('category')
        return X_prep
        
    def fit(self, X, y):
        mask = y > 0
        if mask.sum() < 10:
            self.model_ = None
            return self
            
        y_log = np.log1p(y[mask])
        X_pos = X[mask]
        
        # Identify categorical columns (object or string dtype)
        self.categorical_cols_ = [col for col in X.columns if X[col].dtype == 'object' or pd.api.types.is_string_dtype(X[col])]
        X_pos_prep = self._prepare_categorical(X_pos)
        
        if self.model_type == "lgb":
            import lightgbm as lgb
            self.model_ = lgb.LGBMRegressor(
                n_estimators=300, learning_rate=0.05, num_leaves=31,
                subsample=0.8, colsample_bytree=0.8, reg_lambda=1,
                random_state=42, n_jobs=-1, verbose=-1)
            self.model_.fit(X_pos_prep, y_log, categorical_feature=self.categorical_cols_)
        elif self.model_type == "xgb":
            import xgboost as xgb
            self.label_encoders_ = {}
            X_pos_encoded = X_pos.copy()
            for col in self.categorical_cols_:
                le = LabelEncoder()
                X_pos_encoded[col] = le.fit_transform(X_pos[col].astype(str))
                self.label_encoders_[col] = le
            self.model_ = xgb.XGBRegressor(
                n_estimators=300, learning_rate=0.05, max_depth=4,
                subsample=0.8, colsample_bytree=0.8, reg_lambda=1,
                random_state=42, n_jobs=-1, enable_categorical=True)
            self.model_.fit(X_pos_encoded, y_log)
        elif self.model_type == "cat":
            from catboost import CatBoostRegressor
            self.model_ = CatBoostRegressor(
                iterations=300, learning_rate=0.05, depth=4,
                random_state=42, verbose=False)
            self.model_.fit(X_pos, y_log, cat_features=self.categorical_cols_)
        else:
            from sklearn.ensemble import HistGradientBoostingRegressor
            self.label_encoders_ = {}
            X_pos_encoded = X_pos.copy()
            for col in self.categorical_cols_:
                le = LabelEncoder()
                X_pos_encoded[col] = le.fit_transform(X_pos[col].astype(str))
                self.label_encoders_[col] = le
            self.model_ = HistGradientBoostingRegressor(
                max_iter=300, learning_rate=0.05, max_depth=4,
                min_samples_leaf=20, l2_regularization=0.1, random_state=42)
            self.model_.fit(X_pos_encoded, y_log)
        return self
    
    def _encode_categorical(self, X):
        X_encoded = X.copy()
        for col in self.categorical_cols_:
            if col in X_encoded.columns:
                le = self.label_encoders_[col]
                X_encoded[col] = X[col].astype(str).map(
                    lambda x: le.transform([x])[0] if x in le.classes_ else -1
                )
        return X_encoded
    
    def predict(self, X):
        if self.model_ is None:
            return np.zeros(len(X))
        if self.model_type == "lgb":
            X_prep = self._prepare_categorical(X)
            pred_log = self.model_.predict(X_prep)
        elif self.model_type == "cat":
            pred_log = self.model_.predict(X)
        else:
            X_encoded = self._encode_categorical(X)
            pred_log = self.model_.predict(X_encoded)
        return np.expm1(pred_log)


class TwoStageModel:
    def __init__(self, clf_type="lgb", reg_type="lgb", threshold=0.5):
        self.clf_type = clf_type
        self.reg_type = reg_type
        self.threshold = threshold
        
    def fit(self, X, y):
        from ml import ZeroNonZeroClassifier, LogTargetRegressor
        self.clf_ = ZeroNonZeroClassifier(self.clf_type)
        self.clf_.fit(X, y)
        
        self.reg_ = LogTargetRegressor(self.reg_type)
        self.reg_.fit(X, y)
        return self
    
    def predict(self, X):
        proba = self.clf_.predict_proba(X)[:, 1]
        y_reg = self.reg_.predict(X)
        return proba * y_reg
    
    def predict_proba(self, X):
        return self.clf_.predict_proba(X)