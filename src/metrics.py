"""
Evaluation Metrics for Image Processing
========================================
Implements various metrics for evaluating image quality and denoising performance.
"""

import numpy as np
from typing import Tuple, Dict
from scipy import ndimage
from scipy.fft import fft2, fftshift


class ImageMetrics:
    """
    Collection of image evaluation metrics for denoising assessment.
    """
    
    @staticmethod
    def entropy(image: np.ndarray) -> float:
        """
        Calculate Shannon entropy of an image.
        
        Higher entropy indicates more information content.
        
        Args:
            image: Input image (2D grayscale)
            
        Returns:
            Entropy value in bits
        """
        if image.ndim == 3:
            # Convert to grayscale
            image = np.mean(image, axis=2)
        
        # Flatten and calculate histogram
        hist = np.histogram(image.flatten(), bins=256, range=(0, 256))[0]
        hist = hist / hist.sum()  # Normalize
        
        # Calculate entropy
        entropy = -np.sum(hist * np.log2(hist + 1e-10))
        
        return entropy
    
    @staticmethod
    def rmse(original: np.ndarray, processed: np.ndarray) -> float:
        """
        Calculate Root Mean Square Error.
        
        Lower values indicate better fidelity to original.
        
        Args:
            original: Ground truth image
            processed: Processed image
            
        Returns:
            RMSE value
        """
        return np.sqrt(np.mean((original.astype(float) - processed.astype(float)) ** 2))
    
    @staticmethod
    def psnr(original: np.ndarray, processed: np.ndarray) -> float:
        """
        Calculate Peak Signal-to-Noise Ratio.
        
        Higher values indicate better quality.
        
        Args:
            original: Ground truth image
            processed: Processed image
            
        Returns:
            PSNR value in dB
        """
        mse = np.mean((original.astype(float) - processed.astype(float)) ** 2)
        if mse == 0:
            return float('inf')
        
        max_pixel = 255.0
        psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
        
        return psnr
    
    @staticmethod
    def ssim(original: np.ndarray, processed: np.ndarray) -> float:
        """
        Calculate Structural Similarity Index.
        
        Values range from -1 to 1, with 1 indicating perfect similarity.
        
        Args:
            original: Ground truth image
            processed: Processed image
            
        Returns:
            SSIM value
        """
        if original.ndim == 3:
            original = np.mean(original, axis=2)
        if processed.ndim == 3:
            processed = np.mean(processed, axis=2)
        
        # Constants for stability
        C1 = (0.01 * 255) ** 2
        C2 = (0.03 * 255) ** 2
        
        # Calculate local means
        mu1 = ndimage.uniform_filter(original.astype(float), size=11)
        mu2 = ndimage.uniform_filter(processed.astype(float), size=11)
        
        # Calculate variance and covariance
        sigma1_sq = ndimage.uniform_filter(original.astype(float) ** 2, size=11) - mu1 ** 2
        sigma2_sq = ndimage.uniform_filter(processed.astype(float) ** 2, size=11) - mu2 ** 2
        sigma12 = ndimage.uniform_filter(original.astype(float) * processed.astype(float), size=11) - mu1 * mu2
        
        # Calculate SSIM
        ssim_map = ((2 * mu1 * mu2 + C1) * (2 * sigma12 + C2)) / \
                   ((mu1 ** 2 + mu2 ** 2 + C1) * (sigma1_sq + sigma2_sq + C2))
        
        return np.mean(ssim_map)
    
    @staticmethod
    def autocorrelation(image: np.ndarray, max_lag: int = 10) -> np.ndarray:
        """
        Calculate autocorrelation to assess noise patterns.
        
        Lower autocorrelation at non-zero lags indicates more random (white) noise.
        
        Args:
            image: Input image
            max_lag: Maximum lag to calculate
            
        Returns:
            Autocorrelation values for different lags
        """
        if image.ndim == 3:
            image = np.mean(image, axis=2)
        
        # Normalize image
        image = image.astype(float)
        image = image - np.mean(image)
        
        # Calculate 2D autocorrelation using FFT
        fft_img = fft2(image)
        autocorr = fftshift(np.abs(fft2(np.abs(fft_img) ** 2)))
        
        # Extract center region
        h, w = autocorr.shape
        center_h, center_w = h // 2, w // 2
        
        # Get diagonal autocorrelation values
        autocorr_diag = []
        for lag in range(min(max_lag, min(center_h, center_w))):
            autocorr_diag.append(autocorr[center_h + lag, center_w + lag])
        
        return np.array(autocorr_diag)
    
    @staticmethod
    def mtf_estimate(image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Estimate Modulation Transfer Function.
        
        Higher MTF values at high frequencies indicate better detail preservation.
        
        Args:
            image: Input image
            
        Returns:
            Tuple of (frequencies, MTF values)
        """
        if image.ndim == 3:
            image = np.mean(image, axis=2)
        
        # Calculate 2D FFT
        fft_img = fftshift(fft2(image.astype(float)))
        
        # Get magnitude spectrum
        magnitude = np.abs(fft_img)
        
        # Radial average
        h, w = magnitude.shape
        center_h, center_w = h // 2, w // 2
        
        # Create radial distance map
        y, x = np.ogrid[:h, :w]
        r = np.sqrt((x - center_w) ** 2 + (y - center_h) ** 2)
        
        # Bin by radius
        max_r = min(center_h, center_w)
        frequencies = np.arange(max_r)
        mtf = np.zeros(max_r)
        
        for i in range(max_r):
            mask = (r >= i) & (r < i + 1)
            if np.sum(mask) > 0:
                mtf[i] = np.mean(magnitude[mask])
        
        # Normalize
        mtf = mtf / (mtf[0] + 1e-10)
        
        return frequencies, mtf
    
    @staticmethod
    def bit_depth_linearity(image: np.ndarray) -> float:
        """
        Assess bit-depth linearity to detect banding artifacts.
        
        Values closer to 1.0 indicate smooth gradients without banding.
        
        Args:
            image: Input image
            
        Returns:
            Linearity score (0 to 1)
        """
        if image.ndim == 3:
            image = np.mean(image, axis=2)
        
        # Calculate histogram
        hist, bins = np.histogram(image.flatten(), bins=256, range=(0, 256))
        
        # Calculate smoothness of histogram
        hist_smooth = ndimage.gaussian_filter1d(hist.astype(float), sigma=2)
        
        # Calculate deviation from smoothness
        deviation = np.sum(np.abs(hist.astype(float) - hist_smooth))
        total = np.sum(hist)
        
        # Convert to linearity score
        linearity = 1.0 - (deviation / (total + 1e-10))
        
        return min(1.0, max(0.0, linearity))
    
    @staticmethod
    def edge_preservation(original: np.ndarray, processed: np.ndarray) -> float:
        """
        Measure how well edges are preserved.
        
        Values closer to 1.0 indicate better edge preservation.
        
        Args:
            original: Ground truth image
            processed: Processed image
            
        Returns:
            Edge preservation score
        """
        # Calculate gradients
        if original.ndim == 3:
            original = np.mean(original, axis=2)
        if processed.ndim == 3:
            processed = np.mean(processed, axis=2)
        
        # Sobel operators
        sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
        
        # Apply Sobel
        orig_grad_x = ndimage.convolve(original.astype(float), sobel_x)
        orig_grad_y = ndimage.convolve(original.astype(float), sobel_y)
        orig_edges = np.sqrt(orig_grad_x ** 2 + orig_grad_y ** 2)
        
        proc_grad_x = ndimage.convolve(processed.astype(float), sobel_x)
        proc_grad_y = ndimage.convolve(processed.astype(float), sobel_y)
        proc_edges = np.sqrt(proc_grad_x ** 2 + proc_grad_y ** 2)
        
        # Calculate correlation between edge maps
        correlation = np.corrcoef(orig_edges.flatten(), proc_edges.flatten())[0, 1]
        
        return max(0, correlation)
    
    @staticmethod
    def compute_all_metrics(original: np.ndarray, processed: np.ndarray) -> Dict[str, float]:
        """
        Compute all evaluation metrics at once.
        
        Args:
            original: Ground truth image
            processed: Processed image
            
        Returns:
            Dictionary of metric names and values
        """
        metrics = {
            'entropy': ImageMetrics.entropy(processed),
            'rmse': ImageMetrics.rmse(original, processed),
            'psnr': ImageMetrics.psnr(original, processed),
            'ssim': ImageMetrics.ssim(original, processed),
            'bit_depth_linearity': ImageMetrics.bit_depth_linearity(processed),
            'edge_preservation': ImageMetrics.edge_preservation(original, processed),
        }
        
        # MTF (returns array, so we compute average for high frequencies)
        freqs, mtf = ImageMetrics.mtf_estimate(processed)
        if len(freqs) > 5:
            metrics['mtf_high_freq'] = np.mean(mtf[5:])
        else:
            metrics['mtf_high_freq'] = np.mean(mtf)
        
        # Autocorrelation (compute ratio of non-center to center)
        autocorr = ImageMetrics.autocorrelation(processed)
        if len(autocorr) > 1 and autocorr[0] > 0:
            metrics['autocorr_ratio'] = np.mean(autocorr[1:]) / autocorr[0]
        else:
            metrics['autocorr_ratio'] = 0.0
        
        return metrics
