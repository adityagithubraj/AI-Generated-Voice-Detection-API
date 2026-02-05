"""
Voice detection model to classify AI-generated vs Human voices
Improved model with better feature analysis
"""
import numpy as np
from typing import Dict, Tuple
from utils.audio_processor import extract_audio_features, load_audio_features


class VoiceDetector:
    """
    Advanced detector class for identifying AI-generated vs Human voices
    Uses comprehensive feature analysis with improved thresholds
    """
    
    def __init__(self):
        """Initialize the voice detector"""
        pass
    
    def detect(self, audio_path: str, language: str) -> Tuple[str, float, str]:
        """
        Detect if voice is AI-generated or Human
        
        Args:
            audio_path: Path to audio file
            language: Language of the audio
            
        Returns:
            Tuple of (classification, confidence_score, explanation)
        """
        # Load and extract features
        audio, sr = load_audio_features(audio_path)
        features = extract_audio_features(audio, sr)
        
        # Analyze features to determine if AI-generated
        classification, confidence, explanation = self._analyze_features(features, language)
        
        return classification, confidence, explanation
    
    def _analyze_features(self, features: Dict, language: str) -> Tuple[str, float, str]:
        """
        Advanced feature analysis using multiple indicators
        
        Args:
            features: Extracted audio features
            language: Language of the audio
            
        Returns:
            Tuple of (classification, confidence_score, explanation)
        """
        # Initialize weighted scores
        ai_indicators = []
        human_indicators = []
        reasons = []
        
        # 1. Pitch analysis (most important for AI detection)
        pitch_std = features.get('pitch_std', 0)
        pitch_cv = features.get('pitch_cv', 0)
        pitch_range = features.get('pitch_range', 0)
        
        # AI voices tend to have very consistent pitch
        # Thresholds are intentionally a bit relaxed to be more sensitive to AI patterns.
        if pitch_std < 25 or (pitch_cv > 0 and pitch_cv < 0.08):
            ai_indicators.append(('pitch_consistency', 0.20))
            reasons.append("unusually consistent pitch")
        elif pitch_std > 30 and pitch_range > 150:
            human_indicators.append(('pitch_variation', 0.15))
        
        # 2. MFCC analysis (critical for voice characteristics)
        mfcc_std_mean = np.mean(features.get('mfcc_std', [0]))
        mfcc_delta_std = features.get('mfcc_delta_std', 0)
        
        # AI voices often have less variation in MFCC coefficients
        if mfcc_std_mean < 6.5:
            ai_indicators.append(('mfcc_patterns', 0.18))
            reasons.append("atypical MFCC patterns")
        elif mfcc_std_mean > 7:
            human_indicators.append(('mfcc_variation', 0.12))
        
        # Low MFCC delta indicates less natural transitions
        if mfcc_delta_std < 4.0:
            ai_indicators.append(('mfcc_transitions', 0.12))
            reasons.append("unnatural spectral transitions")
        
        # 3. Spectral features
        spectral_centroid_std = features.get('spectral_centroid_std', 0)
        spectral_bandwidth_std = features.get('spectral_bandwidth_std', 0)
        spectral_contrast_std = features.get('spectral_contrast_std', 0)
        
        # AI voices often have less spectral variation
        if spectral_centroid_std < 600:
            ai_indicators.append(('spectral_consistency', 0.10))
            reasons.append("limited spectral variation")
        elif spectral_centroid_std > 800:
            human_indicators.append(('spectral_variation', 0.10))
        
        if spectral_bandwidth_std < 450:
            ai_indicators.append(('bandwidth_consistency', 0.08))
        
        # 4. Energy analysis
        energy_std = features.get('energy_std', 0)
        energy_cv = features.get('energy_cv', 0)
        
        # Human speech has natural energy fluctuations
        if energy_std < 0.012 or (energy_cv > 0 and energy_cv < 0.18):
            ai_indicators.append(('energy_consistency', 0.12))
            reasons.append("unnatural energy consistency")
        elif energy_std > 0.015:
            human_indicators.append(('energy_variation', 0.10))
        
        # 5. Zero crossing rate
        zcr_std = features.get('zcr_std', 0)
        if zcr_std < 0.012:
            ai_indicators.append(('zcr_patterns', 0.08))
            reasons.append("unnatural zero crossing patterns")
        elif zcr_std > 0.015:
            human_indicators.append(('zcr_variation', 0.08))
        
        # 6. Spectral rolloff
        spectral_rolloff_std = features.get('spectral_rolloff_std', 0)
        if spectral_rolloff_std < 600:
            ai_indicators.append(('rolloff_consistency', 0.08))
        
        # Calculate weighted scores
        ai_weight = sum(weight for _, weight in ai_indicators)
        human_weight = sum(weight for _, weight in human_indicators)
        
        # Normalize to probabilities
        total_weight = ai_weight + human_weight
        if total_weight > 0:
            ai_prob = ai_weight / total_weight
            human_prob = human_weight / total_weight
        else:
            # Default to human if no strong indicators
            ai_prob = 0.4
            human_prob = 0.6
        
        # Adjust probabilities based on number of indicators
        # More indicators = higher confidence
        indicator_count = len(ai_indicators) + len(human_indicators)
        confidence_boost = min(0.2, indicator_count * 0.03)

        # Slight bias towards detecting AI when there is some AI evidence,
        # to make the detector more conservative about synthetic voices.
        if ai_weight > 0 and total_weight > 0:
            ai_prob = min(1.0, ai_prob + 0.08)
            # renormalize
            norm = ai_prob + human_prob
            if norm > 0:
                ai_prob /= norm
                human_prob /= norm
        
        # Determine classification
        if ai_prob > human_prob:
            classification = "AI_GENERATED"
            base_confidence = ai_prob
            # Boost confidence if multiple AI indicators
            if len(ai_indicators) >= 3:
                confidence = min(0.95, base_confidence + confidence_boost)
            else:
                confidence = min(0.90, base_confidence + confidence_boost * 0.5)
            
            # Generate explanation
            if reasons:
                top_reasons = reasons[:3]
                explanation = f"AI-generated voice detected: {', '.join(top_reasons)}"
            else:
                explanation = "AI-generated voice patterns detected through spectral and pitch analysis"
        else:
            classification = "HUMAN"
            base_confidence = human_prob
            if len(human_indicators) >= 3:
                confidence = min(0.95, base_confidence + confidence_boost)
            else:
                confidence = min(0.90, base_confidence + confidence_boost * 0.5)
            
            explanation = "Natural human speech patterns detected with expected variations in pitch, energy, and spectral characteristics"
        
        # Ensure confidence is in valid range (minimum 0.55 for any classification)
        confidence = max(0.55, min(0.95, confidence))
        
        return classification, round(confidence, 2), explanation



