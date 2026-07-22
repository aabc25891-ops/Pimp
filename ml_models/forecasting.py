"""Time-Series Forecasting with Prophet"""

import pandas as pd
import numpy as np
from prophet import Prophet
from typing import Dict, Tuple, List
import logging
from datetime import datetime, timedelta
import joblib

logger = logging.getLogger(__name__)


class TrendForecaster:
    """Time-series forecasting for product trends"""
    
    def __init__(self, interval_width: float = 0.95, yearly_seasonality: bool = True):
        """
        Initialize forecaster
        
        Args:
            interval_width: Confidence interval width
            yearly_seasonality: Include yearly seasonality
        """
        self.interval_width = interval_width
        self.yearly_seasonality = yearly_seasonality
        self.models = {}
    
    def prepare_data(self, df: pd.DataFrame, date_col: str, value_col: str) -> pd.DataFrame:
        """
        Prepare data for Prophet
        
        Args:
            df: Input DataFrame
            date_col: Date column name
            value_col: Value column name
        
        Returns:
            DataFrame formatted for Prophet
        """
        prophet_df = pd.DataFrame({
            'ds': pd.to_datetime(df[date_col]),
            'y': df[value_col].astype(float)
        })
        
        prophet_df = prophet_df.sort_values('ds').reset_index(drop=True)
        return prophet_df
    
    def fit_model(self, df: pd.DataFrame, product_id: str) -> Prophet:
        """
        Fit Prophet model
        
        Args:
            df: Historical data (with 'ds' and 'y' columns)
            product_id: Product identifier
        
        Returns:
            Fitted Prophet model
        """
        try:
            model = Prophet(
                yearly_seasonality=self.yearly_seasonality,
                weekly_seasonality=True,
                daily_seasonality=False,
                interval_width=self.interval_width,
                changepoint_prior_scale=0.05
            )
            
            model.fit(df)
            self.models[product_id] = model
            
            logger.info(f"Fitted Prophet model for product: {product_id}")
            return model
        
        except Exception as e:
            logger.error(f"Error fitting Prophet model: {str(e)}")
            return None
    
    def forecast(self, product_id: str, periods: int = 30) -> pd.DataFrame:
        """
        Generate forecast
        
        Args:
            product_id: Product identifier
            periods: Number of periods to forecast
        
        Returns:
            DataFrame with forecast
        """
        try:
            if product_id not in self.models:
                logger.warning(f"No model found for product: {product_id}")
                return pd.DataFrame()
            
            model = self.models[product_id]
            future = model.make_future_dataframe(periods=periods)
            forecast = model.predict(future)
            
            # Keep only future predictions
            forecast = forecast[forecast['ds'] > forecast['ds'].iloc[-periods-1]]
            
            return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
        
        except Exception as e:
            logger.error(f"Error generating forecast: {str(e)}")
            return pd.DataFrame()
    
    def get_trend_components(self, product_id: str) -> Dict:
        """
        Get trend components
        
        Args:
            product_id: Product identifier
        
        Returns:
            Dictionary with trend components
        """
        try:
            if product_id not in self.models:
                return {}
            
            model = self.models[product_id]
            components = model.plot_components(model.history)
            
            return {'components': components}
        
        except Exception as e:
            logger.error(f"Error getting trend components: {str(e)}")
            return {}
    
    def calculate_metrics(self, actual: np.ndarray, predicted: np.ndarray) -> Dict:
        """
        Calculate forecast accuracy metrics
        
        Args:
            actual: Actual values
            predicted: Predicted values
        
        Returns:
            Dictionary with metrics
        """
        from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
        
        rmse = np.sqrt(mean_squared_error(actual, predicted))
        mae = mean_absolute_error(actual, predicted)
        mape = mean_absolute_percentage_error(actual, predicted)
        
        return {
            'rmse': rmse,
            'mae': mae,
            'mape': mape
        }
    
    def save_model(self, product_id: str, path: str):
        """
        Save model to disk
        
        Args:
            product_id: Product identifier
            path: Save path
        """
        if product_id in self.models:
            joblib.dump(self.models[product_id], path)
            logger.info(f"Saved model for {product_id} to {path}")
    
    def load_model(self, product_id: str, path: str):
        """
        Load model from disk
        
        Args:
            product_id: Product identifier
            path: Model path
        """
        try:
            model = joblib.load(path)
            self.models[product_id] = model
            logger.info(f"Loaded model for {product_id} from {path}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
