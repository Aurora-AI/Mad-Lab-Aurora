const { Jimp } = require('jimp');
const fs = require('fs');
const path = require('path');

/**
 * generate-ascii.js
 * 
 * Automation script for 'Aino' Style ASCII Mask Generation.
 * Ingests an image and outputs a character-map string.
 * REFACTORED: Uses modern Jimp instead of vulnerable asciify-image.
 */

const imagePath = path.join(__dirname, 'public/assets/puzzle-pb.png');
const outputPath = path.join(__dirname, 'public/assets/ascii-data.txt');

const WIDTH = 120;
const HEIGHT = 60;
// Character map for ASCII brightness levels
const RAMP = ' .:-=+*#%@';

async function generate() {
  console.log('--- ASCII MATRIX PIPELINE (MODERN) ---');
  console.log(`Input: ${imagePath}`);

  try {
    if (!fs.existsSync(imagePath)) {
      throw new Error(`File not found: ${imagePath}`);
    }

    const image = await Jimp.read(imagePath);
    
    // Resize to target dimensions using Jimp v1 API (w and h)
    image.resize({ w: WIDTH, h: HEIGHT });
    
    let asciified = '';
    
    for (let y = 0; y < HEIGHT; y++) {
      for (let x = 0; x < WIDTH; x++) {
        // Get pixel color and calculate brightness (0-1)
        const color = image.getPixelColor(x, y);
        
        // Manual RGBA extraction from integer color (ABGR or RGBA depending on platform, Jimp uses RGBA)
        const r = (color >> 24) & 0xFF;
        const g = (color >> 16) & 0xFF;
        const b = (color >> 8) & 0xFF;
        
        // Standard relative luminance formula
        const brightness = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255;
        
        // Map brightness to character ramp
        let charIndex = Math.floor(brightness * (RAMP.length - 1));
        let char = RAMP[charIndex];
        
        // Substitute empty spaces with '0' (background) for the Aino technical look
        if (char === ' ') char = '0';
        
        asciified += char;
      }
      asciified += '\n';
    }

    fs.writeFileSync(outputPath, asciified);
    console.log('✅ ASCII Matrix successfully generated!');
    console.log(`Location: ${outputPath}`);
  } catch (err) {
    console.error('❌ Matrix Error:', err);
    process.exit(1);
  }
}

generate();
