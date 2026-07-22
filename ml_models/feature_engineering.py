"""Feature Engineering for ML Models"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
import logging
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler, MinMaxScaler

logger = logging.getLogger(__name__)


class FeatureEngineer:
    """Feature engineering for trend prediction"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.min_max_scaler = MinMaxScaler()
    
    def extract_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract time-based features from datetime
        
        Args:
            df: DataFrame with datetime column
        
        Returns:
            DataFrame with time features
        """
        df['date'] = pd.to_datetime(df['date'])
        df['day_of_week'] = df['date'].dt.dayofweek
        df['day_of_month'] = df['date'].dt.day
        df['month'] = df['date'].dt.month
        df['quarter'] = df['date'].dt.quarter
        df['week_of_year'] = df['date'].dt.isocalendar().week
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        
        return df
    
    def create_lag_features(self, df: pd.DataFrame, column: str, lags: List[int]) -> pd.DataFrame:
        """
        Create lag features
        
        Args:
            df: DataFrame
            column: Column to create lags for
            lags: List of lag periods
        
        Returns:
            DataFrame with lag features
        """
        for lag in lags:
            df[f'{column}_lag_{lag}'] = df[column].shift(lag)
        
        return df
    
    def create_rolling_features(self, df: pd.DataFrame, column: str, windows: List[int]) -> pd.DataFrame:
        """
        Create rolling window features
        
        Args:
            df: DataFrame
            column: Column to create rolling features for
            windows: List of window sizes
        
        Returns:
            DataFrame with rolling features
        """
        for window in windows:
            df[f'{column}_rolling_mean_{window}'] = df[column].rolling(window=window).mean()
            df[f'{column}_rolling_std_{window}'] = df[column].rolling(window=window).std()
            df[f'{column}_rolling_min_{window}'] = df[column].rolling(window=window).min()
            df[f'{column}_rolling_max_{window}'] = df[column].rolling(window=window).max()
        
        return df
    
    def calculate_volatility(self, df: pd.DataFrame, column: str, window: int = 30) -> pd.DataFrame:
        """
        Calculate volatility (standard deviation)
        
        Args:
            df: DataFrame
            column: Column to calculate volatility for
            window: Window size
        
        Returns:
            DataFrame with volatility
        """
        df[f'{column}_volatility'] = df[column].rolling(window=window).std()
        return df
    
    def normalize_features(self, X: np.ndarray) -> np.ndarray:
        """
        Normalize features using StandardScaler
        
        Args:
            X: Feature matrix
        
        Returns:
            Normalized feature matrix
        """
        return self.scaler.fit_transform(X)
    
    def scale_features(self, X: np.ndarray) -> np.ndarray:
        """
        Scale features to [0, 1] range
        
        Args:
            X: Feature matrix
        
        Returns:
            Scaled feature matrix
        """
        return self.min_max_scaler.fit_transform(X)
    
    def create_interaction_features(self, df: pd.DataFrame, features: List[str]) -> pd.DataFrame:
        """
        Create interaction features
        
        Args:
            df: DataFrame
            features: List of features to interact
        
        Returns:
            DataFrame with interaction features
        """
        for i, feat1 in enumerate(features):
            for feat2 in features[i+1:]:
                df[f'{feat1}_x_{feat2}'] = df[feat1] * df[feat2]
        
        return df
    
    def create_ratio_features(self, df: pd.DataFrame, numerator: str, denominator: str) -> pd.DataFrame:
        """
        Create ratio features
        
        Args:
            df: DataFrame
            numerator: Numerator column
            denominator: Denominator column
        
        Returns:
            DataFrame with ratio feature
        """
        df[f'{numerator}_ratio_{denominator}'] = df[numerator] / (df[denominator] + 1e-8)
        return df
