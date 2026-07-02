"""
PHASE 5: DISTILBERT MODEL
Fine-tuned DistilBERT for fake news detection.
"""

import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from transformers import DistilBertTokenizerFast, DistilBertModel, DistilBertConfig
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsDataset(Dataset):
    """PyTorch Dataset for news articles."""
    
    def __init__(self, texts, labels, tokenizer, max_length=512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]
        
        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].squeeze(),
            'attention_mask': encoding['attention_mask'].squeeze(),
            'labels': torch.tensor(label, dtype=torch.long)
        }


class FakeNewsClassifier(nn.Module):
    """DistilBERT-based classifier for fake news detection."""
    
    def __init__(self, num_classes=2, dropout=0.1, pretrained=True):
        super(FakeNewsClassifier, self).__init__()
        self.distilbert = (DistilBertModel.from_pretrained('distilbert-base-uncased')
                           if pretrained else DistilBertModel(DistilBertConfig()))
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(768, num_classes)
    
    def forward(self, input_ids, attention_mask):
        distil_output = self.distilbert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        pooled_output = distil_output.last_hidden_state[:, 0, :]
        pooled_output = self.dropout(pooled_output)
        logits = self.fc(pooled_output)
        return logits


class DistilBertTrainer:
    """Trainer for DistilBERT model."""
    
    def __init__(self, model_name='distilbert-base-uncased', device='cpu', tokenizer_path=None, pretrained=True):
        self.device = device
        self.tokenizer = DistilBertTokenizerFast.from_pretrained(tokenizer_path or model_name)
        self.model = FakeNewsClassifier(pretrained=pretrained).to(device)
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=2e-5)
    
    def train_epoch(self, train_loader):
        """Train for one epoch."""
        self.model.train()
        total_loss = 0
        
        for batch in tqdm(train_loader, desc="Training"):
            input_ids = batch['input_ids'].to(self.device)
            attention_mask = batch['attention_mask'].to(self.device)
            labels = batch['labels'].to(self.device)
            
            self.optimizer.zero_grad()
            logits = self.model(input_ids, attention_mask)
            loss = self.criterion(logits, labels)
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
        
        return total_loss / len(train_loader)
    
    def evaluate(self, val_loader):
        """Evaluate model."""
        self.model.eval()
        all_preds = []
        all_labels = []
        total_loss = 0
        
        with torch.no_grad():
            for batch in tqdm(val_loader, desc="Evaluating"):
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['labels'].to(self.device)
                
                logits = self.model(input_ids, attention_mask)
                loss = self.criterion(logits, labels)
                total_loss += loss.item()
                
                preds = torch.argmax(logits, dim=1)
                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
        
        metrics = {
            'loss': total_loss / len(val_loader),
            'accuracy': accuracy_score(all_labels, all_preds),
            'precision': precision_score(all_labels, all_preds),
            'recall': recall_score(all_labels, all_preds),
            'f1': f1_score(all_labels, all_preds)
        }
        
        return metrics
    
    def predict(self, texts):
        """Make predictions on new texts."""
        self.model.eval()
        
        encodings = self.tokenizer(
            texts,
            max_length=512,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        input_ids = encodings['input_ids'].to(self.device)
        attention_mask = encodings['attention_mask'].to(self.device)
        
        with torch.no_grad():
            logits = self.model(input_ids, attention_mask)
            probs = torch.softmax(logits, dim=1)
            predictions = torch.argmax(logits, dim=1)
        
        return predictions.cpu().numpy(), probs.cpu().numpy()
    
    def save(self, filepath):
        """Save model."""
        torch.save(self.model.state_dict(), filepath)
        logger.info(f"Model saved to {filepath}")
    
    def load(self, filepath):
        """Load model."""
        state = torch.load(filepath, map_location=self.device, weights_only=True)
        self.model.load_state_dict(state)
        logger.info(f"Model loaded from {filepath}")
    
    def train(
        self,
        X_train, y_train, X_val, y_val,
        epochs=3,
        batch_size=32,
        save_path=None
    ):
        """Complete training pipeline."""
        logger.info("=" * 50)
        logger.info("DISTILBERT MODEL TRAINING")
        logger.info("=" * 50)
        
        # Create datasets
        train_dataset = NewsDataset(X_train, y_train, self.tokenizer)
        val_dataset = NewsDataset(X_val, y_val, self.tokenizer)
        
        # Create dataloaders
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size)
        
        best_f1 = 0
        
        for epoch in range(epochs):
            logger.info(f"\nEpoch {epoch + 1}/{epochs}")
            
            # Train
            train_loss = self.train_epoch(train_loader)
            logger.info(f"Training loss: {train_loss:.4f}")
            
            # Evaluate
            val_metrics = self.evaluate(val_loader)
            logger.info(f"Validation metrics: {val_metrics}")
            
            # Save best model
            if val_metrics['f1'] > best_f1:
                best_f1 = val_metrics['f1']
                if save_path:
                    self.save(save_path)
                    logger.info(f"Best model saved (F1: {best_f1:.4f})")
        
        logger.info("=" * 50)
        logger.info("DISTILBERT TRAINING COMPLETE")
        logger.info("=" * 50)
        
        return {
            'best_f1': best_f1,
            'final_metrics': val_metrics
        }
