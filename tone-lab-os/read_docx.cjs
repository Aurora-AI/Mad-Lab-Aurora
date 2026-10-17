const mammoth = require("mammoth");
const fs = require("fs");
const path = require("path");

const baseDir = "C:\\Users\\rodri\\Documents\\MadLab\\MSICA - LABORATRIO & MANUFATURA-20261005T135521Z-1-001\\MSICA - LABORATRIO & MANUFATURA";
// Let's use a dynamic search to find the docx file ignoring encoding issues
const parentDir = "C:\\Users\\rodri\\Documents\\MadLab";

function findFile(dir, filename) {
  const files = fs.readdirSync(dir);
  for (const file of files) {
    const fullPath = path.join(dir, file);
    if (fs.statSync(fullPath).isDirectory()) {
      const found = findFile(fullPath, filename);
      if (found) return found;
    } else if (file.includes(filename)) {
      return fullPath;
    }
  }
  return null;
}

const ampFile = findFile(parentDir, "Projeto_Amplificador_Signature_v1_1.docx");

if (ampFile) {
  mammoth.extractRawText({path: ampFile})
    .then(function(result){
        const text = result.value; 
        fs.writeFileSync("amp_data.txt", text);
        console.log("Extraction complete. See amp_data.txt");
    })
    .catch(console.error);
} else {
  console.log("File not found");
}
