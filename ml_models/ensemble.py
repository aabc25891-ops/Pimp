"""Ensemble Model combining multiple ML models"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from typing import Dict, Tuple, List
import logging
import joblib

logger = logging.getLogger(__name__)


class EnsemblePredictor:
    """Ensemble model for trend prediction"""
    
    def __init__(self, random_state: int = 42):
        """
        Initialize ensemble model
        
        Args:
            random_state: Random state for reproducibility
        """
        self.random_state = random_state
        self.models = {}
        self.scaler = StandardScaler()
        self.ensemble_weights = {
            'prophet': 0.3,
            'random_forest': 0.35,
            'gradient_boost': 0.35
        }
    
    def build_base_models(self):
        """
        Build individual base models
        """
        self.models['random_forest'] = RandomForestRegressor(
            n_estimators=100,
            max_depth=20,
            random_state=self.random_state,
            n_jobs=-1
        )
        
        self.models['gradient_boost'] = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=self.random_state
        )
        
        self.models['linear'] = LinearRegression()
        
        logger.info("Base models built")
    
    def prepare_features(self, X: np.ndarray) -> np.ndarray:
        """
        Prepare and scale features
        
        Args:
            X: Feature matrix
        
        Returns:
            Scaled feature matrix
        """
        return self.scaler.fit_transform(X)
    
    def train_base_models(self, X: np.ndarray, y: np.ndarray):
        """
        Train all base models
        
        Args:
            X: Feature matrix
            y: Target values
        """
        try:
            X_scaled = self.prepare_features(X)
            
            for model_name, model in self.models.items():
                logger.info(f"Training {model_name}...")
                model.fit(X_scaled, y)
            
            logger.info("All base models trained")
        
        except Exception as e:
            logger.error(f"Error training base models: {str(e)}")
    
    def predict_ensemble(self, X: np.ndarray, prophet_pred: np.ndarray = None) -> Tuple[np.ndarray, Dict]:
        """
        Generate ensemble prediction
        
        Args:
            X: Feature matrix
            prophet_pred: Prophet predictions (optional)
        
        Returns:
            Tuple of (ensemble predictions, component predictions)
        """
        try:
            X_scaled = self.scaler.transform(X)
            
            predictions = {}
            
            # Get predictions from each model
            predictions['random_forest'] = self.models['random_forest'].predict(X_scaled)
            predictions['gradient_boost'] = self.models['gradient_boost'].predict(X_scaled)
            predictions['linear'] = self.models['linear'].predict(X_scaled)
            
            if prophet_pred is not None:
                predictions['prophet'] = prophet_pred
            
            # Weighted ensemble
            ensemble_pred = np.zeros_like(predictions['random_forest'])
            
            for model_name, weight in self.ensemble_weights.items():
                if model_name in predictions:
                    ensemble_pred += weight * predictions[model_name]
            
            return ensemble_pred, predictions
        
        except Exception as e:
            logger.error(f"Error in ensemble prediction: {str(e)}")
            return np.array([]), {}
    
    def calculate_uncertainty(self, predictions: Dict) -> np.ndarray:
        """
        Calculate prediction uncertainty
        
        Args:
            predictions: Dictionary of model predictions
        
        Returns:
            Uncertainty estimates
        """
        pred_array = np.array(list(predictions.values()))
        uncertainty = np.std(pred_array, axis=0)
        return uncertainty
    
    def get_feature_importance(self) -> Dict:
        """
        Get feature importance from tree-based models
        
        Returns:
            Dictionary with feature importances
        """
        importance = {}
        
        if 'random_forest' in self.models:
            importance['random_forest'] = self.models['random_forest'].feature_importances_
        
        if 'gradient_boost' in self.models:
            importance['gradient_boost'] = self.models['gradient_boost'].feature_importances_
        
        return importance
    
    def save_model(self, path: str):
        """
        Save ensemble model
        
        Args:
            path: Save path
        """
        try:
            joblib.dump(self, path)
            logger.info(f"Saved ensemble model to {path}")
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
    
    @staticmethod
    def load_model(path: str):
        """
        Load ensemble model
        
        Args:
            path: Model path
        
        Returns:
            Loaded ensemble model
        """
        try:
            model = joblib.load(path)
            logger.info(f"Loaded ensemble model from {path}")
            return model
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return None
