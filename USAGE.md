# Usage Guide

Comprehensive guide for using the Lo Shu Balance Algorithm.

## 📋 Table of Contents

- [Basic Usage](#basic-usage)
- [Advanced Usage](#advanced-usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Best Practices](#best-practices)

---

## 🚀 Basic Usage

### Loading and Processing Images

```python
import numpy as np
from PIL import Image
from src.lo_shu_filter import LoShuBalanceFilter

# Load image
image = Image.open('input.png')
image_array = np.array(image)

# Create filter
filter_obj = LoShuBalanceFilter()

# Apply denoising
denoised = filter_obj.apply(image_array)

# Save result
result_image = Image.fromarray(denoised)
result_image.save('output.png')
```

### Processing Grayscale Images

```python
from src.lo_shu_filter import LoShuBalanceFilter

# Grayscale image (2D array)
gray_image = np.random.randint(0, 255, (256, 256), dtype=np.uint8)

filter_obj = LoShuBalanceFilter()
denoised = filter_obj.apply(gray_image)
```

### Processing RGB Images

```python
# RGB image (3D array)
rgb_image = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)

filter_obj = LoShuBalanceFilter()
denoised = filter_obj.apply(rgb_image)  # Processes each channel separately
```

---

## ⚡ Advanced Usage

### Edge Preservation Control

```python
# With edge enhancement (default)
denoised = filter_obj.apply(image, preserve_edges=True)

# Without edge enhancement (faster)
denoised = filter_obj.apply(image, preserve_edges=False)
```

### Error Diffusion Mode

```python
from src.lo_shu_filter import lo_shu_denoise

# Standard method
result1 = lo_shu_denoise(image, method='standard')

# Error diffusion method (better for quantization)
result2 = lo_shu_denoise(image, method='error_diffusion')
```

### Batch Processing

```python
from pathlib import Path

def process_directory(input_dir, output_dir):
    """Process all images in a directory."""
    filter_obj = LoShuBalanceFilter()
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    for img_file in input_path.glob('*.png'):
        # Load
        image = np.array(Image.open(img_file))
        
        # Process
        denoised = filter_obj.apply(image)
        
        # Save
        output_file = output_path / img_file.name
        Image.fromarray(denoised).save(output_file)
        print(f"Processed: {img_file.name}")

# Usage
process_directory('input_images/', 'output_images/')
```

### Progress Tracking

```python
from tqdm import tqdm

def process_with_progress(images):
    """Process images with progress bar."""
    filter_obj = LoShuBalanceFilter()
    results = []
    
    for image in tqdm(images, desc="Processing images"):
        denoised = filter_obj.apply(image)
        results.append(denoised)
    
    return results
```

---

## 📊 Quality Evaluation

### Using Metrics

```python
from src.metrics import ImageMetrics

# Load original and processed images
original = np.array(Image.open('original.png'))
processed = np.array(Image.open('processed.png'))

# Calculate all metrics
metrics = ImageMetrics.compute_all_metrics(original, processed)

print("Quality Metrics:")
print(f"  PSNR: {metrics['psnr']:.2f} dB")
print(f"  SSIM: {metrics['ssim']:.4f}")
print(f"  RMSE: {metrics['rmse']:.4f}")
print(f"  Entropy: {metrics['entropy']:.4f}")
print(f"  Edge Preservation: {metrics['edge_preservation']:.4f}")
print(f"  Bit Depth Linearity: {metrics['bit_depth_linearity']:.4f}")
```

### Individual Metrics

```python
# PSNR (Peak Signal-to-Noise Ratio)
psnr = ImageMetrics.psnr(original, processed)
print(f"PSNR: {psnr:.2f} dB (higher is better)")

# SSIM (Structural Similarity Index)
ssim = ImageMetrics.ssim(original, processed)
print(f"SSIM: {ssim:.4f} (closer to 1 is better)")

# RMSE (Root Mean Square Error)
rmse = ImageMetrics.rmse(original, processed)
print(f"RMSE: {rmse:.4f} (lower is better)")

# Entropy
entropy = ImageMetrics.entropy(processed)
print(f"Entropy: {entropy:.4f} (higher = more information)")

# Edge Preservation
edge_pres = ImageMetrics.edge_preservation(original, processed)
print(f"Edge Preservation: {edge_pres:.4f} (closer to 1 is better)")
```

---

## 🔬 Comparative Analysis

### Comparing Multiple Methods

```python
from src.benchmark_filters import BenchmarkFilters
from src.lo_shu_filter import LoShuBalanceFilter
from src.metrics import ImageMetrics

# Create noisy image
noisy = add_gaussian_noise(original, std=25)

# Apply different filters
filters = {
    'Lo Shu': LoShuBalanceFilter().apply,
    'Mean': BenchmarkFilters.mean_filter,
    'Gaussian': BenchmarkFilters.gaussian_filter,
    'Median': BenchmarkFilters.median_filter
}

# Compare
results = {}
for name, filter_func in filters.items():
    filtered = filter_func(noisy)
    psnr = ImageMetrics.psnr(original, filtered)
    ssim = ImageMetrics.ssim(original, filtered)
    results[name] = {'psnr': psnr, 'ssim': ssim}

# Display comparison
print(f"{'Method':<15} {'PSNR (dB)':<12} {'SSIM':<12}")
print("-" * 40)
for name, metrics in results.items():
    print(f"{name:<15} {metrics['psnr']:<12.2f} {metrics['ssim']:<12.4f}")
```

---

## 🎯 Application-Specific Examples

### Medical Imaging (X-ray)

```python
def enhance_xray(image_path, output_path):
    """Enhance X-ray image for better diagnosis."""
    from pydicom import dcmread  # For DICOM files
    
    # Load DICOM
    dicom = dcmread(image_path)
    image = dicom.pixel_array
    
    # Normalize to 0-255
    image = ((image - image.min()) / (image.max() - image.min()) * 255).astype(np.uint8)
    
    # Apply Lo Shu filter
    filter_obj = LoShuBalanceFilter()
    enhanced = filter_obj.apply(image, preserve_edges=True)
    
    # Save
    Image.fromarray(enhanced).save(output_path)
    print(f"Enhanced X-ray saved to {output_path}")
```

### Astronomical Imaging

```python
def enhance_astro_image(image_path, output_path):
    """Enhance astronomical image for star detection."""
    from astropy.io import fits  # For FITS files
    
    # Load FITS
    with fits.open(image_path) as hdul:
        image = hdul[0].data
    
    # Normalize
    image = np.clip((image - np.mean(image)) / np.std(image) * 50 + 128, 0, 255).astype(np.uint8)
    
    # Apply filter
    filter_obj = LoShuBalanceFilter()
    enhanced = filter_obj.apply(image)
    
    # Save
    Image.fromarray(enhanced).save(output_path)
```

### Photography

```python
def denoise_photo(image_path, output_path, strength='medium'):
    """Denoise photograph with adjustable strength."""
    image = np.array(Image.open(image_path))
    
    filter_obj = LoShuBalanceFilter()
    
    if strength == 'low':
        # Light denoising
        result = filter_obj.apply(image, preserve_edges=True)
    elif strength == 'medium':
        # Standard denoising
        result = filter_obj.apply(image, preserve_edges=True)
    elif strength == 'high':
        # Strong denoising with error diffusion
        result = lo_shu_denoise(image, method='error_diffusion')
    
    Image.fromarray(result).save(output_path)
```

---

## 📝 API Reference

### LoShuBalanceFilter

```python
class LoShuBalanceFilter:
    """
    Lo Shu Balance Algorithm for image denoising.
    
    Args:
        kernel_size: Size of processing kernel (default: 3)
    
    Methods:
        apply(image, preserve_edges=True): Apply standard denoising
        apply_with_error_diffusion(image): Apply with error diffusion
    """
    
    def __init__(self, kernel_size: int = 3):
        """Initialize filter with specified kernel size."""
        pass
    
    def apply(self, image: np.ndarray, preserve_edges: bool = True) -> np.ndarray:
        """
        Apply Lo Shu Balance Filter to an image.
        
        Args:
            image: Input image (2D grayscale or 3D RGB)
            preserve_edges: Whether to preserve edge details
            
        Returns:
            Filtered image
        """
        pass
    
    def apply_with_error_diffusion(self, image: np.ndarray) -> np.ndarray:
        """
        Apply filter with quantization error diffusion.
        
        Args:
            image: Input image
            
        Returns:
            Filtered image with error diffusion
        """
        pass
```

### ImageMetrics

```python
class ImageMetrics:
    """Collection of image evaluation metrics."""
    
    @staticmethod
    def entropy(image: np.ndarray) -> float:
        """Calculate Shannon entropy."""
        pass
    
    @staticmethod
    def rmse(original: np.ndarray, processed: np.ndarray) -> float:
        """Calculate Root Mean Square Error."""
        pass
    
    @staticmethod
    def psnr(original: np.ndarray, processed: np.ndarray) -> float:
        """Calculate Peak Signal-to-Noise Ratio."""
        pass
    
    @staticmethod
    def ssim(original: np.ndarray, processed: np.ndarray) -> float:
        """Calculate Structural Similarity Index."""
        pass
    
    @staticmethod
    def edge_preservation(original: np.ndarray, processed: np.ndarray) -> float:
        """Measure edge preservation quality."""
        pass
    
    @staticmethod
    def bit_depth_linearity(image: np.ndarray) -> float:
        """Assess bit-depth linearity (banding detection)."""
        pass
    
    @staticmethod
    def compute_all_metrics(original: np.ndarray, processed: np.ndarray) -> dict:
        """Compute all metrics at once."""
        pass
```

---

## 💡 Best Practices

### 1. Image Preprocessing

```python
# Normalize image before processing
def normalize_image(image):
    """Normalize image to 0-255 range."""
    image_min = image.min()
    image_max = image.max()
    if image_max > image_min:
        image = (image - image_min) / (image_max - image_min) * 255
    return image.astype(np.uint8)
```

### 2. Memory Efficiency

```python
# Process large images in tiles
def process_large_image(image, tile_size=512):
    """Process large image in tiles to save memory."""
    h, w = image.shape[:2]
    result = np.zeros_like(image)
    
    filter_obj = LoShuBalanceFilter()
    
    for i in range(0, h, tile_size):
        for j in range(0, w, tile_size):
            tile = image[i:i+tile_size, j:j+tile_size]
            result[i:i+tile_size, j:j+tile_size] = filter_obj.apply(tile)
    
    return result
```

### 3. Parameter Selection

| Scenario | Recommendation |
|----------|----------------|
| Low noise | `preserve_edges=True` |
| High noise | `method='error_diffusion'` |
| Medical images | `preserve_edges=True` (critical) |
| Natural photos | Default settings |
| Astronomical | Default + multiple passes |

---

## 🐛 Troubleshooting

### Issue: Slow Processing

```python
# Solution: Process without edge enhancement
denoised = filter_obj.apply(image, preserve_edges=False)

# Or use smaller tiles
result = process_large_image(image, tile_size=256)
```

### Issue: Memory Error

```python
# Solution: Process in chunks
import gc

def process_in_chunks(image_paths):
    filter_obj = LoShuBalanceFilter()
    
    for path in image_paths:
        image = np.array(Image.open(path))
        result = filter_obj.apply(image)
        Image.fromarray(result).save(f'output_{path}')
        
        # Free memory
        del image, result
        gc.collect()
```

---

**For more examples, see the `tests/` directory and `docs/` folder.**
